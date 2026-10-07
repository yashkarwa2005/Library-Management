# Library Management System (Athenaeum)
## Information Technology Lab (ITL) & Agile Methodologies (AM) PBL Project Manual
**Academic Year:** 2026-2027 | **Semester:** 5 | **Branch:** B.Tech Computer Engineering / Information Technology  
**Student Name:** Annika Jha | **Topic:** Library Management System using Scrum Agile Methodology  

---

## 1. Project Objective & Aim

To design, develop, and demonstrate a robust, concurrent **Library Management System** managed under the **Scrum Agile Methodology**. The system streamlines textbook discovery, eliminates stock count collisions through atomic database transactions, enforces member borrowing quotas (maximum 3 books), supports self-service renewals and out-of-stock reservations, assesses automated late return penalties (₹5/day), and provides transparent administrative oversight alongside a live Scrum Kanban engine.

---

## 2. Technology Stack & Prerequisites

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Backend** | Python 3.8+ (Tested on 3.13) | Standard library `http.server`, multi-threaded request dispatcher |
| **Database** | SQLite3 | Relational ACID database with Foreign Keys enabled (`PRAGMA foreign_keys = ON`) |
| **Security** | SHA-256 + Salted Hashing | Cryptographic credential protection against rainbow table attacks |
| **Frontend** | HTML5, CSS3, Vanilla JS | Dark modern responsive UI with glassmorphism card design |
| **Testing** | Python `unittest` framework | 16 comprehensive automated unit & integration tests covering all modules |
| **Agile Tools** | In-App ASCII & Web Kanban | 5-stage Kanban flow (Backlog, To Do, In Progress, Review/Testing, Done) |

---

## 3. How to Run the Project on Laptop for Demonstration

### Method 1: One-Click Double Click (Recommended)
1. Navigate to the project folder:
   ```text
   ITL/
   ```
2. Double-click the file:
   ```text
   run.bat
   ```
3. Select Option `1` to start the server and automatically launch your web browser at:
   ```text
   http://127.0.0.1:5000
   ```

### Method 2: Via Terminal Command Line
```powershell
# Open terminal inside the ITL folder and execute:
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

### Method 3: Run Automated Test Suite (To show 100% test pass to teacher)
```powershell
python -m unittest discover tests -v
```

### Method 4: Run Instant Viva Demo (Under 30 Seconds)
```powershell
python src/main.py --demo
```

---

## 4. Test Accounts for Evaluation

| Role | Username | Password | Purpose & Context |
| :--- | :--- | :--- | :--- |
| **Student Member** | `aarav_p` | `aarav123` | Active member with 1 clean checkout; ready to borrow or renew. |
| **Student Member** | `diya_s` | `diya123` | Member with a pre-seeded overdue loan and ₹30 late fine to show fine settlement. |
| **Librarian** | `librarian_anita` | `anita123` | Catalog manager with permissions to add books and audit circulation. |
| **System Admin** | `admin` | `admin123` | Institutional administrator with global health statistics and audit logs. |

---

## 5. Step-by-Step Viva Demonstration Script (For Examiner)

### Step 1: Open Dashboard & Review Institutional Metrics
- Launch `python app.py` and open `http://127.0.0.1:5000`.
- Point out the institutional stats: **10 Titles**, **36 Total Copies**, **29 In Stock**, **7 In Circulation**.

### Step 2: Member Authentication & Real-Time Availability
- Click **Quick Login: Aarav Patel (Member)**.
- In the search bar, type `"Clean Code"` or `"Algorithms"`.
- Show that available copies (`4 of 5 In Stock`) and shelf location (`Shelf A-12`) are dynamically rendered.

### Step 3: Atomic Book Issue & Concurrency Control (US-06)
- Click the **Borrow** button on *Clean Code*.
- The stock count atomically decrements from 4 to 3.
- Navigate to **👤 Member Portal** tab and point out the newly created active loan with an automatic 14-day due date deadline.

### Step 4: Quota Enforcement & Out-of-Stock Reservation (US-09)
- Search for *The Pragmatic Programmer* (seeded with `0 of 3 copies In Stock`).
- Show that the **Borrow** button is replaced with **Reserve**.
- Click **Reserve** to demonstrate FIFO queue placement for out-of-stock volumes.

### Step 5: Book Return & Automated Late Fine Assessment (US-08, US-10)
- Switch to member **Diya Sharma** (has an overdue loan).
- Point out the **💰 Overdue Fines: ₹30.00** warning card.
- Click the **Pay** button to show instant transaction settlement and status update to `Paid`.

### Step 6: Agile Scrum Kanban Board Demonstration (US-12)
- Click the **📊 Agile Kanban** tab (or open `http://127.0.0.1:5000/kanban_board.html`).
- Demonstrate the 5-column flow: `Backlog ➔ To Do ➔ In Progress ➔ Review/Testing ➔ Done`.
- Show drag-and-drop movement of cards, sprint filtering, and live card counter updates.

---

## 6. Automated Test Results (100% Pass)

```text
Ran 16 tests in 0.125s
OK (16 Passed, 0 Failures, 0 Errors, 100% Pass Rate)
```

| Test Case | Scenario Tested | Result |
| :--- | :--- | :--- |
| `TC-01` | Valid user registration with SHA-256 salted hash | 🟢 PASS |
| `TC-02` | Rejection of duplicate username or email | 🟢 PASS |
| `TC-03` | Valid login credential verification | 🟢 PASS |
| `TC-04` | Rejection of invalid password | 🟢 PASS |
| `TC-05` | Catalog addition & unique ISBN constraint | 🟢 PASS |
| `TC-06` | Case-insensitive multi-attribute search | 🟢 PASS |
| `TC-07` | Real-time available copy count query | 🟢 PASS |
| `TC-08` | Atomic borrow transaction & copy decrement | 🟢 PASS |
| `TC-09` | Out-of-stock borrowing rejection | 🟢 PASS |
| `TC-10` | 3-book member borrowing quota enforcement | 🟢 PASS |
| `TC-11` | Member active loan retrieval with overdue flags | 🟢 PASS |
| `TC-12` | Book return & inventory replenishment | 🟢 PASS |
| `TC-13` | Overdue fine calculation (₹5/day) | 🟢 PASS |
| `TC-14` | Fine settlement payment update | 🟢 PASS |
| `TC-15` | Out-of-stock reservation queue hold | 🟢 PASS |
| `TC-16` | Scrum story creation & Kanban status transition | 🟢 PASS |

---

## 7. Viva Voce Questions & Answers

**Q1: Why was SQLite chosen over MySQL/PostgreSQL for this project?**  
*Answer:* SQLite is a zero-configuration, serverless, self-contained relational database that provides full ACID transactional guarantees, foreign key enforcement, and instant portability on any examination machine without requiring database server setup.

**Q2: What is the purpose of salted SHA-256 password hashing?**  
*Answer:* A standard SHA-256 hash is vulnerable to precomputed dictionary and rainbow table lookups. Adding a unique cryptographic salt (`scrum_lib_salt_2026`) ensures that identical passwords yield distinct, unpredictable hashes.

**Q3: How does the system prevent race conditions during book borrowing?**  
*Answer:* We execute an explicit SQL atomic transaction: `UPDATE books SET available_copies = available_copies - 1 WHERE id = ? AND available_copies > 0;`. If two users submit simultaneously, SQLite row locking ensures only one transaction decrements the copy while the second receives `rowcount = 0` and is cleanly aborted.

**Q4: What is the difference between a User Story and a Use Case?**  
*Answer:* A Use Case is a detailed, formal description of steps and system interactions. A User Story is a lightweight statement focusing on user value from the end user's perspective (*As a... I want... So that...*), adhering to the INVEST criteria and accompanied by testable Acceptance Criteria.
