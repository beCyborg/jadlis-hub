#!/usr/bin/env python3
"""split-research.py — materialise one of the four research repos from plugins/jadlis-research.

Dev tool (hub `tools/`, not shipped). Used once for the 2026-09 split (on top of a
`git filter-repo` clone that already carries the history) and again whenever the
monorepo plugin is re-cut. The plugin `plugins/jadlis-research` is the source; the
target directory is a root-as-plugin repo (no marketplace.json).

Usage:
    tools/split-research.py --target search           --out /path/to/split-search
    tools/split-research.py --target research         --out /path/to/split-research
    tools/split-research.py --target science-research --out /path/to/split-science
    tools/split-research.py --target verif            --out /path/to/split-verif
    add --dry-run to list the plan, --report to print leftover `jadlis-research` mentions.

Targets (plugin name == repo suffix, command == /<name>):
    search           .mcp.json, hooks, skills/search + skills/keys, scripts/ (source of truth), shared/
    research         skills/full-research → skills/research, agents/, workflows/full-research-core.js,
                     vendored scripts/ + shared/, dependency search ^1
    science-research skills/search-paper → skills/science-research, agents/researcher-opus.md,
                     workflows/search-paper-core.js, vendored scripts/ + shared/, dependency search ^1
    verif            skills/verif, assets/verif-homes — autonomous
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

HUB = Path(__file__).resolve().parent.parent
SRC = HUB / "plugins" / "jadlis-research"
GITHUB = "https://github.com/beCyborg"
TEXT_EXT = {".md", ".js", ".mjs", ".json", ".sh", ".py", ".toml", ".txt", ".yml", ".yaml"}

# ---------------------------------------------------------------- substitutions
# Order matters: MCP prefix first, then agent namespaces, then slash commands, then paths.
COMMON_SUBS: list[tuple[str, str]] = [
    ("mcp__plugin_jadlis-research_", "mcp__plugin_search_"),
    ("/jadlis-research:full-research", "/research"),
    ("/jadlis-research:search-paper", "/science-research"),
    ("/jadlis-research:verif", "/verif"),
    ("/jadlis-research:search", "/search"),
    ("/jadlis-research:keys", "/search:keys"),
    ("jadlis-research@jadlis", "search@jadlis"),           # every mention is about the keys
    ("skills/full-research/", "skills/research/"),
    ("skills/search-paper/", "skills/science-research/"),
    ("плагина jadlis-research", "ресерч-стека Jadlis"),
    ("плагин jadlis-research", "ресерч-стек Jadlis"),
    ("plugin jadlis-research", "Jadlis research stack"),
    ("jadlis-research@<marketplace>", "search@<marketplace>"),
    ('UA="jadlis-research/1.0"', 'UA="jadlis-search/1.0"'),
    ("generic `jadlis-research`", "generic `jadlis`"),
    ("Keychain `jadlis-research`/`KEY`", "Keychain `jadlis`/`KEY` (fallback `jadlis-research`)"),
    ("service `jadlis-research`, account", "service `jadlis`, account"),
    ("-s jadlis-research -a", "-s jadlis -a"),
    ("disable/enable jadlis-research", "disable/enable search"),
    ("has just installed jadlis-research and needs configuration", "has just installed search and needs configuration"),
    ('\\"/jadlis-research:keys\\"', '\\"/search:keys\\"'),
]
AGENT_NS_RE = re.compile(r"(?<![A-Za-z0-9_./-])jadlis-research:(?=[a-z])")

TARGETS = {
    "search": {
        "display": "Jadlis — поиск и ключи ресерч-стека",
        "description": "Поиск в вебе (Brave — по словам, Exa — по смыслу) и страницы через Firecrawl, плюс пять MCP-серверов и единая точка ключей (scripts/secret.sh → Связка ключей macOS). База для плагинов research и science-research.",
        "keywords": ["jadlis", "search", "brave", "exa", "firecrawl", "mcp"],
        "copy": [".mcp.json", "hooks", "skills/search", "skills/keys", "scripts", "shared"],
        "rename": {},
        "agent_ns": None,
        "dependencies": None,
        "user_config_keys": ["BRAVE_API_KEY", "FIRECRAWL_API_KEY", "REDDITAPIS_KEY", "YOUTUBE_API_KEY"],
        "entry_skill": "skills/search/SKILL.md",
        "problem": "Поиск и ключи для всего ресерч-стека",
    },
    "research": {
        "display": "Jadlis — полный ресерч темы",
        "description": "Четырнадцать каналов (web×3, reddit, twitter, hackernews, substack, yandex, youtube, telegram, языковые слои ja/zh/ko/eu) через workflow, ключевые утверждения проверяются перекрёстно, непроверенные помечены. Требует плагин search (ключи Brave и Firecrawl).",
        "keywords": ["jadlis", "research", "verification", "communities", "workflow"],
        "copy": ["skills/full-research", "agents", "workflows/full-research-core.js", "scripts", "shared"],
        "rename": {"skills/full-research": "skills/research"},
        "agent_ns": "research",
        "dependencies": [{"name": "search", "version": "^1"}],
        "user_config_keys": ["VAULT_PATH"],
        "entry_skill": "skills/research/SKILL.md",
        "problem": "Решение, которому можно доверять: 14 каналов, ключевые утверждения перепроверены",
    },
    "science-research": {
        "display": "Jadlis — научный ресерч",
        "description": "PubMed, Europe PMC, Semantic Scholar, OpenAlex, arXiv, Cochrane; снежный ком по цитированиям, проверка отзыва статьи, GRADE-синтез → заметка в vault. Требует плагин search (ключи Brave и Firecrawl).",
        "keywords": ["jadlis", "science", "pubmed", "openalex", "grade", "workflow"],
        "copy": ["skills/search-paper", "agents/researcher-opus.md", "agents/synth-fable.md", "agents/synth-opus.md", "workflows/search-paper-core.js", "scripts", "shared"],
        "rename": {"skills/search-paper": "skills/science-research"},
        "agent_ns": "science-research",
        "dependencies": [{"name": "search", "version": "^1"}],
        "user_config_keys": ["VAULT_PATH"],
        "entry_skill": "skills/science-research/SKILL.md",
        "problem": "Что реально доказано наукой и не отозвано ли",
    },
    "verif": {
        "display": "Jadlis — проверка плана тремя моделями",
        "description": "Codex, Fable и Grok порознь рвут план или документ, арбитр сводит находки, батч-интервью, правки. Автономен: нужны Codex CLI (подписка ChatGPT) и Grok CLI; веб-проверка первоисточников — через плагин search, если он установлен.",
        "keywords": ["jadlis", "verification", "adversarial", "codex", "grok", "plan-review"],
        "copy": ["skills/verif", "assets/verif-homes"],
        "rename": {},
        "agent_ns": None,
        "dependencies": None,
        "user_config_keys": ["VAULT_PATH"],
        "entry_skill": "skills/verif/SKILL.md",
        "problem": "Три модели рвут твой план порознь до того, как ты в него вложился",
    },
}

SHARED_FILES = ["scripts", "shared/obsidian-write-contract.md"]  # what dependents vendor from search


def load_src_manifest() -> dict:
    return json.loads((SRC / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))


def subst_text(text: str, target: str) -> str:
    for a, b in COMMON_SUBS:
        text = text.replace(a, b)
    ns = TARGETS[target]["agent_ns"]
    if ns:
        text = AGENT_NS_RE.sub(f"{ns}:", text)
    return text


def patch_secret_sh(text: str) -> str:
    """Keychain service `jadlis` with read fallback to the legacy `jadlis-research`."""
    text = text.replace('SERVICE="jadlis-research"\n', 'SERVICE="jadlis"\nSERVICE_LEGACY="jadlis-research"   # ключи, записанные до split 2026-09\n')
    text = text.replace('PLUGIN_ID_PREFIX="jadlis-research@"', 'PLUGIN_ID_PREFIX="search@"')
    old = ('  if have_security; then\n'
           '    v=$(security find-generic-password -s "$SERVICE" -a "$key" -w 2>/dev/null)\n'
           '    if [ -n "${v:-}" ]; then\n'
           '      printf \'%s%s%s\' "keychain generic ($SERVICE/$key)" "$TAB" "$v"; return 0\n'
           '    fi\n'
           '  fi\n')
    new = ('  if have_security; then\n'
           '    for svc in "$SERVICE" "$SERVICE_LEGACY"; do\n'
           '      v=$(security find-generic-password -s "$svc" -a "$key" -w 2>/dev/null)\n'
           '      if [ -n "${v:-}" ]; then\n'
           '        printf \'%s%s%s\' "keychain generic ($svc/$key)" "$TAB" "$v"; return 0\n'
           '      fi\n'
           '    done\n'
           '  fi\n')
    if old not in text:
        sys.exit("secret.sh: resolve() block not found — patch_secret_sh needs updating")
    text = text.replace(old, new)
    text = text.replace("единая точка чтения ключей ресерч-стека Jadlis", "единая точка чтения ключей ресерч-стека Jadlis (плагин search)")
    text = text.replace("service `jadlis-research`, account = имя ключа", "service `jadlis` (legacy `jadlis-research`), account = имя ключа")
    text = text.replace("Keychain generic password: service `jadlis-research`, account KEY", "Keychain generic password: service `jadlis` (fallback `jadlis-research`), account KEY")
    return text


def patch_skill_name(text: str, name: str) -> str:
    return re.sub(r"^name:\s*.+$", f"name: {name}", text, count=1, flags=re.M)


def copy_tree(src: Path, dst: Path, target: str, plan: list[str], dry: bool) -> None:
    if src.is_file():
        files = [src]
        base = src.parent
    else:
        files = [p for p in src.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
        base = src
    for f in files:
        rel = f.relative_to(base)
        out = dst / rel if src.is_dir() else dst
        plan.append(f"{f.relative_to(SRC)} -> {out.relative_to(dst.parent if src.is_file() else dst.parent.parent) if False else out}")
        if dry:
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        if f.suffix in TEXT_EXT:
            text = f.read_text(encoding="utf-8")
            text = subst_text(text, target)
            if f.name == "secret.sh":
                text = patch_secret_sh(text)
            out.write_text(text, encoding="utf-8")
            shutil.copymode(f, out)
        else:
            shutil.copy2(f, out)


def build_manifest(target: str) -> dict:
    src = load_src_manifest()
    t = TARGETS[target]
    m = {
        "$schema": src.get("$schema", "https://json.schemastore.org/claude-code-plugin-manifest.json"),
        "name": target,
        "version": "1.0.0",
        "displayName": t["display"],
        "description": t["description"],
        "author": src.get("author", {"name": "Be Cyborg"}),
        "homepage": f"{GITHUB}/jadlis-{target}",
        "repository": f"{GITHUB}/jadlis-{target}",
        "license": "MIT",
        "keywords": t["keywords"],
    }
    if t["dependencies"]:
        m["dependencies"] = t["dependencies"]
    uc = {}
    for k in t["user_config_keys"]:
        v = json.loads(json.dumps(src["userConfig"][k]))
        v["description"] = subst_text(v["description"], target)
        uc[k] = v
    m["userConfig"] = uc
    return m


def readme_pair(target: str) -> tuple[str, str]:
    t = TARGETS[target]
    install = f"claude plugin marketplace add {GITHUB}/jadlis-start.git\nclaude plugin install {target}@jadlis"
    if target == "search":
        install = f"claude plugin marketplace add {GITHUB}/jadlis-start.git\nclaude plugin install search@jadlis --config BRAVE_API_KEY=… --config FIRECRAWL_API_KEY=…"
    elif target in ("research", "science-research"):
        install = (f"claude plugin marketplace add {GITHUB}/jadlis-start.git\n"
                   f"claude plugin install search@jadlis --config BRAVE_API_KEY=… --config FIRECRAWL_API_KEY=…\n"
                   f"claude plugin install {target}@jadlis")
    ru = f"""Русский · [English](README.en.md)

# {t['problem']}

Плагин `{target}` для Claude Code. Команда — `/{target}`.

## Было → стало

Раздел заполняется по контракту README 2026-09 (фаза 3 плана «GitHub beCyborg как витрина Jadlis»).

## Как это работает

{t['description']}

## Установка и первый запуск

```bash
{install}
```

## Границы, стоимость, обновление

```bash
claude plugin marketplace update jadlis
claude plugin update {target}@jadlis
claude plugin list
```

Переустановка: `claude plugin uninstall {target}@jadlis --keep-data && claude plugin install {target}@jadlis`.
"""
    en = f"""[Русский](README.md) · English

# {target} — Claude Code plugin

Command: `/{target}`.

## Было → стало

To be written (README contract 2026-09, phase 3).

## Как это работает

{t['description']}

## Установка и первый запуск

```bash
{install}
```

## Границы, стоимость, обновление

```bash
claude plugin marketplace update jadlis
claude plugin update {target}@jadlis
claude plugin list
```
"""
    return ru, en


def changelog(target: str) -> str:
    return f"""# Changelog — {target}

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), версии — [SemVer](https://semver.org/lang/ru/).
История до 1.0.0 — плагин `jadlis-research` 1.0.0–1.3.0 в репо [jadlis-start]({GITHUB}/jadlis-start) (`plugins/jadlis-research/CHANGELOG.md` до split).

## [Unreleased]

## [1.0.0] — 2026-09-07

### Для человека

- Первый релиз под именем `{target}`: выделен из `jadlis-research` 1.3.0 (репо на плагин, команда `/{target}`).

### For agents

- Split of `jadlis-research` 1.3.0 by `tools/split-research.py` (hub). Namespaces: MCP tools `mcp__plugin_search_*`, agents `{TARGETS[target]['agent_ns'] or '—'}:*`, commands `/search`, `/search:keys`, `/research`, `/science-research`, `/verif`.
"""


def contributing(target: str) -> str:
    dep = ""
    if TARGETS[target]["dependencies"]:
        dep = ("\n`scripts/` и `shared/` — копия из плагина `search` (источник правды — репо `jadlis-search`). "
               "Не правь их здесь: `bash tools/sync-shared.sh <search--vX.Y.Z>` обновляет копию и `SHARED_FROM.txt`.\n")
    if target == "search":
        dep = ("\n`scripts/` и `shared/` отсюда вендорятся плагинами `research` и `science-research` (`tools/sync-shared.sh` у них). "
               "Смена MCP-серверов, имён ключей или интерфейса `secret.sh` = мажорный бамп версии.\n")
    return f"""Русский · [English](#english)

# Как предложить правку

Репозиторий публичный, пишет в него только владелец. Правки — через **форк + pull request**.

1. Форк и ветка от `main`.
2. Перед коммитом: `claude plugin validate . --strict`, `gitleaks git .`; README — по контракту (RU + EN, одинаковые H2, без Mermaid).
3. Одна тема — один PR. В описании — что меняется для получателя.
4. Ключи, почты, личные пути в репо не попадают.
{dep}
Релизы и теги (`{target}--vX.Y.Z`) делает владелец. Тексты и код написаны вместе с Claude Code; за содержание отвечает владелец.

---

## English

Public repository, owner-only writes. Contributions via **fork + pull request**: branch from `main`, run `claude plugin validate . --strict` and `gitleaks git .`, keep README RU/EN in sync (same H2 set, no Mermaid), one topic per PR, no keys or personal paths.
{'`scripts/` and `shared/` are vendored from the `search` plugin — do not edit them here, run `tools/sync-shared.sh`.' if TARGETS[target]['dependencies'] else ''}
Releases and tags (`{target}--vX.Y.Z`) are cut by the owner. Text and code are written together with Claude Code; the owner is accountable for the content.
"""


CI_YML = """name: CI
on:
  pull_request: {}
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  ci:
    uses: beCyborg/jadlis-start/.github/workflows/plugin-ci.yml@main
    with:
      mode: plugin
    secrets: inherit
"""

SYNC_SH = """#!/usr/bin/env bash
# sync-shared.sh — refresh the vendored copy of scripts/ and shared/ from the search plugin.
# Usage: bash tools/sync-shared.sh search--v1.2.0
set -euo pipefail
TAG="${1:?usage: sync-shared.sh <search--vX.Y.Z>}"
REPO="https://github.com/beCyborg/jadlis-search.git"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git clone -q --depth 1 --branch "$TAG" "$REPO" "$TMP"
SHA="$(git -C "$TMP" rev-parse HEAD)"
rm -rf "$ROOT/scripts"
cp -R "$TMP/scripts" "$ROOT/scripts"
mkdir -p "$ROOT/shared"
cp "$TMP/shared/obsidian-write-contract.md" "$ROOT/shared/obsidian-write-contract.md"
printf 'search %s %s\\n' "$TAG" "$SHA" > "$ROOT/SHARED_FROM.txt"
echo "synced scripts/ + shared/ from $TAG ($SHA)"
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", required=True, choices=sorted(TARGETS))
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", action="store_true", help="print leftover jadlis-research mentions in the output")
    ap.add_argument("--shared-from", default="", help="'<tag> <sha>' of jadlis-search for SHARED_FROM.txt (dependents)")
    args = ap.parse_args()
    target, out, t = args.target, args.out.resolve(), TARGETS[args.target]
    plan: list[str] = []

    # 1. remove everything the split does not keep (filter-repo leaves only the selected paths,
    #    but a re-run on an existing repo must not keep stale files)
    if not args.dry_run:
        out.mkdir(parents=True, exist_ok=True)
        for p in out.iterdir():
            if p.name in {".git"}:
                continue
            shutil.rmtree(p) if p.is_dir() else p.unlink()

    # 2. copy + substitute
    for item in t["copy"]:
        src = SRC / item
        if not src.exists():
            sys.exit(f"missing in source: {item}")
        dst_rel = t["rename"].get(item, item)
        copy_tree(src, out / dst_rel, target, plan, args.dry_run)

    if args.dry_run:
        print("\n".join(plan))
        return 0

    # 3. entry skill frontmatter name == plugin name
    entry = out / t["entry_skill"]
    entry.write_text(patch_skill_name(entry.read_text(encoding="utf-8"), target), encoding="utf-8")

    # 4. manifest and skeleton files
    (out / ".claude-plugin").mkdir(exist_ok=True)
    (out / ".claude-plugin" / "plugin.json").write_text(json.dumps(build_manifest(target), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ru, en = readme_pair(target)
    (out / "README.md").write_text(ru, encoding="utf-8")
    (out / "README.en.md").write_text(en, encoding="utf-8")
    (out / "CHANGELOG.md").write_text(changelog(target), encoding="utf-8")
    (out / "CONTRIBUTING.md").write_text(contributing(target), encoding="utf-8")
    shutil.copy2(HUB / "LICENSE", out / "LICENSE")
    (out / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (out / ".github" / "workflows" / "ci.yml").write_text(CI_YML, encoding="utf-8")
    (out / ".gitignore").write_text("__pycache__/\n*.pyc\n.DS_Store\n", encoding="utf-8")
    if t["dependencies"]:
        (out / "tools").mkdir(exist_ok=True)
        sync = out / "tools" / "sync-shared.sh"
        sync.write_text(SYNC_SH, encoding="utf-8")
        os.chmod(sync, 0o755)
        (out / "SHARED_FROM.txt").write_text(f"search {args.shared_from or 'unreleased (split 2026-09-07 from jadlis-research 1.3.0)'}\n", encoding="utf-8")
    if target == "research":
        smoke = HUB / "tools" / "smoke-core.mjs"
        (out / "tools").mkdir(exist_ok=True)
        text = smoke.read_text(encoding="utf-8").replace("path.join(here, '..', 'plugins', 'jadlis-research', 'workflows', 'full-research-core.js')", "path.join(here, '..', 'workflows', 'full-research-core.js')")
        (out / "tools" / "smoke-core.mjs").write_text(text, encoding="utf-8")

    # 5. report leftovers
    if args.report:
        left = []
        for p in out.rglob("*"):
            if p.is_file() and p.suffix in TEXT_EXT and ".git" not in p.parts and p.name != "CHANGELOG.md":
                for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                    if "jadlis-research" in line:
                        left.append(f"{p.relative_to(out)}:{i}: {line.strip()[:140]}")
        print("\n".join(left) if left else "no leftover jadlis-research mentions")
    print(f"{target}: {len(plan)} files → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
