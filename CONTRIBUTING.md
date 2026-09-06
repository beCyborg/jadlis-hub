Русский · [English](#english)

# Как предложить правку

Репозиторий публичный, пишет в него только владелец. Правки принимаются через **форк + pull request**.

1. Сделай форк и ветку от `main`.
2. Правь в своём клоне; перед коммитом прогони `claude plugin validate .claude-plugin/marketplace.json` и `python3 tools/readme-parity.py`.
3. Коммит — по формату из [CLAUDE.md](CLAUDE.md): тема на английском по Conventional Commits, тело из двух слоёв («Что изменилось» для человека, `Details (for agents)` для агентов). Шаблон — `.gitmessage`.
4. Открой PR: одна тема — один PR. В описании — что меняется для получателя.
5. Ключи, почты, личные пути в репо не попадают: `gitleaks git .` и `python3 tools/privacy-grep.py` должны быть чистыми.

Релизы и теги делает владелец.

---

<a id="english"></a>
[Русский](#как-предложить-правку) · English

# How to contribute

The repository is public; only the owner has write access. Changes come in through **fork + pull request**.

1. Fork and branch off `main`.
2. Edit in your clone; before committing run `claude plugin validate .claude-plugin/marketplace.json` and `python3 tools/readme-parity.py`.
3. Commit in the format from [CLAUDE.md](CLAUDE.md): English Conventional Commits subject, two-layer body (a Russian "what changed" line for people, `Details (for agents)` for agents). Template: `.gitmessage`.
4. Open a PR: one topic per PR. Describe what changes for a recipient.
5. No keys, emails or personal paths: `gitleaks git .` and `python3 tools/privacy-grep.py` must be clean.

Releases and tags are cut by the owner.
