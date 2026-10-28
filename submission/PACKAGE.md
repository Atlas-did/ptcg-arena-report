# Final submission package (id 622)

This folder contains the exact card list and agent used for the final B-board
submission. The platform accepts a `submission.tar.gz` with two files:

```
submission.tar.gz
├── main.py    # agent(obs_dict) -> list[int]
└── deck.csv   # exactly 60 lines, one card id per line
```

## Files

| File | Notes |
|---|---|
| `main.py` | v3 agent: role-based value function + legality guards. Standard library only. |
| `deck.csv` | 60 card ids, the final Hop's Trevenant list. |
| `deck.md` | Human-readable deck list, counts and role notes. |
| `submission_v3.tar.gz` | Archived copy of the uploaded package. |
| `SHA256SUMS` | Checksums for `main.py`, `deck.csv` and the tar.gz. |

## Verify

```bash
python scripts/deck_check.py submission/deck.csv data/cards.csv
tar -tzf submission.tar.gz
```

Expected output: `OK: 60 cards / same-name <= 4 / ACE <= 1 / Basic Pokemon present`.

## Rebuild

```bash
cd submission
tar -czf ../submission.tar.gz main.py deck.csv
```

The agent is deterministic and only reads the public observation. It does not
use the file system, network or any third-party package at play time.

## Provenance

Archived locally as `dist/submission_v3.tar.gz` and uploaded as submission
`622` (`status=active`). The platform reports the same filename and the deck
matches the 60-card list in `deck.csv`.
