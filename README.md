# Library Management System using Scrum Agile Methodology

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![Agile Methodology](https://img.shields.io/badge/Methodology-Scrum%20%2F%20Kanban-success.svg)](https://www.scrum.org/)
[![Tests](https://img.shields.io/badge/Unit%20Tests-16%20Passed%20(100%25)-brightgreen.svg)](tests/test_library.py)
[![License](https://img.shields.io/badge/License-Academic%20PBL-orange.svg)](#)

> **B.Tech 3rd-Year Project-Based Learning (PBL) Submission**  
> **Course:** Agile Methodologies & IT (AM)  
> **Author / Scrum Lead:** Annika Jha  
> **Repository:** [yashkarwa2005/Library-Management](https://github.com/yashkarwa2005/Library-Management.git)

---

## 1. Project Overview

The **Library Management System** is an end-to-end, domain-driven software solution engineered to modernize academic library circulation, eliminate inventory stock discrepancies, track physical stack locations, and deliver transparent textbook availability for university students, faculty, and catalog librarians.

More importantly, the entire development lifecycle serves as a practical demonstration of **Scrum Agile Methodology**. To satisfy the B.Tech Agile Methodologies curriculum, the delivered codebase features a **dual-track architecture**:
1. **Academic Library Circulation Engine:** Salted SHA-256 user authentication, multi-genre catalog search, real-time shelf availability inspection, atomic 14-day book checkouts, borrower quota enforcement (max 3 books), punctual returns, self-service loan renewals, out-of-stock reservation queuing, and automated late penalty assessments (₹5/day).
2. **Built-in Scrum & Kanban Management Engine:** Persistent SQLite tables for user stories, sprint lifecycles, and action items, integrated with a real-time ASCII terminal Kanban board, an interactive web Kanban board with HTML5 drag-and-drop, and automated viva demonstration tooling.

---

## 2. Problem Statement

Traditional academic library operations suffer from three critical bottlenecks:
- **Shelf Search Frustration & Outdated Records:** Students physically scour library stacks only to discover that titles are missing, misclassified, or borrowed without updated records.
- **Stock Discrepancies & Concurrency Conflicts:** Lack of transactional database locking causes book copies to be recorded as available when already checked out, resulting in circulation collisions.
- **Manual Penalty Discretion & Hoarding:** Late returns and overdue fines are often assessed manually or inconsistently, leading to unreturned books and stranded academic resources.

From a software engineering perspective, university projects frequently suffer from monolithic waterfall development, late integration bugs, and lack of requirement traceability. This project solves both the academic library domain problem and the software project management problem through disciplined Scrum iterations.

---

## 3. Project Objectives

- **Zero Stock Inconsistency:** Enforce atomic database transactions to guarantee that available copy counts are decremented and restored accurately without race conditions.
- **Full Circulation Lifecycle:** Support self-service registration, multi-attribute catalog search, atomic checkouts, 14-day renewals, and overdue penalty calculations.
- **Disciplined Scrum Execution:** Practice all Scrum roles, ceremonies, INVEST-compliant user stories, and Gherkin-formatted acceptance criteria across 5 weekly sprints.
- **In-App Agile Tooling:** Integrate real-time Kanban visualization, backlog metrics, and sprint tracking directly inside both the Python console and web dashboard.
- **Zero Third-Party Dependency Hurdles:** Engineer using pure Python standard libraries (`sqlite3`, `http.server`, `hashlib`, `unittest`) to run out-of-the-box on any evaluation workstation.

For detailed curriculum mapping and academic objectives, see [docs/PROJECT_OBJECTIVES.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/docs/PROJECT_OBJECTIVES.md).

---

## 4. Key Features

### 📖 Academic Library Circulation Subsystem
- **Salted SHA-256 Authentication:** Secure registration and credential validation for members, librarians, and administrators.
- **Catalog Management & Shelf Classification:** Textbooks cataloged with unique ISBNs, authors, publishers, publication years, copy counts, and physical shelf coordinates (e.g., `Shelf A-12`).
- **Multi-Attribute Search:** Case-insensitive search across title keywords, authors, ISBNs, and academic disciplines (Computer Science, AI, Systems, etc.).
- **Real-Time Availability Inspection:** Instant query of total copies, on-shelf copies, and borrowed counts.
- **Atomic Borrowing Engine:** Transactional checkouts with 14-day return deadlines, blocking over-borrowing and users with unpaid fines.
- **Borrower Quota Enforcement:** Strict policy limit of maximum 3 active books checked out per student.
- **Punctual Return & Stock Recovery:** Instant restoration of inventory stock upon book return.
- **Self-Service Loan Renewal:** Extend active loans by 14 days (up to 2 renewals) with automatic blocking if another member has reserved the volume.
- **Out-of-Stock Reservation Queue:** Queue holds on unavailable books with automatic fulfillment upon return.
- **Automated Late Fine Assessment:** Computes ₹5/day late fees for overdue loans with itemized payment settlement.
- **Administrative Health Audits:** Global circulation reports, overdue loan lists, and audit log tracking.

### 📊 In-App Scrum Project Management Subsystem
- **Interactive Terminal ASCII Kanban Board:** 5-column live board (`Backlog ➔ To Do ➔ In Progress ➔ Review/Testing ➔ Done`) with task cards, story points, and priority badges.
- **Interactive Web Kanban Board (`kanban_board.html`):** Visual board with HTML5 drag-and-drop, sprint filtering, and live counter updates.
- **Product Backlog Management:** Full tracking of 12 user stories with MoSCoW prioritization and Fibonacci story points.
- **5-Week Sprint Cadence:** Sprint goals, committed vs completed points, and team velocity calculations.
- **Action Item Register:** Weekly impediment and task tracking with owners, due dates, and statuses.
- **Instant Automated Viva Demo (`--demo`):** Automated walkthrough executing the entire system in under 30 seconds.

---

## 5. Technology Stack

| Component | Technology | Rationale |
|---|---|---|
| **Programming Language** | Python 3.8+ (Tested on Python 3.13) | Clean, readable syntax; standard in enterprise engineering and academic evaluation. |
| **Persistence / Database** | SQLite 3 (`sqlite3`) | Zero-configuration ACID-compliant relational database with foreign key integrity. |
| **Cryptography** | `hashlib` (SHA-256 + Salt) | Secure one-way password hashing protecting against rainbow tables. |
| **Testing Framework** | `unittest` | Built-in test runner requiring zero external package installations. |
| **Web Server & REST API** | `http.server` (`ThreadingHTTPServer`) | Zero-dependency multi-threaded HTTP server powering the browser dashboard. |
| **User Interface** | ANSI Terminal Console + HTML5/CSS3 Dashboard | Flexible dual-interface supporting terminal evaluation and modern web interaction. |

---

## 6. Scrum Methodology Implementation

The project strictly follows the Scrum Framework as defined in the official Scrum Guide:

```text
+-----------------------------------------------------------------------------------------+
|                               SCRUM METHODOLOGY CADENCE                                 |
+-----------------------------------------------------------------------------------------+
  Product Vision ────► Product Backlog (Refined & Sized via Planning Poker)
                             │
                             ▼
                     Sprint Planning (Commitment & Goal Definition)
                             │
                             ▼
               Sprint Execution (Weekly Sprints 1 to 5)
                 ├──► Daily Scrum & Impediment Removal
                 └──► Kanban Flow (WIP Limits, 5-Column Progression)
                             │
                             ▼
               Sprint Review (Live Demo & Acceptance Criteria Verification)
                             │
                             ▼
               Sprint Retrospective (Continuous Improvement / Kaizen Action Items)
                             │
                             ▼
                Shippable Product Increment (Definition of Done)
```

---

## 7. Scrum Team Roles

- **Product Owner & Scrum Lead (Annika Jha):** Defines product vision, authors INVEST user stories, maintains and prioritizes the Product Backlog, facilitates ceremonies, and accepts increments based on Acceptance Criteria.
- **Development Team (Annika Jha & Dev Team):** Cross-functional engineering team responsible for relational SQLite schema design, circulation business logic, terminal/web interfaces, and automated test suite execution.

---

## 8. Requirement Priorities (MoSCoW)

Requirements are prioritized using the MoSCoW framework:
- 🔴 **MUST HAVE (35 Points):** User Authentication, Catalog Search, Availability Query, Atomic Issue, Quota Enforcement, Book Return, Overdue Fine Calculation, In-App Scrum Engine.
- 🟠 **SHOULD HAVE (8 Points):** Member Loan History, Self-Service Renewals, Reservation Hold Queue.
- 🟢 **COULD HAVE (3 Points):** Administrative Inventory Audit, Shelf Coordinates Display, Web Drag-and-Drop Kanban.
- ⚪ **WON'T HAVE (Deferred):** Online Stripe/Razorpay Payment Gateway, UHF RFID Hardware Gates, Automated WhatsApp/SMS Gateway.

📖 Full MoSCoW breakdown and point distribution: [scrum/REQUIREMENT_PRIORITIES.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/REQUIREMENT_PRIORITIES.md)

---

## 9. 5-Week Sprint Overview

The project was executed across five structured 1-week sprint iterations:

| Sprint | Theme / Milestone | Committed | Completed | Velocity | Status |
|---|---|---|---|---|---|
| **Sprint 1** | Security, Identity Management & SQLite Schema | 6 pts | 6 pts | 6 pts | 🟢 Done |
| **Sprint 2** | Catalog Management, Advanced Search & Availability | 11 pts | 11 pts | 11 pts | 🟢 Done |
| **Sprint 3** | Circulation Engine: Atomic Issue, Quotas & Returns | 16 pts | 16 pts | 16 pts | 🟢 Done |
| **Sprint 4** | Renewals, Reservations & Overdue Penalties | 10 pts | 10 pts | 10 pts | 🟢 Done |
| **Sprint 5** | In-App Scrum Tooling, Auditing, Testing & Release | 11 pts | 11 pts | 11 pts | 🟢 Done |

📖 Detailed sprint goals, task breakdown, and velocity reports: [scrum/SPRINT_PLAN.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/SPRINT_PLAN.md)

---

## 10. Kanban Board Workflow

The project visualizes work progression across five explicit stages:
```text
BACKLOG ────► TO DO ────► IN PROGRESS ────► REVIEW / TESTING ────► DONE
```
- **Live Terminal Board:** Run `python src/main.py --kanban` to render the ASCII board directly from the SQLite database.
- **Visual Web Board:** Open `kanban_board.html` or visit `http://127.0.0.1:5000/kanban_board.html` for interactive drag-and-drop.
- **GitHub Synchronization:** Run `python scripts/populate_github_issues.py` to sync all user stories as GitHub Issues with milestones and labels.

📖 Complete Kanban documentation: [scrum/KANBAN_BOARD.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/KANBAN_BOARD.md)

---

## 11. Project Directory Structure

```text
Library-Management/
│
├── README.md                         # Main project overview & documentation hub
├── app.py                            # Standalone Python Web Application & REST API
├── kanban_board.html                 # Interactive Visual Web Kanban Board (HTML5 Drag & Drop)
├── requirements.txt                  # Python dependencies (zero-friction standard library)
├── run.bat                           # Windows one-click execution batch launcher
├── .gitignore                        # Git ignore patterns for Python, IDEs, and SQLite
│
├── src/                              # Core application source code
│   ├── __init__.py                   # Package marker
│   ├── main.py                       # Application entry point, CLI menus & --demo runner
│   ├── database.py                   # SQLite schema, connection manager & seed loader
│   ├── library.py                    # Library circulation, catalog & fines service layer
│   ├── user_story.py                 # User Story service & backlog metrics
│   ├── sprint.py                     # Sprint planning & velocity tracking service
│   ├── action_item.py                # Action item register service
│   └── kanban.py                     # Terminal ASCII Kanban board renderer & card transitions
│
├── database/                         # Database storage directory
│   └── library.db                    # SQLite database (auto-generated & seeded on first run)
│
├── readme/                           # Core Agile requirement specifications
│   ├── USER_STORY.md                 # 12 INVEST user stories with priorities & estimates
│   └── ACCEPTANCE_CRITERIA.md        # Verifiable Given-When-Then criteria & DoD
│
├── scrum/                            # Scrum artifacts and ceremony reports
│   ├── PRODUCT_BACKLOG.md            # Prioritized Product Backlog & Epics
│   ├── SPRINT_PLAN.md                # 5-week sprint breakdown, goals & task estimates
│   ├── ACTION_ITEMS.md               # Weekly action items & retrospective register
│   ├── KANBAN_BOARD.md               # 5-column Kanban board & workflow guide
│   ├── REQUIREMENT_PRIORITIES.md     # MoSCoW prioritization & point distribution
│   ├── SPRINT_REVIEW.md              # Sprint review reports & stakeholder feedback
│   └── SPRINT_RETROSPECTIVE.md       # Retrospective logs & continuous improvements (Kaizen)
│
├── templates/                        # Web dashboard assets
│   └── index.html                    # Responsive browser portal with glassmorphism UI
│
├── tests/                            # Automated test suite
│   ├── __init__.py                   # Test package marker
│   └── test_library.py               # 16 automated unit & integration test cases
│
├── scripts/                          # Automation utilities
│   ├── populate_github_issues.py     # GitHub REST API sync script (labels, milestones, issues)
│   └── clean_github_issues.py        # GitHub maintenance utility
│
└── docs/                             # Academic & architectural documentation
    ├── PROJECT_OBJECTIVES.md         # Syllabus mapping & project objectives
    ├── SYSTEM_DESIGN.md              # 3-tier architecture, ERD & sequence diagrams
    └── TESTING.md                    # Test strategy, execution report & traceability matrix
```

---

## 12. Installation & Setup

### Prerequisites
- Python 3.8 or higher installed on your machine ([Download Python](https://www.python.org/downloads/)).
- Git installed on your system.

### Step 1: Clone the Repository
```bash
git clone https://github.com/yashkarwa2005/Library-Management.git
cd Library-Management
```

### Step 2: (Optional) Install Dependencies
The application runs completely out-of-the-box using pure Python standard libraries. For optional terminal styling packages:
```bash
pip install -r requirements.txt
```

---

## 13. Running the Application

### Option A: Web Application (Recommended for Comprehensive Exploration)
Launch the standalone web application:
```bash
python app.py
```
Open your browser and navigate to:
- **Main Circulation Portal:** `http://127.0.0.1:5000`
- **Interactive Drag-and-Drop Kanban Board:** `http://127.0.0.1:5000/kanban_board.html`

Pre-seeded accounts for immediate testing:
- **Member Account 1:** Username: `aarav_p` | Password: `aarav123`
- **Member Account 2:** Username: `diya_s` | Password: `diya123` (Pre-seeded with overdue fine)
- **Librarian Account:** Username: `librarian_anita` | Password: `anita123`
- **Admin Account:** Username: `admin` | Password: `admin123`

### Option B: Interactive Terminal Menu
Launch the interactive console:
```bash
python src/main.py
```

### Option C: Instant Automated Viva Demonstration Mode
Execute a complete automated walkthrough of all 12 user stories in under 30 seconds:
```bash
python src/main.py --demo
```

### Option D: Direct Terminal Kanban Board Display
Display the live SQLite-driven ASCII Kanban board directly:
```bash
python src/main.py --kanban
```

---

## 14. Running the Automated Test Suite

To execute the 16 unit and integration test cases:
```bash
python -m unittest discover tests -v
```
or via the CLI flag:
```bash
python src/main.py --test
```

Execution output:
```text
----------------------------------------------------------------------
Ran 16 tests in 0.127s

OK (16 Passed, 0 Failures, 100% Pass Rate)
```

For complete test case specifications and results, see [docs/TESTING.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/docs/TESTING.md).

---

## 15. Future Scope

1. **RFID Hardware Gates:** Integration of UHF RFID antennas for automated hands-free book detection at library exits.
2. **Automated WhatsApp / SMS Gateway:** Automated courtesy notifications sent 24 hours prior to loan expiry.
3. **Digital E-Book Reader Integration:** Support for EPUB/PDF digital checkouts with DRM lending periods.

---

## 16. Academic Declaration & Author

This project was developed by **Annika Jha** for the **B.Tech 3rd-Year Agile Methodologies (AM)** course. All documentation, source code, tests, and Scrum artifacts represent authentic academic implementation designed to demonstrate mastery of Agile and Scrum engineering practices.

- **Author / Scrum Lead:** Annika Jha
- **Academic Course:** Agile Methodologies & IT (AM)
- **Destination Repository:** [https://github.com/yashkarwa2005/Library-Management.git](https://github.com/yashkarwa2005/Library-Management.git)
