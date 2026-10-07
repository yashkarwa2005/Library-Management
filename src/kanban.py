"""Kanban Board Module for Agile Project Tracking
Visualizes task progression across 5 stages (Backlog -> To Do -> In Progress -> Review/Testing -> Done)
in an interactive terminal display.
Author / Scrum Lead: Annika Jha
"""
from typing import List, Dict, Any, Optional
from .user_story import UserStoryService
from .action_item import ActionItemService


class KanbanService:
    COLUMNS = ["Backlog", "To Do", "In Progress", "Review/Testing", "Done"]

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.story_service = UserStoryService(db_path)
        self.action_service = ActionItemService(db_path)

    def get_board_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Groups user stories and action items into the 5 Kanban columns."""
        stories = self.story_service.list_user_stories()
        actions = self.action_service.list_action_items()

        board: Dict[str, List[Dict[str, Any]]] = {col: [] for col in self.COLUMNS}

        # Map User Stories
        for s in stories:
            col = s["status"]
            if col in board:
                board[col].append({
                    "type": "STORY",
                    "code": s["story_code"],
                    "title": s["title"],
                    "priority": s["priority"],
                    "points": s["story_points"],
                    "assignee": s["assignee"] or "Unassigned"
                })

        # Map Action Items
        action_status_map = {
            "To Do": "To Do",
            "In Progress": "In Progress",
            "Review": "Review/Testing",
            "Done": "Done",
            "Blocked": "In Progress"
        }
        for a in actions:
            target_col = action_status_map.get(a["status"], "To Do")
            if target_col in board:
                board[target_col].append({
                    "type": "ACTION",
                    "code": a["item_code"],
                    "title": a["description"],
                    "priority": a["priority"],
                    "points": 1,
                    "assignee": a["owner"] or "Unassigned"
                })

        return board

    def get_priority_symbol(self, priority: str) -> str:
        """Returns colored badge or emoji representation for task priority."""
        p = priority.lower()
        if "must" in p or "high" in p:
            return "[!] High"
        elif "should" in p or "medium" in p:
            return "[-] Med"
        else:
            return "[*] Low"

    def format_card_header(self, code: str, priority: str, width: int) -> str:
        symbol = self.get_priority_symbol(priority)
        left = f"| {code}"
        right = f"{symbol} |"
        space = width - len(left) - len(right)
        if space < 1:
            space = 1
        return left + (" " * space) + right

    def render_ascii_board(self) -> str:
        """Renders an ASCII text-based multi-column Kanban board."""
        board = self.get_board_data()
        col_width = 30
        sep = "+" + "+".join(["-" * col_width for _ in self.COLUMNS]) + "+"

        lines = []
        lines.append("\n" + "=" * (len(self.COLUMNS) * (col_width + 1) + 1))
        lines.append("     LIBRARY MANAGEMENT SYSTEM - AGILE KANBAN BOARD (5-STAGE WORKFLOW)")
        lines.append("=" * (len(self.COLUMNS) * (col_width + 1) + 1))

        # Header Row
        header_cells = []
        for col in self.COLUMNS:
            count = len(board[col])
            text = f" {col.upper()} ({count}) "
            header_cells.append(text.center(col_width))
        lines.append("|" + "|".join(header_cells) + "|")
        lines.append(sep)

        # Determine maximum number of cards in any single column
        max_cards = max(len(board[col]) for col in self.COLUMNS)
        if max_cards == 0:
            lines.append("|" + "|".join([" (Empty Column) ".center(col_width) for _ in self.COLUMNS]) + "|")
            lines.append(sep)
            return "\n".join(lines)

        for card_idx in range(max_cards):
            # Line 1: Code and Priority
            row_l1 = []
            # Line 2: Title (truncated)
            row_l2 = []
            # Line 3: Assignee and Points
            row_l3 = []

            for col in self.COLUMNS:
                items = board[col]
                if card_idx < len(items):
                    item = items[card_idx]
                    prio_sym = self.get_priority_symbol(item["priority"])
                    pts_str = f"[{item['points']}pt]" if item['type'] == 'STORY' else "[task]"

                    # Line 1
                    l1 = f"{item['code']} {prio_sym}"
                    row_l1.append(f" {l1[:col_width-2]} ".ljust(col_width))

                    # Line 2
                    t = item["title"]
                    if len(t) > col_width - 4:
                        t = t[:col_width - 7] + "..."
                    row_l2.append(f" {t} ".ljust(col_width))

                    # Line 3
                    assignee_str = f"@{item['assignee'][:12]}"
                    l3 = f"{pts_str} {assignee_str}"
                    row_l3.append(f" {l3[:col_width-2]} ".ljust(col_width))
                else:
                    row_l1.append(" " * col_width)
                    row_l2.append(" " * col_width)
                    row_l3.append(" " * col_width)

            lines.append("|" + "|".join(row_l1) + "|")
            lines.append("|" + "|".join(row_l2) + "|")
            lines.append("|" + "|".join(row_l3) + "|")
            lines.append(sep)

        # Summary Metrics
        metrics = self.story_service.get_backlog_metrics()
        lines.append(f"\nKanban Summary: Total Stories: {metrics['total_stories']} | Total Story Points: {metrics['total_points']} | Completed: {metrics['completed_points']} pts ({metrics['completion_percentage']}%)")
        lines.append("=" * (len(self.COLUMNS) * (col_width + 1) + 1) + "\n")

        return "\n".join(lines)
