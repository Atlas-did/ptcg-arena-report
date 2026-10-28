"""Upload a submission package to the platform (multipart/form-data)."""
import json
import os
import sys
import urllib.request
import uuid

sys.stdout.reconfigure(encoding="utf-8")
BASE = "http://115.159.47.81/api"


def login(user, password):
    body = json.dumps({"username": user, "password": password}).encode()
    req = urllib.request.Request(BASE + "/auth/login", data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())["access_token"]


def upload(tok, path):
    boundary = "----dsh" + uuid.uuid4().hex
    name = os.path.basename(path)
    with open(path, "rb") as fh:
        content = fh.read()
    body = b""
    body += ("--" + boundary + "\r\n").encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{name}"\r\n'.encode()
    body += b"Content-Type: application/gzip\r\n\r\n"
    body += content + b"\r\n"
    body += ("--" + boundary + "--\r\n").encode()
    req = urllib.request.Request(BASE + "/submissions", data=body, method="POST",
                                 headers={"Authorization": "Bearer " + tok,
                                          "Content-Type": "multipart/form-data; boundary=" + boundary})
    try:
        r = urllib.request.urlopen(req, timeout=180)
        return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


if __name__ == "__main__":
    tok = login(os.environ["PTCG_USER"], os.environ["PTCG_PASS"])
    code, txt = upload(tok, sys.argv[1])
    print(code, txt[:500])
