import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\DeepSeek Harness\ptcg-arena"
data = json.load(open(ROOT + r"\eval\recon\opponents_decks.json", encoding="utf-8"))

MARK = [
    ("Dragapult", ["Dragapult", "Drakloak", "Dreepy", "Budew"]),
    ("Crustle墙", ["Crustle", "Dwebble"]),
    ("Alakazam", ["Alakazam", "Kadabra", "Abra"]),
    ("MegaLucario", ["Mega Lucario", "Riolu", "Solrock"]),
    ("草系", ["Teal Mask Ogerpon", "Meganium", "Bayleef", "Applin", "Dipplin", "Tapu Bulu"]),
    ("Kangaskhan", ["Mega Kangaskhan", "Zangoose"]),
    ("Hop's", ["Hop’s Trevenant", "Hop's Trevenant", "Hop’s Cramorant", "Hop's Cramorant"]),
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
    late = e["decks"].get("late")
    if not late:
        continue
    top = sorted(late["cards"], key=lambda c: -c["n"])[:6]
    rows.append((tid, e["name"], classify(late["cards"]),
                 " | ".join(f"{c['n']}x{c['name'][:16]}" for c in top)))
rows.sort(key=lambda r: int(r[0]))
for r in rows:
    print(f"{r[0]:>3} {r[1][:18]:<20} {r[2]:<12} {r[3][:96]}")
