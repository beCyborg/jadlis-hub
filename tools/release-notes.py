#!/usr/bin/env python3
"""Тело и заголовок GitHub Release из CHANGELOG.md плагина.

Формат записи в CHANGELOG.md:

  ## [1.2.0] — 2026-09-06 — проба провайдеров / provider probe
  ### Для человека
  - …
  ### For agents
  - Added: …

Использование:
  python3 tools/release-notes.py plugins/jadlis-start            # тело релиза для текущей версии plugin.json
  python3 tools/release-notes.py plugins/jadlis-start --title    # заголовок: «jadlis-start 1.2.0 — … / …»
  python3 tools/release-notes.py plugins/jadlis-start --version 1.1.0
  python3 tools/release-notes.py plugins/jadlis-start --release  # gh release create <tag> с телом и заголовком

Для root-as-plugin репо укажи `.`.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HEAD_RE = re.compile(
    r"^##\s+\[(?P<ver>\d+\.\d+\.\d+)\]"
    r"(?:\s+[—–-]+\s+(?P<date>\d{4}-\d{2}-\d{2}))?"
    r"(?:\s+[—–-]+\s+(?P<summary>.+?))?\s*$"
)


def load_plugin(plugin_dir: Path) -> tuple[str, str]:
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        sys.exit(f"нет {manifest}")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    return data["name"], data.get("version", "")


def parse_changelog(path: Path) -> dict[str, dict]:
    if not path.exists():
        sys.exit(f"нет {path}")
    entries: dict[str, dict] = {}
    current: dict | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HEAD_RE.match(line)
        if m:
            current = {"date": m.group("date") or "", "summary": (m.group("summary") or "").strip(), "body": []}
            entries[m.group("ver")] = current
            continue
        if line.startswith("## "):
            current = None
            continue
        if current is not None:
            current["body"].append(line)
    for e in entries.values():
        e["body"] = "\n".join(e["body"]).strip() + "\n"
    return entries


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plugin_dir")
    ap.add_argument("--version")
    ap.add_argument("--title", action="store_true", help="напечатать только заголовок")
    ap.add_argument("--release", action="store_true", help="создать GitHub Release через gh")
    ap.add_argument("--repo", help="owner/repo для gh (по умолчанию — текущий)")
    args = ap.parse_args()

    plugin_dir = Path(args.plugin_dir)
    name, manifest_ver = load_plugin(plugin_dir)
    version = args.version or manifest_ver
    entries = parse_changelog(plugin_dir / "CHANGELOG.md")
    if version not in entries:
        sys.exit(f"в CHANGELOG.md нет записи [{version}] (есть: {', '.join(entries) or '—'})")
    entry = entries[version]
    for section in ("### Для человека", "### For agents"):
        if section not in entry["body"]:
            print(f"[warn] в записи [{version}] нет секции «{section}»", file=sys.stderr)

    tag = f"{name}--v{version}"
    title = f"{name} {version}" + (f" — {entry['summary']}" if entry["summary"] else "")
    if args.title:
        print(title)
        return 0
    if not args.release:
        print(entry["body"], end="")
        return 0

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tf:
        tf.write(entry["body"])
        notes_path = tf.name
    cmd = ["gh", "release", "create", tag, "--title", title, "--notes-file", notes_path, "--verify-tag"]
    if args.repo:
        cmd += ["--repo", args.repo]
    print("$ " + " ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
