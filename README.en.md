[Русский](README.md) · English

# Jadlis — handing over the stack

Marketplace `jadlis`: one entry point, seven tiers, and a driver that hands you exactly the next step. A Claude Code + Obsidian stack built over a year, transferred one tool at a time — tools first, methodology last.

## Route 0–6

| Tier | What you get | Plugin | Docs |
|---|---|---|---|
| 0 | Workplace: Claude Code, CLI dependencies, an Obsidian folder, a base `CLAUDE.md`, memory, reply style | `setup` | [docs/0-workplace](docs/0-workplace/README.en.md) |
| 1 | Voice: Spokenly, the correction prompt, the replacement dictionary | — | [docs/1-voice](docs/1-voice/README.en.md) |
| 2 | Keys in the Keychain + verif: three models read your plan in isolation | `search`, `verif` | [docs/2-verif](docs/2-verif/README.en.md) |
| 3 | Research: `research` (fourteen channels) and `science-research` (science, GRADE) | `research`, `science-research` | [docs/3-research](docs/3-research/README.en.md) |
| 4 | Your own employees: a skill is a job description | `skill-builder`, `plugin-creator` | [jadlis-skill-builder](https://github.com/beCyborg/jadlis-skill-builder) |
| 5 | Boards of advisors: nine councils, book lenses, skeptics, a verdict | `advisor-decision` … `cognitive-biases` | the `jadlis-advisor-*` repos' READMEs |
| 6 | Methodology: 6.1 vault → 6.2 interviewer → 6.3 news SWOT | `jadlis-vault`, `jadlis-interviewer`, `swot-news` | [docs/6-methodology](docs/6-methodology/README.en.md) |
| E | Extras on request: browser, desktop, video digests, books | `browser`, `computer-use`, `tldr`, `books` | each repo's README |

The next tier is not handed out until machine probes confirm the previous one. Criteria live in the [driver](plugins/jadlis-start/README.en.md).

## How it works

```mermaid
flowchart LR
  H[hub jadlis-start<br/>marketplace jadlis] --> S[plugin jadlis-start<br/>driver: probes → next step]
  S -->|tier 0| T0[setup]
  S -->|tier 1| T1[docs/1-voice]
  S -->|tiers 2–3| T2[search · verif · research · science-research]
  S -->|tier 4| T4[skill-builder · plugin-creator]
  S -->|tier 5| T5[nine councils]
  S -->|tier 6| T6[jadlis-vault · jadlis-interviewer · swot-news]
  T4 -.pin ref+sha.-> R4[(jadlis-skill-builder)]
  T5 -.pin ref+sha.-> R5[(jadlis-advisor-...)]
  T6 -.pin ref+sha.-> R6[(jadlis-swot-news)]
```

Internal plugins live in `plugins/<name>`; external ones are wired into the same `marketplace.json` as `url` / `git-subdir` entries pinned by `ref` (release tag) + `sha`. The recipient sees one marketplace; the owner releases each repo separately and bumps the pin in the hub.

## Install

Open Claude Code (desktop or terminal) and paste:

```
You are an installer. Run exactly these steps and nothing else:
1. Bash: claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
2. Bash: claude plugin install jadlis-start@jadlis
3. Tell me: "Send /reload-plugins, then type: JADLIS-BATCH"
```

The same two commands by hand:

```bash
claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
claude plugin install jadlis-start@jadlis
```

The repositories are public — no git credentials or SSH keys needed; the full HTTPS URL is mandatory (the `owner/repo` shorthand is fetched over SSH). From here the driver leads: `JADLIS-BATCH`, `JADLIS-BATCH 0`, … `JADLIS-BATCH 6.3`.

## Plugins

| Plugin | Tier | Source | Install |
|---|---|---|---|
| `jadlis-start` | — | `plugins/jadlis-start` | `claude plugin install jadlis-start@jadlis` |
| `setup` | 0 | `plugins/setup` | `setup@jadlis` |
| `search`, `verif` | 2 | [jadlis-search](https://github.com/beCyborg/jadlis-search), [jadlis-verif](https://github.com/beCyborg/jadlis-verif) | `search@jadlis --config BRAVE_API_KEY=… --config FIRECRAWL_API_KEY=…`, then `verif@jadlis` |
| `research`, `science-research` | 3 | [jadlis-research](https://github.com/beCyborg/jadlis-research), [jadlis-science-research](https://github.com/beCyborg/jadlis-science-research) | `research@jadlis`, `science-research@jadlis` — both pull `search` |
| `skill-builder`, `plugin-creator` | 4 | [jadlis-skill-builder](https://github.com/beCyborg/jadlis-skill-builder), [jadlis-plugin-creator](https://github.com/beCyborg/jadlis-plugin-creator) | `skill-builder@jadlis`, `plugin-creator@jadlis` |
| nine councils: `advisor-decision` … `cognitive-biases` | 5 | the `jadlis-advisor-*`, `jadlis-robert-greene`, `jadlis-nupp`, `jadlis-cognitive-biases` repos | `advisor-decision@jadlis --config MEMORY_DIR=~/advisors-memory` (the rest the same, one memory folder) |
| `jadlis-vault`, `jadlis-interviewer` | 6.1, 6.2 | `plugins/…` | `jadlis-vault@jadlis`, `jadlis-interviewer@jadlis` |
| `swot-news` | 6.3 | [jadlis-swot-news](https://github.com/beCyborg/jadlis-swot-news) | `swot-news@jadlis` |
| `browser`, `computer-use` | E | [jadlis-desktop](https://github.com/beCyborg/jadlis-desktop) | `browser@jadlis`, `computer-use@jadlis` |
| `tldr` | E | [jadlis-tldr](https://github.com/beCyborg/jadlis-tldr) | `tldr@jadlis` |
| `books` | E | [jadlis-books](https://github.com/beCyborg/jadlis-books) | `books@jadlis` |

Plugins deliberately **almost never depend** on each other — the one exception: `research` and `science-research` pull the base `search`. Otherwise installing tier 5 would pull everything at once and the gate would vanish. Current pins of external entries: `python3 tools/bump-pin.py --list`.

## Update

Every plugin carries a semver in `plugin.json`; each release is tagged `<plugin>--v<version>`. For third-party marketplaces **auto-update is off by default on the recipient side**:

```bash
claude plugin update <plugin>@jadlis
```

Or enable auto-update once: `/plugin` → **Marketplaces** → `jadlis`. External plugins update when the owner bumps the pin in the hub — `claude plugin update` sees the new version after that.

## Keys

No key lives in any repository; every recipient registers their own. One standard: **a key is entered once and lives in the macOS Keychain**, never in files. MCP-server keys are handed to the plugin at install time via `--config KEY=…` (`/plugin configure <plugin>@jadlis` to change them); script keys are written by `/search:keys`; scripts read them through `secret.sh`. Details — [docs/2-verif](docs/2-verif/README.en.md).

## Compatibility

- macOS; Claude Code desktop or CLI (Bash is needed for the install). The desktop app **does not install** the `claude` CLI — tier 0 closes that gap.
- Claude Code ≥ 2.1.239 (`git-subdir` with `sha`, `userConfig`, `/plugin configure`).
- Changes — fork + PR ([CONTRIBUTING.md](CONTRIBUTING.md)); commit and release conventions — [CLAUDE.md](CLAUDE.md).

## Migrating from an older install

Older installs need no action: the marketplace name `jadlis` is unchanged, and GitHub redirects the old hub URL (`jadlis-plugins`) to the new one (`jadlis-start`). The command is the same — `JADLIS-BATCH` — but numbers are now tiers 0–6 (old batch 2 = 6.1, batch 3 = 6.2, batch 4 = tiers 2–3). After `claude plugin update jadlis-start@jadlis` the driver rewrites the state journal from probes on its own.

> [!WARNING]
> Plugin and marketplace names are frozen from the first release. Renaming breaks installs; if it ever becomes necessary — only via `renames` in `marketplace.json`, appending a new entry.

## License

MIT — see [LICENSE](LICENSE). The nine council plugins intentionally carry no license — see their `NOTICE.md`.
