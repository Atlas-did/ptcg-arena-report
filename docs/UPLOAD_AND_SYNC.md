# 上传与同步说明（2026-10-28）

## 1. 当前状态

| 位置 | commit | 说明 |
|---|---|---|
| GitHub `main` | 以 GitHub 页面为准 | **权威版本**，已包含本次全部修订、新文件与本文档 |
| 本地 `repo_策略报告` | `511881e` | 在 `dd91bba` 上多了本文档；未 push 成功 |

本地 `git push` 失败的原因不是权限，而是本机代理把 `github.com` 的 TLS 握手掐断了
（`api.github.com` 正常，`github.com` 报 `unexpected eof`）。
本次是用 GitHub API（blobs → tree → commit → ref）直接更新远端的，所以 **GitHub 上是对的**。

> 本文档不锁定远端 commit 号：上传过程中已经产生过多次 API commit，之后如再更新，
> 以 GitHub 页面显示的 `main` 为准。

## 2. 本次改了什么

### 2.1 事实修正（不改比赛结果）

| # | 初版 | 本版 |
|---|---|---|
| 1 | 每轮 8 局、按胜场积分 | 单循环 27 局/轮、按名次 100→10 积分 |
| 2 | 牌组表 56 张、Pokégear 4 | 按 `submission/deck.csv` 重列 60 张 |
| 3 | Corner 130 基础 / Crustle 110HP | Corner 90→180；Horrifying Revenge 220 为条件值；Crustle 150HP |
| 4 | v3 vs v2 写 z≈3.5 | v3 vs v2 z=0.28；z≈3.5 是 v3 vs 基线 W |
| 5 | 「20 次有统计功效」 | 「20 次改动，13 项可判定否定」 |
| 6 | 「卡池绝对无解」 | 「非 ex 约束下无解」；Zacian/Cape 的代价写清 |

### 2.2 新增文件

- `submission/`：最终 v3 `main.py`、`deck.csv`、`deck.md`、`submission_v3.tar.gz`、`SHA256SUMS`
- `data/cards.csv`：卡池 1267 张
- `data/leaderboard_b_r94.csv`、`data/leaderboard_a_r36.csv`、`data/team_submissions.csv`
- `data/README.md`：数据口径与来源
- `docs/RULES_AND_SCORING.md`：官方赛制/积分/组牌/评分
- `scripts/bot_farm.py`、`scripts/deck_check.py`：补齐复现脚本依赖
- `.gitignore`、`requirements.txt`

### 2.3 修复

- `data/baseline_r73_76.json`、`data/final_arche.json` 原来是 GBK，已转 UTF-8。
- `scripts/*.py` 的 `eval/recon/` 路径改为 `data/opponents_decks.json`，并去掉硬编码 `D:\`。
- 复现脚本统一从 `PTCG_USER` / `PTCG_PASS` 读凭据，不把账号写进文件。

## 3. 本地怎么同步到远端

先确认本地没有未提交改动：

```bash
git status
```

然后二选一：

### 方案 A：网络恢复后重新拉取（推荐）

```bash
# 先确认 github.com 能通
git ls-remote origin HEAD

git fetch origin
git reset --hard origin/main
git status
```

> 本地 `dd91bba` 与远端内容一致，只是行尾不同；`reset --hard` 会丢掉本地这个 commit，
> 但不会丢文件内容。如果本地还有别的未提交改动，先 `git stash`。

### 方案 B：改用 SSH

```bash
git remote set-url origin git@github.com:Atlas-did/ptcg-arena-report.git
git fetch origin
git reset --hard origin/main
git push -u origin main
```

需要本机已配置 GitHub SSH key。

### 方案 C：继续用 API

本次的 API 流程是：

1. `POST /git/blobs`（每个文件）
2. `POST /git/trees`（`base_tree` + 变更文件）
3. `POST /git/commits`（`tree` + `parents`）
4. `PATCH /git/refs/heads/main`（`sha` + `force`）

适合“只改少量文件、git push 又不通”的情况；日常维护还是建议修好代理后用 A/B。

## 4. 上传清单

### 应该上传

```text
README.md
REPORT.md
LICENSE
requirements.txt
.gitignore
submission/
data/                    （cards.csv、榜单快照、逐轮数据、对手牌组、实验台账）
docs/                    （报告研究记录、规则、本文档）
scripts/                 （监控/逆向/校验/打包）
```

### 不要上传

- **账号、密码、token、学号、姓名、邮箱**：只走环境变量。
  本机 `data/full20261022*/03_对话记录.md` 含平台账号密码，**绝对不要放进来**。
- **本地大文件**：`eval/`（约 752 MB）、`vendor/`（269 MB）、`deck_html/`（408 MB）、
  `dist/` 的 PDF/PPTX/MP4、模型权重、卡图素材。
- **第三方代码/受限素材**：`vendor/` 下的他人仓库、PPT 模板、ComfyUI 模型。
- **缓存/临时文件**：`__pycache__/`、`*.obj`、`~$*.pptx`、`.env`、嵌套 `.git`。

### 需要你确认的两件事

1. `data/opponents_decks.json` 含**公开榜单上的队伍名**（来自公开日志逆向）。
   如果不想公开队名，可以改成匿名 ID；但会削弱“38 队逆向”的可核验性。
2. GitHub commit 历史里的作者邮箱（已脱敏；如需公开请改用 noreply 邮箱）。
   如果不想公开，需要 `git filter-repo` 重写历史 + 强推；本仓库没有做这一步。

## 5. 复核命令

```bash
# 牌组合法性
python scripts/deck_check.py submission/deck.csv data/cards.csv

# 脚本语法
python -m py_compile scripts/*.py submission/main.py

# 数据可解析
python - <<'PY'
import json, glob
for f in glob.glob("data/*.json"):
    json.load(open(f, encoding="utf-8"))
print("json ok")
PY
```

## 6. 维护注意

- `report/build_report.py` 现在会检测 `repo_策略报告/.git`，默认**拒绝**重建仓库；
  只有显式加 `--force` 才会覆盖。不要在没有重新同步 `report/part*.md` 的情况下运行。
- 本仓库是**策略报告**，不是官方代码库；`submission/main.py` 仅用于复现最终提交。
- 报告里所有数字以 `data/` 和平台 R94 快照为准；平台若继续跑 R95+，名次需要重新核对。
