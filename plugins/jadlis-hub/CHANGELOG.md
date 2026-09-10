# Changelog — jadlis-hub

Плагин продолжает историю `jadlis-start` (1.0.0 → 2.1.1); с 3.0.0 у него новое имя и новая
команда, поэтому мажорный бамп.

## [3.0.0] — 2026-09-10 — помощник маршрута вместо драйвера тиров / route helper replaces the tier driver

### Для человека
- Команда теперь `/jadlis-hub` вместо слова `JADLIS-BATCH`; аргументы — пусто (продолжить), `status`, `later` и id шага.
- Маршрут перестал быть лестницей 0–6: шесть обязательных шагов за гейтом (рабочее место, Obsidian, голос, поиск, ресерч, проверка планов), дальше семь необязательных инструментов в рекомендованном порядке.
- Перед каждым шагом помощник объясняет простым языком: что это, какую задачу решает, что придётся купить.
- Раздел «Позже» рассказывает про советы директоров и `jadlis-os` и ничего не ставит.

### For agents
- Added: plugin `jadlis-hub` 3.0.0 with skill `skills/jadlis-hub/SKILL.md` (command `/jadlis-hub`, also `/jadlis-hub:jadlis-hub`); route data in `references/route.json` (13 steps + 2 `later` entries, fields `what`/`solves`/`buy`/`closed_when`); probes in `references/probes.md`.
- Changed: probes read `claude plugin list --json` (`id`, `enabled`, `installPath`) instead of parsing the text listing; steps 1–3 delegate to the step plugin's own `scripts/probe.sh` printing `key=PASS|FAIL`; `batch-status` behaviour became the `status` argument, no separate skill; journal path `Система/Передача — состояние.md`, frontmatter key `тир:` → `шаг:`.
- Removed: plugin `jadlis-start` (skills `batch`, `batch-status`, reference `детект-состояния.md`), plugin `setup`, `userConfig.VAULT_PATH` (vault is `~/Jadlis` by convention), the `JADLIS-BATCH` trigger word, tier numbering 0–6.
- Migration: recipients of `jadlis-start` uninstall it (`claude plugin uninstall jadlis-start@jadlis`) and install `jadlis-hub@jadlis`; old journals with `тир:` are rewritten by the helper on the next run (probes win).
- Breaking: plugin name, command name and step ids all changed; tier numbers have no equivalent in the new route.
