# Testing Strategy & Test Execution Report
## Library Management System using Scrum Agile Methodology

---

## 1. Testing Strategy in Scrum Agile

In Agile and Scrum methodologies, testing is an integrated, continuous engineering discipline embedded into every single sprint iteration. Testing serves as the primary verification mechanism to prove that delivered software increments satisfy their formal **Acceptance Criteria** and meet the **Definition of Done (DoD)** before user stories are transitioned to `Done`.

### Testing Levels Implemented
1. **Unit Testing:** Validates isolated business logic methods (e.g., salted password hashing, member quota checks, overdue fine calculations, story point summations) in `unittest`.
2. **Integration Testing:** Tests multi-table relational flows (e.g., book borrowing updates `books`, `borrow_records`, and `audit_logs` atomically).
3. **Defensive Concurrency & Negative Testing:** Explicitly stresses validation guards, including duplicate registrations, invalid credentials, out-of-stock borrow requests, exceeding 3-book quotas, and duplicate returns.
4. **Acceptance Testing:** Maps 1-to-1 with every scenario documented in [readme/ACCEPTANCE_CRITERIA.md](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/ACCEPTANCE_CRITERIA.md).

---

## 2. Test Execution Environment
- **Test Framework:** Python `unittest` (Built-in Standard Library)
- **Database Engine:** Isolated SQLite Test Database (`tests/test_library.db`)
- **Test Suite Location:** `tests/test_library.py`
- **Execution Commands:**
  ```bash
  python -m unittest discover tests -v
  ```
  or
  ```bash
  python src/main.py --test
  ```

---

## 3. Comprehensive Test Case Specifications & Execution Results

| Test ID | Linked Story | Test Scenario | Preconditions | Input Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|---|
| **TC-01** | `US-01` Auth | Member registration with valid credentials | Test user table initialized | username: `test_student_1`, pwd: `StrongPassword123!` | Account created with salted SHA-256 hash | Record created, password verified | 🟢 PASS |
| **TC-02** | `US-01` Auth | Duplicate username registration rejection | User `aarav_p` already exists | username: `aarav_p`, email: `dup@test.edu` | Rejected with duplicate username error | `ValueError: Username already exists` | 🟢 PASS |
| **TC-03** | `US-02` Auth | Member login with correct credentials | User `aarav_p` registered | username: `aarav_p`, password: `aarav123` | Valid session returned with role `member` | Session returned, role matched | 🟢 PASS |
| **TC-04** | `US-02` Auth | User login rejection with invalid password | User `aarav_p` registered | username: `aarav_p`, password: `WrongPassword!` | Authentication fails; returns None | Returned None; login rejected | 🟢 PASS |
| **TC-05** | `US-03` Catalog | Add book and verify unique ISBN constraint | Librarian role active | ISBN: `978-0131103627`, copies: `5` | Book created; duplicate ISBN blocked | Added with ID; duplicate blocked | 🟢 PASS |
| **TC-06** | `US-04` Search | Case-insensitive search by keyword & category | Catalog seeded | keyword: `algorithms`, category: `Operating Systems` | Matching textbooks returned accurately | Filtered records returned | 🟢 PASS |
| **TC-07** | `US-05` Avail | Real-time copy availability query | Book exists in catalog | book_id: `1` (Clean Code) | Returns total vs available copies & shelf | Valid copy numbers & shelf location | 🟢 PASS |
| **TC-08** | `US-06` Borrow | Atomic book borrow and copy decrement | Book has available copies | user_id: `1`, book_id: `3` | `available_copies` drops by 1; loan created | Loan created, stock count decremented | 🟢 PASS |
| **TC-09** | `US-06` Borrow | Borrow rejection when book is out of stock | Book copies = 0 | user_id: `1`, book_id: `9` (0 copies) | Rejected with out-of-stock error | `ValueError: out of stock` raised | 🟢 PASS |
| **TC-10** | `US-06` Quota | Enforce member borrowing limit (3 books) | Member has 3 active loans | Member attempts 4th borrow | Rejected with quota exceeded error | `ValueError: limit reached` raised | 🟢 PASS |
| **TC-11** | `US-07` History | Retrieve member active loans with overdue flags | Member has active loans | user_id: `1` | List of active loans with due dates | Active loans retrieved with deadlines | 🟢 PASS |
| **TC-12** | `US-08` Return | Return borrowed book and restore stock | Active loan exists | loan_id: target active loan | Status = `Returned`; stock increments by 1 | Stock restored, status updated | 🟢 PASS |
| **TC-13** | `US-10` Fine | Overdue fine calculation upon late return | Loan 11 days past due | Overdue loan returned | ₹55.00 fine assessed (11 days * ₹5.0) | Exactly ₹55.00 fine logged as Unpaid | 🟢 PASS |
| **TC-14** | `US-10` Fine | Fine payment settlement and double-pay guard | Unpaid fine exists | fine_id: target fine | Status updated to `Paid`; double-pay blocked | Status `Paid`; repeat payment rejected | 🟢 PASS |
| **TC-15** | `US-09` Reserve| Queue reservation for out-of-stock book | Book has 0 copies | user_id: `2`, book_id: `9` | Reservation created as `Pending` | Queued hold; duplicate blocked | 🟢 PASS |
| **TC-16** | `US-12` Scrum | Create user story and transition Kanban card | Sprints active in DB | code: `US-TEST`, transition to `Done` | Story created, card grouped under `DONE` | Moved to `DONE`; velocity updated | 🟢 PASS |

---

## 4. Test Execution Summary

```text
======================================================================
TEST EXECUTION SUMMARY REPORT
======================================================================
Test Suite File           : tests/test_library.py
Total Test Cases Executed : 16
Tests Passed              : 16
Tests Failed              : 0
Errors Encountered        : 0
Test Pass Rate            : 100.0%
Execution Duration        : 0.127 seconds
Quality Gate Assessment   : 🟢 PASSED (Ready for Viva & Production)
======================================================================
```

---

## 5. Traceability Matrix

Every single test case maps directly to its corresponding requirement, user story, acceptance criteria, and sprint:

```text
[Sprint 1] US-01 & US-02 ---> AC-US01 & AC-US02 ---> TC-01, TC-02, TC-03, TC-04 (Authentication)
[Sprint 2] US-03, US-04, US-05 ---> AC-US03, 04, 05 ---> TC-05, TC-06, TC-07 (Catalog & Search)
[Sprint 3] US-06, US-07, US-08 ---> AC-US06, 07, 08 ---> TC-08, TC-09, TC-10, TC-11, TC-12 (Circulation)
[Sprint 4] US-09, US-10 ---> AC-US09 & AC-US10 ---> TC-13, TC-14, TC-15 (Renewals, Reserves & Fines)
[Sprint 5] US-11, US-12 ---> AC-US11 & AC-US12 ---> TC-16 (In-App Scrum & Kanban Engine)
```
