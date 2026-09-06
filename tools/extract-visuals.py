#!/usr/bin/env python3
"""Вытащить встроенные data-URI картинки из HTML-страниц в docs/img/*.webp.

Ищет <img src="data:image/…;base64,…"> и url(data:image/…) в CSS, пишет файлы
<stem>-<n>.<ext>, дедуплицирует по содержимому, ведёт docs/img/INDEX.md с alt-текстом.
Мелкие картинки (иконки) пропускаются порогом --min-bytes.

Использование:
  python3 tools/extract-visuals.py path/to/*.html --out docs/img
  python3 tools/extract-visuals.py hub.html --out docs/img --stem hub

Скриншоты после извлечения просматриваются глазами — скрипт видит только байты.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import re
import sys
from pathlib import Path

IMG_RE = re.compile(
    r"<img\b[^>]*?\bsrc=[\"'](data:image/(?P<ext>webp|png|jpe?g|gif|svg\+xml);base64,(?P<b64>[A-Za-z0-9+/=\s]+))[\"'][^>]*>",
    re.I,
)
ALT_RE = re.compile(r"\balt=[\"']([^\"']*)[\"']", re.I)
CSS_RE = re.compile(r"url\((?:[\"'])?data:image/(?P<ext>webp|png|jpe?g|gif);base64,(?P<b64>[A-Za-z0-9+/=]+)(?:[\"'])?\)", re.I)

EXT_MAP = {"jpeg": "jpg", "svg+xml": "svg"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", nargs="+")
    ap.add_argument("--out", default="docs/img")
    ap.add_argument("--stem", help="префикс имён (по умолчанию — имя html-файла)")
    ap.add_argument("--min-bytes", type=int, default=4096)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    index_path = out / "INDEX.md"
    seen: dict[str, str] = {}
    for existing in out.glob("*"):
        if existing.is_file() and existing.suffix.lower() in {".webp", ".png", ".jpg", ".gif", ".svg"}:
            seen[hashlib.sha1(existing.read_bytes()).hexdigest()] = existing.name

    index_lines = []
    if index_path.exists():
        index_lines = index_path.read_text(encoding="utf-8").splitlines()
    else:
        index_lines = ["# Индекс иллюстраций", "", "| Файл | Источник | alt | Просмотрен глазами |", "|---|---|---|---|"]

    written = 0
    for html_path in map(Path, args.html):
        text = html_path.read_text(encoding="utf-8", errors="replace")
        stem = args.stem or html_path.stem
        n = 0
        matches = [(m.group("ext"), m.group("b64"), ALT_RE.search(m.group(0))) for m in IMG_RE.finditer(text)]
        matches += [(m.group("ext"), m.group("b64"), None) for m in CSS_RE.finditer(text)]
        for ext, b64, alt_m in matches:
            try:
                data = base64.b64decode(re.sub(r"\s+", "", b64))
            except Exception:
                continue
            if len(data) < args.min_bytes:
                continue
            digest = hashlib.sha1(data).hexdigest()
            if digest in seen:
                continue
            n += 1
            ext = EXT_MAP.get(ext.lower(), ext.lower())
            name = f"{stem}-{n:02d}.{ext}"
            while (out / name).exists():
                n += 1
                name = f"{stem}-{n:02d}.{ext}"
            (out / name).write_bytes(data)
            seen[digest] = name
            alt = (alt_m.group(1).strip() if alt_m else "").replace("|", "\\|")
            index_lines.append(f"| {name} | {html_path.name} | {alt} | ☐ |")
            written += 1
            print(f"{name}  {len(data)//1024} KB  {alt[:60]}")

    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"записано: {written}; индекс: {index_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
