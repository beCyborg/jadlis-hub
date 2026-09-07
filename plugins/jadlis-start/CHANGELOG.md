# Changelog — jadlis-start

## [2.1.1] — 2026-09-07

### Для человека
- Драйвер и доки ссылаются на `jadlis-start.git` (старый адрес `jadlis-plugins` редиректит, но новый — канонический).

### For agents
- Fixed: `HUB`/`DOCS`/`marketplace add` URLs in `skills/batch/SKILL.md`; docs sweep to the new plugin map (22 files).

## [2.1.0] — 2026-09-07 — репо на плагин / one repo per plugin

### Для человека
- Каталог `jadlis` теперь ведёт на отдельные репо: `search`, `research`, `science-research`, `verif` вместо одного `jadlis-research`; девять советов по одному (`advisor-decision` … `cognitive-biases`) вместо `advisors`; `books` вместо `annas-archive`, `advisor-psychologist` вместо `adv-psy`, `skill-builder` вместо `skill-creator`. Команды короткие: `/research`, `/verif`, `/advisor-decision`.
- Тир 2: ключи Brave и Firecrawl передаются `search` явно при установке — авто-установка зависимости их не спрашивает.

### For agents
- Changed: delivery table and probes (`references/детект-состояния.md`) for tiers 2–5 use the new plugin names; tier 5 counts installed councils and reads `MEMORY_DIR` from the first one found.
- Removed from the hub: `plugins/jadlis-research` (lives on as four repos; tags `jadlis-research--v1.0.0…v1.3.0` stay). `renames`: `jadlis-research` → null, `advisors` → null, `adv-psy` → `advisor-psychologist`, `annas-archive` → `books`.

## [2.0.0] — 2026-09-06 — маршрут 0–6 вместо батчей 1–4 / route 0–6 replaces batches 1–4

### Для человека
- Драйвер ведёт по семи тирам: рабочее место → голос → ключи и verif → ресерч → свои сотрудники → советы → методология. Инструменты сначала, методология в конце.
- Пробы машины теперь видят CLI-зависимости, ключи в Связке ключей, установленные плагины каждого тира и папку памяти советов.
- Команда та же — `JADLIS-BATCH <N>`, но `N` теперь номер тира (0–6, у методологии подшаги 6.1/6.2/6.3).

### For agents
- Added: tier probes 0, 2 (Keychain `pluginSecrets`), 3, 4, 5 (`{MEMORY_DIR}/Вердикты`), 6.3 in `skills/batch/references/детект-состояния.md`; delivery table with plugin + follow-up commands per tier in `skills/batch/SKILL.md`; docs links `DOCS/<tier>`.
- Changed: gate semantics — `maxAllowed` = lowest unclosed tier; status report is 7 lines + current tier; journal key `батч:` → `тир:`; `batch-status` prints 8 lines.
- Removed: batch numbering 1–4; the "two of three providers" rule for verif (verif on one Claude closes tier 2).
- Migration: recipients on 1.x keep the same command; existing journals with `батч:` are rewritten by the driver on the next run (probes win).
- Breaking: tier numbers differ from old batch numbers (old batch 2 = new tier 6.1, old batch 3 = 6.2, old batch 4 = tiers 2–3).

## [1.0.0] — 2026-08-01 — первый релиз / first release

### Для человека
- Драйвер батчей 1–4: пробы машины, гейт «не выдавать батч авансом», журнал состояния.

### For agents
- Added: `skills/batch`, `skills/batch-status`, `references/детект-состояния.md`; userConfig `VAULT_PATH`.
