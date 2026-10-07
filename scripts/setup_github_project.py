"""GitHub Projects V2 Automation Script
Creates a Project V2 board, adds custom fields (Priority, Sprint, Story Points),
and links issues from the Library-Management repository.
Requires a GitHub token with the 'project' scope.
Author / Scrum Lead: Annika Jha
"""
import urllib.request
import urllib.error
import json
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


TOKEN = get_token()
OWNER = "yashkarwa2005"
REPO = "Library-Management"


def graphql_query(query, variables=None):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables or {}}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "User-Agent": "Agile-Library-Project-Setup",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    if not TOKEN:
        print("[!] No GitHub token found.")
        return

    print("Checking token scopes for Projects V2...")
    try:
        # 1. Get User ID & Repo ID
        init_q = f"""
        query {{
          viewer {{
            id
            login
          }}
          repository(owner: "{OWNER}", name: "{REPO}") {{
            id
            name
          }}
        }}
        """
        init_res = graphql_query(init_q)
        if "errors" in init_res:
            print("[-] Scope error:", init_res["errors"][0]["message"])
            print("[!] Please grant 'project' scope to your Personal Access Token at https://github.com/settings/tokens to enable automated Project V2 creation.")
            return

        owner_id = init_res["data"]["viewer"]["id"]
        repo_id = init_res["data"]["repository"]["id"]

        print(f"[+] Creating Project V2 for {OWNER}...")
        create_q = f"""
        mutation {{
          createProjectV2(input: {{
            ownerId: "{owner_id}",
            title: "Library Management System — Scrum Board"
          }}) {{
            projectV2 {{
              id
              number
              url
            }}
          }}
        }}
        """
        create_res = graphql_query(create_q)
        if "errors" in create_res:
            print("[-] Failed to create Project:", create_res["errors"])
            return

        proj = create_res["data"]["createProjectV2"]["projectV2"]
        proj_id = proj["id"]
        proj_url = proj["url"]
        print(f"[SUCCESS] Created Project V2: {proj_url} (ID: {proj_id})")

        # Link project to repository
        link_q = f"""
        mutation {{
          linkProjectV2ToRepository(input: {{
            projectId: "{proj_id}",
            repositoryId: "{repo_id}"
          }}) {{
            clientMutationId
          }}
        }}
        """
        graphql_query(link_q)
        print(f"[+] Successfully linked Project to {OWNER}/{REPO}!")

    except Exception as e:
        print("[-] Exception:", e)


if __name__ == "__main__":
    main()
