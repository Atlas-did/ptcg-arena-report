# PTCG-Arena 2026 策略报告 · 对对对队

> **B 榜第 1**（截至 R94：5409 分 / 1286-277-3 / 82.2%）　·　**A 榜第 2**（3008 分）
>
> 报告正文：**[REPORT.md](./REPORT.md)**（约 1.1 万字，含方法、数据与全部否定实验）
> 最终提交：**[submission/](./submission/)**（v3 agent + 60 张牌组）
> 赛制与评分：**[docs/RULES_AND_SCORING.md](./docs/RULES_AND_SCORING.md)**

---

## 一句话结论

**名次不是强度排序，而是规则闭环。** 我们用一个非主流的非 ex 攻击手体系，
吃到 70% 场况的 86–99% 胜率；唯一明显失分的 Dragapult 对位（44.0%）
是卡池层面的数值/规则问题，不是实现问题。

## 成绩（截至 B 榜 R94）

| 项 | 值 |
|---|---|
| B 榜 | 58 轮 · **5409 分 · 第 1**（领先第 2 名 194） |
| 战绩 | 1286 胜 277 负 3 平 · **82.2%**（1566 局） |
| 稳定性 | 17 轮满分 · 46 轮 ≥90 · 最差 R53 = 70，下一轮 97 |
| A 榜 | 34 轮已结算 · 3008 分 · 第 2（与格鲁同分） |
| 提交 | submission **622** · v3 · 本地 18000 局 72.37% |

> 平台 `/api/leaderboard/b` 仍显示 `latest_round=94`、`next_round=95`。
> 因此本报告对 R94 及之前负责，不把「第 1」写成不可变化的最终结论。

## 三个与直觉相反的结论

1. **前五名里三支队伍（Alakazam / 草系 / Crustle）被我们打到 73–89%**，
   唯一明显克制我们的 Dragapult 队伍只排第 5。
2. **Dragapult 44.0% 的根因是卡池数值**：`Phantom Dive 200` 一击必杀我们 140HP 的攻击手，
   而我们要两拳才能推掉 320HP 的 Dragapult ex；奖赏效率 0.5 vs 1.0。
3. **「证明没有更强版本」本身是方法**：20 次改动、13 项可判定的否定结论、
   3 次被复测抓回的假阳性，以及一套可复用的判据。

## 给评审的 3 分钟阅读路径

1. **REPORT §0**：不懂宝可梦也能读的 60 秒导读。
2. **REPORT §2 / §4 / §5 / §10**：牌组为什么这样配、场况怎么分布、死角在哪、结论是什么。
3. **docs/RULES_AND_SCORING.md**：官方赛制/积分/组牌/评分口径，以及本报告的数据快照。
4. **submission/deck.md**：60 张牌的逐张角色说明。

## 评审维度对照

官方规则页写明策略报告权重：**稳定性 30% + 独创性 30% + B 榜排名 40%**。

| 维度 | 本仓库证据 |
|---|---|
| 稳定性 30% | 58 轮 5409 分；17 轮满分；46 轮 ≥90；最差轮 70 且下一轮 97；分段均分 96.9 / 91.5 / 92.2 |
| 独创性 30% | 非 ex 攻击手体系；规则闭环解释；38 队牌组逆向；否定实验协议；本地池偏差校准 |
| B 榜排名 40% | 截至 R94 第 1，领先 194 分 |

## 仓库结构

```
REPORT.md                 策略报告正文（10 节 + 3 附录）
submission/
  main.py                 v3 agent（标准库，无外部依赖）
  deck.csv                最终 60 张牌组（逐行 cardId）
  deck.md                 逐张牌的角色说明
  submission_v3.tar.gz    归档的提交包（main.py + deck.csv）
  SHA256SUMS              三个文件的校验和
  PACKAGE.md              提交包格式与重建方式
data/
  final_stats.json        B/A 榜汇总
  rounds.json             58 轮逐轮得分
  final_arche.json        六体系场况/胜率/胜负场
  behaviour.json          六体系行为节奏
  opponents_decks.json    38 队牌组还原
  实验台账20次.csv        20 次改动台账
  cards.csv               卡池 1267 张（id/名称/HP/招式/效果）
  leaderboard_*.csv       榜单快照
  team_submissions.csv    本队 28 次提交记录（含 622）
  README.md               数据口径与来源
docs/
  RULES_AND_SCORING.md    赛制/积分/组牌/评分
  UPLOAD_AND_SYNC.md      上传/同步/不上传清单
  OPPONENTS_FULL_RE.md    38 队逆向 + 换阵台账 + 实验全过程
  POOL_REPLICATION.md     本地池复刻保真度研究
scripts/
  monitor.py              榜单/对位监控
  recon_all.py            从日志还原对手牌组
  fast_round_check.py     单轮 vs 前 8 轮
  upload_segment_check.py 场况分段验证
  deck_check.py           牌组合法性校验
  pack_candidate.py       打包 candidate
  bot_farm.py             API 客户端（读环境变量）
```

## 快速复现

```bash
# 0) 只读：校验最终牌组
python scripts/deck_check.py submission/deck.csv data/cards.csv

# 1) 需要平台账号（用环境变量，不要把密码写进仓库）
export PTCG_USER=...
export PTCG_PASS=...
python scripts/monitor.py
python scripts/recon_all.py
python scripts/fast_round_check.py 94
python scripts/upload_segment_check.py --since 77

# 2) 重建提交包
cd submission && tar -czf ../submission.tar.gz main.py deck.csv && cd ..
```

## 数据与伦理

- 所有对局数据来自官方排行榜与公开对局日志；不包含账号、密码、学号、手机号。
- 对手牌组是从**公开日志的开局抽牌**反推的，用于战术分析；队伍名本身来自公开榜单。
- 仓库不包含第三方卡图、PPT 素材、模型权重或本地大文件。
- 最终 agent 只读公开观测，不使用文件系统、网络或第三方包。

完整的上传/同步/不上传清单见 **[docs/UPLOAD_AND_SYNC.md](./docs/UPLOAD_AND_SYNC.md)**。

### 不提交什么

- **账号 / 密码 / 学号 / 邮箱**：平台的登录信息只走 `PTCG_USER` / `PTCG_PASS` 环境变量。
- **本地大文件**：`eval/`（约 752 MB）、`vendor/`（269 MB）、`deck_html/`（408 MB）、
  `dist/` 里的 PDF/PPTX/MP4、模型权重、卡图素材。
- **第三方代码与受限素材**：`vendor/` 下的他人仓库、PPT 模板、ComfyUI 模型。
- **缓存与临时文件**：`__pycache__/`、`*.obj`、`~$*.pptx`、`.env`。

## 修订记录（v3.1，2026-10-28）

在不改变任何比赛结果的前提下，修正了 4 处会影响可信度的表述：

1. **赛制**：由「每轮 8 局、按胜场积分」改为「单循环 27 局/轮、按名次 100→10 积分」。
2. **牌组表**：按 `submission/deck.csv` 重列 60 张（原表漏了 Hop's Bag / Buddy-Buddy Poffin / Switch / Xerosic，且误写 Pokégear 数量）。
3. **伤害模型**：`Corner 90 → 180`（Postwick +30 / Choice Band +30 / Snorlax +30），
   `Horrifying Revenge 130 → 220` 是**被击倒后的条件值**；Crustle 是 150HP 而不是 110HP。
4. **统计表述**：v3 vs v2 的 +0.19pp（z=0.28）没有显著差异；z≈3.5 是 v3 vs 基线 W。
   同时把「20 次有统计功效」改为「20 次改动，其中 13 项可判定为否定」。

## License

MIT。见 [LICENSE](./LICENSE)。
