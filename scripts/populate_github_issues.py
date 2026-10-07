"""Script to populate GitHub Issues, Labels, and Milestones
Uses the GitHub REST API to synchronize the Library Management System's
User Stories and Action Items with color-coded priority labels.
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

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def get_token():
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        return token
    # Retrieve from Git Credential Manager
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
    "User-Agent": "Agile-Library-PBL-Setup",
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
        err_msg = e.read().decode("utf-8")
        return {"error": e.code, "message": err_msg}


def create_or_update_label(name, color, description):
    res = api_request("labels", method="POST", data={
        "name": name,
        "color": color,
        "description": description
    })
    if "error" in res and res["error"] == 422:
        safe_name = urllib.parse.quote(name)
        api_request(f"labels/{safe_name}", method="PATCH", data={
            "color": color,
            "description": description
        })
    print(f"[*] Label '{name}' configured with color #{color}")


def create_milestones():
    milestones = [
        ("Sprint 1 - Security & Identity Management", "Deliver member registration, salted SHA-256 password hashing, and role-based authentication.", 1),
        ("Sprint 2 - Catalog Management & Availability", "Deliver textbook catalog persistence, shelf location tags, and case-insensitive keyword search.", 2),
        ("Sprint 3 - Circulation Engine & Concurrency Control", "Implement atomic 14-day book loans, 3-book member quotas, and inventory recovery upon return.", 3),
        ("Sprint 4 - Renewals, Reservations & Overdue Fines", "Deliver 14-day loan renewals, out-of-stock reservation queue, and automated late fine calculation (₹5/day).", 4),
        ("Sprint 5 - In-App Scrum Tooling, Auditing & Release", "Deliver SQLite Scrum tables, terminal ASCII Kanban board, automated test suite, and viva release.", 5),
    ]
    created = {}
    for title, desc, num in milestones:
        res = api_request("milestones", method="POST", data={
            "title": title,
            "description": desc,
            "state": "closed" if num <= 4 else "open"
        })
        if "number" in res:
            created[num] = res["number"]
            print(f"[*] Created Milestone '{title}' (# {res['number']})")
        else:
            list_res = api_request("milestones?state=all")
            if isinstance(list_res, list):
                for m in list_res:
                    if m["title"] == title:
                        created[num] = m["number"]
                        break
    return created


def main():
    if not TOKEN:
        print("[!] No GitHub token found. Please set GITHUB_TOKEN or ensure git credentials are configured.")
        return

    print(f"=== Step 1: Setting up Labels with Color Coding for {OWNER}/{REPO} ===")
    labels = [
        # Color coding for priorities:
        ("priority: high", "d73a4a", "High Priority - Must Have [Red]"),
        ("priority: medium", "fbca04", "Medium Priority - Should Have [Amber/Yellow]"),
        ("priority: low", "0e8a16", "Low Priority - Could Have [Green]"),
        # Types:
        ("type: user-story", "7057ff", "Agile User Story [Purple]"),
        ("type: action-item", "0075ca", "Scrum Action Item [Blue]"),
        # Status columns for Kanban:
        ("status: backlog", "cfd3d7", "Kanban Column: Backlog"),
        ("status: todo", "1d76db", "Kanban Column: To Do"),
        ("status: in-progress", "d93f0b", "Kanban Column: In Progress"),
        ("status: review", "a2eeef", "Kanban Column: Review/Testing"),
        ("status: done", "0e8a16", "Kanban Column: Done"),
    ]
    for name, color, desc in labels:
        create_or_update_label(name, color, desc)

    print("\n=== Step 2: Creating Sprint Milestones ===")
    milestone_map = create_milestones()

    print("\n=== Step 3: Populating User Stories as GitHub Issues ===")
    user_stories = [
        {
            "code": "US-01",
            "title": "[US-01] Member Registration & Credential Hashing",
            "body": """### User Story
**As a** prospective library member,  
**I want** to register an account using my unique username, email, phone number, and password,  
**So that** I can securely access institutional catalog borrowing and digital reserve services.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 1 | Assignee: Annika Jha

### Acceptance Criteria
- [x] Validates unique username and email format.
- [x] Hashes passwords securely with SHA-256 + salt.
- [x] Prevents duplicate accounts with database constraints.
- [x] Records user creation in system audit trail.
""",
            "priority": "priority: high",
            "sprint": 1,
            "status": "status: done"
        },
        {
            "code": "US-02",
            "title": "[US-02] Role-Based Authentication & Session Management",
            "body": """### User Story
**As a** registered system user,  
**I want** to log in using my username and password,  
**So that** the application validates my identity and provisions role-specific capabilities.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 1 | Assignee: Dev Team

### Acceptance Criteria
- [x] Verifies password hash against stored hash in the `users` table.
- [x] Cleanly rejects incorrect credentials with informative message.
- [x] Provisions session role boundaries (`member`, `librarian`, `admin`).
""",
            "priority": "priority: high",
            "sprint": 1,
            "status": "status: done"
        },
        {
            "code": "US-03",
            "title": "[US-03] Book Catalog Management & Shelf Tracking",
            "body": """### User Story
**As a** librarian,  
**I want** to add, edit, and catalog books with ISBN, title, author, category, publisher, year, copy count, and shelf location,  
**So that** physical volumes are systematically classified and physical copies are easy to locate in library stacks.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 2 | Assignee: Dev Team

### Acceptance Criteria
- [x] Enforces unique ISBN constraint in catalog.
- [x] Validates positive copy counts.
- [x] Stores physical stack coordinates (e.g. `Shelf A-12`).
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-04",
            "title": "[US-04] Advanced Book Search & Category Filtering",
            "body": """### User Story
**As a** student or researcher,  
**I want** to search the catalog by title keywords, author name, or category genre,  
**So that** I can rapidly locate relevant study materials without manually browsing stacks.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 2 | Assignee: Dev Team

### Acceptance Criteria
- [x] Case-insensitive keyword search matching title, author, and ISBN.
- [x] Filters by academic category/discipline.
- [x] Returns search results with zero latency.
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-05",
            "title": "[US-05] Real-time Book Availability & Copy Inspection",
            "body": """### User Story
**As a** student,  
**I want** to check real-time available copy counts and shelf coordinates prior to visiting circulation desks,  
**So that** I do not waste time seeking books that are currently checked out.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 2 | Assignee: Dev Team

### Acceptance Criteria
- [x] Displays total copies, available copies, and borrowed counts.
- [x] Shows exact shelf location coordinates.
- [x] Automatically flags out-of-stock titles.
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-06",
            "title": "[US-06] Atomic Book Issue & Concurrency Control",
            "body": """### User Story
**As a** library member,  
**I want** to borrow an available book with an immediate 14-day checkout due date,  
**So that** the copy is atomically locked to my account and cannot be double-issued to another user.

### Story Points: 8 | Priority: High (Must Have)
### Target Sprint: Sprint 3 | Assignee: Annika Jha

### Acceptance Criteria
- [x] Atomic SQLite transaction decrementing stock count.
- [x] Enforces maximum 3 active books quota per member.
- [x] Blocks members with outstanding unpaid fines.
- [x] Generates automatic 14-day due date stamp.
""",
            "priority": "priority: high",
            "sprint": 3,
            "status": "status: done"
        },
        {
            "code": "US-07",
            "title": "[US-07] Member Loan History & Due Date Overview",
            "body": """### User Story
**As a** library member,  
**I want** to view my active checkouts, return timestamps, and countdown to due dates,  
**So that** I can return books punctually and prevent late penalty fines.

### Story Points: 3 | Priority: Medium (Should Have)
### Target Sprint: Sprint 3 | Assignee: Dev Team

### Acceptance Criteria
- [x] Returns active checkouts with calculated overdue flags.
- [x] Maintains complete historical borrowing ledger.
- [x] Clearly indicates remaining days until return deadline.
""",
            "priority": "priority: medium",
            "sprint": 3,
            "status": "status: done"
        },
        {
            "code": "US-08",
            "title": "[US-08] Book Return & Automated Inventory Recovery",
            "body": """### User Story
**As a** library member,  
**I want** to return a borrowed book and have the inventory count restored instantaneously,  
**So that** other students can immediately borrow or reserve the returned title.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 3 | Assignee: Dev Team

### Acceptance Criteria
- [x] Updates borrow record status to `Returned` with timestamp.
- [x] Atomically restores available copy count (`available_copies + 1`).
- [x] Prevents duplicate return submissions.
""",
            "priority": "priority: high",
            "sprint": 3,
            "status": "status: done"
        },
        {
            "code": "US-09",
            "title": "[US-09] Self-Service Book Renewal & Reservation Queue",
            "body": """### User Story
**As a** library member,  
**I want** to renew an unreserved active loan for 14 additional days or reserve an out-of-stock book,  
**So that** I can extend my research period or hold the next available returned copy.

### Story Points: 5 | Priority: Medium (Should Have)
### Target Sprint: Sprint 4 | Assignee: Annika Jha

### Acceptance Criteria
- [x] Extends due date by 14 days (up to 2 renewals max).
- [x] Blocks renewal if another member has placed a reservation.
- [x] Automatically queues holds on out-of-stock volumes with FIFO fulfillment.
""",
            "priority": "priority: medium",
            "sprint": 4,
            "status": "status: done"
        },
        {
            "code": "US-10",
            "title": "[US-10] Automated Overdue Fine Calculation & Settlement",
            "body": """### User Story
**As a** librarian,  
**I want** the system to compute late fees at ₹5 per calendar day past due date upon return and support fee payment,  
**So that** overdue delays are deterred and financial records remain transparent.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 4 | Assignee: Dev Team

### Acceptance Criteria
- [x] Calculates `overdue_days * ₹5.0` automatically on late returns.
- [x] Creates itemized record in `fines` table with status `Unpaid`.
- [x] Supports payment settlement updating fine status to `Paid`.
""",
            "priority": "priority: high",
            "sprint": 4,
            "status": "status: done"
        },
        {
            "code": "US-11",
            "title": "[US-11] Centralized Librarian & Admin Inventory Audit",
            "body": """### User Story
**As an** administrator,  
**I want** to view aggregate circulation metrics, total volumes, active loans, overdue lists, and audit events,  
**So that** I can maintain institutional governance and inventory accountability.

### Story Points: 3 | Priority: Low (Could Have)
### Target Sprint: Sprint 5 | Assignee: Dev Team

### Acceptance Criteria
- [x] Provides centralized institutional inventory health metrics.
- [x] Displays complete circulation audit history and overdue lists.
- [x] Tracks fine collection totals and system event logs.
""",
            "priority": "priority: low",
            "sprint": 5,
            "status": "status: done"
        },
        {
            "code": "US-12",
            "title": "[US-12] Built-in Scrum Backlog, Sprint & Terminal Kanban Engine",
            "body": """### User Story
**As a** Scrum team member,  
**I want** to track user stories, sprint velocity, and Kanban workflows directly inside the application,  
**So that** the project demonstrates transparent Agile engineering and live traceability.

### Story Points: 8 | Priority: High (Must Have)
### Target Sprint: Sprint 5 | Assignee: Annika Jha

### Acceptance Criteria
- [x] Persistent SQLite tables for `sprints`, `user_stories`, and `action_items`.
- [x] Renders 5-column ASCII terminal Kanban board with live card progression.
- [x] Provides automated viva demonstration walkthrough mode (`--demo`).
""",
            "priority": "priority: high",
            "sprint": 5,
            "status": "status: done"
        }
    ]

    for st in user_stories:
        data = {
            "title": st["title"],
            "body": st["body"],
            "labels": [st["priority"], "type: user-story", st["status"]],
        }
        if st["sprint"] in milestone_map:
            data["milestone"] = milestone_map[st["sprint"]]

        res = api_request("issues", method="POST", data=data)
        if "number" in res:
            issue_num = res["number"]
            print(f"[+] Created Issue #{issue_num}: {st['title']}")
            # Close issue to reflect completed status for finished sprints
            api_request(f"issues/{issue_num}", method="PATCH", data={"state": "closed"})
        else:
            print(f"[-] Issue error: {res}")
        time.sleep(0.3)

    print("\n[SUCCESS] All labels, milestones, and issues created on GitHub with color coding!")


if __name__ == "__main__":
    main()
