# Kanban Board & Workflow
## Library Management System using Scrum Agile Methodology

---

## 1. Kanban Methodology Overview

**Kanban** is an Agile visual management method designed to visualize work, limit Work-in-Progress (WIP), and optimize workflow efficiency across software delivery iterations. In this project, all engineering tasks and user stories flow through five explicit stages:

```text
+--------------+     +--------------+     +------------------+     +--------------------+     +--------------+
|   BACKLOG    | --> |    TO DO     | --> |   IN PROGRESS    | --> |  REVIEW / TESTING  | --> |     DONE     |
+--------------+     +--------------+     +------------------+     +--------------------+     +--------------+
```

### Core Kanban Rules Applied
1. **Visualize the Workflow:** Every user story (`US-01` to `US-12`) and technical action item (`AI-01` to `AI-18`) is visualized as a discrete card.
2. **Limit Work In Progress (WIP):** Maximum of 3 cards per engineer in `IN PROGRESS` to prevent multitasking bottlenecks and context-switching overhead.
3. **Manage Flow:** Daily standups emphasize moving active cards rightward toward `Done` before pulling new backlog stories.
4. **Automated Quality Gate:** A card cannot advance to `Done` without satisfying all Gherkin Acceptance Criteria and passing automated unit tests.

### Priority Badges:
- 🔴 **High Priority (Must Have)**
- 🟠 **Medium Priority (Should Have)**
- 🟢 **Low Priority (Could Have)**

---

## 2. Live Project Kanban Board (Sprint 5 Final State)

| 📋 BACKLOG | 🔵 TO DO | 🟡 IN PROGRESS | 🟣 REVIEW / TESTING | 🟢 DONE |
|---|---|---|---|---|
| 🟢 `US-EXT-1` [5 pts]<br>RFID Smart Gate Integration<br>_Assignee: Unassigned_ | 🟢 `AI-EXT-3` [1 pt]<br>Post-Viva Documentation Archive<br>_Assignee: Annika Jha_ | 🟠 `AI-18` [2 pts]<br>Sprint Review & Viva Rehearsal<br>_Assignee: Annika Jha_ | 🔴 `AI-17` [3 pts]<br>16-Case Automated Test Verification<br>_Assignee: Annika Jha_ | 🔴 `US-01` [3 pts]<br>Member Registration Module<br>_Assignee: Annika Jha_ |
| 🟢 `US-EXT-2` [3 pts]<br>SMS Due Date Alerts<br>_Assignee: Unassigned_ | | | | 🔴 `US-02` [3 pts]<br>Role-Based Authentication<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-03` [5 pts]<br>Book Catalog & Shelf Tracking<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-04` [3 pts]<br>Advanced Search & Filter<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-05` [3 pts]<br>Real-Time Availability Query<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-06` [8 pts]<br>Atomic Book Issue & Concurrency<br>_Assignee: Annika Jha_ |
| | | | | 🟠 `US-07` [3 pts]<br>Member Loan History Ledger<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-08` [5 pts]<br>Return & Stock Recovery<br>_Assignee: Dev Team_ |
| | | | | 🟠 `US-09` [5 pts]<br>Renewals & Reservation Queue<br>_Assignee: Annika Jha_ |
| | | | | 🔴 `US-10` [5 pts]<br>Overdue Fine Calculation<br>_Assignee: Dev Team_ |
| | | | | 🟢 `US-11` [3 pts]<br>Admin Inventory Audit<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-12` [8 pts]<br>In-App Scrum Kanban Engine<br>_Assignee: Annika Jha_ |
| | | | | 🔴 `AI-01` to `AI-16`<br>Completed Infrastructure Tasks<br>_Assignee: Annika Jha / Dev_ |

---

## 3. Dual Kanban Implementations Built-in

In addition to this static Markdown specification, the project delivers two live, interactive implementations:

### A. Terminal ASCII Kanban Board (`src/kanban.py`)
Direct terminal display querying the persistent SQLite `user_stories` and `action_items` tables:
```bash
python src/main.py --kanban
```

### B. Interactive Visual Web Kanban Board (`kanban_board.html`)
Open in any browser for full HTML5 drag-and-drop card movement, sprint filters, and live metric updates:
```bash
# Launch via local browser or through Python web server:
python app.py
# Open: http://127.0.0.1:5000/kanban_board.html
```

---

## 4. GitHub Projects & GitHub Issues Integration

The project is structured to seamlessly synchronize with GitHub's native issue tracking and Projects board:

### 1. GitHub Issue Labels & Color Coding
- `priority: high` (🔴 Color: `#d73a4a` | Red)
- `priority: medium` (🟠 Color: `#fbca04` | Amber/Yellow)
- `priority: low` (🟢 Color: `#0e8a16` | Green)
- `type: user-story` (🟣 Color: `#7057ff` | Purple)
- `type: action-item` (🔵 Color: `#0075ca` | Blue)
- `status: backlog` (`#cfd3d7`)
- `status: todo` (`#1d76db`)
- `status: in-progress` (`#d93f0b`)
- `status: review` (`#a2eeef`)
- `status: done` (`#0e8a16`)

### 2. GitHub Sprint Milestones
- `Sprint 1 - Security & Identity Management`
- `Sprint 2 - Catalog Management & Availability`
- `Sprint 3 - Circulation Engine & Concurrency Control`
- `Sprint 4 - Renewals, Reservations & Overdue Fines`
- `Sprint 5 - In-App Scrum Tooling, Auditing & Release`

### 3. Automated Setup Script
Run the automated synchronization script to populate all labels, sprint milestones, and user story issues on GitHub:
```bash
python scripts/populate_github_issues.py
```
*(Uses the local Windows Git Credential Manager or `GITHUB_TOKEN` environment variable).*
