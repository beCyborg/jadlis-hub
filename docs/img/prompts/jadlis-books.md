# jadlis-books

Мысль: ты называешь название, автора или строку DOI — скилл ищет запись с фильтрами, ранжирует кандидатов, качает файл в папку, сверяет его первые байты и печатает остаток быстрых загрузок.

## hero

- Картинка: `docs/img/hero-jadlis-books.webp`
- Заголовок: «Название, автор или DOI — файл в папке»
- Слева: три входа — «Название», «Автор», «DOI»
- Справа: карточка результата — отобранный файл в папке загрузок, подпись «Файл в папке загрузок»
- Под карточкой: тонкая полоса остатка квоты, подпись «Остаток быстрых загрузок»
- Названия сервисов в картинку не идут: только категории; обложки книг пустые

```
Style: clean flat infographic on a light off-white background (#fdfbf7), two accent colors — deep teal (#1a7174) and warm orange (#f37d2c), thin dark-gray (#2f3333) line art, generous whitespace, geometric shapes, a modern geometric sans-serif look. Short Russian labels rendered as crisp, correctly spelled Cyrillic text. No robots, no glowing AI sparkles or glitter, no stock-photo people, no watermark. Wide 2:1 composition, 1280x640.

Hero illustration for a GitHub README about fetching a book or a paper by a plain request. Bold Russian headline across the top «Название, автор или DOI — файл в папке». On the left, three teal blocks stacked one above the other, each with a flat geometric icon above its label: a search field holding a blank book outline labeled «Название», a signature line on a card labeled «Автор», a short identifier string on a paper sheet labeled «DOI». One thick orange arrow gathers the three blocks and points right into a tall orange result card: inside the card an open folder holds a single file row with a blank-cover book icon, labeled «Файл в папке загрузок»; directly under that row a thin flat horizontal bar, drawn as a thin outline partly filled, labeled «Остаток быстрых загрузок» — it must read as a remaining-quota strip, never as a bar chart. All book covers are blank with no titles. No logos, no brand names, no service names. Text must be spelled exactly.
```

## scheme

- Картинка: `docs/img/how-jadlis-books.webp`
- Блоки: «Запрос» → «Поиск с фильтрами» → «Ранжирование кандидатов» → «Загрузка членским API» → «Проверка первых байтов» → «Отчёт с путём и остатком квоты»
- У первого блока развилка на три вида запроса: «Одна книга», «Список», «DOI» — ветки сходятся во второй блок
- У третьего блока: список кандидатов, верхняя строка выделена
- У пятого блока: слишком маленький файл-заглушка отбрасывается, подпись «заглушка — берём следующего кандидата»
- Примечание под последним блоком: «на нуле квоты скилл останавливается»
- Названия сервисов и зеркал в картинку не идут: только категории

```
Style: clean flat infographic on a light off-white background (#fdfbf7), two accent colors — deep teal (#1a7174) and warm orange (#f37d2c), thin dark-gray (#2f3333) line art, generous whitespace, geometric shapes, a modern geometric sans-serif look. Short Russian labels rendered as crisp, correctly spelled Cyrillic text. No robots, no glowing AI sparkles or glitter, no stock-photo people, no watermark. Wide 2:1 composition, 1280x640.

Cause-and-effect diagram with six rounded boxes in a row connected left to right by arrows, alternating teal and orange label plates, a simple geometric icon on top of each box: a text field with a cursor beside a small identifier tag; a funnel over a list of entries; a vertical list of three candidate rows whose top row is outlined in orange; a downward arrow entering an open folder, with a small membership card beside it; a magnifying glass over the leading edge of a file sheet; a report sheet with one path row and a thin horizontal strip under it. Russian labels under the icons: «Запрос» → «Поиск с фильтрами» → «Ранжирование кандидатов» → «Загрузка членским API» → «Проверка первых байтов» → «Отчёт с путём и остатком квоты». From the first box three thin teal branches fan out to three small plates labeled «Одна книга», «Список», «DOI», and the three branches rejoin into the second box. The candidate rows in the third box are flat outlined rectangles of equal width carrying a small numeral 1, 2, 3 on the left, with no 3D depth and no solid fill — they must read as a ranked list of files, never as a bar chart. Beside the fifth box a very small file sheet is pushed aside by a thin orange line, with a small Russian caption «заглушка — берём следующего кандидата». Under the last box a small Russian caption «на нуле квоты скилл останавливается». All book covers are blank with no titles. No logos, no brand names, no service names. Text must be spelled exactly.
```

## alt

- hero (`docs/img/hero-jadlis-books.webp`): Название, автор или DOI на входе — файл в папке и остаток быстрых загрузок на выходе
  Текстом: слева запрос обычными словами или строкой DOI, справа — отобранный файл в папке загрузок и строка с остатком быстрых загрузок.
- scheme (`docs/img/how-jadlis-books.webp`): Запрос делится на одиночный, батч и DOI, кандидаты ранжируются, файл проверяется по первым байтам
  Текстом: запрос → поиск с фильтрами → ранжирование кандидатов → загрузка членским API → проверка первых байтов файла → отчёт с путём и остатком квоты.
