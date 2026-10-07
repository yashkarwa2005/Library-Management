"""Library Service Module
Core business logic for circulation, inventory, member quotas, reservations, and fine accounting.
Author / Scrum Lead: Annika Jha
"""
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from .database import get_connection, hash_password


class LibraryService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def _get_conn(self) -> sqlite3.Connection:
        return get_connection(self.db_path)

    # =========================================================================
    # 1. User Management & Authentication (Sprint 1)
    # =========================================================================

    def register_user(self, username: str, password: str, full_name: str,
                      email: str, phone: str = "", role: str = "member") -> Dict[str, Any]:
        """Registers a new library user with SHA-256 salted password hashing."""
        username = username.strip()
        email = email.strip()
        full_name = full_name.strip()

        if not username or not password or not full_name or not email:
            raise ValueError("All mandatory fields (username, password, full name, email) must be provided.")

        if role not in ("member", "librarian", "admin"):
            raise ValueError(f"Invalid role '{role}'. Permitted roles: 'member', 'librarian', 'admin'.")

        hashed_pwd = hash_password(password)

        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, email, phone, role)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (username, hashed_pwd, full_name, email, phone.strip(), role))
            user_id = cursor.lastrowid

            cursor.execute("""
            INSERT INTO audit_logs (action_type, user_id, user_name, details)
            VALUES ('USER_REGISTER', ?, ?, ?);
            """, (user_id, full_name, f"Registered new user '{username}' with role '{role}'."))

            conn.commit()
            return {
                "id": user_id,
                "username": username,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "role": role
            }
        except sqlite3.IntegrityError as e:
            conn.rollback()
            err = str(e).lower()
            if "username" in err:
                raise ValueError(f"Username '{username}' already exists. Please choose another username.")
            elif "email" in err:
                raise ValueError(f"Email '{email}' is already registered. Please use another email.")
            else:
                raise ValueError(f"Registration integrity conflict: {e}")
        finally:
            conn.close()

    def login_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticates user credentials and returns session payload."""
        username = username.strip()
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT id, username, password_hash, full_name, email, phone, role
            FROM users WHERE username = ?;
            """, (username,))
            row = cursor.fetchone()
            if not row:
                return None

            expected_hash = hash_password(password)
            if row["password_hash"] == expected_hash:
                return {
                    "id": row["id"],
                    "username": row["username"],
                    "full_name": row["full_name"],
                    "email": row["email"],
                    "phone": row["phone"],
                    "role": row["role"]
                }
            return None
        finally:
            conn.close()

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves user profile by primary key."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, username, full_name, email, phone, role FROM users WHERE id = ?;", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    # =========================================================================
    # 2. Book Catalog Management (Sprint 2)
    # =========================================================================

    def add_book(self, isbn: str, title: str, author: str, category: str,
                 publisher: str, publication_year: int, total_copies: int,
                 shelf_location: str) -> Dict[str, Any]:
        """Adds a new academic textbook or literature volume to the library catalog."""
        isbn = isbn.strip()
        title = title.strip()
        author = author.strip()
        category = category.strip()

        if not isbn or not title or not author or not category:
            raise ValueError("ISBN, title, author, and category are mandatory fields.")

        if total_copies < 1:
            raise ValueError("Total copies must be at least 1.")

        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO books (isbn, title, author, category, publisher, publication_year,
                               total_copies, available_copies, shelf_location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (isbn, title, author, category, publisher.strip(), publication_year,
                  total_copies, total_copies, shelf_location.strip()))
            book_id = cursor.lastrowid

            cursor.execute("""
            INSERT INTO audit_logs (action_type, details)
            VALUES ('BOOK_ADD', ?);
            """, (f"Added book '{title}' (ISBN: {isbn}, Copies: {total_copies}, Shelf: {shelf_location}).",))

            conn.commit()
            return {
                "id": book_id,
                "isbn": isbn,
                "title": title,
                "author": author,
                "category": category,
                "publisher": publisher,
                "publication_year": publication_year,
                "total_copies": total_copies,
                "available_copies": total_copies,
                "shelf_location": shelf_location
            }
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError(f"Book with ISBN '{isbn}' already exists in catalog.")
        finally:
            conn.close()

    def update_book(self, book_id: int, **kwargs) -> Dict[str, Any]:
        """Updates metadata or copy counts for an existing book."""
        allowed_fields = ("title", "author", "category", "publisher", "publication_year",
                          "total_copies", "shelf_location")
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            raise ValueError("No valid fields provided to update.")

        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM books WHERE id = ?;", (book_id,))
            current = cursor.fetchone()
            if not current:
                raise ValueError(f"Book with ID {book_id} not found.")

            # If total_copies is changing, adjust available_copies accordingly
            if "total_copies" in updates:
                new_total = int(updates["total_copies"])
                diff = new_total - current["total_copies"]
                new_available = current["available_copies"] + diff
                if new_available < 0:
                    raise ValueError(f"Cannot reduce total copies below active borrowed count ({current['total_copies'] - current['available_copies']}).")
                updates["available_copies"] = new_available

            set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
            values = list(updates.values()) + [book_id]
            cursor.execute(f"UPDATE books SET {set_clause} WHERE id = ?;", values)
            conn.commit()

            cursor.execute("SELECT * FROM books WHERE id = ?;", (book_id,))
            return dict(cursor.fetchone())
        finally:
            conn.close()

    def delete_book(self, book_id: int) -> bool:
        """Deletes a book from the catalog only if zero copies are actively borrowed."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM books WHERE id = ?;", (book_id,))
            book = cursor.fetchone()
            if not book:
                raise ValueError(f"Book with ID {book_id} not found.")

            # Check active loans
            cursor.execute("""
            SELECT COUNT(*) AS active_cnt FROM borrow_records
            WHERE book_id = ? AND status IN ('Borrowed', 'Overdue');
            """, (book_id,))
            if cursor.fetchone()["active_cnt"] > 0:
                raise ValueError(f"Cannot delete book '{book['title']}' while active copies are checked out by members.")

            cursor.execute("DELETE FROM books WHERE id = ?;", (book_id,))
            cursor.execute("""
            INSERT INTO audit_logs (action_type, details)
            VALUES ('BOOK_DELETE', ?);
            """, (f"Deleted book '{book['title']}' (ID: {book_id}).",))

            conn.commit()
            return True
        finally:
            conn.close()

    def get_all_books(self) -> List[Dict[str, Any]]:
        """Returns all books ordered by title."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM books ORDER BY title ASC;")
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_book_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Returns single book dictionary by ID."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM books WHERE id = ?;", (book_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def search_books(self, keyword: str = "", category: str = "") -> List[Dict[str, Any]]:
        """Case-insensitive search matching title, author, ISBN, or genre category."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM books WHERE 1=1"
            params = []

            if keyword:
                kw = f"%{keyword.strip().lower()}%"
                query += " AND (LOWER(title) LIKE ? OR LOWER(author) LIKE ? OR LOWER(isbn) LIKE ?)"
                params.extend([kw, kw, kw])

            if category:
                query += " AND LOWER(category) = ?"
                params.append(category.strip().lower())

            query += " ORDER BY title ASC;"
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    # =========================================================================
    # 3. Circulation Engine: Borrow & Return (Sprint 3)
    # =========================================================================

    def borrow_book(self, user_id: int, book_id: int, days: int = 14) -> Dict[str, Any]:
        """Atomically issues a book to a member, enforcing borrower quotas and stock concurrency."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            # 1. Verify User existence & role
            cursor.execute("SELECT id, username, full_name, role FROM users WHERE id = ?;", (user_id,))
            user = cursor.fetchone()
            if not user:
                raise ValueError(f"User with ID {user_id} does not exist.")

            # 2. Check for unpaid fines (Policy: unpaid fines block borrowing)
            cursor.execute("""
            SELECT SUM(amount) AS total_unpaid FROM fines
            WHERE user_id = ? AND paid_status = 'Unpaid';
            """, (user_id,))
            unpaid_row = cursor.fetchone()
            unpaid_total = unpaid_row["total_unpaid"] or 0.0
            if unpaid_total > 0:
                raise ValueError(f"Borrowing blocked: Member has unpaid fines totaling ₹{unpaid_total:.2f}. Please clear fines first.")

            # 3. Check active loan quota (Max 3 books per member)
            cursor.execute("""
            SELECT COUNT(*) AS active_loans FROM borrow_records
            WHERE user_id = ? AND status IN ('Borrowed', 'Overdue');
            """, (user_id,))
            active_count = cursor.fetchone()["active_loans"]
            if active_count >= 3:
                raise ValueError("Borrowing limit reached: Maximum 3 active books permitted per member.")

            # 4. Check if member already has this exact book borrowed
            cursor.execute("""
            SELECT id FROM borrow_records
            WHERE user_id = ? AND book_id = ? AND status IN ('Borrowed', 'Overdue');
            """, (user_id, book_id))
            if cursor.fetchone():
                raise ValueError("Member already has an active checked-out copy of this book.")

            # 5. Atomic check & decrement of available copies
            cursor.execute("SELECT * FROM books WHERE id = ?;", (book_id,))
            book = cursor.fetchone()
            if not book:
                raise ValueError(f"Book with ID {book_id} not found.")

            if book["available_copies"] <= 0:
                raise ValueError(f"Book '{book['title']}' is currently out of stock (0 copies available). You may place a reservation.")

            now = datetime.now()
            borrow_date_str = now.strftime("%Y-%m-%d %H:%M:%S")
            due_date_str = (now + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
            UPDATE books
            SET available_copies = available_copies - 1
            WHERE id = ? AND available_copies > 0;
            """, (book_id,))

            if cursor.rowcount == 0:
                raise ValueError("Concurrency conflict: The last available copy was checked out simultaneously by another user.")

            # 6. Insert borrow record
            cursor.execute("""
            INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, status, renewal_count)
            VALUES (?, ?, ?, ?, 'Borrowed', 0);
            """, (user_id, book_id, borrow_date_str, due_date_str))
            borrow_id = cursor.lastrowid

            # 7. Record Audit Log
            cursor.execute("""
            INSERT INTO audit_logs (action_type, user_id, user_name, details)
            VALUES ('BOOK_BORROW', ?, ?, ?);
            """, (user_id, user["full_name"], f"Issued '{book['title']}' (Loan #{borrow_id}, Due: {due_date_str[:10]})."))

            conn.commit()
            return {
                "borrow_id": borrow_id,
                "user_id": user_id,
                "book_id": book_id,
                "title": book["title"],
                "borrow_date": borrow_date_str,
                "due_date": due_date_str,
                "status": "Borrowed"
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def return_book(self, borrow_id: int) -> Dict[str, Any]:
        """Returns a borrowed book, restores inventory stock, and assesses overdue penalties."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT br.*, b.title, b.available_copies, u.full_name, u.username
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            JOIN users u ON br.user_id = u.id
            WHERE br.id = ?;
            """, (borrow_id,))
            record = cursor.fetchone()
            if not record:
                raise ValueError(f"Borrow record #{borrow_id} not found.")

            if record["status"] == "Returned":
                raise ValueError(f"Book '{record['title']}' was already returned on {record['return_date']}.")

            now = datetime.now()
            return_date_str = now.strftime("%Y-%m-%d %H:%M:%S")

            # 1. Update borrow record status
            cursor.execute("""
            UPDATE borrow_records
            SET return_date = ?, status = 'Returned'
            WHERE id = ?;
            """, (return_date_str, borrow_id))

            # 2. Replenish available book copies atomically
            cursor.execute("""
            UPDATE books
            SET available_copies = available_copies + 1
            WHERE id = ?;
            """, (record["book_id"],))

            # 3. Assess Overdue Fine (₹5 per calendar day past due date)
            due_dt = datetime.strptime(record["due_date"], "%Y-%m-%d %H:%M:%S")
            fine_amount = 0.0
            overdue_days = 0
            if now > due_dt:
                delta = now - due_dt
                overdue_days = max(1, delta.days)
                fine_amount = round(overdue_days * 5.0, 2)

                cursor.execute("""
                INSERT INTO fines (borrow_id, user_id, amount, fine_date, paid_status)
                VALUES (?, ?, ?, ?, 'Unpaid');
                """, (borrow_id, record["user_id"], fine_amount, return_date_str))

            # 4. Check for pending reservations on this book and fulfill the oldest
            cursor.execute("""
            SELECT id, user_id FROM reservations
            WHERE book_id = ? AND status = 'Pending'
            ORDER BY reservation_date ASC LIMIT 1;
            """, (record["book_id"],))
            res_row = cursor.fetchone()
            reservation_msg = ""
            if res_row:
                cursor.execute("UPDATE reservations SET status = 'Fulfilled' WHERE id = ?;", (res_row["id"],))
                reservation_msg = f" (Held for queued reservation #{res_row['id']})"

            cursor.execute("""
            INSERT INTO audit_logs (action_type, user_id, user_name, details)
            VALUES ('BOOK_RETURN', ?, ?, ?);
            """, (record["user_id"], record["full_name"],
                  f"Returned '{record['title']}' (Loan #{borrow_id}, Overdue Days: {overdue_days}, Fine: ₹{fine_amount}){reservation_msg}."))

            conn.commit()
            return {
                "borrow_id": borrow_id,
                "book_id": record["book_id"],
                "title": record["title"],
                "return_date": return_date_str,
                "overdue_days": overdue_days,
                "fine_amount": fine_amount,
                "reservation_alert": reservation_msg.strip(),
                "status": "Returned"
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # =========================================================================
    # 4. Lifecycle Extensions: Renewals, Reservations & Fines (Sprint 4)
    # =========================================================================

    def renew_book(self, borrow_id: int, additional_days: int = 14) -> Dict[str, Any]:
        """Extends book due date if renewal limit not reached and no pending reservations exist."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT br.*, b.title, u.full_name
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            JOIN users u ON br.user_id = u.id
            WHERE br.id = ?;
            """, (borrow_id,))
            record = cursor.fetchone()
            if not record:
                raise ValueError(f"Borrow record #{borrow_id} not found.")

            if record["status"] != "Borrowed":
                raise ValueError(f"Cannot renew loan with status '{record['status']}'.")

            if record["renewal_count"] >= 2:
                raise ValueError("Renewal limit reached: A maximum of 2 renewals is permitted per loan.")

            # Check if another member has reserved this book
            cursor.execute("""
            SELECT COUNT(*) AS res_count FROM reservations
            WHERE book_id = ? AND status = 'Pending';
            """, (record["book_id"],))
            if cursor.fetchone()["res_count"] > 0:
                raise ValueError(f"Cannot renew '{record['title']}': Another library member has reserved this book.")

            current_due = datetime.strptime(record["due_date"], "%Y-%m-%d %H:%M:%S")
            new_due = current_due + timedelta(days=additional_days)
            new_due_str = new_due.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
            UPDATE borrow_records
            SET due_date = ?, renewal_count = renewal_count + 1
            WHERE id = ?;
            """, (new_due_str, borrow_id))

            cursor.execute("""
            INSERT INTO audit_logs (action_type, user_id, user_name, details)
            VALUES ('BOOK_RENEW', ?, ?, ?);
            """, (record["user_id"], record["full_name"],
                  f"Renewed '{record['title']}' (Loan #{borrow_id}, New Due: {new_due_str[:10]}, Renewal #{record['renewal_count'] + 1})."))

            conn.commit()
            return {
                "borrow_id": borrow_id,
                "title": record["title"],
                "previous_due_date": record["due_date"],
                "new_due_date": new_due_str,
                "renewal_count": record["renewal_count"] + 1
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def reserve_book(self, user_id: int, book_id: int) -> Dict[str, Any]:
        """Places a reservation hold on a currently unavailable book."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT title, available_copies FROM books WHERE id = ?;", (book_id,))
            book = cursor.fetchone()
            if not book:
                raise ValueError(f"Book with ID {book_id} not found.")

            # Check if user already has an active reservation
            cursor.execute("""
            SELECT id FROM reservations
            WHERE user_id = ? AND book_id = ? AND status = 'Pending';
            """, (user_id, book_id))
            if cursor.fetchone():
                raise ValueError(f"You already have an active pending reservation for '{book['title']}'.")

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
            INSERT INTO reservations (user_id, book_id, reservation_date, status)
            VALUES (?, ?, ?, 'Pending');
            """, (user_id, book_id, now_str))
            res_id = cursor.lastrowid

            conn.commit()
            return {
                "reservation_id": res_id,
                "user_id": user_id,
                "book_id": book_id,
                "title": book["title"],
                "reservation_date": now_str,
                "status": "Pending"
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_user_fines(self, user_id: int) -> Dict[str, Any]:
        """Returns itemized fine breakdown and cumulative unpaid balance for a user."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT f.*, b.title, br.borrow_date, br.due_date, br.return_date
            FROM fines f
            JOIN borrow_records br ON f.borrow_id = br.id
            JOIN books b ON br.book_id = b.id
            WHERE f.user_id = ?
            ORDER BY f.fine_date DESC;
            """, (user_id,))
            items = [dict(row) for row in cursor.fetchall()]
            unpaid_total = sum(item["amount"] for item in items if item["paid_status"] == "Unpaid")
            return {
                "fines": items,
                "unpaid_total": round(unpaid_total, 2)
            }
        finally:
            conn.close()

    def pay_fine(self, fine_id: int) -> Dict[str, Any]:
        """Records payment settlement for an outstanding fine."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT f.*, u.full_name FROM fines f
            JOIN users u ON f.user_id = u.id
            WHERE f.id = ?;
            """, (fine_id,))
            fine = cursor.fetchone()
            if not fine:
                raise ValueError(f"Fine #{fine_id} not found.")

            if fine["paid_status"] == "Paid":
                raise ValueError(f"Fine #{fine_id} was already settled on {fine['paid_date']}.")

            paid_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
            UPDATE fines
            SET paid_status = 'Paid', paid_date = ?
            WHERE id = ?;
            """, (paid_str, fine_id))

            cursor.execute("""
            INSERT INTO audit_logs (action_type, user_id, user_name, details)
            VALUES ('FINE_PAY', ?, ?, ?);
            """, (fine["user_id"], fine["full_name"], f"Settled fine #{fine_id} of ₹{fine['amount']:.2f}."))

            conn.commit()
            return {
                "fine_id": fine_id,
                "amount": fine["amount"],
                "paid_status": "Paid",
                "paid_date": paid_str
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # =========================================================================
    # 5. Reporting, Audits & Member Overviews (Sprint 5)
    # =========================================================================

    def get_member_loans(self, user_id: int) -> List[Dict[str, Any]]:
        """Returns active checkouts and overdue indicators for a member."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT br.*, b.title, b.author, b.isbn, b.shelf_location
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            WHERE br.user_id = ? AND br.status IN ('Borrowed', 'Overdue')
            ORDER BY br.due_date ASC;
            """, (user_id,))
            rows = [dict(r) for r in cursor.fetchall()]
            now = datetime.now()
            for r in rows:
                due_dt = datetime.strptime(r["due_date"], "%Y-%m-%d %H:%M:%S")
                r["is_overdue"] = now > due_dt
                if r["is_overdue"]:
                    r["overdue_days"] = (now - due_dt).days
                else:
                    r["overdue_days"] = 0
            return rows
        finally:
            conn.close()

    def get_member_history(self, user_id: int) -> List[Dict[str, Any]]:
        """Returns complete historical borrowing ledger for a member."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT br.*, b.title, b.author, b.isbn, b.category
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            WHERE br.user_id = ?
            ORDER BY br.borrow_date DESC;
            """, (user_id,))
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_all_borrow_records(self) -> List[Dict[str, Any]]:
        """Returns all system-wide circulation transactions for librarians."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT br.*, b.title, b.isbn, u.full_name, u.username
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            JOIN users u ON br.user_id = u.id
            ORDER BY br.borrow_date DESC;
            """, (user_id,))
            return [dict(r) for r in cursor.fetchall()]
        except NameError:
            cursor.execute("""
            SELECT br.*, b.title, b.isbn, u.full_name, u.username
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            JOIN users u ON br.user_id = u.id
            ORDER BY br.borrow_date DESC;
            """)
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_inventory_statistics(self) -> Dict[str, Any]:
        """Computes comprehensive institutional metrics for library administrators."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) AS total_titles, SUM(total_copies) AS total_copies, SUM(available_copies) AS available_copies FROM books;")
            b_stats = cursor.fetchone()

            cursor.execute("SELECT COUNT(*) AS active_loans FROM borrow_records WHERE status IN ('Borrowed', 'Overdue');")
            active_loans = cursor.fetchone()["active_loans"]

            cursor.execute("SELECT COUNT(*) AS overdue_loans FROM borrow_records WHERE status = 'Overdue';")
            overdue_loans = cursor.fetchone()["overdue_loans"]

            cursor.execute("SELECT COUNT(*) AS total_members FROM users WHERE role = 'member';")
            total_members = cursor.fetchone()["total_members"]

            cursor.execute("SELECT COUNT(*) AS pending_res FROM reservations WHERE status = 'Pending';")
            pending_res = cursor.fetchone()["pending_res"]

            cursor.execute("SELECT SUM(amount) AS total_unpaid FROM fines WHERE paid_status = 'Unpaid';")
            unpaid_fines = cursor.fetchone()["total_unpaid"] or 0.0

            cursor.execute("SELECT SUM(amount) AS total_paid FROM fines WHERE paid_status = 'Paid';")
            paid_fines = cursor.fetchone()["total_paid"] or 0.0

            return {
                "total_titles": b_stats["total_titles"] or 0,
                "total_copies": b_stats["total_copies"] or 0,
                "available_copies": b_stats["available_copies"] or 0,
                "borrowed_copies": (b_stats["total_copies"] or 0) - (b_stats["available_copies"] or 0),
                "active_loans": active_loans,
                "overdue_loans": overdue_loans,
                "total_members": total_members,
                "pending_reservations": pending_res,
                "total_unpaid_fines": round(unpaid_fines, 2),
                "total_collected_fines": round(paid_fines, 2)
            }
        finally:
            conn.close()

    def get_audit_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns the recent system audit event logs."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT ?;", (limit,))
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()
