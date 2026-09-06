[Русский](README.md) · English

# jadlis-research — the research stack

Five skills and five MCP servers: ordinary web search, full community research, a science review, and a triple check of your own file. Ships disabled (`defaultEnabled: false`) — it pulls paid services.

## Why

One plugin covers three different jobs that otherwise scatter across a dozen tools.

- **Check your own file** — `verif` has three AIs from three vendors read it separately and merges on the worst verdict.
- **Understand a topic** — `full-research` runs fourteen channels at once and verifies every claim across sources.
- **Lean on science** — `search-paper` builds a review over nine scientific sources with a retraction check.

Reports and verdicts land in the vault instead of staying in the chat.

## What it looks like

<details>
<summary>Synthetic sample: commands and what they return (invented data)</summary>

```
/jadlis-research:search who bids on a competitor's keywords
── BRAVE web · 1256 ms · $0.0050 · 3 res
 1 example.com/pricing · Pricing — Example
 2 docs.example.org/api · API reference

/jadlis-research:verif --file Plan.md
Short version: needs revision — 9 raw findings from 3 checkers, 3 of them serious.
VERDICT: NEEDS-REVISION  (Codex: needs-revision · Fable: needs-revision · Grok: approve)
Artifacts: AI/verif/2026-09-06--plan--{codex,fable,grok,merged,arbiter}.json

/jadlis-research:keys --list
  BRAVE_API_KEY              31     pluginSecrets (Claude Code-credentials)
  PUBMED_API_KEY             36     keychain generic (jadlis-research/PUBMED_API_KEY)
  YC_SEARCH_API_KEY          -      NONE
```

</details>

## Install

Paste the block below into Claude Code — it does the work.

```text
You are an installer. Do exactly these steps and nothing beyond them:
1. Bash: claude plugin marketplace add https://github.com/beCyborg/jadlis-plugins.git
2. Bash: claude plugin install jadlis-research@jadlis
3. Bash: claude plugin enable jadlis-research
4. Tell me: "Plugin enabled. Your turn: run /plugin configure jadlis-research@jadlis and
   enter BRAVE_API_KEY and FIRECRAWL_API_KEY. Then restart Claude Code and run
   /jadlis-research:keys."
```

The same path by hand, same commands:

1. Get the two required keys: Brave (Search plan) and Firecrawl.
2. `claude plugin marketplace add https://github.com/beCyborg/jadlis-plugins.git`
3. `claude plugin install jadlis-research@jadlis`
4. `claude plugin enable jadlis-research` — Claude Code asks for the class A keys and stores them in the macOS Keychain.
5. Restart Claude Code, then run `/jadlis-research:keys` for the remaining keys and the smoke check.

The full install walkthrough and the key standard live in [docs/2-verif](../../docs/2-verif/README.en.md); the research part in [docs/3-research](../../docs/3-research/README.en.md).

## Usage

Five skills, three typical scenarios:

```text
/jadlis-research:search <question>              # Brave + Exa web search with intent routing
/jadlis-research:full-research <topic>          # 14 channels → claim verification → report in the vault
/jadlis-research:verif --file <your plan>       # three verifiers → arbiter → questions back to you
```

The other two: `/jadlis-research:search-paper <question>` — a science review over nine sources with GRADE synthesis; `/jadlis-research:keys` — keys, verifier homes and a PASS/FAIL smoke table.

## Limits and cost

What you have to pay for and set up:

| What | Role | Required |
|---|---|---|
| Brave Search API, Search plan | the main search engine, ≈$0.005/request | yes |
| Firecrawl | page scraping, dynamic sites | yes |
| ChatGPT subscription (Codex CLI) | the `codexweb` channel, the Codex verifier | no |
| Grok subscription (Grok CLI) | the `grokweb` / `twitter` channels, the Grok verifier | no |
| `EXA_API_KEY`, `YC_SEARCH_API_KEY`, science keys | semantic layer, Russian-language web, `search-paper` | no |

What the plugin does not do: it does not review code (that is `/code-review`), does not replace ordinary search on one-phrase questions, and does not decide for you. A channel without its key degrades rather than failing — the run continues on the rest.

## Internals

**Keys** live in the macOS Keychain and are read through a single entry point, `scripts/secret.sh` (env → Keychain `jadlis-research`/`KEY` → `pluginSecrets` of the `Claude Code-credentials` item → `.credentials.json` → `settings.json → env` as legacy). Class A (`BRAVE_API_KEY`, `FIRECRAWL_API_KEY`, `REDDITAPIS_KEY`, `YOUTUBE_API_KEY`) is written by Claude Code via `/plugin configure jadlis-research@jadlis`; class B (science, Exa, Yandex, Places, contact emails) by the `keys` skill over stdin.

**Five MCP servers:** `brave-search` (`BRAVE_API_KEY`), `firecrawl` (`FIRECRAWL_API_KEY`), `reddit` (keyless), `reddit-alt` (`REDDITAPIS_KEY`, optional), `youtube` (`YOUTUBE_API_KEY`, optional). HackerNews, Substack and Telegram go through the plugin's own scripts — there is deliberately no MCP fallback.

**`full-research` channels:**

| Channel | How it fetches | Degradation without a key or CLI |
|---|---|---|
| `web` | Brave MCP + Firecrawl, place layer via `scripts/places-fetch.sh` | the place layer falls back to `brave_place_search` |
| `codexweb` / `grokweb` / `twitter` | Codex CLI, Grok CLI | the channel drops out, the run continues |
| `reddit` / `hackernews` / `substack` / `telegram` | MCP `reddit` + `scripts/{reddit-archive.py,hn-fetch.sh,substack-fetch.py,tg-preview.sh}` | keyless ladder; a broken fetcher falls back to Brave with `sourceQuality=LOW` |
| `yandex` / `youtube` | `scripts/yandex-search.sh`, Brave + MCP `youtube` | `yandex` is not offered at all; `youtube` lives on Brave plus local transcripts |
| `ja` / `zh` / `ko` / `eu` | `scripts/feed-fetch.py` (platform feeds and keyless APIs) | no keys needed; a dead feed degrades the channel |

**External binaries:** `jq` (required by `secret.sh`, `hn-fetch.sh`, `places-fetch.sh`), `uv` (shebang of `substack-fetch.py` and `yt-transcript.py`), `pdftotext` from poppler (for `pdf-fetch.sh`), optional `yt-dlp`, optional `codex` / `grok` CLI.

**Paths:** `${CLAUDE_PLUGIN_ROOT}` is substituted only inside `SKILL.md` and agent text. There is no substitution in `protocols/` and `references/` — those write `{PLUGIN_ROOT}`, and the workflow prompt tells the agent the value. Workflow JS scripts get the root through `args.pluginRoot`. Bash scripts resolve it from their own location. Verifier working homes live in `${CLAUDE_PLUGIN_DATA}/verif-homes/`, templates in `assets/verif-homes/`; `auth.json` there are symlinks to the Codex and Grok logins and never reach the repository.

**Models:** the plugin sets no model aliases and runs on subscription defaults. Research synthesis goes through the headless bridge `claude -p --model claude-fable-5`, falls back to Opus 5 when the bridge dies, and the skill rewrites `ai_model` in the report frontmatter to whichever model actually answered. `verif` verifiers: Codex `gpt-6-astra`, Claude Fable 5, Grok `grok-4.6`; the arbiter is Fable 5.
