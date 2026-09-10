# Пробы машины — как помощник снимает состояние

Состояние определяют **пробы**, а не слова человека и не журнал. Человек искренне считает,
что «рабочее место сделано», когда открыл Claude Code. Проба этого не подтвердит, пока нет
`jq`, Node.js и папки vault — и правильно.

Блок ничего не меняет — только читает. Значения ключей не печатает: только «есть/нет».

## Как найти папку установленного плагина

`${PLUGIN_ROOT_OF:<плагин>}` в `route.json` — не переменная Claude Code, а указание помощнику
найти путь самому. Источник — `claude plugin list --json`, массив объектов с полями
`id` (`имя@маркетплейс`), `version`, `scope`, `enabled`, `installPath`, `installedAt`,
`lastUpdated`. Отдельного поля `name` нет — имя берётся из `id` до `@`.

```bash
claude plugin list --json | jq -r --arg n jadlis-obsidian \
  'map(select((.id|split("@")[0])==$n))|.[0].installPath // empty'
```

## Один блок

Выполни **одним** Bash-вызовом. `V` — папка vault (по соглашению `~/Jadlis`).

```bash
V="$HOME/Jadlis"
have(){ command -v "$1" >/dev/null 2>&1 && echo да || echo нет; }
PL=$(claude plugin list --json 2>/dev/null || echo '[]')
q(){ printf '%s' "$PL" | jq -r --arg n "$1" "$2" 2>/dev/null; }
inst(){ q "$1" 'map(select((.id|split("@")[0])==$n))|if length==0 then "нет" elif .[0].enabled then "да" else "выключен" end'; }
root(){ q "$1" 'map(select((.id|split("@")[0])==$n))|.[0].installPath // empty'; }
sub(){ p=$(root "$1"); if [ -n "$p" ] && [ -x "$p/scripts/probe.sh" ]; then "$p/scripts/probe.sh" 2>/dev/null | sed "s/^/  $1 /"; else echo "  $1 probe=НЕТ"; fi; }

# ── Окружение ──────────────────────────────────────────────────────────────
echo "СРЕДА claude=$(claude --version 2>/dev/null | awk '{print $1}') jq=$(have jq) node=$(have node) папка_vault=$([ -d "$V" ] && echo да || echo нет) obsidian=$([ -d "/Applications/Obsidian.app" ] && echo да || echo нет) spokenly=$([ -f "$HOME/Library/Containers/app.spokenly/Data/Library/Preferences/app.spokenly.plist" ] && echo да || echo нет) codex=$(have codex) grok=$(have grok)"

# ── Сам помощник в CLI ─────────────────────────────────────────────────────
echo "ХАБ jadlis-hub=$(inst jadlis-hub) маркетплейс=$(claude plugin marketplace list 2>/dev/null | command grep -qi '\bjadlis\b' && echo да || echo нет)"

# ── Шаги 1–3: свой probe.sh внутри плагина ─────────────────────────────────
for p in jadlis-claudecode jadlis-obsidian jadlis-voice jadlis-notifications; do
  echo "ШАГ $p=$(inst $p)"; [ "$(inst $p)" = да ] && sub "$p"
done

# ── Шаги 4–6: пробы делает сам помощник ────────────────────────────────────
echo "ШАГ jadlis-search=$(inst jadlis-search)"
kb=нет; kf=нет
for s in jadlis jadlis-search; do
  security find-generic-password -s "$s" -a BRAVE_API_KEY     >/dev/null 2>&1 && kb=да
  security find-generic-password -s "$s" -a FIRECRAWL_API_KEY >/dev/null 2>&1 && kf=да
done
echo "КЛЮЧИ Brave=$kb Firecrawl=$kf (только имена, значения не читаются)"
echo "ШАГ jadlis-research=$(inst jadlis-research) jadlis-science-research=$(inst jadlis-science-research)"
echo "ШАГ jadlis-verif=$(inst jadlis-verif) codex=$(have codex) grok=$(have grok)"

# ── Необязательные шаги ────────────────────────────────────────────────────
for p in jadlis-swot-news jadlis-tldr jadlis-books jadlis-browser jadlis-computer-use jadlis-skill-builder jadlis-plugin-creator; do
  printf 'НЕОБЯЗ %s=%s\n' "$p" "$(inst $p)"
done

# ── Журнал (только «где я внутри шага») ────────────────────────────────────
J="$V/Система/Передача — состояние.md"
[ -f "$J" ] && echo "ЖУРНАЛ есть: $(command grep -m1 '^шаг:' "$J" 2>/dev/null)" || echo "ЖУРНАЛ отсутствует"
```

## Договор с плагинами шагов

Плагины `jadlis-claudecode`, `jadlis-obsidian`, `jadlis-voice` несут `scripts/probe.sh`,
который печатает строки вида `ключ=PASS` или `ключ=FAIL` — по одной на критерий, без
значений ключей и без прозы.

## Таблица критериев

| Шаг | Проба | «Закрыт», если |
|---|---|---|
| 1 claudecode | `inst` + свой `probe.sh` | плагин стоит и включён, ни одного `FAIL` |
| 2 obsidian | `inst` + свой `probe.sh` | плагин стоит и включён, ни одного `FAIL` |
| 3 voice | `inst` + свой `probe.sh` | плагин стоит и включён, ни одного `FAIL` |
| 4 search | `claude plugin list --json` | плагин стоит **и** включён; ключи подтверждает человек через `/jadlis-search:keys --check` |
| 5 research | `claude plugin list --json` | стоят и включены оба: `jadlis-research`, `jadlis-science-research` |
| 6 verif | `claude plugin list --json` + `codex --version` | плагин стоит и включён **и** `codex` отвечает (Grok — по выбору, на закрытие не влияет) |
| необязательные | `claude plugin list --json` | плагин стоит и включён |

## Как читать результат

- `claude=2.1.267`, а `jq=нет` → десктоп поставлен, CLI-окружения нет. Самый частый провал шага 1: десктопное приложение **не ставит** CLI.
- `jadlis-search=выключен` → поставлен, но не включён: после плагина с MCP нужен полный перезапуск Claude Code.
- `probe=НЕТ` у стоящего плагина → версия плагина без `scripts/probe.sh`; считай шаг незакрытым и скажи об этом одной строкой.
- `Brave=нет` → ключ не заведён; значение не спрашивай и не печатай, отправь к `/jadlis-search:keys`.
- `codex=нет` → verif пойдёт в режиме двух моделей; для закрытия шага 6 Codex обязателен.

## Расхождение с журналом

Журнал `Система/Передача — состояние.md` отвечает **только** на «где я внутри шага».
На вопрос «закрыт ли шаг» отвечают пробы. Журнал говорит «шаг закрыт», пробы — нет:
перепиши журнал по пробам и скажи об этом **одной строкой**, без разбирательства.
