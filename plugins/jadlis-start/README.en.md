[Русский](README.md) · English

# jadlis-start — the tier 0–6 route driver

One plugin that knows where you are and hands you exactly the next step. Nothing in advance.

## Why

A stack of a dozen plugins cannot be installed in one evening without drowning. The driver walks you through seven tiers: tools first (workplace, voice, keys and verif, research, your own employees, advisors), methodology last. The next tier is not handed out until machine probes confirm the previous one.

## What it looks like

![Route: a map with six paths leading to one house](../../docs/img/10-overview.v2-10.webp)

<details><summary>Sample reply to <code>JADLIS-BATCH</code></summary>

```
0 Workplace            ✅ closed
1 Voice (Spokenly)     ✅ closed
2 Keys and verif       ⏳ plugin installed, Brave set, Firecrawl missing, verdicts 0
3 Research             ⬜ not started
4 Your own employees   ⬜ not started
5 Advisors             ⬜ not started
6 Methodology          ⬜ 6.1 vault ⬜ · 6.2 interview ⬜ · 6.3 SWOT ⬜

Your tier now: 2 → type `JADLIS-BATCH 2`
```

</details>

## Install

Paste into the Claude Code chat:

```
You are an installer. Run exactly these steps and nothing else:
1. Bash: claude plugin marketplace add https://github.com/beCyborg/jadlis-plugins.git
2. Bash: claude plugin install jadlis-start@jadlis
3. Tell me: "Send /reload-plugins, then type: JADLIS-BATCH"
```

The same two commands by hand in a terminal:

```bash
claude plugin marketplace add https://github.com/beCyborg/jadlis-plugins.git
claude plugin install jadlis-start@jadlis
```

## Usage

- `JADLIS-BATCH` — status of the seven tiers and the next step.
- `JADLIS-BATCH 2` — deliver tier 2: install the plugin, explain the first run.
- `JADLIS-BATCH 6.2 продолжить` — resume inside a sub-step after a break (continuation, not restart).

Status only, no installs: `/jadlis-start:batch-status`.

## Limits and cost

- Never hands out tier N while N−1 is open: criteria live in `skills/batch/references/детект-состояния.md`.
- Never reads or prints key values — only "set / not set" from the macOS Keychain.
- Tier 1 (voice) is set up by hand outside Claude Code; the driver only verifies the result.
- Free. Paid services appear from tier 2 on (Brave, Firecrawl) — each tier's docs say so.

## Update

Third-party marketplaces have auto-update off on the recipient side:

```bash
claude plugin update jadlis-start@jadlis
```
