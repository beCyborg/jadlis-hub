Русский · [English](README.en.md)

# setup — рабочее место (тир 0)

Четыре команды доводят чистый Mac до состояния, в котором Claude Code уже работает
на тебя: программы стоят, настройки на месте, папка для заметок заведена.

## Зачем

Проблема: Claude Code из коробки не знает ни языка, ни твоих правил, ни где живут
заметки — и половина времени первой недели уходит на «а где это настраивается».

Плагин закрывает этот разрыв: ставит недостающие программы, сливает базовый
`settings.json`, кладёт `CLAUDE.md` с правилами ответа, включает память и заводит
папку-vault. Всё остальное на маршруте 0–6 опирается на это.

Ничего не происходит молча: каждая правка показывается диффом и ждёт «да».

## Как выглядит

![Рабочее место: человек за столом, пять панелей, у каждой работает механическая рука, справа стопка готовых листов](../../docs/img/08-employee-01.webp)

<details>
<summary>Таблица зависимостей после <code>/setup:deps</code></summary>

```text
brew   PASS  Homebrew 4.6.0
claude FAIL
jq     PASS  jq-1.8.1
node   PASS  v24.4.0
npx    PASS  11.4.2
git    PASS  git version 2.50.1
gh     FAIL
macOS  26.1 (arm64)

Ставим claude? Ставим gh?
```

</details>

## Как поставить

Вставь этот блок в Claude Code целиком:

```text
Ты — установщик. Выполни ровно эти шаги и ничего сверх них:
1. Bash: claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
2. Bash: claude plugin install setup@jadlis
3. Скажи мне: «Отправь /reload-plugins, потом напиши /setup:deps»
Ничего не читай, не создавай и не ставь помимо этого.
```

Руками — те же две команды в терминале:

```bash
claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
claude plugin install setup@jadlis
```

Полный HTTPS-URL обязателен: короткая форма `owner/repo` клонируется по SSH, а
SSH-ключа у нового пользователя обычно нет.

## Как пользоваться

Порядок команд — сверху вниз; `/setup:terminal` можно пропустить.

```text
/setup:deps         # что стоит, чего нет: Homebrew, CLI claude, jq, Node.js, git, gh
/setup:workplace    # ~/.claude: settings.json через jq, CLAUDE.md, память, уведомления
/setup:obsidian     # папка-vault + короткий CLAUDE.md для заметок
/setup:terminal     # опция: iTerm2, tmux, два алиаса вместо десктопного приложения
/setup:i-have-adhd  # включить режим коротких ответов на текущую сессию
```

Три типовых сценария:

- Чистый Mac: `/setup:deps` → `/setup:workplace` → `/setup:obsidian`.
- Claude Code уже настроен, нужна только папка: сразу `/setup:obsidian`.
- Хочется терминал вместо приложения: `/setup:terminal` — начнёт со сравнения таблицей.

## Границы и стоимость

Что плагин **не** делает:

- Не ставит подписку и приложение Claude Code — это делает человек до тира 0.
- Не строит скелет папок методологии и не заводит метрики — это тир 6 (`jadlis-vault`).
- Не трогает ключи API: они живут в Связке ключей macOS, их заводит тир 2.
- Не перезаписывает существующие `settings.json` и `CLAUDE.md` — только сливает и дописывает.

Стоимость: своих денег плагин не тратит. Нужны подписка Claude (Pro, Max, Team или
Enterprise) и macOS; Homebrew, jq, Node.js, git и gh — бесплатны. Обращений к платным
API плагин не делает.

## Лицензия

MIT. Скилл `i-have-adhd` включён по лицензии MIT автора исходного скилла.
