# jadlis-hub — конвенции репо

Хаб передачи стека Jadlis: маркетплейс `jadlis`, единственный внутренний плагин `plugins/jadlis-hub`, внешние — записями `url` / `git-subdir` с пином `ref` + `sha`. Доки шагов живут в своих репо (`docs/tier/README.md`), в хабе остаются только `docs/brand` и `docs/img`. Эти правила читает агент, который коммитит.

## Коммиты

- Тема — Conventional Commits на английском: `type(scope): subject`, ≤72 символа. `scope` = `hub`, `jadlis-hub` (плагин), `docs` или `tools`.
- Тело двухслойное, шаблон в `.gitmessage` (`git config commit.template .gitmessage`):
  1. `Что изменилось:` — 1–3 предложения по-русски простым языком, для человека.
  2. `Details (for agents):` — буллеты `Added / Changed / Removed / Migration / Refs` с путями.
- Без строк атрибуции (`Co-Authored-By` и подобных).

## Релизы

- Версия живёт только в `plugin.json`; бамп — в том же коммите, что и изменение (версия = ключ кеша обновлений).
- Тег `{plugin}--v{X.Y.Z}`: `claude plugin tag --push plugins/<name>`.
- GitHub Release поверх тега: заголовок `<plugin> X.Y.Z — <кратко по-русски> / <short EN>`, тело — вывод `python3 tools/release-notes.py plugins/<name>` (запись из `CHANGELOG.md`).
- `CHANGELOG.md` плагина: `## [X.Y.Z] — YYYY-MM-DD — <кратко по-русски> / <short EN>`, затем `### Для человека` (≤3 буллета простым языком) и `### For agents` (`Added / Changed / Removed / Migration / Breaking`, с путями).
- Только patch-forward: никаких force-push, переписывания тегов и релизов.

## README и доки

- Пара `README.md` (RU) + `README.en.md` (EN); первая строка — переключатель `Русский · English` со ссылками друг на друга.
- Одинаковое число и порядок H2 в паре. Проверка: `python3 tools/readme-parity.py` (H2, Mermaid через `mmdc`, относительные ссылки).
- Документ инструмента — 5 секций: **Зачем / Как выглядит / Как поставить / Как пользоваться / Границы и стоимость**. Список ≤5 пунктов, первая строка секции — действие.
- Схемы — Mermaid (GitHub рендерит сам; синтаксис проверяется локально `mmdc`, не через API). Иллюстрации — `docs/img/*.webp` (извлекаются `tools/extract-visuals.py`). Примеры вывода — синтетические или заранее обезличенные. Скриншоты просматриваются глазами перед коммитом.
- Числа и механика сверяются с конкретным тегом плагина; тег указывается рядом с числом.

## Внешние плагины в `marketplace.json`

- Каждая внешняя запись несёт `ref` = тег релиза и `sha` (40 hex). Обновить пин: `python3 tools/bump-pin.py <plugin> <tag>`; проверить все: `python3 tools/bump-pin.py --check`.
- `plugins[]` отсортирован по имени; имена плагинов и маркетплейса неизменяемы.

## Приватность

- В файлах репо нет ключей, почт, телефонов, путей владельца (`/Users/<имя>`) и упоминаний приватного бэкапа `.claude/`. Перед пушем: `gitleaks git .` и `python3 tools/privacy-grep.py` (CI гоняет оба).
- Ключи получателя живут в Связке ключей macOS (стандарт описан в репо `jadlis-search`), не в репо.

## Разработка

- Правки только в рабочем клоне `~/jadlis-hub`, никогда в `~/.claude/plugins/marketplaces/` (фоновый рефреш стирает правки).
- Перед коммитом: `claude plugin validate .claude-plugin/marketplace.json` и `python3 tools/readme-parity.py`.
- Язык доков — русский (RU-файл первичен), код и идентификаторы — английский.
