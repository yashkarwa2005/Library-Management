"""Automated Unit and Integration Test Suite
Library Management System using Scrum Agile Methodology
Author / Scrum Lead: Annika Jha
"""
import unittest
import os
import sqlite3
from datetime import datetime, timedelta

from src.database import init_db, seed_initial_data, hash_password
from src.library import LibraryService
from src.user_story import UserStoryService
from src.sprint import SprintService
from src.action_item import ActionItemService
from src.kanban import KanbanService


class TestLibraryManagementSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use an isolated SQLite test database
        cls.test_db = os.path.join(os.path.dirname(__file__), "test_library.db")
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
        init_db(cls.test_db)
        seed_initial_data(cls.test_db)

        cls.lib = LibraryService(cls.test_db)
        cls.story_service = UserStoryService(cls.test_db)
        cls.sprint_service = SprintService(cls.test_db)
        cls.action_service = ActionItemService(cls.test_db)
        cls.kanban = KanbanService(cls.test_db)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db):
            try:
                os.remove(cls.test_db)
            except Exception:
                pass

    # =========================================================================
    # Sprint 1 Tests: Security & Identity Management (US-01, US-02)
    # =========================================================================

    def test_tc01_user_registration(self):
        """TC-01: Valid user registration with SHA-256 salted hash."""
        user = self.lib.register_user(
            username="test_student_1",
            password="StrongPassword123!",
            full_name="Test Student One",
            email="student1@test.edu",
            phone="9876500001",
            role="member"
        )
        self.assertIsNotNone(user["id"])
        self.assertEqual(user["username"], "test_student_1")
        self.assertEqual(user["role"], "member")

    def test_tc02_duplicate_registration_rejection(self):
        """TC-02: Rejection of duplicate username or email."""
        with self.assertRaises(ValueError) as ctx:
            self.lib.register_user(
                username="aarav_p",  # Already seeded
                password="AnotherPassword!",
                full_name="Duplicate User",
                email="aarav_duplicate@example.com"
            )
        self.assertIn("already exists", str(ctx.exception))

    def test_tc03_user_login_success(self):
        """TC-03: Successful authentication with valid credentials."""
        session = self.lib.login_user("aarav_p", "aarav123")
        self.assertIsNotNone(session)
        self.assertEqual(session["username"], "aarav_p")
        self.assertEqual(session["role"], "member")

    def test_tc04_user_login_invalid_credentials(self):
        """TC-04: Rejection of invalid password."""
        session = self.lib.login_user("aarav_p", "WrongPassword!")
        self.assertIsNone(session)

    # =========================================================================
    # Sprint 2 Tests: Catalog & Real-Time Availability (US-03, US-04, US-05)
    # =========================================================================

    def test_tc05_add_book_and_catalog_persistence(self):
        """TC-05: Adding a new academic textbook and verifying inventory."""
        new_book = self.lib.add_book(
            isbn="978-0131103627",
            title="The C Programming Language (2nd Edition)",
            author="Brian W. Kernighan, Dennis M. Ritchie",
            category="Programming",
            publisher="Prentice Hall",
            publication_year=1988,
            total_copies=5,
            shelf_location="Shelf K-01"
        )
        self.assertIsNotNone(new_book["id"])
        self.assertEqual(new_book["available_copies"], 5)

        # Check duplicate ISBN rejection
        with self.assertRaises(ValueError):
            self.lib.add_book(
                isbn="978-0131103627",
                title="Duplicate ISBN Book",
                author="Unknown",
                category="Programming",
                publisher="Prentice Hall",
                publication_year=1990,
                total_copies=1,
                shelf_location="Shelf K-02"
            )

    def test_tc06_search_books_by_keyword_and_category(self):
        """TC-06: Case-insensitive search across title, author, and category."""
        results = self.lib.search_books(keyword="algorithms")
        self.assertTrue(len(results) >= 1)
        self.assertIn("Introduction to Algorithms", results[0]["title"])

        cat_results = self.lib.search_books(category="Operating Systems")
        self.assertTrue(len(cat_results) >= 1)
        self.assertIn("Modern Operating Systems", cat_results[0]["title"])

    def test_tc07_realtime_availability_inspection(self):
        """TC-07: Verifying available copy count and shelf location."""
        book = self.lib.get_book_by_id(1)  # Clean Code
        self.assertIsNotNone(book)
        self.assertGreaterEqual(book["total_copies"], book["available_copies"])
        self.assertTrue(len(book["shelf_location"]) > 0)

    # =========================================================================
    # Sprint 3 Tests: Circulation Engine: Borrow & Return (US-06, US-07, US-08)
    # =========================================================================

    def test_tc08_atomic_book_borrow_and_decrement(self):
        """TC-08: Atomic book borrow, due date generation, and stock decrement."""
        # Book 3: Effective Java
        book_before = self.lib.get_book_by_id(3)
        avail_before = book_before["available_copies"]

        loan = self.lib.borrow_book(user_id=1, book_id=3)
        self.assertIsNotNone(loan["borrow_id"])
        self.assertEqual(loan["status"], "Borrowed")

        book_after = self.lib.get_book_by_id(3)
        self.assertEqual(book_after["available_copies"], avail_before - 1)

    def test_tc09_borrow_out_of_stock_rejection(self):
        """TC-09: Rejection when available copies equal 0."""
        # Book 9 (The Pragmatic Programmer) is seeded with available_copies = 0
        with self.assertRaises(ValueError) as ctx:
            self.lib.borrow_book(user_id=1, book_id=9)
        self.assertIn("out of stock", str(ctx.exception).lower())

    def test_tc10_borrow_quota_enforcement(self):
        """TC-10: Enforcing member maximum checkout limit (3 books)."""
        # Create a fresh test member
        u = self.lib.register_user(
            username="quota_tester",
            password="Password123!",
            full_name="Quota Tester",
            email="quota@test.edu"
        )
        # Borrow 3 books (Book 5, 6, 7)
        self.lib.borrow_book(u["id"], 5)
        self.lib.borrow_book(u["id"], 6)
        self.lib.borrow_book(u["id"], 7)

        # 4th borrow should be rejected
        with self.assertRaises(ValueError) as ctx:
            self.lib.borrow_book(u["id"], 8)
        self.assertIn("limit reached", str(ctx.exception).lower())

    def test_tc11_member_active_loans_retrieval(self):
        """TC-11: Member can retrieve active loans with overdue flags."""
        loans = self.lib.get_member_loans(1)
        self.assertTrue(len(loans) >= 1)
        self.assertIn("title", loans[0])
        self.assertIn("due_date", loans[0])

    def test_tc12_book_return_and_stock_replenishment(self):
        """TC-12: Book return restores available copies atomically."""
        # Member 1 borrowed Book 3 in TC-08. Retrieve that loan.
        loans = self.lib.get_member_loans(1)
        target_loan = [l for l in loans if l["book_id"] == 3][0]

        book_before = self.lib.get_book_by_id(3)
        res = self.lib.return_book(target_loan["id"])

        self.assertEqual(res["status"], "Returned")
        book_after = self.lib.get_book_by_id(3)
        self.assertEqual(book_after["available_copies"], book_before["available_copies"] + 1)

    # =========================================================================
    # Sprint 4 Tests: Lifecycle Extensions & Fines (US-09, US-10)
    # =========================================================================

    def test_tc13_overdue_fine_assessment(self):
        """TC-13: Overdue fine calculated accurately at ₹5/day upon return."""
        # Insert a synthetic overdue loan
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        borrow_dt = (datetime.now() - timedelta(days=25)).strftime("%Y-%m-%d %H:%M:%S")
        due_dt = (datetime.now() - timedelta(days=11)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, status, renewal_count)
        VALUES (1, 8, ?, ?, 'Overdue', 0);
        """, (borrow_dt, due_dt))
        synthetic_loan_id = cursor.lastrowid
        conn.commit()
        conn.close()

        ret_res = self.lib.return_book(synthetic_loan_id)
        self.assertEqual(ret_res["overdue_days"], 11)
        self.assertEqual(ret_res["fine_amount"], 55.0)  # 11 days * 5.0 = ₹55.0

    def test_tc14_fine_settlement_and_payment(self):
        """TC-14: Fine payment updates status to Paid."""
        fines = self.lib.get_user_fines(1)
        self.assertTrue(len(fines["fines"]) >= 1)
        target_fine = fines["fines"][0]

        paid_res = self.lib.pay_fine(target_fine["id"])
        self.assertEqual(paid_res["paid_status"], "Paid")

        # Double payment rejection
        with self.assertRaises(ValueError):
            self.lib.pay_fine(target_fine["id"])

    def test_tc15_out_of_stock_reservation_queue(self):
        """TC-15: Reserving an unavailable book and duplicate check."""
        res = self.lib.reserve_book(user_id=2, book_id=9)
        self.assertEqual(res["status"], "Pending")

        # Duplicate reservation rejection
        with self.assertRaises(ValueError):
            self.lib.reserve_book(user_id=2, book_id=9)

    # =========================================================================
    # Sprint 5 Tests: Built-in Scrum Engine & Kanban (US-11, US-12)
    # =========================================================================

    def test_tc16_scrum_engine_and_kanban_transition(self):
        """TC-16: Creating user story, verifying MoSCoW, and transitioning Kanban status."""
        new_story = self.story_service.create_user_story(
            story_code="US-TEST",
            title="Automated Test Coverage Story",
            role="Developer",
            want="write comprehensive unit tests",
            benefit="we achieve zero regressions",
            priority="Must Have",
            story_points=5,
            sprint_id=5,
            status="In Progress",
            assignee="Annika Jha"
        )
        self.assertEqual(new_story["story_code"], "US-TEST")

        trans = self.story_service.update_user_story_status("US-TEST", "Done")
        self.assertEqual(trans["status"], "Done")

        # Verify board grouping
        board = self.kanban.get_board_data()
        done_codes = [card["code"] for card in board["Done"]]
        self.assertIn("US-TEST", done_codes)


if __name__ == "__main__":
    unittest.main()
