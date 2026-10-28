"""Package a candidate deck with the final v3 agent into submission.tar.gz.

Usage: python scripts/pack_candidate.py <deck.csv> [out_name]
"""
import os
import subprocess
import sys
import tarfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT = os.path.join(ROOT, "submission", "main.py")
deck_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "submission", "deck.csv")
name = sys.argv[2] if len(sys.argv) > 2 else "candidate"

r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "deck_check.py"),
                    deck_path, os.path.join(ROOT, "data", "cards.csv")],
                   capture_output=True, text=True)
print((r.stdout or "").strip()[-300:] or (r.stderr or "").strip()[-300:])
if r.returncode != 0:
    raise SystemExit("deck invalid")

out = os.path.join(ROOT, "dist", f"submission_{name}.tar.gz")
os.makedirs(os.path.dirname(out), exist_ok=True)
with tarfile.open(out, "w:gz") as tf:
    tf.add(AGENT, arcname="main.py")
    tf.add(deck_path, arcname="deck.csv")
with tarfile.open(out) as tf:
    print(out, "->", [(m.name, m.size) for m in tf.getmembers()])
    deck = tf.extractfile("deck.csv").read().decode().split()
    print("cards", len(deck))
