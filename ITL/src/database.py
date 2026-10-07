"""Database Module for Library Management System
Manages SQLite connection, schema definition, foreign key enforcement, and seed data.
Author / Scrum Lead: Annika Jha
"""
import os
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Optional

DEFAULT_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_DIR, "library.db")


def hash_password(password: str, salt: str = "scrum_lib_salt_2026") -> str:
    """Hashes a password with salt using SHA-256."""
    return hashlib.sha256(f"{salt}_{password}".encode("utf-8")).hexdigest()


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Returns a SQLite connection with foreign keys enabled and row_factory set to sqlite3.Row."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    elif db_path != ":memory:":
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Creates database schema if tables do not exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        role TEXT NOT NULL CHECK(role IN ('member', 'librarian', 'admin')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Books Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isbn TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT NOT NULL,
        publisher TEXT NOT NULL,
        publication_year INTEGER NOT NULL,
        total_copies INTEGER NOT NULL CHECK(total_copies >= 0),
        available_copies INTEGER NOT NULL CHECK(available_copies >= 0),
        shelf_location TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Borrow Records Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrow_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
        borrow_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        return_date TEXT,
        status TEXT NOT NULL DEFAULT 'Borrowed' CHECK(status IN ('Borrowed', 'Returned', 'Overdue')),
        renewal_count INTEGER DEFAULT 0 CHECK(renewal_count >= 0),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 4. Reservations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
        reservation_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Fulfilled', 'Cancelled')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 5. Fines Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        borrow_id INTEGER NOT NULL REFERENCES borrow_records(id) ON DELETE CASCADE,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        amount REAL NOT NULL CHECK(amount >= 0),
        fine_date TEXT NOT NULL,
        paid_status TEXT NOT NULL DEFAULT 'Unpaid' CHECK(paid_status IN ('Unpaid', 'Paid')),
        paid_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 6. Sprints Table (Scrum Management)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sprints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sprint_number INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        goal TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Planning' CHECK(status IN ('Planning', 'Active', 'Completed')),
        velocity INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 7. User Stories Table (Product Backlog & Sprint Backlog)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        role TEXT NOT NULL,
        want TEXT NOT NULL,
        benefit TEXT NOT NULL,
        priority TEXT NOT NULL CHECK(priority IN ('Must Have', 'Should Have', 'Could Have', 'Won''t Have')),
        story_points INTEGER NOT NULL,
        sprint_id INTEGER REFERENCES sprints(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'Backlog' CHECK(status IN ('Backlog', 'To Do', 'In Progress', 'Review/Testing', 'Done')),
        assignee TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 8. Action Items Table (Sprint Action Items & Standups)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS action_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_code TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        sprint_id INTEGER REFERENCES sprints(id) ON DELETE SET NULL,
        owner TEXT NOT NULL,
        priority TEXT NOT NULL CHECK(priority IN ('High', 'Medium', 'Low')),
        due_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'To Do' CHECK(status IN ('To Do', 'In Progress', 'Review', 'Done', 'Blocked')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 9. Audit Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type TEXT NOT NULL,
        user_id INTEGER,
        user_name TEXT,
        details TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def seed_initial_data(db_path: Optional[str] = None) -> None:
    """Seeds realistic default users, book catalog, scrum sprints, user stories, and action items."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) AS cnt FROM users;")
    if cursor.fetchone()["cnt"] > 0:
        conn.close()
        return

    # Seed Default Users
    users_data = [
        ("aarav_p", hash_password("aarav123"), "Aarav Patel", "aarav@example.com", "9876543210", "member"),
        ("diya_s", hash_password("diya123"), "Diya Sharma", "diya@example.com", "9876543211", "member"),
        ("librarian_anita", hash_password("anita123"), "Anita Roy", "anita@library.edu", "9876543212", "librarian"),
        ("admin", hash_password("admin123"), "System Administrator", "admin@library.edu", "9876543299", "admin")
    ]
    cursor.executemany("""
    INSERT INTO users (username, password_hash, full_name, email, phone, role)
    VALUES (?, ?, ?, ?, ?, ?);
    """, users_data)

    # Seed Book Catalog
    books_data = [
        ("978-0132350884", "Clean Code: A Handbook of Agile Software Craftsmanship", "Robert C. Martin", "Computer Science", "Prentice Hall", 2008, 5, 4, "Shelf A-12"),
        ("978-0262033848", "Introduction to Algorithms (4th Edition)", "Thomas H. Cormen, Charles E. Leiserson", "Algorithms", "MIT Press", 2022, 4, 3, "Shelf A-15"),
        ("978-0134685991", "Effective Java (3rd Edition)", "Joshua Bloch", "Programming", "Addison-Wesley", 2018, 3, 3, "Shelf B-04"),
        ("978-0136042594", "Artificial Intelligence: A Modern Approach", "Stuart Russell, Peter Norvig", "Artificial Intelligence", "Pearson", 2020, 3, 2, "Shelf B-09"),
        ("978-0201633610", "Design Patterns: Elements of Reusable Object-Oriented Software", "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides", "Software Architecture", "Addison-Wesley", 1994, 4, 4, "Shelf C-01"),
        ("978-0078022159", "Database System Concepts (7th Edition)", "Abraham Silberschatz, Henry F. Korth", "Databases", "McGraw-Hill", 2019, 5, 5, "Shelf C-08"),
        ("978-0133591620", "Modern Operating Systems (4th Edition)", "Andrew S. Tanenbaum, Herbert Bos", "Operating Systems", "Pearson", 2014, 3, 3, "Shelf D-02"),
        ("978-0132126953", "Computer Networks (5th Edition)", "Andrew S. Tanenbaum, David J. Wetherall", "Networking", "Pearson", 2010, 4, 3, "Shelf D-05"),
        ("978-0135957059", "The Pragmatic Programmer (20th Anniversary Edition)", "David Thomas, Andrew Hunt", "Software Craftsmanship", "Addison-Wesley", 2019, 3, 0, "Shelf E-01"),
        ("978-0262035612", "Deep Learning", "Ian Goodfellow, Yoshua Bengio, Aaron Courville", "Machine Learning", "MIT Press", 2016, 2, 2, "Shelf E-07")
    ]
    cursor.executemany("""
    INSERT INTO books (isbn, title, author, category, publisher, publication_year, total_copies, available_copies, shelf_location)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, books_data)

    # Seed Sprints (5 Weekly Sprints)
    sprints_data = [
        (1, "Sprint 1: Security & Identity Management", "Deliver secure member registration, salted SHA-256 password hashing, and role-based session authentication.", "2026-09-01", "2026-09-07", "Completed", 6),
        (2, "Sprint 2: Catalog & Inventory Management", "Deliver book catalog persistence, shelf classification, case-insensitive keyword search, and copy tracking.", "2026-09-08", "2026-09-14", "Completed", 11),
        (3, "Sprint 3: Circulation & Concurrency Engine", "Implement transactional book borrow, double-issue locking, borrower quota enforcement, and inventory recovery upon return.", "2026-09-15", "2026-09-21", "Completed", 16),
        (4, "Sprint 4: Lifecycle Extensions & Financial Compliance", "Support self-service loan renewals, out-of-stock reservation queue, and automated overdue fine calculation.", "2026-09-22", "2026-09-28", "Completed", 10),
        (5, "Sprint 5: In-App Scrum Tooling, Auditing & Release", "Deliver embedded SQLite Scrum management tables, terminal ASCII Kanban board, automated test suite, and viva demo release.", "2026-09-29", "2026-10-05", "Completed", 8)
    ]
    cursor.executemany("""
    INSERT INTO sprints (sprint_number, name, goal, start_date, end_date, status, velocity)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, sprints_data)

    # Seed User Stories (12 INVEST Stories)
    stories_data = [
        ("US-01", "Member Registration & Credential Hashing", "Member", "register an account with username, email, phone, and secure password", "I can access the library circulation services securely", "Must Have", 3, 1, "Done", "Annika Jha", "Implements salted SHA-256 password hashing and uniqueness validation across accounts."),
        ("US-02", "Role-Based Authentication & Session Management", "All Roles", "log in with valid credentials and receive role-specific capabilities", "the system restricts privileges between members, librarians, and administrators", "Must Have", 3, 1, "Done", "Dev Team", "Validates password hashes and provisions session roles (member, librarian, admin)."),
        ("US-03", "Book Catalog Management & Shelf Tracking", "Librarian", "add, edit, and categorize library books with ISBN and shelf locations", "physical copies are organized and discoverable within library stacks", "Must Have", 5, 2, "Done", "Dev Team", "Maintains ISBN uniqueness, publisher data, publication year, and physical shelf coordinates."),
        ("US-04", "Advanced Book Search & Category Filtering", "Member", "search books by title keyword, author, or category", "I can swiftly locate desired academic reference materials", "Must Have", 3, 2, "Done", "Dev Team", "Case-insensitive substring search matching titles, authors, and classification genres."),
        ("US-05", "Real-time Book Availability & Copy Inspection", "Member", "view real-time copy availability before visiting the library desk", "I only attempt to borrow books that are currently in stock", "Must Have", 3, 2, "Done", "Dev Team", "Displays total copies, available copies, and on-loan counts dynamically."),
        ("US-06", "Atomic Book Issue & Concurrency Control", "Member", "borrow an available book with an immediate 14-day due date", "the transaction safely decrements stock and prevents race conditions", "Must Have", 8, 3, "Done", "Annika Jha", "Enforces transactional integrity, checks member borrow quotas, and locks available copy count."),
        ("US-07", "Member Loan History & Due Date Overview", "Member", "review active loans, historical borrows, and approaching due dates", "I can return books punctually and avoid financial penalties", "Should Have", 3, 3, "Done", "Dev Team", "Presents loan records with borrowing timestamp, due dates, return statuses, and active flags."),
        ("US-08", "Book Return & Automated Inventory Recovery", "Member", "return a borrowed book and have the copy count restored immediately", "subsequent readers can check out the returned volume without delays", "Must Have", 5, 3, "Done", "Dev Team", "Marks loan record as Returned and atomically increments available copy stock."),
        ("US-09", "Self-Service Book Renewal & Reservation Queue", "Member", "renew an active loan or reserve an out-of-stock book", "I can keep study materials longer or get placed next in line", "Should Have", 5, 4, "Done", "Annika Jha", "Allows up to 2 renewals when no reservations exist; queues members when available copies reach 0."),
        ("US-10", "Automated Overdue Fine Calculation & Settlement", "Librarian", "compute daily overdue fines and record fee payments", "the institution discourages late returns and maintains circulation turnover", "Must Have", 5, 4, "Done", "Dev Team", "Applies ₹5/day penalty on overdue loans with clear Unpaid/Paid accounting."),
        ("US-11", "Centralized Librarian & Admin Inventory Audit", "Administrator", "audit system-wide loans, overdue items, reservations, and inventory health", "administrators have complete institutional oversight over circulation operations", "Could Have", 3, 5, "Done", "Dev Team", "Provides aggregated circulation statistics, overdue audit trails, and fine collection metrics."),
        ("US-12", "Built-in Scrum Backlog, Sprint & Terminal Kanban Engine", "Scrum Master", "manage user stories, sprint velocity, and ASCII Kanban workflows in-app", "the team practices transparent Agile software engineering with full traceability", "Must Have", 8, 5, "Done", "Annika Jha", "SQLite-backed Agile tables with 5-column Kanban board rendering and velocity metrics.")
    ]
    cursor.executemany("""
    INSERT INTO user_stories (story_code, title, role, want, benefit, priority, story_points, sprint_id, status, assignee, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, stories_data)

    # Seed Action Items (18 Action Items)
    action_items_data = [
        ("AI-01", "Initialize Git repository, branch structure, and .gitignore patterns", 1, "Annika Jha", "High", "2026-09-02", "Done"),
        ("AI-02", "Design relational SQLite schema with foreign keys and index constraints", 1, "Dev Team", "High", "2026-09-03", "Done"),
        ("AI-03", "Implement SHA-256 password salting and authentication module", 1, "Annika Jha", "High", "2026-09-05", "Done"),
        ("AI-04", "Draft User Stories and Gherkin Acceptance Criteria specifications", 1, "Annika Jha", "Medium", "2026-09-06", "Done"),
        ("AI-05", "Develop book catalog model with ISBN uniqueness and shelf locations", 2, "Dev Team", "High", "2026-09-09", "Done"),
        ("AI-06", "Implement case-insensitive book search and genre category filters", 2, "Dev Team", "High", "2026-09-11", "Done"),
        ("AI-07", "Populate initial academic textbook dataset across multiple subjects", 2, "Dev Team", "Low", "2026-09-13", "Done"),
        ("AI-08", "Construct atomic book borrow engine with concurrency protection", 3, "Annika Jha", "High", "2026-09-16", "Done"),
        ("AI-09", "Enforce member borrowing quota (max 3 books) and fine restriction", 3, "Annika Jha", "High", "2026-09-18", "Done"),
        ("AI-10", "Implement book return workflow with automatic inventory replenishment", 3, "Dev Team", "High", "2026-09-20", "Done"),
        ("AI-11", "Build member loan history and active checkouts dashboard query", 3, "Dev Team", "Medium", "2026-09-21", "Done"),
        ("AI-12", "Develop 14-day book loan renewal logic with reservation conflict guard", 4, "Annika Jha", "High", "2026-09-23", "Done"),
        ("AI-13", "Implement out-of-stock reservation queue for unavailable books", 4, "Dev Team", "Medium", "2026-09-25", "Done"),
        ("AI-14", "Create overdue fine calculation engine (₹5/day) and payment settlement", 4, "Dev Team", "High", "2026-09-27", "Done"),
        ("AI-15", "Implement in-app Scrum management database tables and service layer", 5, "Annika Jha", "High", "2026-09-30", "Done"),
        ("AI-16", "Construct 5-column ANSI terminal ASCII Kanban board renderer", 5, "Annika Jha", "High", "2026-10-01", "Done"),
        ("AI-17", "Implement comprehensive 16-case automated test suite with 100% pass rate", 5, "Annika Jha", "High", "2026-10-03", "Done"),
        ("AI-18", "Conduct Sprint Review, Retrospective, and final Viva demo rehearsal", 5, "Annika Jha", "High", "2026-10-05", "Done")
    ]
    cursor.executemany("""
    INSERT INTO action_items (item_code, description, sprint_id, owner, priority, due_date, status)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, action_items_data)

    # Seed Initial Circulation Activity (1 Active Loan, 1 Overdue Loan for Demonstration)
    now = datetime.now()
    two_weeks_ago = (now - timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S")
    overdue_due = (now - timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S")
    today_str = now.strftime("%Y-%m-%d %H:%M:%S")
    due_in_two_weeks = (now + timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")

    # Book 1 (Clean Code) borrowed by Aarav Patel
    cursor.execute("""
    INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, status, renewal_count)
    VALUES (1, 1, ?, ?, 'Borrowed', 0);
    """, (today_str, due_in_two_weeks))

    # Book 9 (The Pragmatic Programmer) borrowed by Diya Sharma and currently overdue
    cursor.execute("""
    INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, status, renewal_count)
    VALUES (2, 9, ?, ?, 'Overdue', 0);
    """, (two_weeks_ago, overdue_due))
    borrow_id_2 = cursor.lastrowid

    # Overdue fine for Diya Sharma (6 days * 5 = ₹30)
    cursor.execute("""
    INSERT INTO fines (borrow_id, user_id, amount, fine_date, paid_status)
    VALUES (?, 2, 30.0, ?, 'Unpaid');
    """, (borrow_id_2, today_str))

    # Reservation for Book 9 (which is out of stock) by Aarav Patel
    cursor.execute("""
    INSERT INTO reservations (user_id, book_id, reservation_date, status)
    VALUES (1, 9, ?, 'Pending');
    """, (today_str,))

    # Audit Logs
    cursor.execute("""
    INSERT INTO audit_logs (action_type, user_id, user_name, details)
    VALUES ('SYSTEM_INIT', 4, 'System Administrator', 'Database initialized with academic library catalog and Scrum sprint baselines.');
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_initial_data()
    print("[SUCCESS] Database schema initialized and seeded successfully.")
