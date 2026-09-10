#!/usr/bin/env python3
"""Впечатать названия сервисов в docs/img/hub-buy: gpt-image-2 подменяет торговые марки на «APP».

Использование:
  uv run --with pillow python3 tools/overlay-captions.py <in.png> <out.png>

Координаты (x-центр, y-верх) подобраны под композицию hub-buy (1280×640, две полки);
для другой картинки — поправить список `items`. Шрифт: Helvetica Neue Bold 21 px.
"""
from PIL import Image, ImageDraw, ImageFont
import sys
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
d = ImageDraw.Draw(im)
# find a bold-ish Helvetica Neue face in the ttc
font = None
for idx in range(0, 12):
    try:
        f = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 21, index=idx)
        name = f.getname()
        if name[1] in ("Bold", "Medium"):
            font = f; print("font", name, idx); break
    except Exception as e:
        break
if font is None:
    font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22); print("font fallback", font.getname())
BLUE, CORAL = (31, 75, 255), (255, 90, 78)
# (x_center, y_top, text, color)
items = [
    (347, 348, "Mac", BLUE),
    (549, 348, "Claude · тариф Max", BLUE),
    (750, 348, "Obsidian Sync", BLUE),
    (949, 348, "ElevenLabs · Anthropic", BLUE),
    (949, 374, "Brave · Firecrawl", BLUE),
    (1160, 348, "ChatGPT (Codex)", BLUE),
    (447, 598, "OpenAI", CORAL),
    (712, 598, "Grok", CORAL),
    (993, 598, "Anna’s Archive", CORAL),
]
for x, y, t, c in items:
    w = d.textlength(t, font=font)
    d.text((x - w/2, y), t, font=font, fill=c)
im.save(dst)
print("saved", dst, im.size)
