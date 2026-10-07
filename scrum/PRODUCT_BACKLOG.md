# Product Backlog
## Library Management System using Scrum Agile Methodology

---

## 1. Product Vision & Backlog Strategy

### Vision Statement
> *"To engineer a high-reliability, zero-friction academic Library Management System that empowers students to discover textbooks, inspect real-time shelf availability, and execute atomic checkouts, renewals, and fine settlements, while exemplifying disciplined Scrum Agile software engineering practices."*

### Product Backlog Overview
The **Product Backlog** is an emergent, prioritized inventory of deliverables and capabilities required to realize the product vision. In adherence to Scrum principles, the backlog is maintained and prioritized by the **Product Owner / Scrum Lead (Annika Jha)** based on:
1. **Business Value & User Utility:** Core circulation and authentication capabilities take highest precedence.
2. **Technical Architecture & Concurrency Risk:** Transactional integrity and copy count decrement concurrency are solved early.
3. **MoSCoW Prioritization:** Strict segregation of Must Have, Should Have, and Could Have requirements.

---

## 2. Product Epics & Architecture Themes

```text
+-----------------------------------------------------------------------------------------+
|                                PRODUCT BACKLOG EPICS                                    |
+-----------------------------------------------------------------------------------------+
     |
     +---> EPIC 1: Security & Identity Management (US-01, US-02)
     +---> EPIC 2: Catalog & Real-Time Availability (US-03, US-04, US-05)
     +---> EPIC 3: Circulation Engine & Concurrency Control (US-06, US-07, US-08)
     +---> EPIC 4: Lifecycle Extensions & Financial Compliance (US-09, US-10)
     +---> EPIC 5: Governance, Auditing & Agile Tooling (US-11, US-12)
```

---

## 3. Prioritized Product Backlog Inventory

| Backlog Rank | Story ID | Title & Epic | Role | Priority | Story Points | Sprint Target | Status |
|---|---|---|---|---|---|---|---|
| **01** | `US-01` | Member Registration & Credential Hashing (Epic 1) | Member | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done |
| **02** | `US-02` | Role-Based Authentication & Session Management (Epic 1) | All Roles | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done |
| **03** | `US-03` | Book Catalog Management & Shelf Tracking (Epic 2) | Librarian | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done |
| **04** | `US-04` | Advanced Book Search & Category Filtering (Epic 2) | Member | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done |
| **05** | `US-05` | Real-time Book Availability & Copy Inspection (Epic 2) | Member | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done |
| **06** | `US-06` | Atomic Book Issue & Concurrency Control (Epic 3) | Member | 🔴 Must Have | 8 | Sprint 3 | 🟢 Done |
| **07** | `US-07` | Member Loan History & Due Date Overview (Epic 3) | Member | 🟠 Should Have | 3 | Sprint 3 | 🟢 Done |
| **08** | `US-08` | Book Return & Automated Inventory Recovery (Epic 3) | Member | 🔴 Must Have | 5 | Sprint 3 | 🟢 Done |
| **09** | `US-09` | Self-Service Book Renewal & Reservation Queue (Epic 4) | Member | 🟠 Should Have | 5 | Sprint 4 | 🟢 Done |
| **10** | `US-10` | Automated Overdue Fine Calculation & Settlement (Epic 4) | Librarian | 🔴 Must Have | 5 | Sprint 4 | 🟢 Done |
| **11** | `US-11` | Centralized Librarian & Admin Inventory Audit (Epic 5) | Administrator | 🟢 Could Have | 3 | Sprint 5 | 🟢 Done |
| **12** | `US-12` | Built-in Scrum Backlog, Sprint & Terminal Kanban Engine (Epic 5) | Scrum Lead | 🔴 Must Have | 8 | Sprint 5 | 🟢 Done |

**Total Backlog Effort:** 51 Story Points  
**Estimation Technique:** Modified Fibonacci Scale (1, 2, 3, 5, 8, 13) via Planning Poker.

---

## 4. Backlog Refinement (Grooming) Ceremonies

Throughout the 5-week project lifecycle, continuous backlog grooming ensured stories remained ready for sprint planning:
1. **Decomposing Circulation Monolith:** The initial generic story *"Manage Circulation"* was split into three independent stories: `US-06 (Borrow/Issue)`, `US-08 (Return & Recovery)`, and `US-09 (Renewal & Reservation)`.
2. **Strengthening Concurrency Constraints:** Following team review of potential race conditions when only 1 copy remains in stock, `US-06` was re-estimated from 5 to 8 story points to account for defensive transactional rollback logic.
3. **Decoupling Fine Accounting:** Late return fee computation (`US-10`) was established as an automated trigger inside the return workflow rather than a disconnected manual process.

---

## 5. Artifact Traceability
- Detailed User Stories: [readme/USER_STORY.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md)
- Verifiable Acceptance Criteria: [readme/ACCEPTANCE_CRITERIA.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md)
- Sprint Allocation: [scrum/SPRINT_PLAN.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/SPRINT_PLAN.md)
