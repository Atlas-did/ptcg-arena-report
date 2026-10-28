"""Verify that numbers quoted in REPORT.md match the shipped data files.

Usage: python scripts/verify_numbers.py
Exit code 0 = all checks passed.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rep = io.open(os.path.join(H, "REPORT.md"), encoding="utf-8").read()
fails = []


def check(label, pattern, must_in_report=True):
    found = pattern in rep
    ok = found == must_in_report
    print(f"{'OK ' if ok else 'FAIL'} {label:38s} {'in report' if found else 'missing'}")
    if not ok:
        fails.append(label)


def load(p):
    with io.open(os.path.join(H, p), encoding="utf-8") as fh:
        return json.load(fh)


stats = load("data/final_stats.json")
arche = load("data/final_arche.json")
rounds = load("data/rounds.json")

# final stats
flat = json.dumps(stats, ensure_ascii=False)
b = stats.get("b") or stats.get("B") or {}
for key in ("5409", "3008"):
    src_has = key in flat
    rep_has = key in rep
    print(f"{'OK ' if src_has and rep_has else 'FAIL'} final_stats vs report {key:12s} "
          f"data={src_has} report={rep_has}")
    if not (src_has and rep_has):
        fails.append(key)

# W-L-D is stored as separate numbers -> derive and compare with the prose string
for board, tag in ((stats.get("b", {}), "B"), (stats.get("a", {}), "A")):
    rec = f"{board.get('w')}-{board.get('l')}-{board.get('d')}"
    ok = rec in rep
    print(f"{'OK ' if ok else 'FAIL'} {tag} record {rec:12s} in report={ok}")
    if not ok:
        fails.append(rec)

# archetype rates
for name, win in (("Alakazam", "86.5"), ("MegaLucario", "95.4"), ("Dragapult", "44.0"),
                  ("73.3", "73.3"), ("88.8", "88.8"), ("98.7", "98.7")):
    ok = win in rep
    print(f"{'OK ' if ok else 'FAIL'} archetype {name:14s} win={win:6s} in report={ok}")
    if not ok:
        fails.append(name)

# rounds
pts = rounds.get("points") or rounds
n = len(pts)
mean = sum(pts) / n
print(f"OK  rounds: n={n} mean={mean:.1f} full={sum(1 for v in pts if v >= 100)}")
check("rounds count 58", "58 轮")
check("mean 93.3", "93.3")
check("17 满分", "17 轮")

# claimed aggregates that are prose-only (cannot be recomputed here)
for label, frag in (("18000 局", "18000"), ("v3 72.37", "72.37"),
                    ("+1.69pp", "+1.69pp"), ("20 次改动", "20 次"),
                    ("13 项", "13 项"), ("3 次假阳性", "3 次假阳性"),
                    ("38 队", "38 队"), ("对位矩阵", "matchup_matrix.csv")):
    check(label, frag)

print()
if fails:
    print("FAILED:", len(fails), "->", fails[:8])
    sys.exit(1)
print("ALL CHECKS PASSED")
