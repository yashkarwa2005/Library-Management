# Project Objectives & Agile Syllabus Mapping
## Library Management System using Scrum Agile Methodology

---

## 1. Project Background & Academic Context

This project is developed as an academic **Project-Based Learning (PBL)** submission for the **B.Tech 3rd-Year Agile Methodologies (AM)** curriculum. 

- **Student / Scrum Lead:** Annika Jha
- **Degree / Year:** B.Tech Computer Science & Engineering (3rd Year)
- **Subject / Course:** Agile Methodologies & IT (AM)
- **Target Repository:** [yashkarwa2005/Library-Management](https://github.com/yashkarwa2005/Library-Management.git)

The core objective is twofold:
1. **Domain Problem Solution:** Deliver an intuitive, high-reliability academic Library Management System empowering students to search textbooks, inspect real-time shelf availability, and execute atomic checkouts, returns, renewals, reservations, and fine settlements.
2. **Pedagogical Demonstration:** Execute the software engineering lifecycle strictly following the **Scrum Agile Methodology**, generating verifiable industry-standard artifacts and integrating Scrum project management directly into the delivered software.

---

## 2. Core Project Objectives

### Technical Objectives
- **Zero Stock Inconsistency Guarantee:** Implement transactional integrity in database operations so that book copies are never double-issued or decremented below zero.
- **Dynamic Catalog & Availability Search:** Enable members to perform case-insensitive keyword searches across titles, authors, and categories while viewing live shelf coordinates and stock counts.
- **Full Circulation Lifecycle Management:** Support self-service borrowing, punctual returns, 14-day renewals, out-of-stock reservation queuing, and automated late penalty calculations (₹5/day).
- **Portability & Zero Friction:** Engineer using pure Python standard libraries (`sqlite3`, `http.server`, `hashlib`, `unittest`) to run flawlessly on any academic evaluation workstation without third-party dependencies.

### Agile Methodology Objectives
- **Scrum Framework Mastery:** Apply Scrum roles (Product Owner, Scrum Master, Developers), ceremonies (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective), and artifacts (Product Backlog, Sprint Backlog, Shippable Increment).
- **Iterative & Incremental Delivery:** Partition system requirements into 5 weekly sprints, delivering demonstrable vertical slices each week.
- **Transparent Work Visualization:** Implement visual tracking using both Markdown and built-in CLI/Web Kanban boards.
- **Continuous Quality Assurance:** Couple every user story with testable Acceptance Criteria and automated unit tests satisfying the Definition of Done (DoD).

---

## 3. Direct Mapping to Agile Methodologies (AM) Syllabus

| Syllabus Concept | How Implemented in Project | Key Project Artifacts |
|---|---|---|
| **Agile Software Development** | Developed incrementally across 5 distinct sprints; responsive to feedback and iterative design. | [docs/SYSTEM_DESIGN.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/docs/SYSTEM_DESIGN.md) |
| **Scrum Roles** | Clearly partitioned duties among Product Owner, Scrum Master, and Developers. | [scrum/SPRINT_PLAN.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/SPRINT_PLAN.md) |
| **User Stories** | Formatted using standard Agile template (`As a... I want... So that...`) satisfying INVEST criteria. | [readme/USER_STORY.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md) |
| **Acceptance Criteria** | Formulated using Gherkin syntax (`Given - When - Then`) with verifiable edge cases. | [readme/ACCEPTANCE_CRITERIA.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md) |
| **Product Backlog** | Comprehensive list of ranked user stories with story points estimated via Planning Poker. | [scrum/PRODUCT_BACKLOG.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/PRODUCT_BACKLOG.md) |
| **Requirement Prioritization** | Formalized using MoSCoW (🔴 Must Have, 🟠 Should Have, 🟢 Could Have, ⚪ Won't Have). | [scrum/REQUIREMENT_PRIORITIES.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/REQUIREMENT_PRIORITIES.md) |
| **Sprint Planning** | Structured into 5 one-week sprints with defined goals, tasks, story point commitments, and velocity. | [scrum/SPRINT_PLAN.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/SPRINT_PLAN.md) |
| **Sprint Execution** | Tracked via daily standup logs and in-app status transitions. | `src/sprint.py`, `src/action_item.py` |
| **Sprint Review** | Formal review records for each sprint evaluating completed increments with stakeholder feedback. | [scrum/SPRINT_REVIEW.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/SPRINT_REVIEW.md) |
| **Sprint Retrospective** | Structured "What went well / What didn't / Improvements" sessions driving real process changes. | [scrum/SPRINT_RETROSPECTIVE.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/SPRINT_RETROSPECTIVE.md) |
| **Action Items** | Weekly register tracking tasks with owners, due dates, priorities, and statuses. | [scrum/ACTION_ITEMS.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/ACTION_ITEMS.md) |
| **Kanban Board** | 5-stage visual board (`Backlog -> Todo -> In Progress -> Review -> Done`) in Markdown, Web & Python CLI. | [scrum/KANBAN_BOARD.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/KANBAN_BOARD.md), `src/kanban.py` |
| **Continuous Improvement** | Measured velocity stabilization and architectural refinements across sprints. | [scrum/SPRINT_RETROSPECTIVE.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/SPRINT_RETROSPECTIVE.md) |
| **Automated Testing** | 16 automated unit test cases mapped directly to acceptance criteria with 100% pass rate. | [docs/TESTING.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/docs/TESTING.md), `tests/test_library.py` |
| **Incremental Development** | Shippable increment produced at the end of every weekly iteration. | [scrum/SPRINT_PLAN.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/scrum/SPRINT_PLAN.md) |

---

## 4. Viva & Demonstration Readiness

For oral viva examination, the project provides:
1. **Interactive Console Menu (`python src/main.py`):** Hands-on live demonstration of Circulation, Catalog Search, Administration, and Scrum Task Management.
2. **Instant Automated Demonstration (`python src/main.py --demo`):** Automatically showcases registration, catalog search, atomic issue, quota checks, late return penalty, renewal, reservation hold, and ASCII Kanban in under 30 seconds.
3. **Interactive Web Dashboard (`python app.py`):** Browser-accessible portal at `http://127.0.0.1:5000` with visual cards, search filtering, fine payment, and live Kanban board.
4. **Automated Test Suite (`python -m unittest discover tests -v`):** Demonstrates that 100% of acceptance criteria pass rigorous testing.
