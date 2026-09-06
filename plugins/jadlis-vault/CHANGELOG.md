# Changelog — jadlis-vault

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), версии — [SemVer](https://semver.org/lang/ru/).

## [1.0.1] — 2026-09-06 — README RU/EN / bilingual README

### Для человека
- У плагина появилась своя страница: зачем он, что появляется в папке, как поставить и что он не делает.
- Английская версия рядом — можно показать человеку, который не читает по-русски.

### For agents
- Added: `README.md` (RU) и `README.en.md` (EN) — пять секций «Зачем / Как выглядит / Как поставить / Как пользоваться / Границы и стоимость», картинка `docs/img/02-methodology-03.webp`, синтетический пример дерева vault и дневной заметки.
- Added: `CHANGELOG.md` в формате хаба (`### Для человека` / `### For agents`).
- Changed: `version` в `.claude-plugin/plugin.json` — 1.0.0 → 1.0.1 (docs-only, patch).
- Migration: не требуется — поведение скилла `vault-setup` не менялось.

## [1.0.0] — 2026-09-01 — первый релиз в маркетплейсе `jadlis` / first marketplace release

### Для человека
- Скилл `/jadlis-vault:vault-setup`: раскладывает скелет папок vault, кладёт `CLAUDE.md`, ставит CSS-сниппет `hide-files` и проводит первый вечерний перезапуск дня.
- Спрашивает путь к папке при включении и никогда не создаёт её молча.

### For agents
- Added: `skills/vault-setup/SKILL.md` — шаги 0–5 (детект состояния, скелет, `CLAUDE.md`, сниппет, первый перезапуск дня, журнал передачи).
- Added: `assets/CLAUDE.md.template`, `assets/hide-files.css`.
- Added: `.claude-plugin/plugin.json` с `userConfig.VAULT_PATH` (тип `directory`, по умолчанию `~/Jadlis`), `$schema`, лицензией MIT и SemVer-версией.
