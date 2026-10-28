# 数据说明

所有数据来自 PTCG-Arena 官方接口 / 公开对局日志，未包含账号、密码、学号等个人信息。

| 文件 | 内容 | 来源 |
|---|---|---|
| `final_stats.json` | B/A 榜汇总（分数、轮次、胜负平、均分、满分轮） | `/api/leaderboard/{a,b}`，R94 快照 |
| `rounds.json` | B 榜 58 轮逐轮积分、胜场、负场 | 同上 |
| `final_arche.json` | 六体系场况占比 / 我方胜率 / 胜负场 | 1566 局逐局归档 |
| `behaviour.json` | 六体系行为节奏（攻击/局、出牌/局、主力招式） | 每队 6 局抽样 |
| `opponents_decks.json` | 38 支队伍（B 榜 28 队与 A 榜 38 队去重后）牌组还原 | 官方 `/matches/{id}/log` 开局抽牌 |
| `baseline_r73_76.json` | R73–R76 分体系胜负基线 | 逐轮日志 |
| `实验台账20次.csv` | 20 次改动的结构化台账 | 本地/场况实验记录 |
| `leaderboard_b_r94.csv` | B 榜 28 队最终快照（截至 R94） | `/api/leaderboard/b` |
| `leaderboard_a_r36.csv` | A 榜 38 队快照（截至 A 榜最新已结算轮） | `/api/leaderboard/a` |
| `team_submissions.csv` | 本队 28 次提交记录（id / 文件名 / 状态 / 时间） | `/api/submissions` |
| `cards.csv` | 卡池 1267 张（id / 名称 / 类型 / HP / 招式 / 效果文本） | 平台 `/api/cards/csv` |

## 口径

- **占比**按 B 榜 1566 局计算，四舍五入到整数百分比，因此合计可能为 99% 或 101%。
- **胜率** = 胜 /（胜 + 负 + 平）；报告正文的 82.2% 为 1286 / 1566。
- **积分**是每轮名次分（100 → 10）之和，不是胜场数。
- **pp** = percentage point（百分点）；**z** = 两比例差的标准化统计量。
- `opponents_decks.json` 只用于公开日志的战术分析；队伍名本身来自公开排行榜。

## 复现

```bash
export PTCG_USER=...   # 平台账号（不要提交到仓库）
export PTCG_PASS=...
python scripts/monitor.py
python scripts/recon_all.py
python scripts/fast_round_check.py 94
python scripts/upload_segment_check.py --since 77
```
