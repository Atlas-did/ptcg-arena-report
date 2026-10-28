# 交付清单（2026-10-28）

## 1. 交付物一览

| # | 交付物 | 位置 | 说明 |
|---|---|---|---|
| 1 | 策略报告（Markdown） | `REPORT.md` | 584 行，11 节 + §4.5 对位矩阵 + 附录 A–D |
| 2 | 策略报告（PDF） | `REPORT.pdf` | A4 / 约 20 页 / 1.1 MB，4 图内嵌 |
| 3 | 仓库入口 | `README.md` | 成绩、90 秒速读、4 图预览、目录结构 |
| 4 | 最终牌组 | `submission/deck.md` / `deck.csv` | 60 张，20 种，含卡 ID 与合法性校验 |
| 5 | 最终 agent | `submission/main.py` | v3（submission 622） |
| 6 | 提交包 | `submission/submission_v3.tar.gz` | 与平台 submission 622 一致 |
| 7 | 数据（逐轮/榜单/体系/对手牌组/台账） | `data/` | 9 个文件，含 `matchup_matrix.csv` |
| 8 | 研究记录 | `docs/OPPONENTS_FULL_RE.md` | 38 队逆向 + 20 次实验全记录（62KB） |
| 9 | 规则与评分口径 | `docs/RULES_AND_SCORING.md` | 每轮局数、积分规则、报告权重 |
| 10 | 本地池复刻研究 | `docs/POOL_REPLICATION.md` | 六体系保真度与偏差 |
| 11 | 上传审计 | `docs/AUDIT.md` | 含什么/不含什么/风险提示 |
| 12 | 修订记录 | `docs/CHANGELOG.md` | v3.0 → v3.3 |
| 13 | 复现脚本 | `scripts/` | 监控、逆向、校验、上传、图表、数字核对 |
| 14 | 配图 | `docs/figures/` | fig1–fig4（逐轮得分/六体系/版本对比/榜单前 10） |

## 2. 关键数字（可在仓库内自证）

| 项 | 值 | 数据来源 |
|---|---|---|
| B 榜 | 5409 分 · 58 轮 · 第 1（领先 194） | `data/final_stats.json`、`data/leaderboard_b_r94.csv` |
| B 榜战绩 | 1286-277-3（w/l/d 字段推导） | `data/final_stats.json` |
| B 榜胜率 | 82.2%（1566 局） | `data/final_arche.json` |
| 六体系胜率 | 86.5 / 95.4 / 98.7 / 73.3 / 44.0 / 88.8 | `data/final_arche.json` |
| A 榜 | 3008 分 · 34 轮 · 第 2 | `data/final_stats.json` |
| 版本对比 | W 70.68 / v2 72.17 / v3 72.37（18000 局） | 报告 §6.4 + `data/` |
| 实验台账 | 20 次 · 13 项收敛 · 0 通过 · 3 次假阳性 | `data/实验台账20次.csv` |
| 逆向 | 38 队 · 58/60 张 · 10 秒/队 | `data/opponents_decks.json` |

## 3. 数字一致性校验

```bash
python scripts/verify_numbers.py
# 输出：ALL CHECKS PASSED（22 项）
```

校验内容：`REPORT.md` 中引用的每个关键数字必须能在 `data/` 里找到对应数据（含由 w/l/d 推导的战绩串），
避免"报告写了但数据没有"。

## 4. 提交状态（比赛后台）

| id | 时间 | 内容 | 格式 | 状态 |
|---|---|---|---|---|
| 17 | 2026-10-28 11:40 | `.../blob/main/REPORT.md` | markdown | submitted |
| 16 | 2026-10-28 10:26 | 仓库首页 | link | submitted |
| 15 | 2026-10-28 10:26 | 仓库首页 | markdown | submitted |

生效提交：**submission 622（v3，active）**。评分字段尚未出分（`score_stability` / `score_originality` 为 null）。

## 5. 复现路径（评审最短路径）

```bash
git clone https://github.com/Atlas-did/ptcg-arena-report.git
cd ptcg-arena-report

# 1) 校验报告数字与数据一致
python scripts/verify_numbers.py

# 2) 校验最终牌组合法性（离线，无需账号）
python scripts/deck_check.py submission/deck.csv data/cards.csv

# 3) 看报告
open REPORT.pdf          # 或 REPORT.md
```

## 6. 未包含 / 不上传

| 项 | 原因 |
|---|---|
| 平台账号密码 | 只走 `PTCG_USER` / `PTCG_PASS` 环境变量 |
| `eval/`、`vendor/`（约 2 GB） | 本地陪练池与训练数据 |
| 原始对局日志 | 含他人对局细节 + 体积大 |
| 答辩 PPT / 视频 | 与本仓库（策略报告）目标无关 |

## 7. 待办（下一轮）

1. 真实榜单页截图（需浏览器登录后台）
2. 若评分仍在进行：评估把 `submission/`（可运行实现）临时移出公开仓库
3. 报告可再压缩一版「5 页评审版」
