"""Library Management System - Standalone Python Web Application & REST API
Zero mandatory external dependencies - uses standard library http.server + sqlite3.
Author / Scrum Lead: Annika Jha
"""
import os
import sys
import json
import sqlite3
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import webbrowser
import threading
import time

# Ensure root directory is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

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

DEFAULT_PORT = 5000

# Initialize and seed database
init_db()
seed_initial_data()

lib_service = LibraryService()
story_service = UserStoryService()
sprint_service = SprintService()
action_service = ActionItemService()
kanban_service = KanbanService()


class LibraryRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status_code=200):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, file_path):
        if not os.path.exists(file_path):
            self.send_error(404, "File not found")
            return
        with open(file_path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Serve Web UI
        if path in ("/", "/index.html"):
            index_path = os.path.join(BASE_DIR, "templates", "index.html")
            return self._send_html(index_path)

        if path in ("/kanban", "/kanban.html", "/kanban_board.html"):
            kanban_path = os.path.join(BASE_DIR, "kanban_board.html")
            return self._send_html(kanban_path)

        # API Endpoints
        try:
            if path == "/api/books":
                books = lib_service.get_all_books()
                return self._send_json({"success": True, "books": books})

            elif path == "/api/books/search":
                keyword = query.get("q", [""])[0]
                category = query.get("category", [""])[0]
                results = lib_service.search_books(keyword=keyword, category=category)
                return self._send_json({"success": True, "books": results})

            elif path == "/api/stats":
                stats = lib_service.get_inventory_statistics()
                return self._send_json({"success": True, "stats": stats})

            elif path == "/api/loans":
                uid = int(query.get("user_id", [0])[0])
                if uid:
                    loans = lib_service.get_member_loans(uid)
                    return self._send_json({"success": True, "loans": loans})
                else:
                    all_loans = lib_service.get_all_borrow_records()
                    return self._send_json({"success": True, "loans": all_loans})

            elif path == "/api/fines":
                uid = int(query.get("user_id", [0])[0])
                fines_data = lib_service.get_user_fines(uid)
                return self._send_json({"success": True, **fines_data})

            elif path == "/api/scrum/kanban":
                board = kanban_service.get_board_data()
                return self._send_json({"success": True, "columns": board})

            elif path == "/api/scrum/backlog":
                stories = story_service.list_user_stories()
                metrics = story_service.get_backlog_metrics()
                return self._send_json({"success": True, "stories": stories, "metrics": metrics})

            elif path == "/api/scrum/sprints":
                sprints = sprint_service.list_sprints()
                detailed = [sprint_service.get_sprint_details(s["id"]) for s in sprints]
                return self._send_json({"success": True, "sprints": detailed})

            elif path == "/api/scrum/action-items":
                items = action_service.list_action_items()
                return self._send_json({"success": True, "action_items": items})

            elif path == "/api/audit":
                logs = lib_service.get_audit_logs(limit=25)
                return self._send_json({"success": True, "logs": logs})

            else:
                self.send_error(404, f"API route '{path}' not found")

        except Exception as e:
            return self._send_json({"success": False, "error": str(e)}, status_code=500)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.wfile.read(content_length) if content_length > 0 else b""
        payload = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}

        try:
            if path == "/api/auth/register":
                u = payload.get("username", "")
                p = payload.get("password", "")
                name = payload.get("full_name", "")
                email = payload.get("email", "")
                phone = payload.get("phone", "")
                role = payload.get("role", "member")
                user = lib_service.register_user(u, p, name, email, phone, role)
                return self._send_json({"success": True, "user": user})

            elif path == "/api/auth/login":
                u = payload.get("username", "")
                p = payload.get("password", "")
                session = lib_service.login_user(u, p)
                if session:
                    return self._send_json({"success": True, "user": session})
                else:
                    return self._send_json({"success": False, "error": "Invalid username or password."}, status_code=401)

            elif path == "/api/books":
                isbn = payload.get("isbn")
                title = payload.get("title")
                author = payload.get("author")
                category = payload.get("category")
                publisher = payload.get("publisher", "")
                year = int(payload.get("publication_year", 2024))
                copies = int(payload.get("total_copies", 1))
                shelf = payload.get("shelf_location", "General Stack")
                book = lib_service.add_book(isbn, title, author, category, publisher, year, copies, shelf)
                return self._send_json({"success": True, "book": book})

            elif path == "/api/borrow":
                user_id = int(payload.get("user_id"))
                book_id = int(payload.get("book_id"))
                res = lib_service.borrow_book(user_id, book_id)
                return self._send_json({"success": True, "borrow": res})

            elif path == "/api/return":
                borrow_id = int(payload.get("borrow_id"))
                res = lib_service.return_book(borrow_id)
                return self._send_json({"success": True, "result": res})

            elif path == "/api/renew":
                borrow_id = int(payload.get("borrow_id"))
                res = lib_service.renew_book(borrow_id)
                return self._send_json({"success": True, "renewal": res})

            elif path == "/api/reserve":
                user_id = int(payload.get("user_id"))
                book_id = int(payload.get("book_id"))
                res = lib_service.reserve_book(user_id, book_id)
                return self._send_json({"success": True, "reservation": res})

            elif path == "/api/fines/pay":
                fine_id = int(payload.get("fine_id"))
                res = lib_service.pay_fine(fine_id)
                return self._send_json({"success": True, "payment": res})

            elif path == "/api/scrum/transition":
                code = payload.get("code", "").strip().upper()
                new_status = payload.get("status", "").strip()
                if code.startswith("US-"):
                    res = story_service.update_user_story_status(code, new_status)
                elif code.startswith("AI-"):
                    res = action_service.update_action_item_status(code, new_status)
                else:
                    raise ValueError(f"Unrecognized entity code '{code}'.")
                return self._send_json({"success": True, "result": res})

            else:
                self.send_error(404, f"API route '{path}' not found")

        except Exception as e:
            return self._send_json({"success": False, "error": str(e)}, status_code=400)


def start_server(port=DEFAULT_PORT, open_browser=False):
    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, LibraryRequestHandler)
    print(f"\n===============================================================================")
    print(f"  LIBRARY MANAGEMENT SYSTEM - WEB APPLICATION & REST API")
    print(f"  Author / Scrum Lead: Annika Jha")
    print(f"  Local Server Running: http://127.0.0.1:{port}")
    print(f"  Kanban Board URL   : http://127.0.0.1:{port}/kanban_board.html")
    print(f"===============================================================================\n")

    if open_browser:
        threading.Thread(target=lambda: (time.sleep(1), webbrowser.open(f"http://127.0.0.1:{port}"))).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        httpd.shutdown()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    start_server(port, open_browser=False)
