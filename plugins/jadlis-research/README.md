Русский · [English](README.en.md)

# jadlis-research — ресерч-стек

Пять скиллов и пять MCP-серверов: обычный поиск, полный ресерч по сообществам, научный обзор и тройная проверка своего файла. Ставится выключенным (`defaultEnabled: false`) — тянет платные сервисы.

## Зачем

Один плагин закрывает три разные задачи, которые иначе разъезжаются по десятку инструментов.

- **Проверить свой файл** — `verif` читает его тремя ИИ разных компаний порознь и сводит итог по худшему.
- **Разобраться в теме** — `full-research` идёт по четырнадцати каналам сразу и проверяет каждое утверждение по нескольким источникам.
- **Опереться на науку** — `search-paper` собирает обзор по девяти научным источникам с проверкой отзывов статей.

Отчёты и вердикты ложатся в vault, а не остаются в чате.

## Как выглядит

<details>
<summary>Синтетический пример: команды и что они возвращают (данные вымышленные)</summary>

```
/jadlis-research:search кто платит за ключи конкурента
── BRAVE web · 1256 ms · $0.0050 · 3 res
 1 example.com/pricing · Pricing — Example
 2 docs.example.org/api · API reference

/jadlis-research:verif --file План.md
Коротко: нужны правки — 9 сырых находок от 3 проверяющих, из них 3 серьёзных.
VERDICT: NEEDS-REVISION  (Codex: needs-revision · Fable: needs-revision · Grok: approve)
Артефакты: AI/verif/2026-09-06--plan--{codex,fable,grok,merged,arbiter}.json

/jadlis-research:keys --list
  BRAVE_API_KEY              31     pluginSecrets (Claude Code-credentials)
  PUBMED_API_KEY             36     keychain generic (jadlis-research/PUBMED_API_KEY)
  YC_SEARCH_API_KEY          -      НЕТ
```

</details>

## Как поставить

Скопируй блок ниже в Claude Code — он всё сделает сам.

```text
Ты — установщик. Выполни ровно эти шаги и ничего сверх них:
1. Bash: claude plugin marketplace add https://github.com/beCyborg/jadlis-plugins.git
2. Bash: claude plugin install jadlis-research@jadlis
3. Bash: claude plugin enable jadlis-research
4. Скажи мне: «Плагин включён. Дальше руками: /plugin configure jadlis-research@jadlis —
   введи BRAVE_API_KEY и FIRECRAWL_API_KEY. Потом перезапусти Claude Code и вызови
   /jadlis-research:keys».
```

Тот же путь руками, теми же командами:

1. Заведи два обязательных ключа: Brave (тариф Search) и Firecrawl.
2. `claude plugin marketplace add https://github.com/beCyborg/jadlis-plugins.git`
3. `claude plugin install jadlis-research@jadlis`
4. `claude plugin enable jadlis-research` — Claude Code спросит ключи класса A и положит их в Связку ключей macOS.
5. Перезапусти Claude Code, затем `/jadlis-research:keys` — остальные ключи и smoke-проверка.

Подробный разбор установки и стандарта ключей — [docs/2-verif](../../docs/2-verif/README.md); ресерч-часть — [docs/3-research](../../docs/3-research/README.md).

## Как пользоваться

Пять скиллов, три типовых сценария:

```text
/jadlis-research:search <вопрос>                  # веб-поиск Brave + Exa с роутингом по интенту
/jadlis-research:full-research <тема>             # 14 каналов → верификация утверждений → отчёт в vault
/jadlis-research:verif --file <свой план>         # три верификатора → арбитр → вопросы к тебе
```

Остальные два: `/jadlis-research:search-paper <вопрос>` — научный обзор по девяти источникам с GRADE-синтезом; `/jadlis-research:keys` — ключи, homes верификаторов и smoke-таблица PASS/FAIL.

## Границы и стоимость

Что нужно оплатить и завести:

| Что | Роль | Обязательно |
|---|---|---|
| Brave Search API, тариф Search | основной поисковый движок, ≈$0.005/запрос | да |
| Firecrawl | скрап страниц и динамики | да |
| Подписка ChatGPT (Codex CLI) | канал `codexweb`, верификатор Codex | нет |
| Подписка Grok (Grok CLI) | каналы `grokweb` / `twitter`, верификатор Grok | нет |
| `TWITTERAPI_IO_KEY` | реплаи, био и тренды в канале `twitter`; keyword-фолбэк при мёртвом Grok (~$0.003 за страницу) | нет |
| `EXA_API_KEY`, `YC_SEARCH_API_KEY`, научные ключи | семантический слой, Рунет, `search-paper` | нет |

Чего плагин не делает: не ревьюит код (для этого `/code-review`), не заменяет обычный поиск на однофразовых вопросах, не принимает решений за человека. Каналы без ключа не падают, а деградируют — прогон продолжается на остальных.

## Устройство

**Ключи** живут в Связке ключей macOS и читаются одной точкой `scripts/secret.sh` (env → Keychain `jadlis-research`/`KEY` → `pluginSecrets` записи `Claude Code-credentials` → `.credentials.json` → `settings.json → env` как legacy). Класс A (`BRAVE_API_KEY`, `FIRECRAWL_API_KEY`, `REDDITAPIS_KEY`, `YOUTUBE_API_KEY`) пишет Claude Code через `/plugin configure jadlis-research@jadlis`; класс B (научные, Exa, Yandex, Places, почты) — скилл `keys` через stdin.

**Пять MCP-серверов:** `brave-search` (`BRAVE_API_KEY`), `firecrawl` (`FIRECRAWL_API_KEY`), `reddit` (без ключа), `reddit-alt` (`REDDITAPIS_KEY`, опц.), `youtube` (`YOUTUBE_API_KEY`, опц.). HackerNews, Substack и Telegram идут своими скриптами — MCP-фоллбэка сознательно нет.

**Каналы `full-research`:**

| Канал | Чем берёт | Деградация без ключа или CLI |
|---|---|---|
| `web` | Brave MCP + Firecrawl, place-слой `scripts/places-fetch.sh` | place-слой уходит в `brave_place_search` |
| `codexweb` / `grokweb` / `twitter` | Codex CLI, Grok CLI (+ `scripts/twitterapi.sh` для реплаев/био/трендов) | `codexweb`/`grokweb` выпадают; `twitter` без Grok живёт keyword-only на TwitterAPI.io, без ключа выпадает |
| `reddit` / `hackernews` / `substack` / `telegram` | MCP `reddit` + `scripts/{reddit-archive.py,hn-fetch.sh,substack-fetch.py,tg-preview.sh}` | лестница без ключей; сломался фетчер → Brave, `sourceQuality=LOW` |
| `yandex` / `youtube` | `scripts/yandex-search.sh`, Brave + MCP `youtube` | `yandex` не предлагается; `youtube` живёт на Brave и локальных транскриптах |
| `ja` / `zh` / `ko` / `eu` | `scripts/feed-fetch.py` (фиды и keyless-API площадок) | ключей не нужно; мёртвый фид → канал деградирует |

**Внешние бинарники:** `jq` (обязателен для `secret.sh`, `hn-fetch.sh`, `places-fetch.sh`), `uv` (шебанг `substack-fetch.py` и `yt-transcript.py`), `pdftotext` из poppler (для `pdf-fetch.sh`), опц. `yt-dlp`, опц. `codex` / `grok` CLI.

**Пути:** `${CLAUDE_PLUGIN_ROOT}` подставляется только в тексте `SKILL.md` и агентов. В `protocols/` и `references/` подстановки нет — там пишется `{PLUGIN_ROOT}`, значение агенту сообщает промпт workflow. В JS-скриптах workflow корень приходит через `args.pluginRoot`. В Bash-скриптах резолвится от самого скрипта. Рабочие homes верификаторов живут в `${CLAUDE_PLUGIN_DATA}/verif-homes/`, шаблоны — в `assets/verif-homes/`; `auth.json` там — симлинки на логины Codex и Grok, в репозиторий не попадают никогда.

**Модели:** плагин не задаёт алиасов и работает на дефолтах подписки. Синтез ресерча идёт через headless-мост `claude -p --model claude-fable-5`, при падении доигрывается на Opus 5, а скилл правит `ai_model` во frontmatter отчёта по фактически ответившей модели. Верификаторы `verif`: Codex `gpt-6-astra`, Claude Fable 5, Grok `grok-4.6`; арбитр — Fable 5.
