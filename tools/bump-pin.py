#!/usr/bin/env python3
"""Пин внешних плагинов в marketplace.json: ref = тег релиза, sha = коммит тега.

Использование:
  python3 tools/bump-pin.py tldr tldr--v1.1.0          # обновить ref+sha у записи tldr
  python3 tools/bump-pin.py --check                     # у всех внешних записей sha соответствует ref
  python3 tools/bump-pin.py --list                      # таблица внешних записей

Внутренние записи (source — строка "./plugins/…") не трогаются.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_MARKETPLACE = Path(__file__).resolve().parent.parent / ".claude-plugin" / "marketplace.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def ls_remote(url: str, ref: str) -> str | None:
    """SHA коммита для тега/ветки; для аннотированных тегов берёт разыменованный ^{}."""
    proc = subprocess.run(
        ["git", "ls-remote", "--tags", "--heads", url, ref, f"{ref}^{{}}"],
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        print(f"[error] git ls-remote {url} {ref}: {proc.stderr.strip()}", file=sys.stderr)
        return None
    sha = None
    for line in proc.stdout.splitlines():
        h, name = line.split("\t", 1)
        if name.endswith("^{}"):
            return h
        sha = h
    return sha


def external(entry: dict) -> bool:
    return isinstance(entry.get("source"), dict) and "url" in entry["source"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plugin", nargs="?")
    ap.add_argument("tag", nargs="?")
    ap.add_argument("--marketplace", type=Path, default=DEFAULT_MARKETPLACE)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    data = json.loads(args.marketplace.read_text(encoding="utf-8"))
    plugins = data["plugins"]

    if args.list or args.check:
        bad = 0
        for e in plugins:
            if not external(e):
                continue
            src = e["source"]
            ref, sha = src.get("ref", ""), src.get("sha", "")
            status = ""
            if args.check:
                if not ref or not SHA_RE.match(sha or ""):
                    status, bad = "НЕТ ref/sha", bad + 1
                else:
                    live = ls_remote(src["url"], ref)
                    status = "ok" if live == sha else f"РАСХОЖДЕНИЕ live={live}"
                    bad += 0 if live == sha else 1
            print(f"{e['name']:<16} {src['source']:<10} {ref:<28} {sha[:12] if sha else '—':<12} {src.get('path','')} {status}")
        return 1 if bad else 0

    if not args.plugin or not args.tag:
        ap.error("нужны <plugin> <tag>, либо --check / --list")
    for e in plugins:
        if e["name"] == args.plugin:
            if not external(e):
                sys.exit(f"{args.plugin}: внутренняя запись, пин не нужен")
            sha = ls_remote(e["source"]["url"], args.tag)
            if not sha or not SHA_RE.match(sha):
                sys.exit(f"{args.plugin}: тег {args.tag} не найден в {e['source']['url']}")
            e["source"]["ref"] = args.tag
            e["source"]["sha"] = sha
            data["plugins"] = sorted(plugins, key=lambda p: p["name"])
            args.marketplace.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"{args.plugin}: ref={args.tag} sha={sha}")
            return 0
    sys.exit(f"{args.plugin}: записи нет в {args.marketplace}")


if __name__ == "__main__":
    sys.exit(main())
