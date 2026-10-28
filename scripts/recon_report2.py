"""Print a compact table of reconstructed decks (team / archetype / top cards)."""
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, "data", "opponents_decks.json"), encoding="utf-8"))

MARK = [
    ("Dragapult", ["Dragapult", "Drakloak", "Dreepy", "Budew"]),
    ("CrustleWall", ["Crustle", "Dwebble"]),
    ("Alakazam", ["Alakazam", "Kadabra", "Abra"]),
    ("MegaLucario", ["Mega Lucario", "Riolu", "Solrock"]),
    ("Grass", ["Teal Mask Ogerpon", "Meganium", "Bayleef", "Applin", "Dipplin", "Tapu Bulu"]),
    ("Kangaskhan", ["Mega Kangaskhan", "Zangoose"]),
    ("Hop", ["Hop's Trevenant", "Hop's Cramorant", "Hop's Snorlax"]),
]


def classify(cards):
    names = {c["name"] for c in cards}
    best, hits = "other", 0
    for label, keys in MARK:
        h = sum(1 for k in keys if any(k in n for n in names))
        if h > hits:
            best, hits = label, h
    return best


rows = []
for tid, e in data.items():
    late = (e.get("decks") or {}).get("late")
    if not late:
        continue
    top = sorted(late["cards"], key=lambda c: -c["n"])[:6]
    rows.append((tid, e["name"], classify(late["cards"]),
                 " | ".join(f"{c['n']}x{c['name'][:16]}" for c in top)))
rows.sort(key=lambda r: int(r[0]))
for r in rows:
    print(f"{r[0]:>3} {r[1][:18]:<20} {r[2]:<12} {r[3][:96]}")
