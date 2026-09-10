# Визуальная айдентика витрины Jadlis (выбрана 07.09.2026)

Стиль A мудборда: **чистая плоская инфографика на светлом фоне, две акцентные краски**. Визуал несёт больше информации, чем текст: у каждой картинки есть подписи на русском, картинки иллюстрируют ровно то, что подписано.

## Палитра (снято с эталонных картинок)

| Роль | Hex |
|---|---|
| Фон | `#fdfbf7` (тёплый off-white) |
| Акцент 1 — бирюза (основные фигуры, стрелка процесса) | `#1a7174` (тёмный вариант `#0a5352`) |
| Акцент 2 — оранжевый (результат, цель, подсветка) | `#f37d2c` (тёмный вариант `#e26e13`) |
| Линии и текст | `#2f3333` |
| Вторичный серый | `#666969`, светлый `#b3b3b0` |

## Палитра хаба (README `jadlis-hub`, выбрана 10.09.2026 по трём пробам hero)

Только для README хаба; советы и репо каталога остаются на палитре выше, их картинки не перерисовываются.

| Роль | Hex |
|---|---|
| Фон | `#f7f8fc` (очень светлый бело-голубой) |
| Акцент 1 — электрик-синий (нечётные блоки, стрелки, ссылка) | `#1f4bff` |
| Акцент 2 — коралл (чётные блоки, подсветка) | `#ff5a4e` |
| Текст | почти чёрный `#111318` |

Стиль: светлый минимализм, крупные плоские формы, тонкие контуры, мягкая тень; предметы и схемы без людей; короткий русский тезис внутри картинки. Префикс промпта (English):

```
Style: clean minimalist infographic on a very light background (#f7f8fc), generous whitespace, large flat geometric shapes, crisp thin outlines, two saturated accent colors — electric blue (#1f4bff) and coral (#ff5a4e) — plus near-black text, subtle soft shadows only, premium and precise, no gradients, no glow, no robots, no people, no stock photos, no watermark, no brand names or logos. Short Russian labels rendered as crisp, correctly spelled Cyrillic text in a modern geometric sans-serif. Wide 2:1 composition, 1280x640.
```

## Шрифтовой характер

Геометрический гротеск, жирные заголовки, подписи в одну-две строки. Кириллица в картинках держится (проверено на 7 картинках 07.09) — подписи ставятся внутрь картинки; текстовая альтернатива под картинкой всё равно обязательна (доступность).

## Типы визуалов

- **hero** 1280×640 (она же social preview): заголовок = проблема или тезис одной фразой, три-четыре блока с подписями, стрелка, результат справа (график вверх, не галочка).
- **схема причина → следствие**: четыре скруглённых блока в ряд, иконка сверху, подпись снизу на цветной подложке (чередование бирюза/оранжевый), подпись-примечание под последним блоком.
- **mind-карта**: центральный узел + ветви по той же палитре (пока без эталона).
- **таблица-картинка «было → стало»**: три колонки, левая серая, правая оранжевая.

## Запреты

**Названия брендов и сервисов в картинку не идут** (gpt-image-2 подменяет их на «APP» даже по референсу, проверено 07.09): в картинке — категории («форумы», «поиск по смыслу»), бренды — в тексте под картинкой. Без роботов, без «AI-глиттера» и свечения, без стоковых людей, без водяных знаков, без неона и тёмных фонов, без Mermaid в README.

## Стилевой префикс промпта (English, для gpt-image-2 через /codex-image)

```
Style: clean flat infographic on a light off-white background (#fdfbf7), two accent colors — deep teal (#1a7174) and warm orange (#f37d2c), thin dark-gray (#2f3333) line art, generous whitespace, geometric shapes, a modern geometric sans-serif look. Short Russian labels rendered as crisp, correctly spelled Cyrillic text. No robots, no glowing AI sparkles or glitter, no stock-photo people, no watermark. Wide 2:1 composition, 1280x640.
```

Правки по одной картинке — image-to-image: `codex exec -i <эталон>.png -C <dir> '$imagegen Based on the attached image, redraw ... with these changes: ...'`. Эталоны: `docs/img/brand-reference-hero.webp`, `docs/img/scheme-context-goal-tools.webp` (первый переименован 07.09 из `hero-jadlis-start.webp`, чтобы освободить каноническое имя картинке первого экрана README); промпты — `docs/img/prompts/<имя>.md`.
