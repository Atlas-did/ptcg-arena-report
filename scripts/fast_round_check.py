"""Fast single-round check: R{since} vs the previous 8 rounds, per archetype."""
import collections
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from bot_farm import login, call  # noqa: E402

OURS = int(os.environ.get("PTCG_TEAM_ID", "39"))
MARK = [("Dragapult", ["Dragapult", "Drakloak", "Dreepy"]),
        ("CrustleWall", ["Crustle", "Dwebble"]),
        ("Alakazam", ["Alakazam", "Kadabra", "Abra"]),
        ("MegaLucario", ["Mega Lucario", "Riolu", "Solrock"]),
        ("Grass", ["Ogerpon", "Meganium", "Applin", "Dipplin"])]


def load_recon():
    path = os.path.join(ROOT, "data", "opponents_decks.json")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def arche(recon, tid):
    e = recon.get(str(tid)) or {}
    late = (e.get("decks") or {}).get("late") or (e.get("decks") or {}).get("early") or {}
    names = " ".join(c["name"] for c in late.get("cards", []))
    best, hits = "other", 0
    for label, keys in MARK:
        h = sum(1 for k in keys if k in names)
        if h > hits:
            best, hits = label, h
    return best


def main():
    since = int(sys.argv[1]) if len(sys.argv) > 1 else 85
    recon = load_recon()
    tok = login(os.environ["PTCG_USER"], os.environ["PTCG_PASS"])
    ms = [m for m in call("/matches", tok) if OURS in (m["player_a"], m["player_b"])]
    cur = collections.defaultdict(lambda: [0, 0])
    base = collections.defaultdict(lambda: [0, 0])
    for m in ms:
        rn = m.get("round_no", 0)
        opp = m["player_b"] if m["player_a"] == OURS else m["player_a"]
        won = (m["winner"] == "a") == (m["player_a"] == OURS)
        a = arche(recon, opp)
        if rn == since:
            cur[a][0] += 1 if won else 0
            cur[a][1] += 1
        elif since - 8 <= rn <= since - 1:
            base[a][0] += 1 if won else 0
            base[a][1] += 1

    print(f"round {since} vs previous 8 rounds")
    print(f"{'archetype':<12}{'R-since':>12}{'baseline':>14}")
    for a in sorted(set(cur) | set(base)):
        w1, n1 = cur.get(a, [0, 0])
        w2, n2 = base.get(a, [0, 0])
        print(f"{a:<12}{f'{w1}/{n1}':>12}{f'{w2}/{n2} {w2 / max(1, n2):.0%}':>14}")
    tw = sum(v[0] for v in cur.values())
    tn = sum(v[1] for v in cur.values())
    bw = sum(v[0] for v in base.values())
    bn = sum(v[1] for v in base.values())
    print(f"{'TOTAL':<12}{f'{tw}/{tn} {tw / max(1, tn):.0%}':>12}{f'{bw}/{bn} {bw / max(1, bn):.0%}':>14}")


if __name__ == "__main__":
    main()
