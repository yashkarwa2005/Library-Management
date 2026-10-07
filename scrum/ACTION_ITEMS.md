# Action Items Register
## Library Management System using Scrum Agile Methodology

---

## 1. Action Items Management in Scrum

In Scrum, **Action Items** represent concrete, owner-assigned engineering tasks identified during **Sprint Planning**, **Daily Scrum**, and **Sprint Retrospectives**. They serve to track actionable development commitments, eliminate team impediments, and drive continuous process improvements (Kaizen).

### Status Indicators:
- 🔵 **To Do:** Queued for implementation in the current iteration.
- 🟡 **In Progress:** Actively under development.
- 🟣 **Review / Testing:** Implementation complete; awaiting code review or automated test verification.
- 🟢 **Done:** Verified against the Definition of Done (DoD).
- 🔴 **Blocked:** Halted pending external dependency resolution.

---

## 2. Weekly Action Items Register

| ID | Action Item Description | Sprint | Owner | Priority | Due Date | Status |
|---|---|---|---|---|---|---|
| **AI-01** | Initialize Git repository structure, `.gitignore`, and licensing | Sprint 1 | Annika Jha | 🔴 High | Week 1 - Day 2 | 🟢 Done |
| **AI-02** | Design normalized SQLite schema with foreign key enforcement | Sprint 1 | Dev Team | 🔴 High | Week 1 - Day 4 | 🟢 Done |
| **AI-03** | Implement SHA-256 password salting and authentication module | Sprint 1 | Annika Jha | 🔴 High | Week 1 - Day 5 | 🟢 Done |
| **AI-04** | Draft User Story and Gherkin Acceptance Criteria specifications | Sprint 1 | Annika Jha | 🟠 Medium | Week 1 - Day 6 | 🟢 Done |
| **AI-05** | Develop book catalog data model with unique ISBN and shelf tags | Sprint 2 | Dev Team | 🔴 High | Week 2 - Day 2 | 🟢 Done |
| **AI-06** | Implement case-insensitive book search and category filters | Sprint 2 | Dev Team | 🔴 High | Week 2 - Day 4 | 🟢 Done |
| **AI-07** | Populate initial academic textbook catalog across computer science | Sprint 2 | Dev Team | 🟢 Low | Week 2 - Day 6 | 🟢 Done |
| **AI-08** | Construct atomic book borrow engine with concurrency protection | Sprint 3 | Annika Jha | 🔴 High | Week 3 - Day 3 | 🟢 Done |
| **AI-09** | Enforce member borrowing quota (max 3 books) and fine restriction | Sprint 3 | Annika Jha | 🔴 High | Week 3 - Day 4 | 🟢 Done |
| **AI-10** | Implement book return workflow with automatic inventory replenishment | Sprint 3 | Dev Team | 🔴 High | Week 3 - Day 5 | 🟢 Done |
| **AI-11** | Build member loan history and active checkouts dashboard query | Sprint 3 | Dev Team | 🟠 Medium | Week 3 - Day 6 | 🟢 Done |
| **AI-12** | Develop 14-day book loan renewal logic with reservation conflict guard | Sprint 4 | Annika Jha | 🔴 High | Week 4 - Day 3 | 🟢 Done |
| **AI-13** | Implement out-of-stock reservation queue for unavailable books | Sprint 4 | Dev Team | 🟠 Medium | Week 4 - Day 4 | 🟢 Done |
| **AI-14** | Create overdue fine calculation engine (₹5/day) and payment settlement | Sprint 4 | Dev Team | 🔴 High | Week 4 - Day 6 | 🟢 Done |
| **AI-15** | Implement in-app Scrum management database tables and service layer | Sprint 5 | Annika Jha | 🔴 High | Week 5 - Day 2 | 🟢 Done |
| **AI-16** | Construct 5-column ANSI terminal ASCII Kanban board renderer | Sprint 5 | Annika Jha | 🔴 High | Week 5 - Day 3 | 🟢 Done |
| **AI-17** | Implement comprehensive 16-case automated test suite with 100% pass rate | Sprint 5 | Annika Jha | 🔴 High | Week 5 - Day 4 | 🟢 Done |
| **AI-18** | Conduct Sprint Review, Retrospective, and final Viva demo rehearsal | Sprint 5 | Annika Jha | 🔴 High | Week 5 - Day 6 | 🟢 Done |

---

## 3. Retrospective Continuous Improvement Action Items (Kaizen)

The following action items originated directly from Sprint Retrospectives to drive systematic engineering enhancements:

| Source Ceremony | Identified Problem / Friction | Agreed Improvement Action | Owner | Outcome / Resolution |
|---|---|---|---|---|
| **Sprint 1 Retrospective** | Manual database resets slowed down local testing | Introduce automated `seed_initial_data()` on application launch | Annika Jha | Implemented in `src/database.py`; seed loads in <0.05s. |
| **Sprint 2 Retrospective** | Search queries failed when user typed mixed-case titles | Force lowercase comparison via `LOWER(title)` and `LOWER(author)` | Dev Team | Applied in `search_books()`; 100% case-insensitive matching. |
| **Sprint 3 Retrospective** | Over-borrowing risk if multiple students checked out simultaneously | Enforce explicit SQLite transaction rollback and stock lock check | Annika Jha | Zero concurrency collisions verified in `TC-08` and `TC-09`. |
| **Sprint 4 Retrospective** | Complex CLI inputs caused demonstration typos during practice | Add automated `--demo` flag for instant 30-second viva walkthrough | Annika Jha | Created one-command automated walkthrough in `src/main.py`. |
| **Sprint 5 Retrospective** | Evaluating examiner may prefer browser over terminal | Create standalone zero-dependency Python web application (`app.py`) | Annika Jha | Embedded HTTP web server on port 5000 with rich UI. |
