"""Compact standing monitor: rank, lead, recent rounds, per-archetype rate, flags."""
import collections
import json
import os
import sys
import urllib.request

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
    ("草系", ["Ogerpon", "Meganium", "Applin", "Dipplin"]),
]
RECENT = 6


def main():
    board = json.loads(urllib.request.urlopen("http://115.159.47.81/api/leaderboard/b", timeout=40).read().decode())
    me = next(r for r in board["rows"] if "对对对" in r["team_name"])
    rows = [(x["round_no"], x["points"]) for x in me["rounds"]]
    print(f"B board  latest R{board['latest_round']}  next R{board.get('next_round')}")
    print(f"we: rank {me['rank']}  total {me['total_points']}  rounds {len(rows)}")
    recent = rows[-RECENT:]
    print(f"last {RECENT}: " + " ".join(f"R{r}:{p}" for r, p in recent)
          + f"   mean {sum(p for _, p in recent) / len(recent):.1f}")

    others = sorted(board["rows"], key=lambda r: -r["total_points"])[1:4]
    for r in others:
        pts = [x["points"] for x in r["rounds"]]
        gap = me["total_points"] - r["total_points"]
        print(f"  #{r['rank']} {r['team_name'][:16]:<18}{r['total_points']:>6}  gap {gap:>+4}"
              f"  last{RECENT} {sum(pts[-RECENT:]) / len(pts[-RECENT:]):.1f}")

    lead = me["total_points"] - others[0]["total_points"]
    if lead < 0:
        print("FLAG: we are no longer first")
    elif lead < 60:
        print(f"FLAG: lead down to {lead} (a single bad round is ~-10)")

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
    since = board["latest_round"] - 11
    agg = collections.defaultdict(lambda: [0, 0])
    for m in ms:
        if m.get("round_no", 0) < since:
            continue
        opp = m["player_b"] if m["player_a"] == OURS else m["player_a"]
        won = (m["winner"] == "a") == (m["player_a"] == OURS)
        a = arche(opp)
        agg[a][0] += 1 if won else 0
        agg[a][1] += 1
    print(f"\nlast 12 rounds by archetype (R{since}+):")
    for a, (w, n) in sorted(agg.items(), key=lambda kv: -kv[1][1]):
        flag = "  <-- watch" if (a in ("Dragapult", "Crustle墙") and w / max(1, n) < 0.6) else ""
        print(f"  {a:<12}{w:>3}/{n:<3} = {w / max(1, n):>5.0%}{flag}")


if __name__ == "__main__":
    main()
