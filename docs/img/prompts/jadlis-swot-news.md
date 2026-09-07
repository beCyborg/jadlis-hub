# jadlis-swot-news

Мысль: общий поток новостей по выбранным направлениям проходит через файл с твоим профилем, кластеры разбирают параллельные аналитики, и наружу выходит только дельта — короткий выпуск дня и карточка темы, которая держится не первый день.

## hero

- Картинка: `docs/img/hero-jadlis-swot-news.webp`
- Заголовок: «Что из мировых новостей меняется у тебя»
- Слева: общий поток новостей; подпись «Поток новостей»
- Посередине: файл с твоим профилем, через который поток проходит; подпись «Профиль»
- Справа: короткий выпуск дня; подпись «Выпуск дня»
- Справа же: карточка темы, которая держится не первый день; подпись «Карточка темы» и пометка «держится не первый день»
- Названия источников и сервисов в картинку не идут: только категории

```
Style: clean flat infographic on a light off-white background (#fdfbf7), two accent colors — deep teal (#1a7174) and warm orange (#f37d2c), thin dark-gray (#2f3333) line art, generous whitespace, geometric shapes, a modern geometric sans-serif look. Short Russian labels rendered as crisp, correctly spelled Cyrillic text. No robots, no glowing AI sparkles or glitter, no stock-photo people, no watermark. Wide 2:1 composition, 1280x640.

Hero illustration for a GitHub README about a personal daily news digest. Bold Russian headline across the top «Что из мировых новостей меняется у тебя». On the left, a broad flow of many small teal news cards drifting to the right, drawn as thin outlined rectangles of equal height scattered at different offsets — it must read as a loose stream of cards, never as a bar chart and never as a column diagram; the flow is labeled «Поток новостей». In the middle, one upright document card with four short gray rows inside it, labeled «Профиль»; the whole flow narrows and passes straight through this card, and only a few cards come out on its right side. On the right, a thick orange arrow from the profile card points to a short document with five text lines and a small triangle delta glyph in its corner, labeled «Выпуск дня». Below that document, a separate single rounded card carrying a short horizontal row of three small dots that stand for previous days, labeled «Карточка темы», with a small Russian caption under it «держится не первый день». No logos, no brand names, no service names. Text must be spelled exactly.
```

## scheme

- Картинка: `docs/img/how-jadlis-swot-news.webp`
- Блоки: «Конфиг» → «Проверка свежести батча» → «Сбор по категориям» → «Аналитики и обогатитель параллельно» → «Сборка дельты» → «Файл выпуска» → «Карточки и watchlist» → «Дайджест»
- Раскладка: два ряда по четыре блока, переход с конца верхнего ряда в начало нижнего
- Пометка сбоку от второго блока: «батч не новее — выпуска нет»
- Подпись под четвёртым блоком: «до четырёх, по одному на кластер»
- Примечание под седьмым блоком: «затухшая тема уходит в архив»

```
Style: clean flat infographic on a light off-white background (#fdfbf7), two accent colors — deep teal (#1a7174) and warm orange (#f37d2c), thin dark-gray (#2f3333) line art, generous whitespace, geometric shapes, a modern geometric sans-serif look. Short Russian labels rendered as crisp, correctly spelled Cyrillic text. No robots, no glowing AI sparkles or glitter, no stock-photo people, no watermark. Wide 2:1 composition, 1280x640.

Cause-and-effect diagram with eight rounded boxes arranged in two rows of four. Arrows connect the top row left to right, then one curved arrow runs down the right side to the first box of the bottom row, then arrows continue left to right along the bottom row. Alternating teal and orange label plates, a simple geometric icon on top of each box: a gear over a small settings file; a calendar sheet with a clock badge and a check mark; a fan of small cards being sorted into three folders; four short parallel arrows pointing right side by side, drawn as thin outlined arrows of equal length so they read as parallel lanes and never as a bar chart, with a fifth thinner arrow branching off to a small globe; several arrows merging into one triangle delta glyph; a document card with text lines; a small stack of cards beside a checklist with an eye outline; a speech bubble with three short lines. Russian labels under the icons, in order: «Конфиг» → «Проверка свежести батча» → «Сбор по категориям» → «Аналитики и обогатитель параллельно» → «Сборка дельты» → «Файл выпуска» → «Карточки и watchlist» → «Дайджест». Beside the second box a short dashed arrow turns aside and ends in a crossed-out document, with a small Russian caption «батч не новее — выпуска нет». Under the fourth box a small Russian caption «до четырёх, по одному на кластер». Under the seventh box a small Russian caption «затухшая тема уходит в архив». No logos, no brand names, no service names. Text must be spelled exactly.
```

## alt

- hero (`docs/img/hero-jadlis-swot-news.webp`): Общий поток новостей проходит через файл с профилем, наружу выходит короткий выпуск дня и карточка темы
  Текстом: слева общий поток новостей, посередине — файл с твоим профилем, справа — короткий выпуск дня и карточка темы, которая держится не первый день.
- scheme (`docs/img/how-jadlis-swot-news.webp`): Конфиг и проверка свежести, потом кластеры расходятся по параллельным аналитикам, на выходе выпуск дня и карточки
  Текстом: конфиг → проверка свежести батча → сбор по категориям → аналитики и обогатитель параллельно → сборка дельты → файл выпуска → карточки и watchlist → дайджест.
