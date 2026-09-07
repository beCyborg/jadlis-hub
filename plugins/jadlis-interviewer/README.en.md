[Русский](README.md) · English

# jadlis-interviewer — the interview: meaning, metrics, quarterly goals

Sub-step 6.2 of the handover route. The `/jadlis-interviewer:vault-interviewer` skill takes an empty vault to a planned quarter in four stages — one question per turn, and it writes the notes itself.

## Why

Goals pulled out of thin air cannot be checked: "I want a million" says nothing about which part of a good life it improves. And a verdict of "seems fine" never shows what is actually sagging or where to push.

The interviewer turns the person's own words into a checkable structure (tag `jadlis-interviewer--v1.0.1`):

- **Stage 1** — the "meaning of life" note: 5–15 sentences in their own wording.
- **Stage 2** — 4–6 need groups, named by them rather than by someone else's taxonomy.
- **Stage 3** — 10–15 metrics with a direction, a measurement cadence and four bands.
- **Stage 4** — 2–3 quarterly goals, each tied to a metric and to a dated kill criterion.
- Between stages the skill stops and says how many stages are left.

## What it looks like

![On the left a blurred silhouette in fog, on the right the same figure with measurement scales and dials](../../docs/img/02-methodology-02.webp)

<details>
<summary>A metric note and a goal note (synthetic example)</summary>

Field values are Russian by design — the vault is written in Russian.

```markdown
---
type: metric
need_name: "Движение"
frequency: weekly
direction: up
red: "< 1"
yellow: "1–2"
green: "> 2"
blue: "> 4"
status:
last_value:
last_date:
---

## Как мерить

Source: training app
Unit: workouts per week

## Диапазоны

🔴 less than 1 — the week fell through
🟡 1–2 — holding on
🟢 more than 2 — normal
🔵 more than 4 — above normal

## История измерений

| Дата | Значение | Статус |
|---|---|---|
```

```markdown
---
type: goal
title: "Вернуть регулярный спорт"
status: active
quarter: "2026-Q3"
metrics_target:
  - "[[Тренировок в неделю]]"
kill_criterion: "к 15 числу первый шаг не сделан → снимаю"
---

## Definition of Done

Three weeks in a row at three workouts each, with no reschedules.
```

`status`, `last_value` and `last_date` stay empty: the first real measurement fills them, not the interview.

</details>

## Install

Paste this block to an agent in Claude Code opened in the vault folder:

```text
You are an installer. Do exactly these steps and nothing beyond them:
1. Bash: claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
2. Bash: claude plugin install jadlis-interviewer@jadlis
3. Tell me in one line: "Send /reload-plugins, then write: /jadlis-interviewer:vault-interviewer"
Do not read, create or install anything else.
```

The manual path is the same commands:

```bash
claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
claude plugin install jadlis-interviewer@jadlis
```

Then `/reload-plugins` and `/jadlis-interviewer:vault-interviewer`. On enable the plugin asks for `VAULT_PATH` — the path to the vault folder, `~/Jadlis` by default. The full HTTPS marketplace URL is required: the short `owner/repo` form expands to an SSH address, and a new user usually has no SSH key. The whole 6.2 sub-step can also be driven by the route driver: `JADLIS-BATCH 6`.

## Usage

Three typical scenarios:

1. **Start the interview** — `/jadlis-interviewer:vault-interviewer`. The skill inspects the vault and says in one line which stage it starts from.
2. **Come back a week later** — the same command. This is a continuation, not a restart: finished stages are not asked again, and the skill keys off the `type:` frontmatter field rather than folder names.
3. **Check whether the sub-step is closed** — `JADLIS-BATCH статус`. Sub-step 6.2 is closed once the meaning note exists, there are ≥ 10 metrics and ≥ 2 quarterly goals.

## Limits and cost

What the skill does not do, and what it needs:

- **It does not fit into one sitting.** Four stages, with a stop and a "shall we continue?" between them; stage 3 is honestly better split across two sessions.
- **The metric ceiling is hard — 15.** More than that is a guaranteed abandoned list; the overflow goes to a candidates note. Seven metrics someone actually measures beat fifteen picked to hit a number.
- **It does not invent things for the person.** Someone else's numbers, medical values and norms are never substituted; an unknown field stays empty, and a borrowed reference band is labelled with its source.
- **It needs the skeleton in place.** The skill writes into `Потребности/` and `Цели/`, which `jadlis-vault` (sub-step 6.1) lays out.
- **No keys, no payments.** All it needs is Claude Code and the vault folder; nothing leaves the machine.
