# jadlis-start

Мысль: одно слово в чате показывает семь строк маршрута 0 → 6 со статусами и ту строку, на которой ты стоишь сейчас; следующий шаг открывается только после пробы на твоей машине.

> Сюжеты приведены к тексту README от 07.09.2026: прежний эталон `hero-jadlis-start.webp` («Контекст → Цель → Инструменты») задаёт стиль A и палитру, но сюжет hero и схемы теперь другой — README требует маршрут со статусами.

## hero

- Картинка: `docs/img/hero-jadlis-start.webp`
- Заголовок: «Семь шагов, и видно, где ты сейчас»
- Содержимое: вертикальный список из семи строк, номера 0…6, у каждой строки статус — «готово», «идёт», «не начат»
- Акцент: одна строка вынесена из карточки и помечена «ты здесь» — с неё и продолжаешь

```
Style: clean flat infographic on a light off-white background (#fdfbf7), two accent colors — deep teal (#1a7174) and warm orange (#f37d2c), thin dark-gray (#2f3333) line art, generous whitespace, geometric shapes, a modern geometric sans-serif look. Short Russian labels rendered as crisp, correctly spelled Cyrillic text. No robots, no glowing AI sparkles or glitter, no stock-photo people, no watermark. Wide 2:1 composition, 1280x640.

Hero illustration for a GitHub README about a setup route. Bold Russian headline across the top «Семь шагов, и видно, где ты сейчас». Under it, one wide teal-outlined card holding a vertical list of exactly seven rows. Each row has a large numeral on the left, running 0, 1, 2, 3, 4, 5, 6 from top to bottom, then a plain neutral gray bar standing in for the step name, and a small status plate on the right: rows 0, 1 and 2 read «готово» on teal plates, row 3 reads «идёт» on an orange plate, rows 4, 5 and 6 read «не начат» on light gray plates. Row 3 is pulled slightly out to the left of the card, drawn with a thicker orange outline, and an orange marker beside it is labeled «ты здесь». No logos, no brand names. Text must be spelled exactly.
```

## scheme

- Картинка: `docs/img/how-jadlis-start.webp`
- Блоки: «Слово в чате» → «Маршрут 0 → 6 со статусами» → «Проба на машине» → «Шаг открывается»
- Ветка вниз от пробы: «Не подтвердилось — не открывается», примечание под ней «сказано, что именно упало»

```
Style: clean flat infographic on a light off-white background (#fdfbf7), two accent colors — deep teal (#1a7174) and warm orange (#f37d2c), thin dark-gray (#2f3333) line art, generous whitespace, geometric shapes, a modern geometric sans-serif look. Short Russian labels rendered as crisp, correctly spelled Cyrillic text. No robots, no glowing AI sparkles or glitter, no stock-photo people, no watermark. Wide 2:1 composition, 1280x640.

Cause-and-effect diagram with four rounded boxes in a row connected left to right by arrows, alternating teal and orange label plates, a simple geometric icon on top of each box: a chat bubble with one short word bar inside it, a list of seven short rows with small status plates, a laptop-like window with a checkmark drawn inside it, a step card with an opened padlock beside it. Russian labels: «Слово в чате» → «Маршрут 0 → 6 со статусами» → «Проба на машине» → «Шаг открывается». From the third box a thin orange arrow branches downward to one smaller box «Не подтвердилось — не открывается», and under that smaller box a small Russian caption «сказано, что именно упало». No logos, no brand names. Text must be spelled exactly.
```

## alt

- hero (`docs/img/hero-jadlis-start.webp`): Семь строк маршрута со статусами, отдельной строкой отмечено, где ты сейчас.
  Текстом: список из семи шагов, у каждого статус, одна строка помечена «ты здесь» — с неё и продолжаешь, вспоминать ничего не нужно.
- scheme (`docs/img/how-jadlis-start.webp`): Маршрут из семи шагов: после каждого проба на машине, и только потом следующий.
  Текстом: слово в чате → маршрут 0 → 6 со статусами → проба на машине → шаг открывается; не подтвердилось — не открывается, и сказано, что именно упало.
