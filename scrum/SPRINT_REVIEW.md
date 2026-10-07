# Sprint Review Reports
## Library Management System using Scrum Agile Methodology

---

## 1. Purpose of the Sprint Review

In Scrum Agile software development, the **Sprint Review** ceremony is held at the conclusion of each sprint iteration. The Scrum Team inspects the potentially shippable increment, demonstrates working software functionality to stakeholders, and validates delivered features against the formal Acceptance Criteria.

---

## 2. Sprint 1 Review Report

- **Date:** Week 1, Day 7
- **Sprint Theme:** Security, Identity Management & SQLite Schema
- **Attendees:** Product Owner / Scrum Lead (Annika Jha), Dev Team
- **Demo Agenda:**
  1. Live demonstration of new member registration with username, email, and password.
  2. Inspection of database verifying that passwords are saved as salted SHA-256 hashes (`password_hash`).
  3. Demonstration of user authentication and role session provision (`member`, `librarian`, `admin`).
- **User Stories Evaluated:**
  - `US-01` (Member Registration): Accepted 🟢 — Unique constraints and hashing verified.
  - `US-02` (Authentication & Session): Accepted 🟢 — Invalid passwords cleanly rejected.
- **Velocity Metrics:**
  - Committed: 6 pts | Completed: 6 pts | Completion: 100%
- **Stakeholder Feedback:** The authentication mechanism is robust. Stakeholders recommended adding quick test login shortcuts for smooth examination demonstrations. Incorporated into the UI.

---

## 3. Sprint 2 Review Report

- **Date:** Week 2, Day 7
- **Sprint Theme:** Catalog Management, Advanced Search & Availability
- **Attendees:** Product Owner / Scrum Lead (Annika Jha), Dev Team
- **Demo Agenda:**
  1. Demonstration of catalog insertion with unique ISBN validation and physical shelf tags (`Shelf A-12`).
  2. Demonstration of multi-keyword search matching title, author, and category.
  3. Real-time inspection of total copies versus currently available stock counts.
- **User Stories Evaluated:**
  - `US-03` (Catalog Management): Accepted 🟢 — Duplicate ISBN cleanly blocked.
  - `US-04` (Advanced Search): Accepted 🟢 — Case-insensitive keyword matching verified.
  - `US-05` (Availability Query): Accepted 🟢 — Live stock count calculations confirmed.
- **Velocity Metrics:**
  - Committed: 11 pts | Completed: 11 pts | Completion: 100%
- **Stakeholder Feedback:** Search results should clearly display the shelf coordinates to help students locate books immediately. Incorporated into output.

---

## 4. Sprint 3 Review Report

- **Date:** Week 3, Day 7
- **Sprint Theme:** Circulation Engine: Atomic Issue, Quotas & Returns
- **Attendees:** Product Owner / Scrum Lead (Annika Jha), Dev Team
- **Demo Agenda:**
  1. Atomic checkout of available books with automatic 14-day due date generation.
  2. Attempting to borrow a 4th book to demonstrate enforcement of the 3-book member borrowing quota.
  3. Attempting to borrow an out-of-stock book to demonstrate stock exhaustion handling.
  4. Returning a borrowed volume and verifying instantaneous inventory recovery (`available_copies + 1`).
- **User Stories Evaluated:**
  - `US-06` (Atomic Issue & Concurrency): Accepted 🟢 — Defensive transaction lock verified.
  - `US-07` (Loan History Ledger): Accepted 🟢 — Active checkouts and due dates rendered accurately.
  - `US-08` (Return & Recovery): Accepted 🟢 — Inventory restored immediately.
- **Velocity Metrics:**
  - Committed: 16 pts | Completed: 16 pts | Completion: 100%
- **Stakeholder Feedback:** Outstanding concurrency control; the 3-book quota effectively deters book hoarding.

---

## 5. Sprint 4 Review Report

- **Date:** Week 4, Day 7
- **Sprint Theme:** Lifecycle Extensions: Renewals, Reservations & Overdue Fines
- **Attendees:** Product Owner / Scrum Lead (Annika Jha), Dev Team
- **Demo Agenda:**
  1. Self-service renewal extending due date by 14 days; testing rejection after 2 renewals.
  2. Placing a reservation hold on an out-of-stock book and verifying rejection of renewal by current borrower.
  3. Returning a synthetic overdue loan and demonstrating automated calculation of ₹5/day penalty.
  4. Settling an outstanding fine and verifying status update to `Paid`.
- **User Stories Evaluated:**
  - `US-09` (Renewals & Reservations): Accepted 🟢 — Hold queue and renewal caps operational.
  - `US-10` (Overdue Fine Settlement): Accepted 🟢 — Penalty calculations and payments verified.
- **Velocity Metrics:**
  - Committed: 10 pts | Completed: 10 pts | Completion: 100%
- **Stakeholder Feedback:** The automatic fine assessment upon return is clean and prevents discretionary errors by circulation staff.

---

## 6. Sprint 5 Review Report

- **Date:** Week 5, Day 7
- **Sprint Theme:** In-App Scrum Tooling, Auditing, Testing & Viva Release
- **Attendees:** Product Owner / Scrum Lead (Annika Jha), Dev Team
- **Demo Agenda:**
  1. Demonstration of built-in SQLite Scrum tables, terminal ASCII Kanban board (`python src/main.py --kanban`).
  2. Demonstration of instant 30-second automated viva walkthrough (`python src/main.py --demo`).
  3. Execution of full 16-case automated test suite (`python -m unittest discover tests -v`) with 100% pass rate.
  4. Inspection of browser-based web dashboard (`app.py`) and drag-and-drop web Kanban board (`kanban_board.html`).
- **User Stories Evaluated:**
  - `US-11` (Admin Inventory Audit): Accepted 🟢 — System-wide health metrics verified.
  - `US-12` (In-App Scrum Kanban Engine): Accepted 🟢 — ASCII board and backlog metrics verified.
- **Velocity Metrics:**
  - Committed: 11 pts | Completed: 11 pts | Completion: 100%
- **Stakeholder Feedback:** Final increment exceeds academic requirements. Dual-track architecture (Library Engine + In-App Scrum Tooling) provides exceptional pedagogical value.
