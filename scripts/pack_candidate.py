"""Package a candidate deck with the unchanged w_v3 agent for a field A/B test."""
import os
import subprocess
import sys
import tarfile

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\DeepSeek Harness\ptcg-arena"
AGENT = os.path.join(ROOT, "src", "agents", "w_v3.py")
deck_name = sys.argv[1] if len(sys.argv) > 1 else "snorlax3"
DECK = os.path.join(ROOT, "eval", "decks", "ultimate", deck_name + ".csv")

r = subprocess.run([sys.executable, os.path.join(ROOT, "deck_check.py"), DECK,
                    os.path.join(ROOT, "cards.csv")], capture_output=True, text=True)
print((r.stdout or "").strip()[-160:] or (r.stderr or "").strip()[-160:])
if r.returncode != 0:
    raise SystemExit("deck invalid")

out = os.path.join(ROOT, "dist", f"submission_{deck_name}.tar.gz")
with tarfile.open(out, "w:gz") as tf:
    tf.add(AGENT, arcname="main.py")
    tf.add(DECK, arcname="deck.csv")
with tarfile.open(out) as tf:
    print(out, "->", [(m.name, m.size) for m in tf.getmembers()])
    deck = tf.extractfile("deck.csv").read().decode().split()
    print("cards", len(deck), "Snorlax(304):", deck.count("304"), "Mist(11):", deck.count("11"))
