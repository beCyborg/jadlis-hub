[Русский](README.md) · English

# Tier 0 — your workplace

A subscription, an app, four commands. At the end Claude Code knows your language, your
answer-shaping rules and the folder where your notes live.

## Why

Eighty percent of the result comes from context about your life; twenty from the task
itself. Without that context the agent guesses — and gets it convincingly wrong.

Tier 0 builds the place where the context accumulates: a configured Claude Code, memory
switched on, and an Obsidian folder for notes. Everything else on the route — tiers 1
through 6 — sits on top of it.

The `setup` plugin does this with commands, not with a twenty-step manual.

## What it looks like

![A computer on a desk, robotic arms reaching out of the screen to handle a calendar, a chart, an envelope and a folder](../img/hub-12.webp)

<details>
<summary>What <code>/setup:workplace</code> shows before writing settings</summary>

```diff
--- current ~/.claude/settings.json
+++ after merge
+  "language": "Russian",
+  "timeFormat": "24-hour",
+  "alwaysThinkingEnabled": true,
+  "autoMemoryEnabled": true,
+  "effortLevel": "high",
+  "permissions": { "defaultMode": "default" }

Apply? A backup stays next to it: settings.json.bak-20260906-181500
```

</details>

## Install

Three steps before the plugin, then four commands.

1. **A Claude subscription.** Claude Code runs on the Pro, Max, Team and Enterprise
   plans. Terms and pricing live on claude.ai; pick and pay for a plan there.
2. **The Claude Code desktop app.** Download it from the
   [install page](https://code.claude.com/docs/en/desktop-quickstart), sign in, open the
   **Code** tab and pick a folder.
3. **The `claude` CLI.** The app does **not** install it — and `claude plugin …`
   commands need it. `/setup:deps` installs it, or do it by hand:
   `curl -fsSL https://claude.ai/install.sh | bash`.

Then paste this block into Claude Code as is:

```text
You are an installer. Run exactly these steps and nothing else:
1. Bash: claude plugin marketplace add https://github.com/beCyborg/jadlis-plugins.git
2. Bash: claude plugin install setup@jadlis
3. Tell me: "Send /reload-plugins, then type /setup:deps"
Read nothing, create nothing, install nothing beyond this.
```

By hand — the same two commands in a terminal:

```bash
claude plugin marketplace add https://github.com/beCyborg/jadlis-plugins.git
claude plugin install setup@jadlis
```

The full HTTPS URL is required: the short `owner/repo` form clones over SSH, and a new
user usually has no SSH key.

## Usage

Four commands, top to bottom. Each one asks first and shows a diff before changing anything.

```text
/setup:deps       # Homebrew, claude CLI, jq, Node.js, git, gh — a PASS/FAIL table, then installs what is missing
/setup:workplace  # ~/.claude: settings.json via jq, CLAUDE.md, memory, notifications, status line
/setup:obsidian   # the vault folder + a short CLAUDE.md for notes
/setup:terminal   # optional: iTerm2, tmux, two aliases — if you prefer a terminal to the app
```

Three runs:

- Clean Mac: `/setup:deps` → `/setup:workplace` → `/setup:obsidian`.
- Claude Code already configured, only the folder is missing: go straight to `/setup:obsidian`.
- Answers are too long: `/setup:i-have-adhd` — short, action-first steps for this session.

**Check it with one action.** Ask: "show me what is in my notes folder". A list of files
back means tier 0 is closed; next is `JADLIS-BATCH 1`.

## Limits and cost

What tier 0 does **not** do:

- It does not buy the subscription or install the app for you — those are steps 1–2 above.
- It does not build the methodology folder structure or create metrics — that is tier 6.
- It does not create API keys: those live in the macOS Keychain and arrive at tier 2.
- It never overwrites an existing `settings.json` or `CLAUDE.md` — it merges and appends.

Cost: you need a Claude subscription and macOS. Homebrew, jq, Node.js, git, gh and
Obsidian are free. Tier 0 makes no paid requests at all.

## Desktop or terminal

Start with the desktop app: it covers the whole 0–6 route with no shell wrangling.

Shared by both: the same `CLAUDE.md`, `~/.claude/settings.json`, MCP servers, hooks,
skills, plugins and models. Configure it in one, it works in the other.

| Terminal only | Desktop only |
|---|---|
| the `dontAsk` permission mode | Dispatch sessions in the sidebar |
| `--print` and the Agent SDK — your own scheduled runs (`launchd`, `cron`) | scheduled tasks inside the app |
| the status line and terminal dialog commands (`/permissions`, `/config`, `/keybindings`) | chat, diff, terminal, file and browser panes |
| agent teams | a separate git worktree per parallel session |
| Remote Control — the session runs on your machine, you continue it from your phone | attachments: images and PDFs straight into the prompt |

Separately: the app does **not** install the `claude` CLI. It ships its own embedded
engine, but `claude …` commands in Bash come from a separate install — `/setup:deps`
handles that.

Add the terminal when you need your own scheduled runs, `--print` for scripts, or work
from your phone. Then run `/setup:terminal`.
