# Changelog — jadlis-hub

Плагин продолжает историю `jadlis-start` (1.0.0 → 2.1.1); с 3.0.0 у него новое имя и новая
команда, поэтому мажорный бамп.

## [3.0.2] — 2026-11-04 — адрес маркетплейса на GitLab, уведомления отдельно / marketplace URL on GitLab, notifications standalone

### Для человека
- Команда добавления маркетплейса теперь ведёт на GitLab. Старый адрес на GitHub больше не открывается: тот аккаунт заблокирован.
- Шаг «Рабочее место» больше не обещает, что уведомления приедут сами. Их предлагает `/claudecode` отдельной командой.

### For agents
- Fixed: `skills/jadlis-hub/SKILL.md`, `references/route.json`, `README.md`, `README.en.md` — `https://github.com/beCyborg/jadlis-hub` → `https://gitlab.com/beCyborg/jadlis-hub.git` (full URL: the `owner/repo` shorthand is GitHub-only).
- Changed: `references/route.json` step `claudecode` drops `installs_dependency`, `what` names `cld`/`tld` and the optional CLAUDE.md, styles and notifications (jadlis-claudecode 2.0.0).
- Changed: `SKILL.md` §4.4 and `references/probes.md` say `jadlis-notifications` is a separate install.

## [3.0.1] — 2026-10-17 — шаг «Свои плагины» ведёт на jadlis-plugin-builder / route step points to jadlis-plugin-builder

### Для человека
- Плагин для сборки своих плагинов теперь называется `jadlis-plugin-builder`, команда — `/plugin-builder`.
- Помощник маршрута предлагает новое имя и проверяет установку по нему.

### For agents
- Changed: `references/route.json` step `plugin-creator` → `plugin-builder` (`plugin`, `command`, `closed_when`); ids are not persisted, so no state migration.
- Changed: `references/probes.md` optional-step loop checks `jadlis-plugin-builder`.
- Migration: the marketplace `renames` map carries `jadlis-plugin-creator` → `jadlis-plugin-builder`.

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
