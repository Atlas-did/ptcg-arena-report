"""Minimal client for the PTCG-Arena API used by the reproduction scripts.

Credentials are read from PTCG_USER / PTCG_PASS (or PTCG_TOKEN). No secrets are
stored in this repository.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("PTCG_BASE", "http://115.159.47.81/api")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "bot_farm")


def call(path, token, method="GET", body=None, timeout=180, tries=4):
    data = json.dumps(body).encode() if body is not None else None
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(
                BASE + path, data=data, method=method,
                headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
            return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                raise SystemExit(f"auth failed ({exc.code}); token expired?")
            last = exc
        except Exception as exc:
            last = exc
        time.sleep(2 + 2 * i)
    raise SystemExit(f"{path} failed: {last}")


def raw(path, token, timeout=120):
    req = urllib.request.Request(BASE + path, headers={"Authorization": "Bearer " + token})
    return urllib.request.urlopen(req, timeout=timeout).read()


def login(user, password):
    body = json.dumps({"username": user, "password": password}).encode()
    req = urllib.request.Request(BASE + "/auth/login", data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
    return d["access_token"]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", default=None)
    ap.add_argument("--user", default=None)
    ap.add_argument("--password", default=None)
    ap.add_argument("--n", type=int, default=20, help="max matches per bot")
    ap.add_argument("--until-win", action="store_true")
    ap.add_argument("--only", default=None)
    ap.add_argument("--save-replay", action="store_true")
    a = ap.parse_args()

    if not a.token:
        a.token = os.environ.get("PTCG_TOKEN")
    if not a.token:
        a.user = a.user or os.environ.get("PTCG_USER")
        a.password = a.password or os.environ.get("PTCG_PASS")
        if not (a.user and a.password):
            raise SystemExit("need --token, or PTCG_USER/PTCG_PASS env vars")
        a.token = login(a.user, a.password)
        print("logged in, token acquired", flush=True)

    bots = call("/bots", a.token)
    if isinstance(bots, dict):
        bots = bots.get("bots") or bots.get("items") or []
    if a.only:
        bots = [b for b in bots if a.only in str(b.get("name", ""))]
    print(f"{len(bots)} bots")

    os.makedirs(OUT, exist_ok=True)
    summary = []
    for b in bots:
        bid = b.get("team_id") or b.get("id") or b.get("bot_team_id")
        name = b.get("name") or str(bid)
        w = l = d = 0
        got_win = False
        for i in range(a.n):
            r = call("/bot-matches", a.token, "POST", {"bot_team_id": bid})
            res = r.get("my_result")
            w += res == "win"
            l += res == "loss"
            d += res == "draw"
            if a.save_replay and r.get("id"):
                try:
                    blob = raw(f"/bot-matches/{r['id']}/replay", a.token)
                    open(os.path.join(OUT, f"{bid}_{r['id']}.html"), "wb").write(blob)
                except Exception:
                    pass
            if res == "win":
                got_win = True
                if a.until_win:
                    break
            print(f"  {name:<16} game {i+1:>2}: {res:<6} total {w}-{l}-{d}", flush=True)
        total = max(1, w + l + d)
        summary.append((name, w, l, d, w / total))
        print(f"== {name}: {w}-{l}-{d} = {w/total:.0%}" + ("  [beaten]" if got_win else "  [not beaten]"), flush=True)

    print("\n=== summary ===")
    for name, w, l, d, wr in sorted(summary, key=lambda x: -x[4]):
        print(f"  {name:<18} {w:>2}-{l:<2}-{d:<2} {wr:>5.0%}")

    json.dump([{"bot": n, "w": w, "l": l, "d": d, "wr": wr} for n, w, l, d, wr in summary],
              open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
