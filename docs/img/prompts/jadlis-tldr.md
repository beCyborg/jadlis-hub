# jadlis-tldr

Мысль: субтитры видео или текст файла проходят через одну и ту же рамку разбора — суть, ключевые идеи, что делать, ограничения — и ложатся отдельной markdown-заметкой в твою папку.

## hero

- Картинка: `docs/img/hero-jadlis-tldr.webp`
- Заголовок: «Видео или файл — одна рамка разбора, заметка в папке»
- Слева: два входа один под другим — «Ссылка на видео» и «Путь к файлу»
- Посередине: общая рамка разбора с четырьмя пронумерованными строками — «Суть», «Ключевые идеи», «Что делать», «Ограничения»
- Справа: готовая заметка в папке; подпись «Заметка в твоей папке»
- Названия сервисов в картинку не идут: только категории

```
Style: clean flat infographic on a light off-white background (#fdfbf7), two accent colors — deep teal (#1a7174) and warm orange (#f37d2c), thin dark-gray (#2f3333) line art, generous whitespace, geometric shapes, a modern geometric sans-serif look. Short Russian labels rendered as crisp, correctly spelled Cyrillic text. No robots, no glowing AI sparkles or glitter, no stock-photo people, no watermark. Wide 2:1 composition, 1280x640.

Hero illustration for a GitHub README about turning a video or a file into one saved note. Bold Russian headline across the top «Видео или файл — одна рамка разбора, заметка в папке». On the left, two teal cards stacked one above the other: a play triangle inside a rounded rectangle labeled «Ссылка на видео», and a document with a folded corner labeled «Путь к файлу». Two thick orange arrows run from both cards and meet in a single large teal frame in the middle of the composition, labeled «Одна рамка разбора». Inside that frame four short rows of thin outlined text lines sit one under another, each carrying a small numeral 1, 2, 3, 4 beside it and a short Russian caption: «Суть», «Ключевые идеи», «Что делать», «Ограничения» — flat outlined rows of equal length, no 3D depth, no solid fill, they must read as four sections of one document, never as a bar chart. From the right edge of the frame one thick orange arrow points into an orange note card with a small tag shape in its upper corner and a short bullet list on it, resting inside an open folder outline, labeled «Заметка в твоей папке». No logos, no brand names, no service names. Text must be spelled exactly.
```

## scheme

- Картинка: `docs/img/how-jadlis-tldr.webp`
- Блоки: «Ссылка или файл» → «Субтитры либо чтение файла» → «Разбор по одной рамке» → «Заметка с тегами в твоей папке»
- Во втором блоке два значка рядом: два пути входа сходятся в один
- Примечание под третьим блоком: «суть · ключевые идеи · что делать · ограничения»
- Названия сервисов и переменных в картинку не идут: только категории

```
Style: clean flat infographic on a light off-white background (#fdfbf7), two accent colors — deep teal (#1a7174) and warm orange (#f37d2c), thin dark-gray (#2f3333) line art, generous whitespace, geometric shapes, a modern geometric sans-serif look. Short Russian labels rendered as crisp, correctly spelled Cyrillic text. No robots, no glowing AI sparkles or glitter, no stock-photo people, no watermark. Wide 2:1 composition, 1280x640.

Cause-and-effect diagram with four rounded boxes in a row connected left to right by arrows, alternating teal and orange label plates, a simple geometric icon on top of each box: a link chain beside a document with a folded corner; two small icons side by side to show two ways in — a caption rectangle with two text lines and an open document; a card holding four short outlined rows with small numerals 1, 2, 3, 4 beside them; a note card with a bullet list and a small tag shape, resting inside an open folder outline. Russian labels under the icons: «Ссылка или файл» → «Субтитры либо чтение файла» → «Разбор по одной рамке» → «Заметка с тегами в твоей папке». The four rows inside the third box are flat outlined lines of equal length with no 3D depth and no solid fill — they must read as four sections of one note, never as a bar chart. Under the third box a small Russian caption in one line «суть · ключевые идеи · что делать · ограничения». No logos, no brand names, no service names. Text must be spelled exactly.
```

## alt

- hero (`docs/img/hero-jadlis-tldr.webp`): Ссылка на видео и файл сходятся в одну рамку разбора, из неё выходит markdown-заметка
  Текстом: слева два входа — ссылка на YouTube и путь к файлу, — посередине общая рамка разбора, справа готовая заметка в папке, которую ты указал при установке.
- scheme (`docs/img/how-jadlis-tldr.webp`): Ссылка или файл на входе, снятие субтитров или чтение файла, общая рамка разбора, заметка на выходе
  Текстом: ссылка или файл → субтитры либо чтение файла → разбор «суть, ключевые идеи, что делать, ограничения» → markdown-заметка с тегами в `TLDR_SAVE_DIR`.
