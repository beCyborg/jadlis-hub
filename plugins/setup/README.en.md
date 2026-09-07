[Русский](README.md) · English

# setup — your workplace (tier 0)

Four commands take a clean Mac to the point where Claude Code already works for you:
tools installed, settings in place, a notes folder ready.

## Why

The problem: out of the box Claude Code knows neither your language, nor your rules,
nor where your notes live — and the first week goes into "where do I configure this".

This plugin closes that gap: it installs the missing tools, merges a baseline
`settings.json`, drops a `CLAUDE.md` with answer-shaping rules, turns memory on and
creates the vault folder. Everything else on the 0–6 route builds on top of it.

Nothing happens silently: every change is shown as a diff and waits for a yes.

## What it looks like

![A workplace: a person at a wide desk, five panels, a robotic arm working at each, a neat stack of finished sheets on the right](../../docs/img/08-employee-01.webp)

<details>
<summary>Dependency table after <code>/setup:deps</code></summary>

```text
brew   PASS  Homebrew 4.6.0
claude FAIL
jq     PASS  jq-1.8.1
node   PASS  v24.4.0
npx    PASS  11.4.2
git    PASS  git version 2.50.1
gh     FAIL
macOS  26.1 (arm64)

Install claude? Install gh?
```

</details>

## Install

Paste this block into Claude Code as is:

```text
You are an installer. Run exactly these steps and nothing else:
1. Bash: claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
2. Bash: claude plugin install setup@jadlis
3. Tell me: "Send /reload-plugins, then type /setup:deps"
Read nothing, create nothing, install nothing beyond this.
```

By hand — the same two commands in a terminal:

```bash
claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
claude plugin install setup@jadlis
```

The full HTTPS URL is required: the short `owner/repo` form clones over SSH, and a new
user usually has no SSH key.

## Usage

Run the commands top to bottom; `/setup:terminal` is optional.

```text
/setup:deps         # what is installed and what is missing: Homebrew, claude CLI, jq, Node.js, git, gh
/setup:workplace    # ~/.claude: settings.json via jq, CLAUDE.md, memory, notifications
/setup:obsidian     # vault folder + a short CLAUDE.md for notes
/setup:terminal     # optional: iTerm2, tmux, two aliases instead of the desktop app
/setup:i-have-adhd  # turn on short, action-first answers for this session
```

Three typical runs:

- Clean Mac: `/setup:deps` → `/setup:workplace` → `/setup:obsidian`.
- Claude Code already configured, only the folder is missing: go straight to `/setup:obsidian`.
- You prefer a terminal to the app: `/setup:terminal` — it starts with a comparison table.

## Limits and cost

What the plugin does **not** do:

- It does not buy the subscription or install the Claude Code app — you do that before tier 0.
- It does not build the methodology folder skeleton or create metrics — that is tier 6 (`jadlis-vault`).
- It does not touch API keys: those live in the macOS Keychain and arrive at tier 2.
- It never overwrites an existing `settings.json` or `CLAUDE.md` — it merges and appends.

Cost: the plugin spends no money of its own. You need a Claude subscription (Pro, Max,
Team or Enterprise) and macOS; Homebrew, jq, Node.js, git and gh are free. The plugin
makes no paid API calls.

## License

MIT. The `i-have-adhd` skill is bundled under the MIT license of its original author.
