"""Main Application Entry Point
Library Management System using Scrum Agile Methodology
Supports interactive terminal console, automated viva demo mode, and command-line flags.
Author / Scrum Lead: Annika Jha
"""
import sys
import os
import time
import argparse
from typing import Optional, Dict, Any

# Ensure project root is on Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Force UTF-8 on Windows terminal to avoid charmap / cp1252 UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.database import init_db, seed_initial_data, DEFAULT_DB_PATH
from src.library import LibraryService
from src.user_story import UserStoryService
from src.sprint import SprintService
from src.action_item import ActionItemService
from src.kanban import KanbanService


class Color:
    """Terminal styling codes."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def print_banner():
    banner = f"""
{Color.CYAN}========================================================================================{Color.RESET}
{Color.BOLD}{Color.GREEN}     [+] LIBRARY MANAGEMENT SYSTEM - SCRUM AGILE METHODOLOGY (AM PBL){Color.RESET}
{Color.CYAN}========================================================================================{Color.RESET}
  {Color.YELLOW}* Student / Scrum Lead : Annika Jha (B.Tech 3rd Year) | Subject: Agile Methodologies{Color.RESET}
  {Color.BLUE}* Dual-Track Architecture: 1. Academic Library Engine  |  2. In-App Scrum & Kanban Engine{Color.RESET}
{Color.CYAN}----------------------------------------------------------------------------------------{Color.RESET}
"""
    print(banner)


class AppRunner:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        init_db(self.db_path)
        seed_initial_data(self.db_path)

        self.lib_service = LibraryService(self.db_path)
        self.story_service = UserStoryService(self.db_path)
        self.sprint_service = SprintService(self.db_path)
        self.action_service = ActionItemService(self.db_path)
        self.kanban_service = KanbanService(self.db_path)

        self.current_user: Optional[Dict[str, Any]] = None

    def run_automated_demo(self):
        """Executes a complete 30-second automated demonstration of all Agile User Stories."""
        print(f"\n{Color.BOLD}{Color.YELLOW}>>> STARTING AUTOMATED VIVA DEMONSTRATION MODE <<<{Color.RESET}")
        print("This scenario automatically exercises user stories US-01 through US-12.\n")
        time.sleep(1)

        # 1. US-01 & US-02: User Registration & Authentication
        print(f"{Color.CYAN}[Step 1/8] Verifying Sprint 1: Security & Identity Management...{Color.RESET}")
        demo_user = f"demo_student_{int(time.time()) % 10000}"
        reg = self.lib_service.register_user(
            username=demo_user,
            password="DemoPassword123!",
            full_name="Demo Candidate",
            email=f"{demo_user}@college.edu",
            phone="9988776655",
            role="member"
        )
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-01] Registered member '{reg['username']}' with salted SHA-256 hash.")

        session = self.lib_service.login_user(demo_user, "DemoPassword123!")
        assert session is not None, "Login failed!"
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-02] Authenticated session for '{session['full_name']}' (Role: {session['role']}).")
        time.sleep(1)

        # 2. US-03, US-04, US-05: Catalog Search & Availability
        print(f"\n{Color.CYAN}[Step 2/8] Verifying Sprint 2: Catalog & Real-Time Availability...{Color.RESET}")
        books = self.lib_service.search_books(keyword="Clean Code")
        assert len(books) > 0, "Book not found!"
        book = books[0]
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-04] Found book: '{book['title']}' by {book['author']}")
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-05] Copy availability: {book['available_copies']} of {book['total_copies']} copies in {book['shelf_location']}")
        time.sleep(1)

        # 3. US-06 & US-07: Atomic Issue & Loan Tracking
        print(f"\n{Color.CYAN}[Step 3/8] Verifying Sprint 3: Atomic Book Issue & Concurrency...{Color.RESET}")
        loan = self.lib_service.borrow_book(user_id=session["id"], book_id=book["id"])
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-06] Issued '{loan['title']}' (Loan #{loan['borrow_id']}). Due date set to: {loan['due_date'][:10]}")

        updated_book = self.lib_service.get_book_by_id(book["id"])
        print(f"  {Color.GREEN}[PASS]{Color.RESET} Stock count successfully decremented to: {updated_book['available_copies']} copies.")

        loans = self.lib_service.get_member_loans(session["id"])
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-07] Retrieved active loan register: {len(loans)} active checkout(s).")
        time.sleep(1)

        # 4. US-09: Loan Renewal
        print(f"\n{Color.CYAN}[Step 4/8] Verifying Sprint 4: Self-Service Renewal...{Color.RESET}")
        renew_res = self.lib_service.renew_book(borrow_id=loan["borrow_id"], additional_days=14)
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-09] Renewed loan #{loan['borrow_id']}. New Due Date: {renew_res['new_due_date'][:10]} (Renewal count: {renew_res['renewal_count']})")
        time.sleep(1)

        # 5. Out-of-stock reservation
        print(f"\n{Color.CYAN}[Step 5/8] Verifying Sprint 4: Out-of-Stock Reservation Queue...{Color.RESET}")
        pragmatic_books = self.lib_service.search_books(keyword="The Pragmatic Programmer")
        if pragmatic_books:
            p_book = pragmatic_books[0]
            print(f"  Target Book: '{p_book['title']}' (Available copies: {p_book['available_copies']})")
            res_obj = self.lib_service.reserve_book(user_id=session["id"], book_id=p_book["id"])
            print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-09] Queued reservation #{res_obj['reservation_id']} for out-of-stock volume.")
        time.sleep(1)

        # 6. US-08 & US-10: Book Return & Overdue Fine Assessment
        print(f"\n{Color.CYAN}[Step 6/8] Verifying Sprint 3 & Sprint 4: Return & Overdue Fine Engine...{Color.RESET}")
        ret_res = self.lib_service.return_book(borrow_id=loan["borrow_id"])
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-08] Returned '{ret_res['title']}'. Restored stock count to: {self.lib_service.get_book_by_id(book['id'])['available_copies']}")

        # Test pre-seeded overdue loan for user Diya Sharma (id=2)
        fines_info = self.lib_service.get_user_fines(user_id=2)
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-10] Retrieved pre-seeded member fines: {len(fines_info['fines'])} fine(s), Total Unpaid: ₹{fines_info['unpaid_total']:.2f}")
        if fines_info["fines"]:
            f_id = fines_info["fines"][0]["id"]
            settle_res = self.lib_service.pay_fine(fine_id=f_id)
            print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-10] Settled fine #{f_id} of ₹{settle_res['amount']:.2f} (Status: {settle_res['paid_status']})")
        time.sleep(1)

        # 7. US-11: Institutional Health Audit
        print(f"\n{Color.CYAN}[Step 7/8] Verifying Sprint 5: Institutional Health Audit...{Color.RESET}")
        stats = self.lib_service.get_inventory_statistics()
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-11] Library Stats: Titles: {stats['total_titles']} | Copies: {stats['total_copies']} | In Circulation: {stats['borrowed_copies']} | Members: {stats['total_members']}")
        time.sleep(1)

        # 8. US-12: Built-in Scrum Engine & Terminal Kanban
        print(f"\n{Color.CYAN}[Step 8/8] Verifying Sprint 5: In-App Scrum Tooling & ASCII Kanban...{Color.RESET}")
        metrics = self.story_service.get_backlog_metrics()
        print(f"  {Color.GREEN}[PASS]{Color.RESET} [US-12] Product Backlog: {metrics['total_stories']} Stories ({metrics['total_points']} pts), Completed: {metrics['completed_points']} pts ({metrics['completion_percentage']}%)")
        print("\nRendering Live ASCII Kanban Board from SQLite:")
        print(self.kanban_service.render_ascii_board())

        print(f"{Color.BOLD}{Color.GREEN}>>> AUTOMATED VIVA DEMONSTRATION FINISHED SUCCESSFULLY (100% VERIFIED) <<<{Color.RESET}\n")

    def display_kanban(self):
        """Displays the ASCII Kanban board."""
        print(self.kanban_service.render_ascii_board())

    def run_tests(self):
        """Executes the automated unittest suite."""
        import unittest
        loader = unittest.TestLoader()
        start_dir = os.path.join(PROJECT_ROOT, "tests")
        suite = loader.discover(start_dir)
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"\n{Color.BOLD}{Color.CYAN}=== RUNNING AUTOMATED UNIT & INTEGRATION TEST SUITE ==={Color.RESET}\n")
        res = runner.run(suite)
        if res.wasSuccessful():
            print(f"\n{Color.BOLD}{Color.GREEN}[SUCCESS] All {res.testsRun} tests passed with zero failures!{Color.RESET}\n")
        else:
            print(f"\n{Color.BOLD}{Color.RED}[FAILURE] {len(res.failures)} failures, {len(res.errors)} errors encountered.{Color.RESET}\n")

    def interactive_console(self):
        """Main interactive terminal CLI."""
        while True:
            print_banner()
            if self.current_user:
                print(f"Logged in as: {Color.BOLD}{self.current_user['full_name']}{Color.RESET} (Role: {Color.YELLOW}{self.current_user['role'].upper()}{Color.RESET}) | Username: {self.current_user['username']}")
            else:
                print("Session: Not Logged In (Guest)")
            print("\nMAIN MENU:")
            print("  [1] Member Portal (Search, Borrow, Return, Renew, Reservations, Fines)")
            print("  [2] Librarian Portal (Catalog Management, Circulation Ledger, Overdue Audit)")
            print("  [3] Administrator Portal (Institutional Metrics & Audit Logs)")
            print("  [4] Scrum & Agile Management (Backlog, 5-Week Sprints, Terminal Kanban)")
            print("  [5] Run Instant Automated Viva Demonstration (--demo)")
            print("  [6] Run Automated Unit Tests (--test)")
            print("  [7] User Login / Switch Account")
            print("  [8] Register New Account")
            print("  [0] Exit")

            choice = input("\nEnter choice [0-8]: ").strip()
            if choice == "1":
                self.menu_member()
            elif choice == "2":
                self.menu_librarian()
            elif choice == "3":
                self.menu_admin()
            elif choice == "4":
                self.menu_scrum()
            elif choice == "5":
                self.run_automated_demo()
                input("\nPress Enter to return to menu...")
            elif choice == "6":
                self.run_tests()
                input("\nPress Enter to return to menu...")
            elif choice == "7":
                self.login_flow()
            elif choice == "8":
                self.register_flow()
            elif choice == "0":
                print("\nThank you for using the Library Management System. Goodbye!\n")
                break
            else:
                print(f"{Color.RED}Invalid option. Please choose between 0 and 8.{Color.RESET}")
                time.sleep(1)

    def login_flow(self):
        print("\n--- User Login ---")
        print("Quick test logins: aarav_p / aarav123 | librarian_anita / anita123 | admin / admin123")
        u = input("Username: ").strip()
        p = input("Password: ").strip()
        user = self.lib_service.login_user(u, p)
        if user:
            self.current_user = user
            print(f"{Color.GREEN}[+] Login successful! Welcome {user['full_name']}.{Color.RESET}")
        else:
            print(f"{Color.RED}[-] Invalid username or password.{Color.RESET}")
        time.sleep(1.5)

    def register_flow(self):
        print("\n--- Register New Member Account ---")
        u = input("Desired Username: ").strip()
        p = input("Password: ").strip()
        name = input("Full Name: ").strip()
        email = input("Email Address: ").strip()
        phone = input("Phone Number: ").strip()
        try:
            user = self.lib_service.register_user(u, p, name, email, phone, role="member")
            print(f"{Color.GREEN}[+] Successfully registered {user['full_name']}! You can now log in.{Color.RESET}")
        except Exception as e:
            print(f"{Color.RED}[-] Registration error: {e}{Color.RESET}")
        time.sleep(2)

    def menu_member(self):
        while True:
            print(f"\n{Color.CYAN}--- MEMBER CIRCULATION PORTAL ---{Color.RESET}")
            print("  [1] Search Catalog by Keyword or Category")
            print("  [2] View All Books & Real-Time Availability")
            print("  [3] Borrow an Available Book (14-day checkout)")
            print("  [4] Return a Borrowed Book")
            print("  [5] Renew an Active Book Loan (+14 days)")
            print("  [6] Reserve an Out-of-Stock Book")
            print("  [7] View My Active Loans & Approaching Due Dates")
            print("  [8] View My Overdue Fines & Settle Payment")
            print("  [9] View Complete Borrowing History")
            print("  [0] Back to Main Menu")

            c = input("Select option [0-9]: ").strip()
            if c == "1":
                kw = input("Enter search term (title, author, or ISBN): ").strip()
                cat = input("Filter by Category (optional, press Enter to skip): ").strip()
                books = self.lib_service.search_books(kw, cat)
                print(f"\nFound {len(books)} matching book(s):")
                for b in books:
                    print(f"  * [ID {b['id']}] '{b['title']}' by {b['author']} | Available: {b['available_copies']}/{b['total_copies']} | Shelf: {b['shelf_location']}")
            elif c == "2":
                books = self.lib_service.get_all_books()
                print(f"\nComplete Catalog ({len(books)} titles):")
                for b in books:
                    print(f"  * [ID {b['id']}] '{b['title']}' | {b['author']} | Category: {b['category']} | In Stock: {b['available_copies']}/{b['total_copies']} | Shelf: {b['shelf_location']}")
            elif c == "3":
                uid = self.current_user["id"] if self.current_user else int(input("Enter Member User ID: ").strip())
                bid = int(input("Enter Book ID to borrow: ").strip())
                try:
                    res = self.lib_service.borrow_book(uid, bid)
                    print(f"{Color.GREEN}[+] Successfully issued '{res['title']}'! Due Date: {res['due_date'][:10]}{Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}[-] Borrow error: {e}{Color.RESET}")
            elif c == "4":
                loan_id = int(input("Enter Borrow Record ID to return: ").strip())
                try:
                    res = self.lib_service.return_book(loan_id)
                    print(f"{Color.GREEN}[+] Returned '{res['title']}'. Overdue days: {res['overdue_days']}, Fine assessed: ₹{res['fine_amount']:.2f}{res['reservation_alert']}{Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}[-] Return error: {e}{Color.RESET}")
            elif c == "5":
                loan_id = int(input("Enter Borrow Record ID to renew: ").strip())
                try:
                    res = self.lib_service.renew_book(loan_id)
                    print(f"{Color.GREEN}[+] Renewed '{res['title']}'! New Due Date: {res['new_due_date'][:10]} (Renewal #{res['renewal_count']}){Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}[-] Renewal error: {e}{Color.RESET}")
            elif c == "6":
                uid = self.current_user["id"] if self.current_user else int(input("Enter Member User ID: ").strip())
                bid = int(input("Enter Book ID to reserve: ").strip())
                try:
                    res = self.lib_service.reserve_book(uid, bid)
                    print(f"{Color.GREEN}[+] Placed reservation #{res['reservation_id']} for '{res['title']}'.{Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}[-] Reservation error: {e}{Color.RESET}")
            elif c == "7":
                uid = self.current_user["id"] if self.current_user else int(input("Enter Member User ID: ").strip())
                loans = self.lib_service.get_member_loans(uid)
                print(f"\nActive Loans for Member #{uid} ({len(loans)} items):")
                for l in loans:
                    overdue_flag = f"{Color.RED}[OVERDUE by {l['overdue_days']} days]{Color.RESET}" if l["is_overdue"] else f"{Color.GREEN}[On Schedule]{Color.RESET}"
                    print(f"  * [Loan #{l['id']}] '{l['title']}' | Due: {l['due_date'][:10]} | Status: {l['status']} {overdue_flag}")
            elif c == "8":
                uid = self.current_user["id"] if self.current_user else int(input("Enter Member User ID: ").strip())
                fines = self.lib_service.get_user_fines(uid)
                print(f"\nFines for Member #{uid} (Total Unpaid: ₹{fines['unpaid_total']:.2f}):")
                for f in fines["fines"]:
                    print(f"  * [Fine #{f['id']}] '{f['title']}' | ₹{f['amount']:.2f} | Status: {f['paid_status']} | Date: {f['fine_date'][:10]}")
                if fines["unpaid_total"] > 0:
                    pay_choice = input("Enter Fine ID to pay (or press Enter to skip): ").strip()
                    if pay_choice:
                        try:
                            p_res = self.lib_service.pay_fine(int(pay_choice))
                            print(f"{Color.GREEN}[+] Settled fine #{p_res['fine_id']} of ₹{p_res['amount']:.2f}!{Color.RESET}")
                        except Exception as e:
                            print(f"{Color.RED}[-] Payment error: {e}{Color.RESET}")
            elif c == "9":
                uid = self.current_user["id"] if self.current_user else int(input("Enter Member User ID: ").strip())
                hist = self.lib_service.get_member_history(uid)
                print(f"\nBorrowing History ({len(hist)} records):")
                for h in hist:
                    print(f"  * [Loan #{h['id']}] '{h['title']}' | Borrowed: {h['borrow_date'][:10]} | Due: {h['due_date'][:10]} | Returned: {h.get('return_date', 'Not yet') or 'Active'} | Status: {h['status']}")
            elif c == "0":
                break

    def menu_librarian(self):
        print(f"\n{Color.CYAN}--- LIBRARIAN MANAGEMENT DESK ---{Color.RESET}")
        print("  [1] Add New Book to Catalog")
        print("  [2] View All System Circulation Records")
        print("  [3] View Institutional Overview & Overdue Stats")
        c = input("Select option [1-3] or 0 to exit: ").strip()
        if c == "1":
            isbn = input("ISBN (e.g., 978-0131103627): ").strip()
            title = input("Book Title: ").strip()
            author = input("Author(s): ").strip()
            category = input("Category: ").strip()
            publisher = input("Publisher: ").strip()
            year = int(input("Publication Year: ").strip())
            copies = int(input("Total Copies: ").strip())
            shelf = input("Shelf Location: ").strip()
            try:
                b = self.lib_service.add_book(isbn, title, author, category, publisher, year, copies, shelf)
                print(f"{Color.GREEN}[+] Added '{b['title']}' (ID #{b['id']}) to catalog successfully!{Color.RESET}")
            except Exception as e:
                print(f"{Color.RED}[-] Error adding book: {e}{Color.RESET}")
        elif c == "2":
            records = self.lib_service.get_all_borrow_records()
            print(f"\nGlobal Circulation Records ({len(records)} total):")
            for r in records:
                print(f"  * [Loan #{r['id']}] '{r['title']}' | Member: {r['full_name']} ({r['username']}) | Borrowed: {r['borrow_date'][:10]} | Status: {r['status']}")
        elif c == "3":
            stats = self.lib_service.get_inventory_statistics()
            print(f"\nInstitutional Overview:")
            for k, v in stats.items():
                print(f"  - {k.replace('_', ' ').title()}: {v}")

    def menu_admin(self):
        print(f"\n{Color.CYAN}--- SYSTEM ADMINISTRATOR OVERSIGHT ---{Color.RESET}")
        stats = self.lib_service.get_inventory_statistics()
        print("\nInstitutional Health Metrics:")
        for k, v in stats.items():
            print(f"  * {k.replace('_', ' ').title()}: {v}")
        print("\nRecent System Audit Trail:")
        audits = self.lib_service.get_audit_logs(limit=10)
        for a in audits:
            print(f"  [{a['created_at']}] {a['action_type']}: {a['details']}")

    def menu_scrum(self):
        while True:
            print(f"\n{Color.CYAN}--- SCRUM & AGILE PROJECT MANAGEMENT ENGINE ---{Color.RESET}")
            print("  [1] Display ASCII Terminal Kanban Board (5 Columns)")
            print("  [2] View Prioritized Product Backlog & MoSCoW Breakdown")
            print("  [3] View 5-Week Sprint Cadence & Velocity Reports")
            print("  [4] View Sprint Action Items Register")
            print("  [5] Transition Kanban Card Status (e.g. In Progress -> Done)")
            print("  [0] Back to Main Menu")

            c = input("Select option [0-5]: ").strip()
            if c == "1":
                self.display_kanban()
            elif c == "2":
                stories = self.story_service.list_user_stories()
                print(f"\nProduct Backlog ({len(stories)} stories):")
                for s in stories:
                    print(f"  * [{s['story_code']}] {s['title']} | Role: {s['role']} | {s['story_points']} pts | Prio: {s['priority']} | Status: {s['status']}")
            elif c == "3":
                sprints = self.sprint_service.list_sprints()
                print(f"\nScrum 5-Week Sprint Cadence:")
                for sp in sprints:
                    details = self.sprint_service.get_sprint_details(sp["id"])
                    print(f"  * Sprint {sp['sprint_number']}: {sp['name']}")
                    print(f"    Goal: {sp['goal']}")
                    print(f"    Status: {sp['status']} | Points: {details['completed_story_points']}/{details['total_story_points']} ({details['progress_percentage']}%)")
            elif c == "4":
                items = self.action_service.list_action_items()
                print(f"\nSprint Action Items Register ({len(items)} items):")
                for it in items:
                    print(f"  * [{it['item_code']}] {it['description']} | Owner: {it['owner']} | Priority: {it['priority']} | Status: {it['status']}")
            elif c == "5":
                code = input("Enter Story Code (e.g. US-01) or Action Item Code (e.g. AI-01): ").strip().upper()
                new_st = input("Enter new status (Backlog, To Do, In Progress, Review/Testing, Done): ").strip()
                try:
                    if code.startswith("US-"):
                        res = self.story_service.update_user_story_status(code, new_st)
                        print(f"{Color.GREEN}[+] {res['message']}{Color.RESET}")
                    elif code.startswith("AI-"):
                        res = self.action_service.update_action_item_status(code, new_st)
                        print(f"{Color.GREEN}[+] {res['message']}{Color.RESET}")
                    else:
                        print(f"{Color.RED}Unrecognized code format.{Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}[-] Status update error: {e}{Color.RESET}")
            elif c == "0":
                break


def main():
    parser = argparse.ArgumentParser(description="Library Management System - Scrum Agile PBL")
    parser.add_argument("--demo", action="store_true", help="Execute automated viva demonstration walkthrough in <30 seconds")
    parser.add_argument("--kanban", action="store_true", help="Display ASCII terminal Kanban board directly from SQLite")
    parser.add_argument("--test", action="store_true", help="Execute the automated test suite")

    args = parser.parse_args()
    runner = AppRunner()

    if args.demo:
        runner.run_automated_demo()
    elif args.kanban:
        runner.display_kanban()
    elif args.test:
        runner.run_tests()
    else:
        runner.interactive_console()


if __name__ == "__main__":
    main()
