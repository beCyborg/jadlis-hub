---
name: workplace
description: "Тир 0: настраивает ~/.claude под получателя — сливает settings.json через jq с показом диффа, кладёт базовый CLAUDE.md, включает память, ставит уведомления и строку состояния. Опции спрашивает, чужие ключи не перезаписывает.\nTRIGGER when: user says \"/setup:workplace\", \"настрой claude code\", \"настрой рабочее место\", \"настрой settings.json\", \"положи CLAUDE.md\", \"включи память\", \"включи уведомления\", \"поставь statusline\", \"настрой язык ответов\", \"configure claude code\", \"setup workplace\".\nDO NOT TRIGGER when: не хватает jq, node или CLI claude — сначала /setup:deps; папка-vault и её CLAUDE.md — /setup:obsidian; iTerm2, tmux, алиасы — /setup:terminal; ключи API — тир 2 (/search:keys)."
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
argument-hint: "[настроить | показать дифф]"
---

# Настройка ~/.claude

`$ARGUMENTS`

```
ASSETS = ${CLAUDE_PLUGIN_ROOT}/assets
```

Читателю с СДВГ: **первая строка — действие**, один шаг за реплику. Ни один файл
не меняется без показанного диффа и явного «да».

## Шаг 0 — что уже есть

```bash
mkdir -p "$HOME/.claude"
command -v jq >/dev/null 2>&1 && echo "jq PASS" || echo "jq FAIL — сначала /setup:deps"
[ -f "$HOME/.claude/settings.json" ] && echo "settings.json есть: $(wc -c < "$HOME/.claude/settings.json") байт" || echo "settings.json нет"
[ -f "$HOME/.claude/CLAUDE.md" ] && echo "CLAUDE.md есть: $(wc -l < "$HOME/.claude/CLAUDE.md") строк" || echo "CLAUDE.md нет"
[ -f "$HOME/.claude/statusline.sh" ] && echo "statusline.sh есть" || echo "statusline.sh нет"
```

`jq FAIL` — останавливайся и отправляй на `/setup:deps`. Без `jq` слияние настроек
делать нельзя: ручная правка JSON затирает чужие ключи.

## Шаг 1 — четыре вопроса

Один `AskUserQuestion` с четырьмя вопросами. В описании каждого варианта — **одна**
строка «что это значит», без абзацев.

| Вопрос | Варианты | Что объяснить одной строкой |
|---|---|---|
| Язык ответов | Русский · English | На каком языке Claude Code пишет ответы и заметки. |
| Режим «читатель с СДВГ» | Включить · Не надо | Первая строка = действие, шаги списком, никаких простыней. |
| Уведомления | Плагин · Только звук · Не надо | Плагин различает события; звук — один хук `Stop`. |
| Разрешения | `default` · `acceptEdits` · `bypassPermissions` | `default` спрашивает перед записью; `bypassPermissions` не спрашивает вообще. |

Про `bypassPermissions` скажи прямо одной строкой: агент выполняет команды без вопросов —
включать осознанно и не в первый день. Дефолт предлагай `default`.

## Шаг 2 — settings.json через jq, с диффом

Собери оверлей из ответов и слей три слоя: текущий файл → базовый набор плагина →
оверлей. Оператор `*` в jq сливает объекты вглубь — чужие ключи остаются на месте.

```bash
CFG="$HOME/.claude/settings.json"
[ -s "$CFG" ] || echo '{}' > "$CFG"
BASE="${CLAUDE_PLUGIN_ROOT}/assets/settings.minimal.json"
TMP_BASE=$(mktemp -t setup-base); TMP_OVL=$(mktemp -t setup-ovl); TMP_NEW=$(mktemp -t setup-new)

# LANG=Russian|English, MODE=default|acceptEdits|bypassPermissions — из ответов шага 1
jq -n --arg lang "Russian" --arg mode "default" \
  '{language:$lang, permissions:{defaultMode:$mode}}' > "$TMP_OVL"

# лишнее выкидываем из базового набора, а не дописываем в файл пользователя:
#   уведомления не нужны        → del(.hooks)
#   строка состояния не нужна   → del(.statusLine)
jq '.' "$BASE" > "$TMP_BASE"

jq -s '.[0] * .[1] * .[2]' "$CFG" "$TMP_BASE" "$TMP_OVL" > "$TMP_NEW"
diff <(jq -S . "$CFG") <(jq -S . "$TMP_NEW") || true
echo "---"; echo "TMP_NEW=$TMP_NEW"
```

Покажи **только дифф** — не весь файл. Затем спроси «применяем?». Ответ «да»:

```bash
CFG="$HOME/.claude/settings.json"
cp "$CFG" "$CFG.bak-$(date +%Y%m%d-%H%M%S)"
mv "$TMP_NEW" "$CFG"
jq -e . "$CFG" >/dev/null && echo "settings.json валиден, бэкап рядом"
```

Что именно кладётся — по строке на ключ:

- `language` — язык ответов.
- `timeFormat: 24-hour` — время без AM/PM.
- `alwaysThinkingEnabled` — модель думает перед каждым ответом, точнее на сложном.
- `autoMemoryEnabled` — **память**: уроки и поправки переживают перезапуск сессии.
- `effortLevel: high` — сколько усилий на ответ; `xhigh` ест недельную квоту быстрее.
- `theme: auto` — тема за системной.
- `permissions.defaultMode` — как часто спрашивают разрешение.
- `hooks.Stop` — звук по завершении (если выбрали «Только звук»).
- `statusLine` — строка состояния в терминале (шаг 5).

Комментированный вариант того же набора — `assets/settings.template.jsonc`.
Показывай его, только если спросят «а что ещё бывает».

## Шаг 3 — CLAUDE.md

**Файл уже есть — не перезаписывай.** Прочитай его, сравни заголовки с шаблоном
`assets/CLAUDE.md.template` и предложи дописать только недостающие блоки:

```bash
for h in "## Стиль ответа" "## Форма вывода (СДВГ-читатель)" "## Язык артефактов" "## Память"; do
  grep -qF "$h" "$HOME/.claude/CLAUDE.md" && echo "есть: $h" || echo "нет:  $h"
done
```

Дописывай блоками через `Edit`, по одному, каждый — с подтверждением. Решает пользователь.

Файла нет — скопируй шаблон и обработай маркеры блока СДВГ:

```bash
SRC="${CLAUDE_PLUGIN_ROOT}/assets/CLAUDE.md.template"
DST="$HOME/.claude/CLAUDE.md"
# режим СДВГ включён → снять только маркеры:
sed '/<!-- adhd:\(start\|end\) -->/d' "$SRC" > "$DST"
# режим СДВГ не нужен → вырезать блок целиком:
# sed '/<!-- adhd:start -->/,/<!-- adhd:end -->/d' "$SRC" > "$DST"
wc -l < "$DST" | xargs echo "CLAUDE.md строк:"
```

Скилл `/setup:i-have-adhd` — англоязычный вариант тех же правил, включается на сессию
командой. Одно отличие: он просит давать оценки времени в конкретных единицах, а блок
в `CLAUDE.md` — не давать вовсе. Включил блок — скилл отдельно не нужен.

## Шаг 4 — уведомления

Ответ «Плагин» — прочитай `${CLAUDE_PLUGIN_ROOT}/assets/hooks/notify.md` и выполни
две команды оттуда. Ответ «Только звук» — хук `Stop` уже приехал с шагом 2, ничего
делать не надо. Ответ «Не надо» — выкинь `.hooks` из базового набора до слияния.

## Шаг 5 — строка состояния (только терминал)

Спроси, нужна ли. Десктопное приложение строку состояния не рисует — предлагай её,
только если человек работает в терминале.

```bash
cp "${CLAUDE_PLUGIN_ROOT}/assets/statusline.sh" "$HOME/.claude/statusline.sh"
chmod +x "$HOME/.claude/statusline.sh"
bash -n "$HOME/.claude/statusline.sh" && echo "statusline.sh на месте"
```

Показывает: папку, ветку git, процент заполнения контекста, модель и уровень усилий.
Не нужна — выкинь `.statusLine` из базового набора до слияния.

## Шаг 6 — проверка одним действием

```bash
jq -e '{language, effortLevel, autoMemoryEnabled, mode: .permissions.defaultMode}' "$HOME/.claude/settings.json"
```

Затем ровно две строки:

1. Что теперь работает: язык, память, режим разрешений — значениями, а не словами.
2. Дальше: `/setup:obsidian`, а перезапуск Claude Code подхватит настройки.

## Чего не делать

- Не редактировать `settings.json` текстом, `Write` или `sed` — только `jq` во временный
  файл, дифф, подтверждение, `mv`.
- Не перезаписывать существующий `CLAUDE.md`.
- Не писать в `settings.json` ключи API — они живут в Связке ключей macOS (тир 2).
- Не включать `bypassPermissions` по своей инициативе.
- Не пересказывать содержимое файлов целиком: дифф и строка итога.
