"""GitHub Issue Cleanup and Reset Utility
Author / Scrum Lead: Annika Jha
"""
import urllib.request
import urllib.error
import urllib.parse
import json
import time
import os
import subprocess
import sys


def get_token():
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        return token
    try:
        cmd = "git credential fill"
        inp = "protocol=https\nhost=github.com\n"
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        out, _ = proc.communicate(input=inp)
        for line in out.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return ""


OWNER = "yashkarwa2005"
REPO = "Library-Management"
TOKEN = get_token()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "Agile-Library-Cleanup",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json"
}


def api_request(endpoint, method="GET", data=None):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/{endpoint}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=HEADERS,
        method=method
    )
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        return {"error": e.code, "message": e.read().decode("utf-8")}


def main():
    if not TOKEN:
        print("[!] No GitHub token found.")
        return

    print(f"[*] Fetching existing issues from {OWNER}/{REPO}...")
    issues = api_request("issues?state=all")
    if isinstance(issues, list):
        print(f"[*] Found {len(issues)} issues.")
        for issue in issues:
            print(f"  - Issue #{issue['number']}: {issue['title']} (State: {issue['state']})")
    else:
        print(f"[-] Error querying issues: {issues}")


if __name__ == "__main__":
    main()
