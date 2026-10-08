# Jadlis — плагины для Claude Code

<p align="center">
  <img src="docs/img/05-full-research-01.webp" width="100%" alt="Две лупы над одной карточкой: через одну она целая, через другую треснула">
</p>

Каталог плагинов `jadlis` для Claude Code. Сейчас в нём семь плагинов: ресёрч, проверка планов, браузер и инструменты,
чтобы собирать своих ИИ-сотрудников. Остальные плагины переедут сюда позже.

| Плагин | Команда | Что даёт |
|---|---|---|
| [`jadlis-search`](https://gitlab.com/beCyborg/jadlis-search) | `/search` | ИИ ищет в интернете и читает страницы. Здесь же хранятся ключи. Это база для обоих ресёрчей. |
| [`jadlis-research`](https://gitlab.com/beCyborg/jadlis-research) | `/research` | Один вопрос — отчёт из 14 каналов. Ключевые утверждения перепроверены, непроверенные помечены. |
| [`jadlis-science-research`](https://gitlab.com/beCyborg/jadlis-science-research) | `/science-research` | Что реально доказано наукой: научные базы, проверка на отзыв статьи, вывод по силе доказательства. |
| [`jadlis-verif`](https://gitlab.com/beCyborg/jadlis-verif) | `/verif` | Две модели разных компаний ищут дыры в твоём плане порознь, арбитр сводит находки в один список. |
| [`jadlis-browser`](https://gitlab.com/beCyborg/jadlis-browser) | `/browser` | ИИ работает в твоём Chrome на сайтах, где ты уже залогинен, без передачи паролей. |
| [`jadlis-skill-builder`](https://gitlab.com/beCyborg/jadlis-skill-builder) | `/skill-builder` | Свой ИИ-сотрудник: пишешь инструкцию, как для нового работника, и ИИ делает эту работу сам. |
| [`jadlis-plugin-creator`](https://gitlab.com/beCyborg/jadlis-plugin-creator) | `/plugin-creator` | Собрать, проверить и выпустить свой плагин, чтобы отдать его другому человеку. |

> [!IMPORTANT]
> Нужен Mac и подписка [Claude](https://claude.ai) на тарифе Max.
> Для поиска и ресёрча нужны два ключа: [Brave Search](https://brave.com/search/api/) и [Firecrawl](https://firecrawl.dev).
> Для `jadlis-verif` нужна своя подписка [ChatGPT](https://chatgpt.com): он работает через Codex CLI.
> Для `jadlis-browser` нужен Chrome и расширение-мост из Chrome Web Store, подробности в README плагина.

## Установка

Ресёрч — скопируй в терминал по очереди:

```
claude plugin marketplace add https://gitlab.com/beCyborg/jadlis-hub.git
claude plugin install jadlis-search@jadlis
claude plugin install jadlis-research@jadlis
claude plugin install jadlis-science-research@jadlis
```

Первая команда ничего не ставит, она добавляет каталог. Ссылку пиши целиком, с `https://` и `.git`:
короткая запись `владелец/репозиторий` в Claude Code работает только для GitHub.

`jadlis-search` ставь первым. Потом введи ключи в чате Claude Code командой `/plugin configure jadlis-search@jadlis`.
Поля с ключами при вводе скрыты, значения уходят в Связку ключей macOS.

Остальные плагины ставятся по одному и не зависят друг от друга:

```
claude plugin install jadlis-verif@jadlis
claude plugin install jadlis-browser@jadlis
claude plugin install jadlis-skill-builder@jadlis
claude plugin install jadlis-plugin-creator@jadlis
```

Подробности по каждому плагину, текст для вставки агенту и первый запуск — в README плагина по ссылке из таблицы.

## Обновление

У стороннего каталога автообновление по умолчанию выключено. Обновиться можно так:

```
claude plugin marketplace update jadlis
claude plugin update <плагин>@jadlis
```

Например, `claude plugin update jadlis-research@jadlis`. Повтори для каждого плагина, который у тебя стоит.

Чтобы обновления приходили сами, включи автообновление для `jadlis`: `/plugin` → Marketplaces → `jadlis`.

## Если каталог уже стоял со ссылки GitHub

Раньше каталог жил на `github.com/beCyborg/jadlis-hub`. Сейчас этот аккаунт заблокирован, и старая ссылка открывает 404.
Удали каталог командой `claude plugin marketplace remove jadlis` и поставь всё заново по разделу «Установка».
Плагины этого каталога при удалении тоже снимутся, поэтому ключи для `jadlis-search` придётся ввести ещё раз.

<details>
<summary>Условия использования, ошибки и правки</summary>

**Условия использования.** Лицензии нет: все права сохранены за автором. Читать и
пользоваться лично можно. Коммерческое использование, переиздание и включение в свои
продукты — по договорённости со мной.

**Если не встало** — напиши в issue этого репозитория. Для этого нужен аккаунт GitLab.

**Как предложить правку** — [CONTRIBUTING.md](CONTRIBUTING.md).

</details>
