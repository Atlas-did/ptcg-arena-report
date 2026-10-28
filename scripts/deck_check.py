"""Validate a 60-card deck against the platform rules.

Usage: python scripts/deck_check.py submission/deck.csv data/cards.csv
Exit code 0 = legal, 1 = illegal (all reasons printed).
"""
import csv
import sys
from collections import Counter

FOSSILS = {1099, 1136, 1138, 1150, 1151}


def load_cards(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return {int(r["cardId"]): r for r in csv.DictReader(fh)}


def check(deck_path, cards_path):
    cards = load_cards(cards_path)
    ids = []
    with open(deck_path, encoding="utf-8-sig") as fh:
        for line in fh:
            s = line.strip()
            if not s:
                continue
            if not s.lstrip("-").isdigit():
                return [f"non-integer line: {s!r}"]
            ids.append(int(s))

    errs = []
    if len(ids) != 60:
        errs.append(f"deck has {len(ids)} cards, must be exactly 60")

    missing = [i for i in ids if i not in cards]
    if missing:
        errs.append(f"card ids not in pool: {sorted(set(missing))}")
        return errs

    by_name = Counter(cards[i]["name"] for i in ids)
    for name, n in by_name.items():
        first = next(i for i in ids if cards[i]["name"] == name)
        if n > 4 and cards[first]["cardType"] != "5":
            errs.append(f"same-name > 4: {name} x {n}")

    ace = [i for i in ids if cards[i]["aceSpec"] == "1"]
    if len(ace) > 1:
        errs.append(f"ACE SPEC x {len(ace)}, max 1: {[cards[i]['name'] for i in ace]}")

    basics = [i for i in ids
              if cards[i]["cardType"] == "0" and cards[i]["basic"] == "1" and i not in FOSSILS]
    if not basics:
        errs.append("no real Basic Pokemon (cardType=0, basic=1; fossils do not count)")

    return errs


if __name__ == "__main__":
    deck = sys.argv[1] if len(sys.argv) > 1 else "submission/deck.csv"
    pool = sys.argv[2] if len(sys.argv) > 2 else "data/cards.csv"
    problems = check(deck, pool)
    if problems:
        print("ILLEGAL:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("OK: 60 cards / same-name <= 4 / ACE <= 1 / Basic Pokemon present")
