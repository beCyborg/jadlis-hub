# Changelog — setup

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), версии — [SemVer](https://semver.org/lang/ru/).

## [1.0.0] — 2026-09-06 — рабочее место тира 0 / tier 0 workplace

### Для человека

- Четыре команды собирают рабочее место с нуля: `/setup:deps` ставит недостающие
  программы, `/setup:workplace` настраивает Claude Code, `/setup:obsidian` заводит папку
  для заметок, `/setup:terminal` — по желанию терминал вместо приложения.
- Ничего не меняется молча: настройки сливаются через `jq`, дифф показывается,
  существующие файлы не перезаписываются.
- Память включается сразу — уроки и поправки переживают перезапуск сессии.

### For agents

- Added: `plugins/setup/.claude-plugin/plugin.json` — manifest v1.0.0, `userConfig.VAULT_PATH`
  (directory, default `~/Jadlis`, optional).
- Added: skills `plugins/setup/skills/{deps,workplace,terminal,obsidian}/SKILL.md` —
  commands `/setup:deps`, `/setup:workplace`, `/setup:terminal`, `/setup:obsidian`.
- Added: `plugins/setup/skills/i-have-adhd/SKILL.md` — user-invocable-only output style
  (`disable-model-invocation: true`), MIT.
- Added: assets `settings.template.jsonc` (commented), `settings.minimal.json` (jq merge
  source), `CLAUDE.md.template` (ADHD block fenced by `<!-- adhd:start|end -->`),
  `vault-CLAUDE.md.template`, `statusline.sh`, `hooks/notify.md`.
- Added: `plugins/setup/README.md` + `README.en.md` (5 sections), `plugins/setup/CHANGELOG.md`.
- Migration: none — first release. `/setup:obsidian` never overwrites an existing
  vault `CLAUDE.md`, so tier 6 `jadlis-vault` can lay its skeleton on top without conflict.
