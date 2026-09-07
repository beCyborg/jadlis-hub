#!/usr/bin/env python3
"""render-live.py — render the live ~/.claude research stack FROM the four plugin repos.

This is the INVERSE of the documented sync procedure (live -> plugin).
Since the 2026-09-07 split the research stack lives in four root-as-plugin
repos, and together they are the source of truth:

    ~/jadlis-search           plugin `search`   — skills/search, skills/keys,
                                                  scripts/, shared/, hooks/, .mcp.json
    ~/jadlis-research         plugin `research` — skills/research, agents/,
                                                  workflows/full-research-core.js
    ~/jadlis-science-research plugin `science-research` — skills/science-research,
                                                  workflows/search-paper-core.js
    ~/jadlis-verif            plugin `verif`    — skills/verif, assets/verif-homes

The tool materialises the personal contour in ~/.claude, undoing the
plugin-specific adaptations (placeholders, MCP name prefixes, namespaced
slash-commands / agent types) and restoring the live folder names the owner's
routing rules refer to: `skills/research` -> `skills/full-research`,
`skills/science-research` -> `skills/search-paper`.

`scripts/` is taken from the `search` repo only — the copies vendored into
`research` / `science-research` (for standalone installs) are ignored, as are
the duplicated `agents/` in `science-research`.

Dev tool only: it lives in the repo root `tools/` and is NOT part of any plugin.

Usage:
    tools/render-live.py --dry-run          # print the plan, change nothing
    tools/render-live.py --check            # only verify invariants
    tools/render-live.py                    # render
    tools/render-live.py --prune --yes      # render + drop stale skill files
    tools/render-live.py --search ~/src/jadlis-search --verif ~/src/jadlis-verif
                                            # override any of the four source roots
"""

from __future__ import annotations

import argparse
import difflib
import os
import re
import shutil
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

DEFAULT_ROOTS = {
    "search": Path.home() / "jadlis-search",
    "research": Path.home() / "jadlis-research",
    "science-research": Path.home() / "jadlis-science-research",
    "verif": Path.home() / "jadlis-verif",
}
DEFAULT_DEST = Path.home() / ".claude"

# Value the placeholders resolve to in the live contour.
LIVE_ROOT = str(Path.home() / ".claude")
LIVE_ROOT_TILDE = "~/.claude"
# ${CLAUDE_PLUGIN_DATA} holds the verifier homes. In the live contour those
# live at $HOME/.claude/verif-homes (see ~/.claude/skills/verif/SKILL.md:62),
# so the plugin-data root maps onto $HOME/.claude itself -- NOT a verif-data dir.
PLUGIN_DATA_ROOT = LIVE_ROOT
VAULT_PATH = str(Path.home() / "Jadlis")

TEXT_SUFFIXES = {".md", ".js", ".py", ".sh", ".json", ".toml"}

# Directory trees rendered wholesale: (source root, source rel, dest rel).
# The dest names are the historical live ones -- the owner's routing rules and
# memory notes point at /full-research and /search-paper.
SKILL_TREES = [
    ("research", "skills/research", "skills/full-research"),
    ("science-research", "skills/science-research", "skills/search-paper"),
    ("search", "skills/search", "skills/search"),
    ("verif", "skills/verif", "skills/verif"),
]

# Non-skill trees rendered wholesale (never pruned): (source root, source rel, dest rel)
ASSET_TREES = [
    # first-run deploy templates for the verifier homes
    ("verif", "assets/verif-homes", "assets/verif-homes"),
]

# Single files: (source root, source rel, dest rel)
SINGLE_FILES = [
    ("search", "shared/obsidian-write-contract.md", "skills/_shared/obsidian-write-contract.md"),
    ("research", "agents/researcher-opus.md", "agents/researcher-opus.md"),
    ("research", "agents/orchestrator-opus.md", "agents/orchestrator-opus.md"),
    ("research", "agents/synth-fable.md", "agents/synth-fable.md"),
    ("research", "agents/synth-opus.md", "agents/synth-opus.md"),
]

# Flat globs: (source root, source dir, glob, dest dir)
FLAT_GLOBS = [
    ("research", "workflows", "*.js", "workflows"),
    ("science-research", "workflows", "*.js", "workflows"),
    # `search` is the single source of truth for the shared scripts; the copies
    # vendored into research/ and science-research/ are deliberately ignored.
    ("search", "scripts", "*", "scripts"),
]

# Protocols rendered into full-research are symlinked into search-community.
PROTOCOL_SRC = ("research", "skills/research/protocols")
PROTOCOL_DEST = "skills/full-research/protocols"
PROTOCOL_LINK_DIR = "skills/search-community/protocols"

# Extra symlinks: (link path rel to dest, target path rel to dest). The target
# must itself be rendered; the link is created only if the source exists.
EXTRA_LINKS = [
    # websearch.py moved plugin-side from skills/search/scripts/ to scripts/
    ("skills/search/scripts/websearch.py", "scripts/websearch.py"),
]

# Never rendered: plugin-only service skill (source-root-relative).
SKIP_SOURCE_PREFIXES = ("skills/keys/",)

# The skill frontmatter `name:` must match the live folder name, so a tree whose
# folder is renamed on render gets its `name:` rewritten too (derived from
# SKILL_TREES, keyed by the dest-relative SKILL.md path).
SKILL_NAME_RENAMES = {
    f"{dst}/SKILL.md": (Path(src).name, Path(dst).name)
    for _, src, dst in SKILL_TREES
    if Path(src).name != Path(dst).name
}

# Files where a bare `/research` etc. is NOT a slash command and must survive.
# Keyed by dest-relative path.
COMMAND_SUBST_EXEMPT = {
    # Exa REST endpoints: `/search`, `/research`, `/findSimilar`, `/answer`.
    "skills/search/references/exa-api.md",
}

# Invariants
DEST_FORBIDDEN = [
    "plugin_search",
    "plugin_jadlis-research",
    "CLAUDE_PLUGIN_ROOT",
    "{PLUGIN_ROOT}",
    "user_config.",
]
PLUGIN_FORBIDDEN = ["/Users/cyborg", "~/.claude/"]
# Deliberate exceptions: these reference the *recipient's* config, not a plugin
# path. Keys are source-root-relative, so a path shared by several repos (the
# vendored scripts) is covered by one entry.
PLUGIN_EXCEPTIONS = {
    "skills/keys/SKILL.md",
    "skills/verif/SKILL.md",
    "skills/research/protocols/grok-web-protocol.md",
    # telemetry path of the recipient (~/.claude/telemetry/search-ab)
    "scripts/websearch.py",
    # venv path of a third-party plugin on the recipient's machine
    "scripts/yt-transcript.py",
    # recipient-side config / environment notes
    "README.md",
    "skills/verif/TESTS.md",
    "skills/verif/system-prompts/fable-verifier.md",
}
# Whole subtrees exempt from the plugin invariant (recipient-side data paths).
PLUGIN_EXCEPTION_PREFIXES = (
    "skills/search/",
)


# --------------------------------------------------------------------------
# Text substitution
# --------------------------------------------------------------------------

def substitute(text: str, rel: str | None = None) -> str:
    """Apply the plugin -> live substitutions. Order matters.

    `rel` is the dest-relative path of the rendered file; it only gates the
    slash-command renames (see COMMAND_SUBST_EXEMPT).
    """
    # 0. Skill folder names: the live contour keeps the historical names.
    text = text.replace("skills/science-research/", "skills/search-paper/")
    text = text.replace("skills/research/", "skills/full-research/")
    if rel in SKILL_NAME_RENAMES:
        src_name, dst_name = SKILL_NAME_RENAMES[rel]
        text = re.sub(rf"^name: {re.escape(src_name)}$", f"name: {dst_name}", text, flags=re.M)

    # 1. ${CLAUDE_PLUGIN_ROOT} -> absolute live root (shared write contract lives in skills/_shared locally).
    text = text.replace("${CLAUDE_PLUGIN_ROOT}/shared/obsidian-write-contract.md", LIVE_ROOT + "/skills/_shared/obsidian-write-contract.md")
    text = text.replace("${CLAUDE_PLUGIN_ROOT}", LIVE_ROOT)

    # 2. {PLUGIN_ROOT} placeholder (protocols/references). A leading `$` means it
    #    is a JS template interpolation of the local `PLUGIN_ROOT` const, not the
    #    placeholder -- leave those alone.
    text = re.sub(r"(?<!\$)\{PLUGIN_ROOT\}/scripts/", LIVE_ROOT_TILDE + "/scripts/", text)
    text = re.sub(r"(?<!\$)\{PLUGIN_ROOT\}", LIVE_ROOT_TILDE, text)

    # 3. MCP tool names. All five servers ship with the `search` plugin, so the
    #    host prefix is `mcp__plugin_search_`. reddit-alt BEFORE the generic
    #    rule, otherwise the generic rule eats the prefix and leaves
    #    `mcp__reddit__-alt`.
    text = text.replace("mcp__plugin_search_reddit-alt__", "mcp__reddit-alt__")
    text = re.sub(r"mcp__plugin_search_([A-Za-z0-9-]+?)__", r"mcp__\1__", text)

    # 4. Namespaced agent types. Quoted (JS strings) or backticked (SKILL prose):
    #    'research:researcher-opus' -> 'researcher-opus',
    #    `science-research:synth-fable` -> `synth-fable`.
    #    Only the quoted form is touched, so prose about the *plugin* `research:`
    #    stays intact.
    text = re.sub(
        r"(['\"`])(?:jadlis-|science-)?research:([A-Za-z0-9_-]+)\1",
        r"\1\2\1",
        text,
    )

    # 5. Slash commands. `/search` and `/verif` are the same on both sides;
    #    the two research commands and the keys sub-command are renamed.
    if rel not in COMMAND_SUBST_EXEMPT:
        text = re.sub(r"(?<![\w/.-])/science-research(?![\w-])", "/search-paper", text)
        text = re.sub(r"(?<![\w/.-])/research(?![\w-])", "/full-research", text)
        text = re.sub(r"(?<![\w/.-])/search:keys(?![\w-])", "/keys", text)

    # 6. Verifier data root.
    text = text.replace("${CLAUDE_PLUGIN_DATA}", PLUGIN_DATA_ROOT)

    # 7. Plugin userConfig placeholder.
    text = text.replace("${user_config.VAULT_PATH}", VAULT_PATH)

    # 8. Workflow fallbacks: in the plugin they are dry-run stubs fed by args;
    #    in the live contour there is no plugin host to supply them.
    text = text.replace("A.pluginRoot || '.'", f"A.pluginRoot || '{LIVE_ROOT}'")
    text = text.replace("A.vaultPath || ''", f"A.vaultPath || '{VAULT_PATH}'")

    # 9. Recipient-side model window suffix. `[1m]` selects the 1M-context
    #    window of Opus 5 in Claude Code; it is a harness detail of THIS
    #    machine, not a plugin fact, so the plugin stays suffix-free and the
    #    live contour gets it back on render. Without this rule the first
    #    render silently reverts the 2026-09-04 hand edit of the 5 files that
    #    pin Opus 5 (2 skills, 2 agents, verif fallback).
    text = re.sub(r"^(model: claude-opus-5)$", r"\1[1m]", text, flags=re.M)
    text = text.replace(
        'FABLE_MODEL_FALLBACK="claude-opus-5"',
        'FABLE_MODEL_FALLBACK="claude-opus-5[1m]"',
    )

    return text


def is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


# --------------------------------------------------------------------------
# Plan building
# --------------------------------------------------------------------------

class Item:
    """One rendered file."""

    def __init__(self, src: Path, dst: Path, rel: str, root: str):
        self.src = src
        self.dst = dst
        self.rel = rel          # path relative to dest root, for display
        self.root = root        # which source plugin it came from
        self.status = "new"     # new | changed | same
        self.plus = 0
        self.minus = 0
        self.diff: list[str] = []

    def rendered(self) -> str:
        return substitute(self.src.read_text(encoding="utf-8"), self.rel)

    def compute(self) -> None:
        if not self.dst.exists() or self.dst.is_symlink():
            self.status = "new"
            return
        if is_text(self.src):
            new = self.rendered()
            try:
                old = self.dst.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                self.status = "changed"
                return
            if old == new:
                self.status = "same"
                return
            self.status = "changed"
            self.diff = list(
                difflib.unified_diff(
                    old.splitlines(keepends=True),
                    new.splitlines(keepends=True),
                    fromfile=f"dest/{self.rel}",
                    tofile=f"render/{self.rel}",
                )
            )
            for line in self.diff[2:]:
                if line.startswith("+") and not line.startswith("+++"):
                    self.plus += 1
                elif line.startswith("-") and not line.startswith("---"):
                    self.minus += 1
        else:
            self.status = "same" if self.dst.read_bytes() == self.src.read_bytes() else "changed"


class Link:
    """One protocol symlink in search-community."""

    def __init__(self, link: Path, target: Path, rel: str):
        self.link = link
        self.target = target
        self.rel = rel
        self.status = "new"     # new | ok | retarget | replace-file

    def compute(self) -> None:
        if self.link.is_symlink():
            self.status = "ok" if os.readlink(self.link) == str(self.target) else "retarget"
        elif self.link.exists():
            self.status = "replace-file"
        else:
            self.status = "new"


def collect(roots: dict[str, Path], dest: Path) -> tuple[list[Item], list[Link]]:
    items: list[Item] = []

    def add(root: str, src: Path, dst: Path) -> None:
        rel_src = src.relative_to(roots[root]).as_posix()
        if any(rel_src.startswith(p) for p in SKIP_SOURCE_PREFIXES):
            return
        items.append(Item(src, dst, dst.relative_to(dest).as_posix(), root))

    for root, src_rel, dst_rel in SKILL_TREES + ASSET_TREES:
        base = roots[root] / src_rel
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*")):
            if f.is_file():
                add(root, f, dest / dst_rel / f.relative_to(base))

    for root, src_rel, dst_rel in SINGLE_FILES:
        f = roots[root] / src_rel
        if f.is_file():
            add(root, f, dest / dst_rel)

    for root, src_dir, pattern, dst_dir in FLAT_GLOBS:
        base = roots[root] / src_dir
        if not base.is_dir():
            continue
        for f in sorted(base.glob(pattern)):
            if f.is_file():
                add(root, f, dest / dst_dir / f.name)

    links: list[Link] = []
    proto_dest = dest / PROTOCOL_DEST
    proto_root, proto_rel = PROTOCOL_SRC
    proto_src = roots[proto_root] / proto_rel
    if proto_src.is_dir():
        for f in sorted(proto_src.glob("*.md")):
            link = dest / PROTOCOL_LINK_DIR / f.name
            links.append(Link(link, proto_dest / f.name, link.relative_to(dest).as_posix()))

    rendered = {it.dst for it in items}
    for link_rel, target_rel in EXTRA_LINKS:
        target = dest / target_rel
        if target in rendered:
            links.append(Link(dest / link_rel, target, link_rel))

    seen: dict[Path, Item] = {}
    for it in items:
        if it.dst in seen:
            print(f"warning: {it.rel} rendered twice ({seen[it.dst].root} and {it.root})", file=sys.stderr)
        seen[it.dst] = it

    for it in items:
        it.compute()
    for ln in links:
        ln.compute()
    return items, links


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render(items: list[Item], links: list[Link]) -> tuple[int, int]:
    written = 0
    for it in items:
        if it.status == "same":
            continue
        it.dst.parent.mkdir(parents=True, exist_ok=True)
        if it.dst.is_symlink():
            it.dst.unlink()
        if is_text(it.src):
            it.dst.write_text(it.rendered(), encoding="utf-8")
        else:
            shutil.copyfile(it.src, it.dst)
        shutil.copymode(it.src, it.dst)  # preserve exec bits
        written += 1

    linked = 0
    for ln in links:
        if ln.status == "ok":
            continue
        ln.link.parent.mkdir(parents=True, exist_ok=True)
        if ln.link.is_symlink() or ln.link.exists():
            ln.link.unlink()
        ln.link.symlink_to(ln.target)
        linked += 1
    return written, linked


def prune(items: list[Item], links: list[Link], dest: Path, assume_yes: bool, dry_run: bool) -> list[Path]:
    """Files inside the rendered skill trees that the plugins no longer provide."""
    keep = {it.dst.resolve() for it in items} | {ln.link.resolve() for ln in links}
    stale: list[Path] = []
    for _, _, dst_rel in SKILL_TREES:
        base = dest / dst_rel
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*")):
            if f.is_file() and not f.is_symlink() and f.resolve() not in keep:
                stale.append(f)
    if not stale:
        return []
    print("\nPrune candidates (in dest, absent from the plugins):")
    for f in stale:
        print(f"  - {f.relative_to(dest)}")
    if dry_run:
        return stale
    if not assume_yes:
        print("Refusing to delete without --yes.")
        return []
    for f in stale:
        f.unlink()
    print(f"Deleted {len(stale)} stale file(s).")
    return stale


# --------------------------------------------------------------------------
# Invariants
# --------------------------------------------------------------------------

def scan(path: Path, needles: list[str]) -> list[tuple[int, str, str]]:
    if not is_text(path):
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for needle in needles:
            if needle not in line:
                continue
            # `${PLUGIN_ROOT}` inside workflow JS is the JS template variable, not the placeholder.
            if needle == "{PLUGIN_ROOT}" and path.suffix == ".js" and "${PLUGIN_ROOT}" in line and line.count("{PLUGIN_ROOT}") == line.count("${PLUGIN_ROOT}"):
                continue
            # Machine-local read-side telemetry hook is intentionally referenced by ~/.claude path (guarded call).
            if "full-research-telemetry.py" in line:
                continue
            hits.append((n, needle, line.strip()[:160]))
    return hits


def check(roots: dict[str, Path], dest: Path, items: list[Item]) -> tuple[int, int]:
    print("\n--- invariants: dest ---")
    dest_bad = 0
    for it in items:
        if it.dst.is_symlink() or not it.dst.exists():
            continue
        for n, needle, line in scan(it.dst, DEST_FORBIDDEN):
            print(f"{it.dst}:{n}: [{needle}] {line}")
            dest_bad += 1
    print(f"dest violations: {dest_bad}")

    print("\n--- invariants: plugins ---")
    plugin_bad = 0
    for name, root in roots.items():
        if not root.is_dir():
            continue
        for f in sorted(root.rglob("*")):
            if not f.is_file():
                continue
            rel = f.relative_to(root).as_posix()
            if (
                rel in PLUGIN_EXCEPTIONS
                or rel.startswith(PLUGIN_EXCEPTION_PREFIXES)
                or rel.startswith(".git/")
            ):
                continue
            for n, needle, line in scan(f, PLUGIN_FORBIDDEN):
                print(f"{name}:{rel}:{n}: [{needle}] {line}")
                plugin_bad += 1
    exempt = sorted(PLUGIN_EXCEPTIONS) + [p + "**" for p in PLUGIN_EXCEPTION_PREFIXES]
    print(f"plugin violations: {plugin_bad} (exceptions: {', '.join(exempt)})")
    return dest_bad, plugin_bad


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for name, default in DEFAULT_ROOTS.items():
        ap.add_argument(f"--{name}", type=Path, default=default, help=f"source root of the `{name}` plugin (default {default})")
    ap.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    ap.add_argument("--dry-run", action="store_true", help="print the plan, change nothing")
    ap.add_argument("--check", action="store_true", help="only verify invariants")
    ap.add_argument("--prune", action="store_true", help="drop dest files the plugins no longer have")
    ap.add_argument("--yes", action="store_true", help="confirm --prune deletions")
    ap.add_argument("--verbose", action="store_true", help="full diffs instead of +/- counts")
    args = ap.parse_args()

    roots = {name: getattr(args, name.replace("-", "_")).resolve() for name in DEFAULT_ROOTS}
    dest = args.dest.resolve()
    missing = [f"{n}: {p}" for n, p in roots.items() if not p.is_dir()]
    if missing:
        print("error: source root(s) not found:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 3

    for name, path in roots.items():
        print(f"{name:<17} {path}")
    print(f"dest:             {dest}")

    items, links = collect(roots, dest)

    if not args.check:
        print(f"\n--- plan ({len(items)} files, {len(links)} symlinks) ---")
        for it in items:
            if it.status == "same":
                continue
            mark = "NEW    " if it.status == "new" else f"CHANGED"
            extra = "" if it.status == "new" else f"  (+{it.plus}/-{it.minus})"
            print(f"  {mark} {it.rel}{extra}")
            if args.verbose and it.diff:
                sys.stdout.writelines(it.diff)
        for ln in links:
            if ln.status != "ok":
                print(f"  SYMLINK[{ln.status}] {ln.rel} -> {ln.target}")

        n_new = sum(1 for i in items if i.status == "new")
        n_chg = sum(1 for i in items if i.status == "changed")
        n_same = sum(1 for i in items if i.status == "same")
        l_new = sum(1 for l in links if l.status == "new")
        l_re = sum(1 for l in links if l.status == "retarget")
        l_file = sum(1 for l in links if l.status == "replace-file")
        l_ok = sum(1 for l in links if l.status == "ok")
        print(
            f"\nsummary: {n_new} new, {n_chg} changed, {n_same} same | "
            f"symlinks: {l_new} new, {l_re} retarget, {l_file} replacing regular file, {l_ok} ok"
        )

    replaced: list[str] = []
    if not args.check and not args.dry_run:
        written, linked = render(items, links)
        replaced = [l.rel for l in links if l.status == "replace-file"]
        print(f"\nrendered {written} file(s), {linked} symlink(s)")
        if replaced:
            print("regular files replaced by symlinks:")
            for r in replaced:
                print(f"  - {r}")

    if args.prune:
        prune(items, links, dest, args.yes, args.dry_run or args.check)

    dest_bad, plugin_bad = check(roots, dest, items)

    if dest_bad:
        return 1
    if plugin_bad:
        if args.dry_run:
            print("(dry-run: plugin violations are a warning only)")
            return 0
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
