# Уведомление, когда Claude Code закончил

Проблема: агент доработал и ждёт тебя, а ты этого не видишь — окно свёрнуто,
внимание уехало. Уведомление возвращает внимание ровно в момент готовности.

## Готовый вариант — плагин `claude-notifications-go`

Нативные macOS-уведомления по событиям Claude Code: ответ готов, нужен ответ
на вопрос, задача упала. Ставится одной парой команд:

```bash
claude plugin marketplace add https://github.com/777genius/claude-notifications-go.git
claude plugin install claude-notifications-go@claude-notifications-go
```

Дальше `/reload-plugins` — и уведомления начинают приходить. Хуки плагин ставит сам,
руками в `settings.json` ничего дописывать не нужно.

## Ручной минимум — один звук

Если плагин ставить не хочешь, хватит хука `Stop` в `~/.claude/settings.json`
(он же лежит в `settings.minimal.json` этого плагина):

```json
"hooks": {
  "Stop": [
    { "hooks": [ { "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff", "timeout": 5 } ] }
  ]
}
```

Звук поменять — любой файл из `/System/Library/Sounds/`. Выключить — удалить блок `Stop`.

## Границы

- Плагин и хук работают на macOS. На других системах команду `afplay` заменить своей.
- Хук `Stop` срабатывает на каждый завершённый ответ, а не только на длинные.
  Раздражает — оставь только плагин, он различает события.
