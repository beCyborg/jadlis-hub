English · [Русский](README.md)

# You paid for the assistant, and the evening goes on working out where to start instead of on the work

One word in the chat shows the seven lines of the 0 → 6 route and the one you are standing on right
now; the next step is not handed out until a probe on your own machine confirms the previous one.

```
claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
claude plugin install jadlis-start@jadlis
```

It installs on top of a machine that is already set up: the base config is merged into your current
one, every edit is shown in full and waits for your "yes", and it all comes off in one command —
`claude plugin uninstall jadlis-start@jadlis --keep-data`.

![Seven route lines with their statuses, with a separate line marking where you are now](docs/img/hero-jadlis-start.webp)

In words: a list of seven steps, each with a status, one line marked "you are here" — you carry on
from that one, and there is nothing to remember.

This is my workbench published as it is, not a product: whatever I stopped using, I removed.

## Before → after

| By hand | With an AI chat | With this plugin |
|---|---|---|
| **The order of the steps.** There are plenty of tools and no order between them: you open the list and close it again, because choosing among twenty is work in itself. | The chat hands you every step at once, and the choosing is yours again. | You type `JADLIS-BATCH` into the chat — seven lines of the 0 → 6 route with statuses and a "where you are now" line. |
| **The state of the machine.** On step 3 it turns out step 2 never landed, and it looks like everything is broken. | The chat takes your word for it: you said "done", so on we go. | The probe runs on your own machine; the next step is not handed out until it confirms the previous one. |
| **A week's break.** You come back, and where exactly you stopped is somewhere in the terminal history. | A new session does not remember the last one. | You type the same word — and you are back where you stopped, down to the substep. |
| **Keys to paid services.** The values wander across config files and settle in your command history. | You dictate the key into the chat so that "it can check". | Keys are never read: only "present" or "absent" is checked, and no value is printed anywhere. |
| **A machine that is already set up.** A new config overwrites what took months to tune. | "I will replace the whole file" — you see the difference afterwards. | The base config is merged into your current one; say "no" and the file stays as it was, while the remaining steps carry on. |

## How it works

![A route of seven steps: a probe on the machine after each one, and only then the next](docs/img/how-jadlis-start.webp)

Going in — the word `JADLIS-BATCH` in the chat.
Inside — a probe of the current step right on your machine: is what the step needs there, and does it
answer.
Coming out — seven route lines with statuses and exactly one next step.

In words: a word in the chat → the 0 → 6 route with statuses → a probe on the machine → the step
opens; if it did not confirm, it does not open, and you are told exactly what failed.

## Installing and the first run

**a) Text to paste to an agent.** Copy the whole thing into a Claude Code chat:

```
You are the installer. Install the plugin jadlis-start from the jadlis marketplace on this Mac.
First check that Claude Code is installed and the subscription is active; if not, stop and say so.
Then run exactly these commands, verbatim, shortening nothing:
1. claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
2. claude plugin install jadlis-start@jadlis
3. claude plugin list — show me the line about jadlis-start and its version.
Then type the word JADLIS-BATCH into the chat and show me the route with its statuses.
Before each command show it to me in full and wait for "yes". If I say "no", do not run it,
leave the file as it was, tell me what you skipped, and move on.
Do not replace my config, merge it with the current one; show every edit in full.
Do not ask me for keys: this step does not need them. Never print key values.
If a command returns an error, stop, show me the output, and do not move to the next one.
```

**b) Commands by hand.**

```
claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
claude plugin install jadlis-start@jadlis
claude plugin list
```

The first command installs nothing — it adds the marketplace.

**c) The first word.** Open Claude Code in the folder you work in and type one word, no slash:

```
JADLIS-BATCH
```

It is a word, not a slash command. It opens the route, it brings you back into it after a break, and
it is repeated at the end of every answer — you will never have to hunt for it in the chat history.

The first step of the route is the workplace: the route installs `setup@jadlis` itself and walks you
through its steps — `/setup:deps`, `/setup:workplace`, `/setup:obsidian` and, if you want it,
`/setup:terminal`. There is no need to install it separately beforehand.

## Limits, cost, updating

**What it does not do.** It does not read the values of your keys — it only checks whether they are
set up or not. It does not take out subscriptions for you and does not pay for them. It does not
decide which tool from the catalogue you need: the route shows the order, the choice is yours. And it
does not hand out the next step on trust — not out of spite: without keys a later step will not work
on your machine, and you will conclude that everything is broken.

**What you need.** A Mac and an active Claude Code subscription. Missing either one and nothing
further works; better to find that out now than on the third step. The route steps where search
switches on need the paid Brave and Firecrawl keys — said here, before installing, not halfway
through. Brave and Firecrawl are the ones who bill you, so check their pricing with them: I name no
figures of my own. Checked on macOS 27.0 and Claude Code 2.1.263; below those versions I have not
tested it.

**The catalogue.** The route leads through the other 17 repositories of the showcase: each is
installed by its own command, there is no single "install everything" button and there never will be
— you install whatever you have reached. The tier map, with docs for each one, is in [docs](docs/).

**How tokens get spent.** The route itself is light: it asks, it checks, it prints a table. The heavy
part starts where the route takes you: a heavy run is dozens of subagents out of your own quota, and
the route names such steps in advance. What it costs in money I have not measured and will not name a
figure.

**Verified where I work:** my Mac, my subscription, my keys. I have not tested it on anyone else's
machine — if it did not install for you, open an issue in the repository.

**Terms of use.** There is no license: all rights reserved by the author. You may read it and use it
personally. Commercial use, republishing and bundling it into your own products — by arrangement
with me.

**Updating.** With a third-party marketplace, auto-update is off on your side: until you run the
first command you keep the version you installed.

```
claude plugin marketplace update jadlis
claude plugin update jadlis-start@jadlis
claude plugin list
```

Reinstall, if something ended up crooked:

```
claude plugin uninstall jadlis-start@jadlis --keep-data && claude plugin install jadlis-start@jadlis
```
