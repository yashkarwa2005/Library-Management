# System Design & Architecture
## Library Management System using Scrum Agile Methodology

---

## 1. Architectural Overview

The **Library Management System** is engineered following a clean **3-Tier Layered Architecture** with strict decoupling between the user interface, business logic domain services, and database persistence layers:

```mermaid
graph TD
    subgraph Presentation_Layer["1. Presentation Layer"]
        CLI["Terminal Interactive Console (src/main.py)"]
        DEMO["Instant Automated Viva Demo (--demo)"]
        KANBAN_CLI["Terminal ASCII Kanban Renderer (src/kanban.py)"]
        WEB["Standalone Web App (app.py / templates/index.html)"]
        WEB_KB["Interactive Web Kanban Board (kanban_board.html)"]
    end

    subgraph Service_Layer["2. Business Logic & Service Layer"]
        AUTH["Authentication Service (SHA-256 + Salt)"]
        LIB["Library Circulation Engine (src/library.py)"]
        SCRUM_SVC["Scrum Management Services (src/user_story.py, sprint.py, action_item.py)"]
    end

    subgraph Data_Layer["3. Data Persistence Layer (SQLite 3)"]
        DB[(library.db)]
        T_USERS["users"]
        T_BOOKS["books"]
        T_LOANS["borrow_records"]
        T_RES["reservations"]
        T_FINES["fines"]
        T_SPRINTS["sprints"]
        T_STORIES["user_stories"]
        T_ACTIONS["action_items"]
        T_AUDIT["audit_logs"]
    end

    CLI --> LIB
    CLI --> SCRUM_SVC
    DEMO --> LIB
    DEMO --> SCRUM_SVC
    KANBAN_CLI --> SCRUM_SVC
    WEB --> LIB
    WEB --> SCRUM_SVC
    WEB_KB --> SCRUM_SVC

    LIB --> AUTH
    LIB --> DB
    SCRUM_SVC --> DB
```

---

## 2. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS ||--o{ BORROW_RECORDS : "borrows"
    USERS ||--o{ RESERVATIONS : "reserves"
    USERS ||--o{ FINES : "incurs"
    BOOKS ||--o{ BORROW_RECORDS : "loaned_in"
    BOOKS ||--o{ RESERVATIONS : "queued_in"
    BORROW_RECORDS ||--o{ FINES : "generates"
    SPRINTS ||--o{ USER_STORIES : "contains"
    SPRINTS ||--o{ ACTION_ITEMS : "tracks"

    USERS {
        int id PK
        string username UK
        string password_hash
        string full_name
        string email UK
        string phone
        string role
        timestamp created_at
    }

    BOOKS {
        int id PK
        string isbn UK
        string title
        string author
        string category
        string publisher
        int publication_year
        int total_copies
        int available_copies
        string shelf_location
        timestamp created_at
    }

    BORROW_RECORDS {
        int id PK
        int user_id FK
        int book_id FK
        string borrow_date
        string due_date
        string return_date
        string status
        int renewal_count
        timestamp created_at
    }

    RESERVATIONS {
        int id PK
        int user_id FK
        int book_id FK
        string reservation_date
        string status
        timestamp created_at
    }

    FINES {
        int id PK
        int borrow_id FK
        int user_id FK
        real amount
        string fine_date
        string paid_status
        string paid_date
        timestamp created_at
    }

    SPRINTS {
        int id PK
        int sprint_number UK
        string name
        string goal
        string start_date
        string end_date
        string status
        int velocity
        timestamp created_at
    }

    USER_STORIES {
        int id PK
        string story_code UK
        string title
        string role
        string want
        string benefit
        string priority
        int story_points
        int sprint_id FK
        string status
        string assignee
        string description
        timestamp created_at
    }

    ACTION_ITEMS {
        int id PK
        string item_code UK
        string description
        int sprint_id FK
        string owner
        string priority
        string due_date
        string status
        timestamp created_at
    }
```

---

## 3. Core Circulation Sequence Diagrams

### A. Atomic Book Borrowing Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Member as Student Member
    participant Lib as LibraryService
    participant DB as SQLite (library.db)

    Member->>Lib: borrow_book(user_id, book_id)
    Lib->>DB: Check unpaid fines for user_id
    DB-->>Lib: Unpaid fines = ₹0.00
    Lib->>DB: Check active loans count for user_id
    DB-->>Lib: Active loans count = 1 (< 3 quota)
    Lib->>DB: SELECT available_copies FROM books WHERE id = book_id
    DB-->>Lib: available_copies = 3 (> 0)
    
    rect rgb(20, 35, 45)
        note over Lib, DB: Atomic SQLite Transaction
        Lib->>DB: UPDATE books SET available_copies = available_copies - 1 WHERE id = book_id AND available_copies > 0
        Lib->>DB: INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, status)
        Lib->>DB: INSERT INTO audit_logs (BOOK_BORROW)
        Lib->>DB: COMMIT TRANSACTION
    end

    Lib-->>Member: Return Borrow Confirmation (Due: 14 days)
```

### B. Book Return & Automated Overdue Fine Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Member as Student / Librarian
    participant Lib as LibraryService
    participant DB as SQLite (library.db)

    Member->>Lib: return_book(borrow_id)
    Lib->>DB: SELECT * FROM borrow_records WHERE id = borrow_id
    DB-->>Lib: Borrow record found (due_date, book_id, user_id)
    
    rect rgb(20, 35, 45)
        note over Lib, DB: Atomic Inventory & Penalty Recovery
        Lib->>DB: UPDATE borrow_records SET status = 'Returned', return_date = now
        Lib->>DB: UPDATE books SET available_copies = available_copies + 1
        alt If now > due_date
            Lib->>Lib: Calculate late fine = overdue_days * ₹5.0
            Lib->>DB: INSERT INTO fines (borrow_id, user_id, amount, paid_status='Unpaid')
        end
        Lib->>DB: Check pending reservations on book_id
        opt Pending reservation exists
            Lib->>DB: UPDATE reservations SET status = 'Fulfilled' WHERE id = res_id
        end
        Lib->>DB: INSERT INTO audit_logs (BOOK_RETURN)
        Lib->>DB: COMMIT TRANSACTION
    end

    Lib-->>Member: Return Summary (overdue_days, fine_amount, reservation_alert)
```

---

## 4. Database Schema Specifications & Data Dictionary

| Table Name | Purpose | Primary Key | Foreign Keys | Key Constraints |
|---|---|---|---|---|
| `users` | Stores accounts & roles | `id` | None | `username UNIQUE`, `email UNIQUE`, `role IN ('member', 'librarian', 'admin')` |
| `books` | Physical textbook catalog | `id` | None | `isbn UNIQUE`, `available_copies >= 0`, `total_copies >= 0` |
| `borrow_records` | Circulation loan transactions | `id` | `user_id` -> `users.id`, `book_id` -> `books.id` | `status IN ('Borrowed', 'Returned', 'Overdue')` |
| `reservations` | Out-of-stock hold queue | `id` | `user_id` -> `users.id`, `book_id` -> `books.id` | `status IN ('Pending', 'Fulfilled', 'Cancelled')` |
| `fines` | Overdue penalty ledger | `id` | `borrow_id` -> `borrow_records.id`, `user_id` -> `users.id` | `paid_status IN ('Unpaid', 'Paid')`, `amount >= 0` |
| `sprints` | Scrum 5-week sprint schedule | `id` | None | `sprint_number UNIQUE`, `status IN ('Planning', 'Active', 'Completed')` |
| `user_stories` | Product & Sprint backlogs | `id` | `sprint_id` -> `sprints.id` | `story_code UNIQUE`, MoSCoW priorities, INVEST attributes |
| `action_items` | Weekly task register | `id` | `sprint_id` -> `sprints.id` | `item_code UNIQUE`, Kanban workflow statuses |
| `audit_logs` | System security event ledger | `id` | `user_id` -> `users.id` | Append-only event history |
