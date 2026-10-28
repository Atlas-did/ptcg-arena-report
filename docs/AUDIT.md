# 上传审计（2026-10-28）

## 已上传（及其理由）

| 路径 | 大小 | 为什么传 |
|---|---:|---|
| `REPORT.md` / `REPORT.pdf` | 30KB / 963KB | 报告正文与打印版，评审直接看 |
| `README.md` | 8KB | 入口：成绩、图表、复现线索 |
| `docs/figures/*.png` | 4 张 | 报告配图 |
| `docs/OPPONENTS_FULL_RE.md` | 62KB | 38 队逆向与实验全记录（可核对性） |
| `docs/RULES_AND_SCORING.md` | 3KB | 赛制与评分口径 |
| `docs/POOL_REPLICATION.md` | 4KB | 本地池保真度研究 |
| `docs/UPLOAD_AND_SYNC.md` | 5KB | 上传清单与本地同步方法 |
| `data/*.json,csv` | ~300KB | 逐轮、分体系、榜单、对手牌组、实验台账 |
| `data/cards.csv` | 192KB | 官方卡牌表（1267 张），用于核对卡面数值 |
| `scripts/*.py` | 9 个 | 复现脚本（监控/逆向/校验/上传） |
| `submission/deck.md,csv` | 3KB | 最终 60 张牌组 |
| `submission/main.py` | 353KB | v3 agent 实现（可运行） |
| `submission/submission_v3.tar.gz` | 49KB | 最终提交包（submission 622） |

## 明确不上传

| 项 | 原因 |
|---|---|
| 平台账号 / 密码 / token | 只走 `PTCG_USER` / `PTCG_PASS` 环境变量 |
| `eval/`、`vendor/`（约 2GB） | 本地陪练池与训练数据，体积大且非必需 |
| `deck_html/`、`dist/`、`handover*/` | 答辩材料与中间产物，与本仓库目标无关 |
| 原始对局日志 | 含其他队伍对局细节，且体积大 |
| `__pycache__`、`.env`、日志 | 已在 `.gitignore` 排除 |

## 风险提示

1. **`submission/main.py` + `submission_v3.tar.gz`**：公开等于把可运行方案给其他队伍。
   若评分未结束，建议临时把仓库设为 Private，或改为「接口说明 + 牌组」而不含实现。
2. **git 历史作者邮箱**：已用 `filter-branch` 重写为 noreply（本地已验证）；
   若尚未 force-push 成功，远端历史里仍可能是旧邮箱。
3. 未包含身份证/学号等实名信息（未上传）。
