# 38 队逆向档案（对手牌组还原）

> **还原方法**：每队日志 → 归一化起手 + 同名卡 ≤4 / ACE ≤1 / ≥1 基础宝可梦三条公开规则约束，
> 还原到 **58/60 张，约 10 秒/队**；同名卡靠招式名反查。数据：`data/opponents_decks.json`。
>
> **换阵判定（两级）**：
> - **结构性换阵** = 前/后两段主力体系不同（如 毒系 → Dragapult）；
> - **卡位微调** = 体系不变、个别卡数量调整（判定为「否」，附 Jaccard 相似度表示幅度）；
> - **样本不足** = 该队只有单段日志（10 支），不做换阵判定。

| 队伍 | 名次 | 积分 | 早期体系 | 后期体系 | 相似度 | 结构性换阵 | 后期核心（前 5） |
|---|---:|---:|---|---|---:|:--:|---|
| 对对对队 | 1 | 5409 | Hop's一击 | Hop's一击 | 0.74 | 否 | 4×Hop's Phantump / 4×Hop’s Bag / 4×Poké Pad / 4×Hop’s Choice Band / 4×Lillie's Determination |
| SSS | 10 | 4096 | Dragapult | Dragapult | 0.89 | 否 | 6×Basic {R} Energy / 4×Buddy-Buddy Poffin / 4×Crispin / 4×Dreepy / 4×Lillie's Determination |
| 狗熊岭群区闪耀之时 | 11 | 3914 | MegaLucario | 其它 | 0.30 | 是 | 6×Basic {G} Energy / 4×Switch / 4×Hilda / 4×Mega Lopunny ex / 4×Hop’s Choice Band |
| 牛马面包 | 12 | 3713 | MegaLucario | MegaLucario | 0.83 | 否 | 10×Basic {F} Energy / 4×Carmine / 4×Lillie's Determination / 4×Poké Pad / 4×Rock Fighting Energy |
| 老实写代码，很枯燥吧 | 13 | 3637 | 其它 | Dragapult | 0.12 | 是 | 4×Drakloak / 4×Poké Pad / 4×Crispin / 4×Rare Candy / 4×Dragapult ex |
| 睡着觉把题都做对 | 14 | 3434 | MegaLucario | MegaLucario | 0.79 | 否 | 15×Basic {F} Energy / 4×Mega Lucario ex / 4×Lillie's Determination / 4×Cheren / 4×Judge |
| Spirit | 15 | 3428 | Alakazam | Alakazam | 0.82 | 否 | 8×Basic {P} Energy / 4×Abra / 4×Xerosic’s Machinations / 4×Dawn / 4×Dudunsparce |
| 大狗队 | 16 | 2708 | Alakazam | Alakazam | 1.00 | 否 | 6×Basic {P} Energy / 4×Xerosic’s Machinations / 4×Dawn / 4×Hilda / 4×Kadabra |
| 奶蛙打牌智能体 | 17 | 2696 | Dragapult | Dragapult | 0.72 | 否 | 7×Basic {P} Energy / 4×Rare Candy / 4×Duskull / 4×Crispin / 4×Dreepy |
| 谁是大明星队 | 18 | 2564 | MegaLucario | Alakazam | 0.00 | 是 | 6×Basic {P} Energy / 4×Poké Pad / 4×Hilda / 4×Dawn / 4×Telepath Psychic Energy |
| 全对不秃头 | 19 | 2324 | Alakazam | Alakazam | 0.63 | 否 | 9×Basic {P} Energy / 4×Boss’s Orders / 4×Rare Candy / 4×Abra / 3×Hilda |
| 咪咪汪汪队 | 2 | 5215 | Alakazam | Alakazam | 1.00 | 否 | 4×Buddy-Buddy Poffin / 4×Kadabra / 4×Dawn / 4×Enhanced Hammer / 4×Xerosic’s Machinations |
| 我说的都队 | 20 | 2238 | MegaLucario | MegaLucario | 0.93 | 否 | 11×Basic {F} Energy / 4×Riolu / 4×Cheren / 4×Hitmontop / 4×Fighting Gong |
| 我有仁义礼智信 | 21 | 2206 | 草系 | 草系 | 0.71 | 否 | 19×Basic {G} Energy / 4×Night Stretcher / 4×Cheren / 4×Lillie's Determination / 4×Teal Mask Ogerpon ex |
| 起床困难队 | 22 | 2042 | 草系 | 草系 | 0.75 | 否 | 11×Basic {G} Energy / 6×Basic {L} Energy / 4×Crispin / 4×Teal Mask Ogerpon ex / 4×Raging Bolt ex |
| 我和梁圣站一队 | 23 | 1433 | MegaLucario | MegaLucario | 0.60 | 否 | 21×Basic {F} Energy / 4×Urbain / 4×Pokégear 3.0 / 4×Mega Kangaskhan ex / 4×Riolu |
| 阿帕茨 | 24 | 1356 | MegaLucario | MegaLucario | 0.88 | 否 | 8×Basic {F} Energy / 4×Urbain / 4×Ultra Ball / 4×Billy & O'Nare / 4×Riolu |
| 站中间混两边 | 25 | 1216 | 草系 | 草系 | 0.87 | 否 | 18×Basic {F} Energy / 4×Koraidon ex / 4×Cyrano / 4×Ultra Ball / 3×Billy & O'Nare |
| 11111 | 25 | 790 | MegaLucario | — | — | 样本不足 | — |
| bug hunter | 26 | 1045 | 其它 | 其它 | 1.00 | 否 | 17×Basic {R} Energy / 4×Gouging Fire ex / 4×Reshiram ex / 4×Judge / 4×Boss’s Orders |
| 1111 | 26 | 756 | Alakazam | — | — | 样本不足 | — |
| 奶卷打牌智能体 | 27 | 900 | 其它 | 其它 | 0.88 | 否 | 8×Basic {F} Energy / 4×Boss’s Orders / 4×Fan Rotom / 4×Zangoose ex / 4×Ultra Ball |
| 1111111 | 27 | 754 | MegaLucario | — | — | 样本不足 | — |
| 都挺好 | 28 | 852 | 其它 | 其它 | 1.00 | 否 | 28×Basic {P} Energy / 4×Switch / 4×Team Rocket's Mewtwo ex / 4×Pokégear 3.0 / 4×Mega Gardevoir ex |
| 111 | 29 | 664 | MegaLucario | — | — | 样本不足 | — |
| 重生之我要起个响亮的队名 | 3 | 5182 | 草系 | 草系 | 0.50 | 否 | 17×Basic {G} Energy / 4×Ultra Ball / 4×Bug Catching Set / 4×Teal Mask Ogerpon ex / 4×Applin |
| 111111 | 30 | 631 | Alakazam | — | — | 样本不足 | — |
| 奶娃 | 32 | 588 | Alakazam | — | — | 样本不足 | — |
| 牛来 | 33 | 568 | Alakazam | — | — | 样本不足 | — |
| hetui | 34 | 557 | Alakazam | — | — | 样本不足 | — |
| null | 35 | 530 | Alakazam | — | — | 样本不足 | — |
| 妈妈告诉我只要名字起的够长总会有人念完对不队 | 38 | 200 | 其它 | — | — | 样本不足 | — |
| 山里灵活的狗 | 4 | 4987 | Crustle墙 | Crustle墙 | 0.76 | 否 | 12×Basic {G} Energy / 4×Buddy-Buddy Poffin / 4×Waitress / 4×Grow Grass Energy / 4×Dwebble |
| 坐巴士要排队 | 5 | 4840 | Dragapult | Dragapult | 0.74 | 否 | 4×Drakloak / 4×Ultra Ball / 4×Dreepy / 4×Crushing Hammer / 4×Lillie's Determination |
| 往里区队 | 6 | 4689 | MegaLucario | MegaLucario | 0.92 | 否 | 15×Basic {F} Energy / 4×Premium Power Pro / 4×Carmine / 4×Solrock / 4×Fighting Gong |
| 格鲁 | 7 | 4587 | Alakazam | Alakazam | 0.89 | 否 | 4×Abra / 4×Xerosic’s Machinations / 4×Poké Pad / 4×Kadabra / 4×Rare Candy |
| 不说对不队 | 8 | 4460 | Alakazam | Alakazam | 0.68 | 否 | 4×Poké Pad / 4×Telepath Psychic Energy / 4×Rare Candy / 4×Buddy-Buddy Poffin / 4×Enhanced Hammer |
| 食堂不要插队 | 9 | 4149 | Crustle墙 | Crustle墙 | 0.71 | 否 | 15×Basic {G} Energy / 4×Budew / 4×Mega Lopunny ex / 4×Lillie's Determination / 4×Buneary |

## 统计

- 还原完成：**38 队**；其中 **28 队**有前后两段日志，可判定换阵
- **结构性换阵 3 队**：狗熊岭群区闪耀之时（MegaLucario→其它）、老实写代码，很枯燥吧（其它→Dragapult）、谁是大明星队（MegaLucario→Alakazam）
- 其余双段队伍：体系不变，仅卡位调整（相似度多在 0.70–0.95）
- 单段队伍 10 支：标记「样本不足」，不参与换阵统计
- 我方（对对对队）在档案中：还原结果与 `submission/deck.md` 一致性可人工核对

## 与报告 §4.4「6 支换阵台账」的口径差异

同一批日志用两种口径会得到不同计数，这里写清楚，避免数字打架：

| 口径 | 判定方式 | 结果 |
|---|---|---|
| **机器判定（本文档）** | 前后两段各取出现 ≥2 次的卡名集合，Jaccard < 0.70 记为变动；体系变了记为「结构性换阵」 | 结构性换阵 **3 支**；同体系大幅卡位调整 **4 支**；合计 **7 支** |
| **人工台账（报告 §4.4）** | 逐队对照卡表，只要出现**关键道具/支援者**的增删（如 Battle Cage、Xerosic、Budew）即记为换阵 | **6 支** |

差异来源：10 局/段的样本里，只加 2–3 张道具的队伍 Jaccard 仍在 0.70 以上，
机器判定不会触发；而人工核对能直接看到卡表变化。两种口径互补：
**机器口径抓「体系级」变动，人工台账抓「道具级」针对**。
