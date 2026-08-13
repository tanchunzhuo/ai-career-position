#!/usr/bin/env bash
# ============================================================
# AI职业选位（ai-career-position）一键安装脚本
#
# 用法：
#   ./install.sh                  # 安装到所有支持的平台（默认）
#   ./install.sh workbuddy        # 只装 WorkBuddy
#   ./install.sh claude codex     # 装指定平台
#
# 远程一句话安装（无需先 clone，直接贴进终端回车）：
#   curl -fsSL https://raw.githubusercontent.com/tanchunzhuo/ai-career-position/main/install.sh | bash
#
# 支持的平台及其用户级 skills 目录（以各平台官方文档为准，2026-08）：
#   WorkBuddy   -> ~/.workbuddy/skills
#   Claude Code -> ~/.claude/skills
#   Codex       -> ~/.agents/skills
#   Cursor      -> ~/.cursor/skills
# ============================================================
set -euo pipefail

SKILL_NAME="ai-career-position"
REPO_OWNER="tanchunzhuo"
REPO_NAME="ai-career-position"
REPO_BRANCH="main"
# GitHub 官方 tarball 端点，下载解压即可，不依赖 git
TARBALL_URL="https://codeload.github.com/${REPO_OWNER}/${REPO_NAME}/tar.gz/refs/heads/${REPO_BRANCH}"

usage() {
  cat <<'EOF'
用法：
  ./install.sh               安装到所有支持的平台（workbuddy/claude/codex/cursor）
  ./install.sh <平台...>     只装指定平台，例如：./install.sh workbuddy claude

远程一句话安装：
  curl -fsSL https://raw.githubusercontent.com/tanchunzhuo/ai-career-position/main/install.sh | bash
EOF
}

# 平台名 -> 用户级 skills 目录（环境变量可覆盖）
get_dir() {
  case "$1" in
    workbuddy) echo "${WORKBUDDY_DIR:-$HOME/.workbuddy/skills}" ;;
    claude)    echo "${CLAUDE_DIR:-$HOME/.claude/skills}" ;;
    codex)     echo "${CODEX_DIR:-$HOME/.agents/skills}" ;;
    cursor)    echo "${CURSOR_DIR:-$HOME/.cursor/skills}" ;;
  esac
}

# ---- 解析参数 ----
TARGETS=""
if [ $# -eq 0 ]; then
  TARGETS="workbuddy claude codex cursor"
else
  for arg in "$@"; do
    case "$arg" in
      --help|-h) usage; exit 0 ;;
      --all|-a)  TARGETS="workbuddy claude codex cursor" ;;
      workbuddy|claude|codex|cursor) TARGETS="$TARGETS $arg" ;;
      *) echo "未知参数：$arg"; usage; exit 1 ;;
    esac
  done
fi

# ---- 定位 skill 源目录 ----
# 若在项目目录内运行（旁边有 SKILL.md），直接用当前目录；
# 否则（如 curl | bash 管道执行）下载 tarball 解压到临时目录。
SOURCE_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ]; then
  SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi
TMP_DIR=""
if [ -z "$SOURCE_DIR" ] || [ ! -f "$SOURCE_DIR/SKILL.md" ]; then
  echo "→ 未在项目目录中运行，正在下载..."
  TMP_DIR="$(mktemp -d)"
  ARCHIVE="$TMP_DIR/repo.tar.gz"
  curl -fsSL "$TARBALL_URL" -o "$ARCHIVE" \
    || curl -fsSL --http1.1 "$TARBALL_URL" -o "$ARCHIVE" \
    || { echo "✗ 下载失败，请检查网络后重试。"; exit 1; }
  tar -xzf "$ARCHIVE" -C "$TMP_DIR"
  SOURCE_DIR="$TMP_DIR/${REPO_NAME}-${REPO_BRANCH}"
fi
if [ ! -f "$SOURCE_DIR/SKILL.md" ]; then
  echo "✗ 找不到 SKILL.md，安装中止。"
  exit 1
fi

# ---- 复制到各目标 ----
installed=""
for t in $TARGETS; do
  dest="$(get_dir "$t")"
  echo "→ 安装到 [$t] $dest"
  mkdir -p "$dest"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete \
      --exclude '.git' \
      --exclude 'workspace' \
      --exclude '.DS_Store' \
      "$SOURCE_DIR/" "$dest/$SKILL_NAME/"
  else
    rm -rf "$dest/$SKILL_NAME"
    cp -R "$SOURCE_DIR" "$dest/$SKILL_NAME"
    rm -rf "$dest/$SKILL_NAME/.git" "$dest/$SKILL_NAME/workspace"
  fi
  installed="$installed $t"
done

# ---- 清理临时目录 ----
[ -n "$TMP_DIR" ] && rm -rf "$TMP_DIR"

# ---- 结果 ----
echo ""
echo "✔ 安装完成，已装到：$installed"
echo ""
echo "  重启你的 AI 工具，然后直接说一句话即可触发："
echo "    「帮我找方向」  或  「评估这个 JD」"
echo "  无需记命令，AI 会识别并自动调用。"
