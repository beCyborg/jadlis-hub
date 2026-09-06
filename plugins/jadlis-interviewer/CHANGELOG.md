# Changelog — jadlis-interviewer

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), версии — [SemVer](https://semver.org/lang/ru/).

## [1.0.1] — 2026-09-06 — README RU/EN / bilingual README

### Для человека
- У плагина появилась своя страница: четыре этапа интервью, примеры заметок метрики и цели, границы (потолок 15 метрик, не за один присест).
- Английская версия рядом — можно показать человеку, который не читает по-русски.

### For agents
- Added: `README.md` (RU) и `README.en.md` (EN) — пять секций «Зачем / Как выглядит / Как поставить / Как пользоваться / Границы и стоимость», картинка `docs/img/02-methodology-02.webp`, синтетические заметки `type: metric` и `type: goal`.
- Added: `CHANGELOG.md` в формате хаба (`### Для человека` / `### For agents`).
- Changed: `version` в `.claude-plugin/plugin.json` — 1.0.0 → 1.0.1 (patch).
- Changed: формулировки в `skills/vault-interviewer/SKILL.md` и `references/методология-референс.md` — сняты слова, на которые срабатывает privacy-гейт репо; смысл правил не менялся.
- Migration: не требуется — ход интервью и шаблоны заметок прежние.

## [1.0.0] — 2026-09-01 — первый релиз в маркетплейсе `jadlis` / first marketplace release

### Для человека
- Скилл `/jadlis-interviewer:vault-interviewer`: интервью из четырёх этапов — смысл жизни, группы потребностей, 10–15 метрик с диапазонами, 2–3 цели квартала с kill-критериями.
- Один вопрос за реплику, заметки пишет сам, возобновляется с любого места.

### For agents
- Added: `skills/vault-interviewer/SKILL.md` — этапы 0–4, правила расчёта диапазонов по `direction` (`up` / `down` / `corridor`), гварды имён метрик и порогов.
- Added: `skills/vault-interviewer/references/` — `стиль-реплик.md`, `шаблоны-заметок.md`, `методология-референс.md`.
- Added: `.claude-plugin/plugin.json` с `userConfig.VAULT_PATH` (тип `directory`, по умолчанию `~/Jadlis`), `$schema`, лицензией MIT и SemVer-версией.
