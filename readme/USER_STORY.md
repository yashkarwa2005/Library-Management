# User Story Documentation
## Library Management System using Scrum Agile Methodology

---

## 1. What is a User Story?

In Agile and Scrum methodologies, a **User Story** is an informal, natural-language explanation of a software feature articulated from the perspective of the end user or beneficiary. Its primary goal is to encapsulate the *who*, *what*, and *why* of a requirement, shifting the focus from rigid documentation to meaningful stakeholder conversation.

### Standard Agile Format
> **As a** `<type of user>`,  
> **I want** `<some goal / functionality>`,  
> **So that** `<some reason / benefit / business value>`.

### The 3 C's of User Stories
1. **Card**: Physical or digital representation containing the user story statement, identifier, priority, and estimation.
2. **Conversation**: Collaborative discussions between the Product Owner, Scrum Master, and Developers to clarify edge cases and business rules.
3. **Confirmation**: Rigorous Acceptance Criteria confirming that the feature meets the agreed Definition of Done (DoD).

### INVEST Criteria
All user stories in this project adhere strictly to the **INVEST** principle:
- **I**ndependent: Stories are decoupled so that implementation order does not introduce circular blockers.
- **N**egotiable: Scopes and edge cases remain open to refinement during sprint grooming.
- **V**aluable: Delivers measurable utility to student members, librarians, or institutional administrators.
- **E**stimable: Sized using modified Fibonacci points (1, 2, 3, 5, 8, 13) via team Planning Poker.
- **S**mall: Scoped to be reliably completed within a single 1-week sprint iteration.
- **T**estable: Accompanied by verifiable Gherkin Acceptance Criteria ([ACCEPTANCE_CRITERIA.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md)).

---

## 2. User Roles & Personas

| Role | Persona Name | Description & Context |
|---|---|---|
| **Library Member / Student** | Aarav Patel | Undergraduate engineering student who needs 24/7 catalog search, real-time shelf availability inspection, atomic 14-day book loans, self-service renewals, and fine visibility. |
| **Librarian / Catalog Manager** | Anita Roy | Institutional librarian responsible for book acquisition, ISBN cataloging, shelf classification, physical circulation checkouts, returns inspection, and penalty enforcement. |
| **System Administrator** | Vikram Mehta | Academic IT administrator overseeing server health, audit trails, member quotas, fine collection integrity, and relational database health. |
| **Scrum Development Team** | Annika Jha & Dev Team | Scrum Lead / Developer (Annika Jha) driving sprint planning, backlog grooming, SQLite persistence, Python services, and Kanban workflow tracking. |

---

## 3. User Story Inventory & Backlog Mapping

The complete set of 12 User Stories mapped across the 5 Sprints, MoSCoW priorities, and Fibonacci story points:

| Story ID | Story Title | Role | Priority | Story Points | Sprint | Status | Assignee |
|---|---|---|---|---|---|---|---|
| **US-01** | Member Registration & Credential Hashing | Library Member | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done | Annika Jha |
| **US-02** | Role-Based Authentication & Session Management | All Roles | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done | Dev Team |
| **US-03** | Book Catalog Management & Shelf Tracking | Librarian | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done | Dev Team |
| **US-04** | Advanced Book Search & Category Filtering | Library Member | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done | Dev Team |
| **US-05** | Real-time Book Availability & Copy Inspection | Library Member | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done | Dev Team |
| **US-06** | Atomic Book Issue & Concurrency Control | Library Member | 🔴 Must Have | 8 | Sprint 3 | 🟢 Done | Annika Jha |
| **US-07** | Member Loan History & Due Date Overview | Library Member | 🟠 Should Have | 3 | Sprint 3 | 🟢 Done | Dev Team |
| **US-08** | Book Return & Automated Inventory Recovery | Library Member | 🔴 Must Have | 5 | Sprint 3 | 🟢 Done | Dev Team |
| **US-09** | Self-Service Book Renewal & Reservation Queue | Library Member | 🟠 Should Have | 5 | Sprint 4 | 🟢 Done | Annika Jha |
| **US-10** | Automated Overdue Fine Calculation & Settlement | Librarian | 🔴 Must Have | 5 | Sprint 4 | 🟢 Done | Dev Team |
| **US-11** | Centralized Librarian & Admin Inventory Audit | Administrator | 🟢 Could Have | 3 | Sprint 5 | 🟢 Done | Dev Team |
| **US-12** | Built-in Scrum Backlog, Sprint & Terminal Kanban Engine | Scrum Lead | 🔴 Must Have | 8 | Sprint 5 | 🟢 Done | Annika Jha |

**Total Backlog Story Points:** 51 Points (100% Completed in Sprints 1–5).

---

## 4. Detailed User Story Specifications

---

### US-01: Member Registration & Credential Hashing
- **Story ID:** `US-01`
- **Role:** Library Member / Student
- **User Story:**
  > **As a** prospective library member,  
  > **I want** to register an account using my unique username, email, phone number, and password,  
  > **So that** I can securely access institutional catalog borrowing and digital reserve services.
- **Priority:** 🔴 Must Have (MoSCoW)
- **Story Points:** 3 Points
- **Target Sprint:** Sprint 1
- **Assignee:** Annika Jha
- **Acceptance Criteria Reference:** [AC-US01](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us01-member-registration)
- **Description:** Implements input validation, database uniqueness constraints for username and email, and SHA-256 cryptographic password hashing with unique salt string.

---

### US-02: Role-Based Authentication & Session Management
- **Story ID:** `US-02`
- **Role:** All Roles (Member, Librarian, Admin)
- **User Story:**
  > **As a** registered system user,  
  > **I want** to log in using my username and password,  
  > **So that** the application validates my identity and provisions role-specific capabilities.
- **Priority:** 🔴 Must Have (MoSCoW)
- **Story Points:** 3 Points
- **Target Sprint:** Sprint 1
- **Assignee:** Dev Team
- **Acceptance Criteria Reference:** [AC-US02](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us02-role-based-authentication)
- **Description:** Verifies entered password hash against stored hash in the `users` table, establishes session context, and enforces role boundaries (`member`, `librarian`, `admin`).

---

### US-03: Book Catalog Management & Shelf Tracking
- **Story ID:** `US-03`
- **Role:** Librarian
- **User Story:**
  > **As a** librarian,  
  > **I want** to add, edit, and catalog books with ISBN, title, author, category, publisher, year, copy count, and shelf location,  
  > **So that** physical volumes are systematically classified and physical copies are easy to locate in library stacks.
- **Priority:** 🔴 Must Have (MoSCoW)
- **Story Points:** 5 Points
- **Target Sprint:** Sprint 2
- **Assignee:** Dev Team
- **Acceptance Criteria Reference:** [AC-US03](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us03-book-catalog-management)
- **Description:** Manages catalog insertions into the `books` table with unique ISBN constraints, copy count validations, and shelf classification tags (e.g. `Shelf A-12`).

---

### US-04: Advanced Book Search & Category Filtering
- **Story ID:** `US-04`
- **Role:** Library Member / Student
- **User Story:**
  > **As a** student or researcher,  
  > **I want** to search the catalog by title keywords, author name, or category genre,  
  > **So that** I can rapidly locate relevant study materials without manually browsing stacks.
- **Priority:** 🔴 Must Have (MoSCoW)
- **Story Points:** 3 Points
- **Target Sprint:** Sprint 2
- **Assignee:** Dev Team
- **Acceptance Criteria Reference:** [AC-US04](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us04-advanced-book-search)
- **Description:** Implements multi-field case-insensitive query engine with SQL `LIKE` patterns matching titles, authors, and classification categories.

---

### US-05: Real-time Book Availability & Copy Inspection
- **Story ID:** `US-05`
- **Role:** Library Member / Student
- **User Story:**
  > **As a** student,  
  > **I want** to check real-time available copy counts and shelf coordinates prior to visiting circulation desks,  
  > **So that** I do not waste time seeking books that are currently checked out.
- **Priority:** 🔴 Must Have (MoSCoW)
- **Story Points:** 3 Points
- **Target Sprint:** Sprint 2
- **Assignee:** Dev Team
- **Acceptance Criteria Reference:** [AC-US05](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us05-real-time-availability)
- **Description:** Returns live counts of `total_copies`, `available_copies`, active borrow count, and shelf location from the database.

---

### US-06: Atomic Book Issue & Concurrency Control
- **Story ID:** `US-06`
- **Role:** Library Member / Student
- **User Story:**
  > **As a** library member,  
  > **I want** to borrow an available book with an immediate 14-day checkout due date,  
  > **So that** the copy is atomically locked to my account and cannot be double-issued to another user.
- **Priority:** 🔴 Must Have (MoSCoW)
- **Story Points:** 8 Points
- **Target Sprint:** Sprint 3
- **Assignee:** Annika Jha
- **Acceptance Criteria Reference:** [AC-US06](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us06-atomic-book-issue)
- **Description:** Executes ACID transaction: verifies available copies > 0, enforces 3-book checkout quota, blocks users with outstanding fines, decrements available copy count, and creates a `borrow_records` entry.

---

### US-07: Member Loan History & Due Date Overview
- **Story ID:** `US-07`
- **Role:** Library Member / Student
- **User Story:**
  > **As a** library member,  
  > **I want** to view my active checkouts, return timestamps, and countdown to due dates,  
  > **So that** I can return books punctually and prevent late penalty fines.
- **Priority:** 🟠 Should Have (MoSCoW)
- **Story Points:** 3 Points
- **Target Sprint:** Sprint 3
- **Assignee:** Dev Team
- **Acceptance Criteria Reference:** [AC-US07](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us07-loan-history)
- **Description:** Queries `borrow_records` joining `books` by `user_id`, calculating overdue days dynamically for pending loans.

---

### US-08: Book Return & Automated Inventory Recovery
- **Story ID:** `US-08`
- **Role:** Library Member / Student
- **User Story:**
  > **As a** library member,  
  > **I want** to return a borrowed book and have the inventory count restored instantaneously,  
  > **So that** other students can immediately borrow or reserve the returned title.
- **Priority:** 🔴 Must Have (MoSCoW)
- **Story Points:** 5 Points
- **Target Sprint:** Sprint 3
- **Assignee:** Dev Team
- **Acceptance Criteria Reference:** [AC-US08](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us08-book-return)
- **Description:** Updates loan status to `Returned`, sets return timestamp, increments `available_copies` on the `books` table, and automatically triggers reservation fulfillment checks.

---

### US-09: Self-Service Book Renewal & Reservation Queue
- **Story ID:** `US-09`
- **Role:** Library Member / Student
- **User Story:**
  > **As a** library member,  
  > **I want** to renew an unreserved active loan for 14 additional days or reserve an out-of-stock book,  
  > **So that** I can extend my research period or hold the next available returned copy.
- **Priority:** 🟠 Should Have (MoSCoW)
- **Story Points:** 5 Points
- **Target Sprint:** Sprint 4
- **Assignee:** Annika Jha
- **Acceptance Criteria Reference:** [AC-US09](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us09-renewal-and-reservation)
- **Description:** Enforces a 2-renewal cap, validates absence of pending reservations before extending due dates, and manages FIFO reservation queue for out-of-stock books.

---

### US-10: Automated Overdue Fine Calculation & Settlement
- **Story ID:** `US-10`
- **Role:** Librarian
- **User Story:**
  > **As a** librarian,  
  > **I want** the system to compute late fees at ₹5 per calendar day past due date upon return and support fee payment,  
  > **So that** overdue delays are deterred and financial records remain transparent.
- **Priority:** 🔴 Must Have (MoSCoW)
- **Story Points:** 5 Points
- **Target Sprint:** Sprint 4
- **Assignee:** Dev Team
- **Acceptance Criteria Reference:** [AC-US10](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us10-overdue-fines)
- **Description:** Calculates `overdue_days * 5.0` on return transactions, logs entries in the `fines` table, blocks delinquent borrowers, and supports payment updates.

---

### US-11: Centralized Librarian & Admin Inventory Audit
- **Story ID:** `US-11`
- **Role:** System Administrator
- **User Story:**
  > **As an** administrator,  
  > **I want** to view aggregate circulation metrics, total volumes, active loans, overdue lists, and audit events,  
  > **So that** I can maintain institutional governance and inventory accountability.
- **Priority:** 🟢 Could Have (MoSCoW)
- **Story Points:** 3 Points
- **Target Sprint:** Sprint 5
- **Assignee:** Dev Team
- **Acceptance Criteria Reference:** [AC-US11](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us11-admin-audit)
- **Description:** Consolidates library inventory metrics, circulation turnover, collected fine balances, and audit logs.

---

### US-12: Built-in Scrum Backlog, Sprint & Terminal Kanban Engine
- **Story ID:** `US-12`
- **Role:** Scrum Lead / Developer
- **User Story:**
  > **As a** Scrum team member,  
  > **I want** to track user stories, sprint velocity, and Kanban workflows directly inside the application,  
  > **So that** the project demonstrates transparent Agile engineering and live traceability.
- **Priority:** 🔴 Must Have (MoSCoW)
- **Story Points:** 8 Points
- **Target Sprint:** Sprint 5
- **Assignee:** Annika Jha
- **Acceptance Criteria Reference:** [AC-US12](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us12-scrum-kanban-engine)
- **Description:** Implements persistent `sprints`, `user_stories`, and `action_items` tables, an ASCII terminal Kanban board with 5 columns, and real-time backlog progress calculations.
