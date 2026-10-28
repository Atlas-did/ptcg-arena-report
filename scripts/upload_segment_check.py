"""Segment check: our win rate before vs after a given round, per archetype.

Used right after an upload: pick the round the new version went live (`--since`),
and this compares the two windows on the live board, which is the only field truth.
"""
import argparse
import collections
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from bot_farm import login, call  # noqa: E402

OURS = 39
MARK = [
    ("Dragapult", ["Dragapult", "Drakloak", "Dreepy"]),
    ("Crustle墙", ["Crustle", "Dwebble"]),
    ("Alakazam", ["Alakazam", "Kadabra", "Abra"]),
    ("MegaLucario", ["Mega Lucario", "Riolu", "Solrock"]),
    ("草系", ["Ogerpon", "Meganium", "Baylin", "Applin", "Dipplin"]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", type=int, required=True, help="first round of the new version")
    ap.add_argument("--window", type=int, default=8, help="rounds on each side")
    args = ap.parse_args()

    recon = json.load(open(os.path.join(ROOT, "eval", "recon", "opponents_decks.json"), encoding="utf-8"))

    def arche(tid):
        e = recon.get(str(tid)) or {}
        late = (e.get("decks") or {}).get("late") or (e.get("decks") or {}).get("early")
        if not late:
            return "unknown"
        names = " ".join(c["name"] for c in late["cards"])
        best, hits = "other", 0
        for label, keys in MARK:
            h = sum(1 for k in keys if k in names)
            if h > hits:
                best, hits = label, h
        return best

    tok = login(os.environ["PTCG_USER"], os.environ["PTCG_PASS"])
    ms = [m for m in call("/matches", tok) if OURS in (m["player_a"], m["player_b"])]
    lo, hi = args.since - args.window, args.since + args.window
    agg = {"before": collections.defaultdict(lambda: [0, 0]),
           "after": collections.defaultdict(lambda: [0, 0])}
    for m in ms:
        rn = m.get("round_no", 0)
        if not (lo <= rn < args.since or args.since <= rn <= hi):
            continue
        opp = m["player_b"] if m["player_a"] == OURS else m["player_a"]
        won = (m["winner"] == "a") == (m["player_a"] == OURS)
        seg = "before" if rn < args.since else "after"
        a = arche(opp)
        agg[seg][a][0] += 1 if won else 0
        agg[seg][a][1] += 1

    print(f"window R{lo}-R{hi}; split at R{args.since}")
    print(f"{'archetype':<12}{'before':>14}{'after':>14}{'delta':>9}")
    keys = set(agg["before"]) | set(agg["after"])
    for a in sorted(keys):
        w1, n1 = agg["before"][a]
        w2, n2 = agg["after"][a]
        r1 = w1 / n1 if n1 else 0
        r2 = w2 / n2 if n2 else 0
        print(f"{a:<12}{f'{w1}/{n1} {r1:.0%}':>14}{f'{w2}/{n2} {r2:.0%}':>14}"
              f"{(r2 - r1) * 100 if n1 and n2 else 0:>8.1f}pp")


if __name__ == "__main__":
    main()
