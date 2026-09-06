#!/bin/bash
# Простой statusline для Claude Code: папка | ветка git | контекст % | модель/effort.
# Ставится скиллом /setup:workplace в ~/.claude/statusline.sh.
# Работает только в терминальном CLI — десктоп строку состояния не рисует.
# Нужен jq: brew install jq.

input=$(cat)

if ! command -v jq >/dev/null 2>&1; then
  printf 'statusline: нужен jq (brew install jq)\n'
  exit 0
fi

GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
DIM='\033[2m'
RESET='\033[0m'

colorize() {
  if   [ "$1" -ge 80 ]; then printf '%b' "$RED"
  elif [ "$1" -ge 60 ]; then printf '%b' "$YELLOW"
  else                       printf '%b' "$GREEN"
  fi
}

# --- Папка проекта ---
project_dir=$(printf '%s' "$input" | jq -r '.workspace.project_dir // .cwd // ""')
project_name="${project_dir##*/}"
[ -z "$project_name" ] && project_name="~"

# --- Ветка git (пусто вне репозитория) ---
branch=""
if [ -n "$project_dir" ] && command -v git >/dev/null 2>&1; then
  branch=$(git -C "$project_dir" rev-parse --abbrev-ref HEAD 2>/dev/null)
  [ "$branch" = "HEAD" ] && branch=$(git -C "$project_dir" rev-parse --short HEAD 2>/dev/null)
fi

# --- Заполненность окна контекста ---
used_pct=$(printf '%s' "$input" | jq -r '.context_window.used_percentage // 0')
used_int=$(printf '%.0f' "$used_pct")
ctx_color=$(colorize "$used_int")

# --- Модель и уровень усилий (effort.level есть не у всех моделей) ---
model_name=$(printf '%s' "$input" | jq -r '.model.display_name // .model.id // empty')
effort_lvl=$(printf '%s' "$input" | jq -r '.effort.level // empty')
model_part="${model_name}${effort_lvl:+/$effort_lvl}"

# --- Сборка строки ---
out="$project_name"
[ -n "$branch" ] && out="${out} ${DIM}${branch}${RESET}"
out="${out} | ${ctx_color}${used_int}%${RESET}"
[ -n "$model_part" ] && out="${out} | ${model_part}"

printf '%b\n' "$out"
