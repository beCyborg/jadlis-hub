# Changelog — jadlis-start

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
