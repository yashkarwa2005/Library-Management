# Sprint Plan (5-Week Scrum Iteration Schedule)
## Library Management System using Scrum Agile Methodology

---

## 1. Scrum Sprint Cadence & Roles

The project was executed across **5 weekly Scrum Sprints** (7 calendar days per iteration).

### Scrum Team Roles & Responsibilities
- **Product Owner & Scrum Lead (Annika Jha):** Defines product backlog priorities, authors INVEST user stories, facilitates sprint ceremonies, and validates deliverables against Acceptance Criteria.
- **Development Team (Annika Jha & Dev Team):** Multi-disciplinary engineering team responsible for relational SQLite schema design, Python service layer, CLI interface, and automated test automation.

---

## 2. Weekly Sprint Breakdown

---

### 🚀 SPRINT 1 (Week 1)
**Theme:** User Authentication, Profile Management & Core Infrastructure

- **Sprint Goal:** Establish the relational SQLite schema and deliver secure member registration and session authentication with salted SHA-256 password hashing.
- **Sprint Duration:** Week 1 (Day 1 – Day 7)
- **Committed Points:** 6 Points | **Completed Points:** 6 Points | **Velocity:** 6 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 1:
| Story ID | Story Title | Priority | Story Points | Assignee | Status |
|---|---|---|---|---|---|
| `US-01` | Member Registration & Credential Hashing | 🔴 Must Have | 3 | Annika Jha | 🟢 Done |
| `US-02` | Role-Based Authentication & Session Management | 🔴 Must Have | 3 | Dev Team | 🟢 Done |

#### Sprint 1 Task Breakdown:
1. Initialize repository structure, `.gitignore`, and Git remote. (Owner: Annika Jha, Est: 2h)
2. Design and implement `src/database.py` with `users` table and foreign key support. (Owner: Dev Team, Est: 3h)
3. Implement password hashing using SHA-256 with salt in `src/database.py`. (Owner: Annika Jha, Est: 2h)
4. Implement `register_user` and `login_user` methods in `src/library.py`. (Owner: Dev Team, Est: 3h)
5. Write and execute test cases `TC-01`, `TC-02`, `TC-03`, `TC-04` in `tests/test_library.py`. (Owner: Annika Jha, Est: 2h)

- **Expected Increment:** Working authentication engine where users can register with unique usernames/emails, passwords are encrypted, and logins return valid user sessions.
- **Actual Increment Delivered:** 100% completed, zero defects.

---

### 🚀 SPRINT 2 (Week 2)
**Theme:** Catalog Management, Advanced Search & Shelf Tracking

- **Sprint Goal:** Deliver book catalog persistence, shelf location coordinates, multi-genre classification, and case-insensitive keyword search.
- **Sprint Duration:** Week 2 (Day 8 – Day 14)
- **Committed Points:** 11 Points | **Completed Points:** 11 Points | **Velocity:** 11 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 2:
| Story ID | Story Title | Priority | Story Points | Assignee | Status |
|---|---|---|---|---|---|
| `US-03` | Book Catalog Management & Shelf Tracking | 🔴 Must Have | 5 | Dev Team | 🟢 Done |
| `US-04` | Advanced Book Search & Category Filtering | 🔴 Must Have | 3 | Dev Team | 🟢 Done |
| `US-05` | Real-time Book Availability & Copy Inspection | 🔴 Must Have | 3 | Dev Team | 🟢 Done |

#### Sprint 2 Task Breakdown:
1. Create `books` table schema with unique ISBN and copy counts in `src/database.py`. (Owner: Dev Team, Est: 3h)
2. Implement `add_book`, `update_book`, and `get_all_books` in `src/library.py`. (Owner: Dev Team, Est: 3h)
3. Implement `search_books` with SQL `LIKE` wildcard filters matching titles, authors, and categories. (Owner: Dev Team, Est: 3h)
4. Seed realistic academic textbook catalog spanning Computer Science, AI, and Systems. (Owner: Annika Jha, Est: 2h)
5. Write and execute unit test cases `TC-05`, `TC-06`, `TC-07` in `tests/test_library.py`. (Owner: Annika Jha, Est: 2h)

- **Expected Increment:** A searchable textbook catalog showing real-time total vs available copies and physical shelf locations.
- **Actual Increment Delivered:** 100% completed, verified across multiple subject genres.

---

### 🚀 SPRINT 3 (Week 3)
**Theme:** Circulation Engine: Atomic Issue, Quotas & Return

- **Sprint Goal:** Implement transactional book checkouts, concurrency protection against over-borrowing, member loan quotas (max 3 books), and inventory recovery upon return.
- **Sprint Duration:** Week 3 (Day 15 – Day 21)
- **Committed Points:** 16 Points | **Completed Points:** 16 Points | **Velocity:** 16 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 3:
| Story ID | Story Title | Priority | Story Points | Assignee | Status |
|---|---|---|---|---|---|
| `US-06` | Atomic Book Issue & Concurrency Control | 🔴 Must Have | 8 | Annika Jha | 🟢 Done |
| `US-07` | Member Loan History & Due Date Overview | 🟠 Should Have | 3 | Dev Team | 🟢 Done |
| `US-08` | Book Return & Automated Inventory Recovery | 🔴 Must Have | 5 | Dev Team | 🟢 Done |

#### Sprint 3 Task Breakdown:
1. Create `borrow_records` schema with foreign key relationships. (Owner: Dev Team, Est: 2h)
2. Implement `borrow_book` with atomic available copy decrement and 14-day due date calculation. (Owner: Annika Jha, Est: 4h)
3. Add defensive quota guard rejecting checkouts when a member holds 3 active books. (Owner: Annika Jha, Est: 2h)
4. Build `return_book` method with atomic stock restoration. (Owner: Dev Team, Est: 3h)
5. Construct member loan query `get_member_loans` with dynamic overdue indicators. (Owner: Dev Team, Est: 2h)
6. Write test cases `TC-08`, `TC-09`, `TC-10`, `TC-11`, `TC-12` in `tests/test_library.py`. (Owner: Annika Jha, Est: 3h)

- **Expected Increment:** End-to-end borrowing and return lifecycle with zero risk of stock count inconsistencies.
- **Actual Increment Delivered:** 100% completed, transactional integrity verified.

---

### 🚀 SPRINT 4 (Week 4)
**Theme:** Lifecycle Extensions: Renewals, Reservations & Overdue Penalties

- **Sprint Goal:** Enable self-service loan extensions, out-of-stock reservation queue, and automated late fee calculation (₹5/day).
- **Sprint Duration:** Week 4 (Day 22 – Day 28)
- **Committed Points:** 10 Points | **Completed Points:** 10 Points | **Velocity:** 10 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 4:
| Story ID | Story Title | Priority | Story Points | Assignee | Status |
|---|---|---|---|---|---|
| `US-09` | Self-Service Book Renewal & Reservation Queue | 🟠 Should Have | 5 | Annika Jha | 🟢 Done |
| `US-10` | Automated Overdue Fine Calculation & Settlement | 🔴 Must Have | 5 | Dev Team | 🟢 Done |

#### Sprint 4 Task Breakdown:
1. Create `reservations` and `fines` schemas in `src/database.py`. (Owner: Dev Team, Est: 2h)
2. Implement `renew_book` enforcing a 2-renewal cap and checking for reservation holds. (Owner: Annika Jha, Est: 3h)
3. Implement `reserve_book` for out-of-stock titles and auto-fulfillment trigger upon return. (Owner: Annika Jha, Est: 3h)
4. Implement automatic fine assessment on late returns (₹5/day) and fee payment settlement. (Owner: Dev Team, Est: 3h)
5. Block delinquent members with unpaid fines from checking out additional books. (Owner: Annika Jha, Est: 2h)
6. Write test cases `TC-13`, `TC-14`, `TC-15` in `tests/test_library.py`. (Owner: Annika Jha, Est: 2h)

- **Expected Increment:** Complete financial and lifecycle management preventing stranded books and overdue losses.
- **Actual Increment Delivered:** 100% completed, fines and reservations fully operational.

---

### 🚀 SPRINT 5 (Week 5)
**Theme:** In-App Scrum Tooling, Auditing, Testing & Viva Release

- **Sprint Goal:** Integrate persistent SQLite Scrum tables, terminal ASCII Kanban board, interactive web dashboard, automated test suite, and viva demonstration mode.
- **Sprint Duration:** Week 5 (Day 29 – Day 35)
- **Committed Points:** 11 Points | **Completed Points:** 11 Points | **Velocity:** 11 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 5:
| Story ID | Story Title | Priority | Story Points | Assignee | Status |
|---|---|---|---|---|---|
| `US-11` | Centralized Librarian & Admin Inventory Audit | 🟢 Could Have | 3 | Dev Team | 🟢 Done |
| `US-12` | Built-in Scrum Backlog, Sprint & Terminal Kanban Engine | 🔴 Must Have | 8 | Annika Jha | 🟢 Done |

#### Sprint 5 Task Breakdown:
1. Create `sprints`, `user_stories`, and `action_items` tables in `src/database.py`. (Owner: Annika Jha, Est: 3h)
2. Implement `UserStoryService`, `SprintService`, and `ActionItemService`. (Owner: Annika Jha, Est: 4h)
3. Build ASCII terminal Kanban board renderer (`src/kanban.py`). (Owner: Annika Jha, Est: 4h)
4. Develop automated viva demonstration mode (`--demo`) in `src/main.py`. (Owner: Annika Jha, Est: 3h)
5. Construct standalone Python web server (`app.py`) with REST API and web UI (`templates/index.html`). (Owner: Annika Jha, Est: 5h)
6. Build interactive HTML5 drag-and-drop Kanban board (`kanban_board.html`). (Owner: Annika Jha, Est: 3h)
7. Finalize automated test case `TC-16` and conduct end-to-end regression testing. (Owner: Annika Jha, Est: 2h)

- **Expected Increment:** Production-ready shippable release with full Agile documentation and instant viva walkthrough capability.
- **Actual Increment Delivered:** 100% completed, all 16 tests passing, zero defects.

---

## 3. Sprint Velocity Summary

```text
+----------+--------------------------------------------------+-----------+-----------+----------+
| Sprint   | Iteration Theme                                  | Committed | Completed | Velocity |
+----------+--------------------------------------------------+-----------+-----------+----------+
| Sprint 1 | Security & Identity Management                   | 6 pts     | 6 pts     | 6 pts    |
| Sprint 2 | Catalog Management & Availability                | 11 pts    | 11 pts    | 11 pts   |
| Sprint 3 | Circulation Engine & Concurrency Control         | 16 pts    | 16 pts    | 16 pts   |
| Sprint 4 | Renewals, Reservations & Overdue Fines           | 10 pts    | 10 pts    | 10 pts   |
| Sprint 5 | In-App Scrum Tooling, Auditing & Release         | 11 pts    | 11 pts    | 11 pts   |
+----------+--------------------------------------------------+-----------+-----------+----------+
| TOTAL    | Cumulative 5-Week Velocity                       | 54 pts    | 54 pts    | 54 pts   |
+----------+--------------------------------------------------+-----------+-----------+----------+
```
*(Average Team Velocity: 10.8 Story Points per Sprint)*
