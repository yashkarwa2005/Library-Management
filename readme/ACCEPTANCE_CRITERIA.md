# Acceptance Criteria Documentation
## Library Management System using Scrum Agile Methodology

---

## 1. What are Acceptance Criteria?

In Scrum and Agile software engineering, **Acceptance Criteria (AC)** represent the formal, predetermined conditions that a software feature or user story must satisfy before it can be accepted by the Product Owner and considered **Done** according to the Definition of Done (DoD).

### Key Functions of Acceptance Criteria:
1. **Defines Scope Boundaries:** Explicitly specifies what is included and excluded in each user story.
2. **Eliminates Ambiguity:** Aligns developers, testers, and stakeholders on expected behavior.
3. **Forms Automated Test Basis:** Serves as the blueprint for unit and integration test scenarios in `tests/test_library.py`.
4. **Enforces Quality Gate:** A user story cannot transition across the Kanban board to `Done` until 100% of its acceptance criteria pass verification.

---

## 2. Standard Agile Formats Used

### A. Scenario-Oriented Format (Gherkin Syntax)
```gherkin
Scenario: [Context / Scenario Title]
Given [Precondition or initial state]
When [Action triggered by user or system event]
Then [Expected observable outcome]
And [Additional consequence or state update]
```

### B. Rule-Oriented Checklist Format
```markdown
- [x] Rule 1: Specific input validation constraint
- [x] Rule 2: Database state transition & concurrency rule
- [x] Rule 3: Error response and security safeguard
```

---

## 3. Detailed Acceptance Criteria for Core User Stories

---

### AC-US01: Member Registration
**Linked Story:** [US-01: Member Registration & Credential Hashing](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-01-member-registration--credential-hashing)

#### Scenario 1: Successful member account registration
- **Given** an unregistered student accesses the registration interface,
- **When** the user provides a valid username (`aarav_p`), strong password (`aarav123`), full name (`Aarav Patel`), email (`aarav@example.com`), and phone (`9876543210`),
- **Then** the system hashes the password using SHA-256 with a unique salt (`scrum_lib_salt_2026`),
- **And** stores the new user record in the `users` database table with role `member`,
- **And** creates a audit log entry for `USER_REGISTER`,
- **And** returns a successful user dictionary without exposing raw credentials.

#### Scenario 2: Duplicate username or email rejection
- **Given** a user is on the registration interface,
- **When** the user attempts to register with a username or email that already exists in the `users` table,
- **Then** the database unique constraint prevents duplicate insertion,
- **And** the service catches the conflict and raises a descriptive `ValueError: Username already exists`,
- **And** no duplicate database rows are created.

#### Scenario 3: Missing mandatory fields
- **Given** a prospective member submits the registration form,
- **When** any mandatory field (username, password, full name, email) is empty or whitespace,
- **Then** the system rejects the operation with `ValueError: All mandatory fields must be provided`.

---

### AC-US02: Role-Based Authentication
**Linked Story:** [US-02: Role-Based Authentication & Session Management](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-02-role-based-authentication--session-management)

#### Scenario 1: Valid credential login
- **Given** a registered user exists in the `users` table,
- **When** the user submits their registered username and correct password,
- **Then** the system re-hashes the input password with salt and compares it to `password_hash`,
- **And** returns an authenticated user session dictionary containing `id`, `username`, `full_name`, and `role`.

#### Scenario 2: Invalid password rejection
- **Given** a registered user exists in the system,
- **When** the user enters an incorrect password,
- **Then** the hash comparison fails,
- **And** the system returns `None` (or HTTP 401 in REST API),
- **And** displays: `"Invalid username or password"`.

---

### AC-US03: Book Catalog Management
**Linked Story:** [US-03: Book Catalog Management & Shelf Tracking](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-03-book-catalog-management--shelf-tracking)

#### Scenario 1: Adding a new academic volume to catalog
- **Given** an authorized librarian is managing the catalog,
- **When** the librarian enters valid ISBN (`978-0131103627`), title (`The C Programming Language`), author (`Brian W. Kernighan`), category (`Programming`), total copies (`5`), and shelf location (`Shelf K-01`),
- **Then** the system inserts the book into the `books` table with `available_copies = 5`,
- **And** logs a `BOOK_ADD` audit record,
- **And** assigns a unique auto-incremented book ID.

#### Scenario 2: Duplicate ISBN prevention
- **Given** a book with ISBN `978-0131103627` already exists in catalog,
- **When** a user attempts to add another book with the identical ISBN,
- **Then** the database unique constraint blocks the insertion,
- **And** the service raises a `ValueError` indicating duplicate ISBN.

---

### AC-US04: Advanced Book Search
**Linked Story:** [US-04: Advanced Book Search & Category Filtering](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-04-advanced-book-search--category-filtering)

#### Scenario 1: Search by title keyword
- **Given** catalog books are populated in the database,
- **When** a member searches for keyword `"clean"`,
- **Then** the system performs a case-insensitive match on title, author, and ISBN,
- **And** returns `Clean Code: A Handbook of Agile Software Craftsmanship`.

#### Scenario 2: Filter by category genre
- **Given** catalog books span multiple genres,
- **When** a member selects category `"Algorithms"`,
- **Then** the system filters books where `LOWER(category) = 'algorithms'`,
- **And** excludes books belonging to other disciplines.

---

### AC-US05: Real-Time Availability Inspection
**Linked Story:** [US-05: Real-time Book Availability & Copy Inspection](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-05-real-time-book-availability--copy-inspection)

#### Scenario 1: Verifying available stock counts
- **Given** a book exists with `total_copies = 4` and `available_copies = 3`,
- **When** a user queries the book by ID or search,
- **Then** the response displays `available_copies: 3` and `total_copies: 4`,
- **And** displays physical stack coordinates (e.g., `Shelf A-15`).

---

### AC-US06: Atomic Book Issue & Concurrency Control
**Linked Story:** [US-06: Atomic Book Issue & Concurrency Control](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-06-atomic-book-issue--concurrency-control)

#### Scenario 1: Successful book checkout
- **Given** a member has 0 active loans and zero unpaid fines,
- **And** a book has `available_copies = 4`,
- **When** the member requests to borrow the book,
- **Then** the system begins an atomic transaction,
- **And** decrements `available_copies` to `3`,
- **And** inserts a new row into `borrow_records` with `borrow_date = today` and `due_date = today + 14 days`,
- **And** records a `BOOK_BORROW` audit entry,
- **And** commits the transaction.

#### Scenario 2: Rejection on out-of-stock book
- **Given** a book has `available_copies = 0`,
- **When** a member attempts to borrow the book,
- **Then** the system aborts checkout before modifying tables,
- **And** raises `ValueError: Book is currently out of stock (0 copies available). You may place a reservation.`.

#### Scenario 3: Enforcing member borrowing limit (3 books quota)
- **Given** a member currently has 3 active loans with status `Borrowed` or `Overdue`,
- **When** the member attempts to borrow a 4th book,
- **Then** the quota check fails,
- **And** the transaction is blocked with `ValueError: Borrowing limit reached: Maximum 3 active books permitted per member.`.

#### Scenario 4: Blocking members with outstanding unpaid fines
- **Given** a member has unpaid fines recorded in the `fines` table totaling > ₹0.00,
- **When** the member attempts to borrow any book,
- **Then** the system blocks checkout with: `"Borrowing blocked: Member has unpaid fines totaling ₹X.XX. Please clear fines first."`.

---

### AC-US07: Member Loan History
**Linked Story:** [US-07: Member Loan History & Due Date Overview](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-07-member-loan-history--due-date-overview)

#### Scenario 1: Displaying active loans with overdue flags
- **Given** an authenticated member has active book checkouts,
- **When** the member requests their active loans list,
- **Then** the system returns all loans with status `Borrowed` or `Overdue`,
- **And** calculates `is_overdue = (now > due_date)` dynamically,
- **And** computes `overdue_days` past deadline.

---

### AC-US08: Book Return & Inventory Recovery
**Linked Story:** [US-08: Book Return & Automated Inventory Recovery](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-08-book-return--automated-inventory-recovery)

#### Scenario 1: Punctual book return
- **Given** an active loan exists with `status = 'Borrowed'` and `due_date >= today`,
- **When** the borrower initiates return,
- **Then** the loan status changes to `Returned` with `return_date = now`,
- **And** the book's `available_copies` increments by 1 atomically,
- **And** zero fine is assessed (`fine_amount = 0.0`),
- **And** an audit log entry for `BOOK_RETURN` is recorded.

#### Scenario 2: Duplicate return rejection
- **Given** a loan record already marked `Returned`,
- **When** an attempt is made to return the same loan again,
- **Then** the system rejects the operation with `ValueError: Book was already returned`.

---

### AC-US09: Self-Service Renewal & Reservation Queue
**Linked Story:** [US-09: Self-Service Book Renewal & Reservation Queue](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-09-self-service-book-renewal--reservation-queue)

#### Scenario 1: Successful 14-day renewal
- **Given** an active loan has `renewal_count < 2` and zero pending reservations on that book,
- **When** the member requests a renewal,
- **Then** `due_date` is extended by 14 days,
- **And** `renewal_count` is incremented by 1,
- **And** an audit entry is created.

#### Scenario 2: Renewal rejection when reserved by another member
- **Given** an active loan on book `B1` has a pending reservation queued by another student,
- **When** the current borrower attempts to renew the loan,
- **Then** the renewal is rejected with `ValueError: Cannot renew: Another library member has reserved this book.`.

#### Scenario 3: Reserving an out-of-stock book
- **Given** a book has 0 available copies in stock,
- **When** an authenticated student places a reservation,
- **Then** the system inserts a record into `reservations` with status `Pending`,
- **And** when the book is subsequently returned, the reservation is automatically flagged as `Fulfilled`.

---

### AC-US10: Overdue Fine Calculation & Settlement
**Linked Story:** [US-10: Automated Overdue Fine Calculation & Settlement](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-10-automated-overdue-fine-calculation--settlement)

#### Scenario 1: Late return penalty assessment
- **Given** an active loan has a `due_date` that is 6 days in the past,
- **When** the borrower returns the book,
- **Then** the system calculates `6 days * ₹5.0 = ₹30.00`,
- **And** inserts a new record into the `fines` table with `paid_status = 'Unpaid'`,
- **And** informs the member of the assessed penalty.

#### Scenario 2: Settling an unpaid fine
- **Given** an unpaid fine of ₹30.00 exists in the `fines` table,
- **When** the member or librarian initiates payment for that fine ID,
- **Then** the system updates `paid_status = 'Paid'` and sets `paid_date = now`,
- **And** subsequent payment attempts on the same fine ID are rejected.

---

### AC-US11: Centralized Admin Audit
**Linked Story:** [US-11: Centralized Librarian & Admin Inventory Audit](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-11-centralized-librarian--admin-inventory-audit)

#### Scenario 1: Querying institutional metrics
- **Given** books, members, loans, and fines exist in the database,
- **When** an administrator queries the statistics endpoint,
- **Then** the system aggregates `total_titles`, `total_copies`, `available_copies`, `borrowed_copies`, `total_members`, `overdue_loans`, `total_unpaid_fines`, and `total_collected_fines`.

---

### AC-US12: Built-in Scrum & Kanban Engine
**Linked Story:** [US-12: Built-in Scrum Backlog, Sprint & Terminal Kanban Engine](file:///D:/COLLEGE/Sem-5/AM&IT/annika/pbl/readme/USER_STORY.md#us-12-built-in-scrum-backlog-sprint--terminal-kanban-engine)

#### Scenario 1: Displaying the 5-column ASCII Kanban board
- **Given** user stories and action items exist in SQLite tables,
- **When** the user runs `python src/main.py --kanban`,
- **Then** the system queries the database and renders an ASCII board with columns: `Backlog`, `To Do`, `In Progress`, `Review/Testing`, `Done`,
- **And** cards display code, title, priority, story points, and assignee.

#### Scenario 2: Card status transition
- **Given** a story exists in status `In Progress`,
- **When** the user transitions the story to `Done`,
- **Then** the `user_stories` table is updated,
- **And** the board reflects the card under the `DONE` column with updated completion velocity.
