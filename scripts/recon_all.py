"""Reconstruct every team's deck from official match logs (opening draws).

Two eras are tracked separately so a mid-season deck switch shows up as a diff.
Output: data/recon/opponents_decks.json
"""
import collections
import csv
import json
import os
import re
import sys
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from bot_farm import BASE, login, call  # noqa: E402

EARLY_MAX = int(os.environ.get("RECON_EARLY_MAX", 55))
PER_ERA = int(os.environ.get("RECON_PER_ERA", 12))
OUT = os.path.join(ROOT, "data", "recon")
os.makedirs(OUT, exist_ok=True)

DRAW = re.compile(r"^\s*([AB])\s.*?\u62bd\u5230\W*(.+?)\W*$")
ATK = re.compile(r"^\s*([AB])\s.*?\u4f7f\u7528\u62db\u5f0f\W*(.+?)\W*$")
TURN1 = re.compile(r"\u3010\u7b2c 1 \u56de\u5408")

cards = list(csv.DictReader(open(os.path.join(ROOT, "data", "cards.csv"), encoding="utf-8-sig")))
by_name = collections.defaultdict(list)
for r in cards:
    by_name[r["name"]].append(r)
id2name = {r["cardId"]: r["name"] for r in cards}


def attacks_of(card):
    return set(re.findall(r"\d+:([^(]+)\(", card["attacks"] or ""))


def pick_id(name, team_atks):
    cands = by_name.get(name) or []
    if not cands:
        return None
    if len(cands) == 1:
        return int(cands[0]["cardId"])
    best, hit = None, -1
    for c in cands:
        h = len(attacks_of(c) & team_atks)
        if h > hit:
            best, hit = int(c["cardId"]), h
    return best


def main():
    tok = login(os.environ["PTCG_USER"], os.environ["PTCG_PASS"])
    names = {}
    for board in ("b", "a"):
        d = json.loads(urllib.request.urlopen(f"{BASE}/leaderboard/{board}", timeout=40).read().decode())
        for r in d["rows"]:
            names[r["team_id"]] = r["team_name"]
    ms = call("/matches", tok)
    print("matches", len(ms), "teams", len(names), flush=True)

    draws = collections.defaultdict(lambda: {"early": collections.Counter(), "late": collections.Counter()})
    atks = collections.defaultdict(set)
    games = collections.defaultdict(lambda: {"early": 0, "late": 0})

    order = sorted(ms, key=lambda m: -m.get("round_no", 0))
    budget = int(os.environ.get("RECON_MAX_LOGS", 900))
    used = 0
    for m in order:
        if used >= budget:
            break
        a, b = m["player_a"], m["player_b"]
        era = "early" if m.get("round_no", 0) <= EARLY_MAX else "late"
        need = (games[a][era] < PER_ERA and a in names) or (games[b][era] < PER_ERA and b in names)
        if not need:
            continue
        try:
            log = call(f"/matches/{m['id']}/log", tok).get("log") or ""
        except Exception:
            continue
        if len(log) < 500:
            continue
        used += 1
        seat = {"A": a, "B": b}
        head, sep, body = log.partition("\u3010\u7b2c 1 \u56de\u5408")
        if not sep:
            head, body = "", log
        seen = collections.Counter()
        for line in head.splitlines():
            mm = DRAW.match(line)
            if mm:
                seen[(seat[mm.group(1)], mm.group(2))] += 1
        for (tid, nm), k in seen.items():
            if tid in names:
                draws[tid][era][nm] += k
        for line in body.splitlines():
            mm = ATK.match(line)
            if mm:
                tid = seat[mm.group(1)]
                if tid in names:
                    atks[tid].add(mm.group(2))
        for tid in (a, b):
            if tid in names:
                games[tid][era] += 1
        if used % 50 == 0:
            print("logs used", used, flush=True)

    summary = {}
    for tid, nm in names.items():
        entry = {"team_id": tid, "name": nm, "games": dict(games[tid]), "decks": {}}
        for era in ("early", "late"):
            c = draws[tid][era]
            total = sum(c.values())
            if total < 20:
                entry["decks"][era] = None
                continue
            rows = []
            for card_name, k in c.items():
                cid = pick_id(card_name, atks[tid])
                if cid is None:
                    continue
                n = round(k * 60.0 / total)
                kind = next(x["cardTypeName"] for x in by_name[card_name])
                if kind != "BASIC_ENERGY":
                    n = min(n, 4)
                if n <= 0:
                    continue
                rows.append({"n": n, "id": cid, "name": id2name.get(str(cid), card_name)})
            rows.sort(key=lambda r: -r["n"])
            entry["decks"][era] = {"draws": total, "cards": rows}
        entry["attacks"] = sorted(atks[tid])
        summary[str(tid)] = entry

    p = os.path.join(OUT, "opponents_decks.json")
    json.dump(summary, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", p, "logs used", used, flush=True)


if __name__ == "__main__":
    main()
