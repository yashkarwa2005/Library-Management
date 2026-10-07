# Sprint Retrospective Logs
## Library Management System using Scrum Agile Methodology

---

## 1. Purpose of the Sprint Retrospective

The **Sprint Retrospective** is the core continuous improvement ceremony in Scrum. Held at the conclusion of each sprint, the team reflects on the iteration to inspect *people*, *relationships*, *process*, and *tools*, answering three fundamental questions:
1. **What went well during the sprint?**
2. **What challenges or bottlenecks were encountered?**
3. **What actionable improvements (Kaizen) will we commit to in the next sprint?**

---

## 2. Sprint 1 Retrospective Log

- **Date:** Week 1, Day 7
- **Participants:** Annika Jha (Scrum Lead), Dev Team
- **What Went Well:**
  - Salted SHA-256 cryptographic hashing was cleanly encapsulated in `src/database.py`.
  - SQLite foreign key constraints (`PRAGMA foreign_keys = ON;`) ensured relational integrity from day one.
  - Sized and completed 6 story points right on target.
- **What Could Be Improved:**
  - Manual recreation and deletion of local SQLite `.db` files during test runs proved tedious and error-prone.
  - Terminal output formatting lacked visual clarity when invalid passwords were submitted.
- **Kaizen Action Item:**
  - *Action:* Implement automated database initialization and seed data loading in `src/database.py` with an isolated `:memory:` or test fixture for tests.
  - *Owner:* Annika Jha | *Status:* Completed in Sprint 2.

---

## 3. Sprint 2 Retrospective Log

- **Date:** Week 2, Day 7
- **Participants:** Annika Jha (Scrum Lead), Dev Team
- **What Went Well:**
  - Multi-attribute search SQL queries (`LIKE %keyword%`) executed with sub-millisecond latency.
  - Realistic seed catalog of 10 Computer Science volumes provided immediate context for testing.
  - Velocity increased to 11 story points without defect leakage.
- **What Could Be Improved:**
  - Case-sensitivity nuances initially caused queries like `"clean code"` to miss `"Clean Code"`.
  - Book physical locations lacked standardization (inconsistent shelf naming).
- **Kaizen Action Item:**
  - *Action:* Standardize shelf coordinate format (e.g., `Shelf [A-Z]-[0-9]{2}`) and force SQL `LOWER()` transformations on all keyword comparisons.
  - *Owner:* Dev Team | *Status:* Completed in Sprint 2.

---

## 4. Sprint 3 Retrospective Log

- **Date:** Week 3, Day 7
- **Participants:** Annika Jha (Scrum Lead), Dev Team
- **What Went Well:**
  - Atomic borrowing logic successfully prevented stock counts from dropping below zero.
  - The 3-book member borrowing quota was enforced cleanly at the service layer.
  - High team velocity (16 story points delivered) achieved through disciplined task slicing.
- **What Could Be Improved:**
  - If two members attempted to checkout the last remaining copy simultaneously, SQLite concurrency handling required explicit transaction checks rather than relying purely on client-side state.
- **Kaizen Action Item:**
  - *Action:* Embed explicit `UPDATE books SET available_copies = available_copies - 1 WHERE id = ? AND available_copies > 0;` with `cursor.rowcount` verification inside `borrow_book()`.
  - *Owner:* Annika Jha | *Status:* Completed in Sprint 3.

---

## 5. Sprint 4 Retrospective Log

- **Date:** Week 4, Day 7
- **Participants:** Annika Jha (Scrum Lead), Dev Team
- **What Went Well:**
  - Automated overdue fine computation (₹5/day) removed subjective ambiguity for library staff.
  - The FIFO reservation queue seamlessly fulfilled holds upon book returns.
  - Zero regression bugs introduced across prior sprint modules.
- **What Could Be Improved:**
  - Demonstrating full circulation cycles (borrow -> wait -> late return -> fine) during practice viva presentations took over 5 minutes due to manual CLI navigation.
- **Kaizen Action Item:**
  - *Action:* Engineer a single-command automated viva walkthrough flag (`--demo`) in `src/main.py` to demonstrate all 12 user stories in under 30 seconds.
  - *Owner:* Annika Jha | *Status:* Completed in Sprint 5.

---

## 6. Sprint 5 Retrospective Log

- **Date:** Week 5, Day 7
- **Participants:** Annika Jha (Scrum Lead), Dev Team
- **What Went Well:**
  - Dual-track architecture (Library Engine + In-App Scrum & Kanban Engine) delivered complete pedagogical alignment with the AM curriculum.
  - Pure Python standard library implementation (`sqlite3`, `http.server`, `unittest`) ensures zero setup friction on any evaluation computer.
  - 16 automated test cases executed in 0.12s with 100% pass rate.
- **What Could Be Improved:**
  - Adding optional visual drag-and-drop web interfaces complements terminal evaluators who prefer browser visualization.
- **Kaizen Action Item:**
  - *Action:* Deliver both the standalone visual web Kanban board (`kanban_board.html`) and the browser-based dashboard (`app.py`).
  - *Owner:* Annika Jha | *Status:* Completed in Sprint 5.

---

## 7. Retrospective Action Summary Matrix

```text
+---------------------+---------------------------------------------------+------------+-----------+
| Source Ceremony     | Agreed Kaizen Improvement Commitment              | Owner      | Outcome   |
+---------------------+---------------------------------------------------+------------+-----------+
| Sprint 1 Retro      | Automated database seeding and isolated test DB   | Annika Jha | Delivered |
| Sprint 2 Retro      | Standardized shelf format & case-insensitive SQL  | Dev Team   | Delivered |
| Sprint 3 Retro      | Explicit transactional stock decrement guard      | Annika Jha | Delivered |
| Sprint 4 Retro      | One-command automated viva walkthrough (--demo)   | Annika Jha | Delivered |
| Sprint 5 Retro      | Dual-interface web & terminal Kanban delivery     | Annika Jha | Delivered |
+---------------------+---------------------------------------------------+------------+-----------+
```
