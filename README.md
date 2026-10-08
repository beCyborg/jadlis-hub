# Jadlis — ресёрч для Claude Code

<p align="center">
  <img src="docs/img/05-full-research-01.webp" width="100%" alt="Две лупы над одной карточкой: через одну она целая, через другую треснула">
</p>

Каталог плагинов `jadlis` для Claude Code. Сейчас в нём три плагина: поиск, полный ресёрч и научный ресёрч.
Остальные плагины переедут сюда позже.

| Плагин | Команда | Что даёт |
|---|---|---|
| [`jadlis-search`](https://gitlab.com/beCyborg/jadlis-search) | `/search` | ИИ ищет в интернете и читает страницы. Здесь же хранятся ключи. Это база для обоих ресёрчей. |
| [`jadlis-research`](https://gitlab.com/beCyborg/jadlis-research) | `/research` | Один вопрос — отчёт из 14 каналов. Ключевые утверждения перепроверены, непроверенные помечены. |
| [`jadlis-science-research`](https://gitlab.com/beCyborg/jadlis-science-research) | `/science-research` | Что реально доказано наукой: научные базы, проверка на отзыв статьи, вывод по силе доказательства. |

> [!IMPORTANT]
> Нужен Mac и подписка [Claude](https://claude.ai) на тарифе Max.
> Для поиска нужны два ключа: [Brave Search](https://brave.com/search/api/) и [Firecrawl](https://firecrawl.dev).

## Установка

Скопируй в терминал по очереди:

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

Подробности по каждому плагину, текст для вставки агенту и первый запуск — в README плагина по ссылке из таблицы.

## Обновление

У стороннего каталога автообновление по умолчанию выключено. Обновиться можно так:

```
claude plugin marketplace update jadlis
claude plugin update jadlis-search@jadlis
claude plugin update jadlis-research@jadlis
claude plugin update jadlis-science-research@jadlis
```

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
