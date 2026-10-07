# Information Technology Lab (ITL) Demonstration Package
## Library Management System using Scrum Agile Methodology

**Student Name:** Annika Jha  
**Course:** Agile Methodologies & IT (AM) / ITL Lab — B.Tech 3rd Year  
**Destination Repository:** [yashkarwa2005/Library-Management](https://github.com/yashkarwa2005/Library-Management.git)

---

## Quickstart Instructions

This folder (`ITL/`) contains the complete standalone, runnable code and web dashboard for hands-on evaluation and oral examination viva demonstration.

### 1. Launch Web Dashboard (Recommended)
```bash
python app.py
```
- Open browser at: `http://127.0.0.1:5000`
- Instant logins available on top bar for **Aarav Patel** (Member), **Diya Sharma** (Member with Fine), **Anita Roy** (Librarian), and **Admin**.

### 2. Run Instant 30-Second Viva Demo
```bash
python src/main.py --demo
```

### 3. Run Automated Unit & Integration Tests (16/16 Passed)
```bash
python -m unittest discover tests -v
```

### 4. Open Interactive Drag & Drop Kanban Board
- Open in browser: `http://127.0.0.1:5000/kanban_board.html` (or open file `../kanban_board.html`).

---

For the complete experiment writeup, step-by-step examiner script, and viva voce questions, see [ITL_LAB_MANUAL.md](ITL_LAB_MANUAL.md).
