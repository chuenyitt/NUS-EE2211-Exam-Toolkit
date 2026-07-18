import collections
import tkinter as tk
from tkinter import ttk

from gui.constants import MAIN_BG, ACCENT, FONT_FAMILY
from gui.base_frame import ModuleFrame


class SearchFrame(ModuleFrame):
    def __init__(self, parent):
        super().__init__(parent, "Search Algorithms")
        f = self.input_frame

        row_ctrl = tk.Frame(f, bg=MAIN_BG)
        row_ctrl.pack(fill=tk.X, pady=2)

        self.algorithm_var = self.add_button_group(row_ctrl, "Algorithm", ["BFS", "DFS"], "BFS")
        self.start_var = self.add_entry(row_ctrl, "Start", "A", width=8)
        self.goal_var = self.add_entry(row_ctrl, "Goal", "D", width=8)

        self.graph_txt = self.add_text_input(
            f,
            "Graph adjacency list",
            hint="Format: A:B,C means node A connects to B and C. One pair per line.",
            height=8,
            width=60,
        )
        self.graph_txt.insert(
            "1.0",
            "A:B,C\nB:D\nC:D\nD:\n",
        )

    def run(self):
        try:
            graph = self._parse_graph(self.get_text(self.graph_txt))
            start = self.start_var.get().strip()
            goal = self.goal_var.get().strip()

            if not start or not goal:
                raise ValueError("Start and Goal nodes must be provided.")
            if start not in graph:
                raise ValueError(f"Start node '{start}' is not in the graph.")
            if goal not in graph:
                raise ValueError(f"Goal node '{goal}' is not in the graph.")

            algorithm = self.algorithm_var.get()
            visited, path = self._search(graph, start, goal, algorithm)

            lines = []
            lines.append(f"Algorithm: {algorithm}")
            lines.append(f"Start: {start}")
            lines.append(f"Goal: {goal}")
            lines.append("")
            lines.append(f"Visited order: {', '.join(visited)}")
            if path is None:
                lines.append("No path found.")
            else:
                lines.append(f"Path: {' -> '.join(path)}")

            self.show_output("\n".join(lines))
        except Exception as e:
            self.show_output(f"ERROR: {e}")

    def _parse_graph(self, text):
        graph = {}
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if ':' not in line:
                raise ValueError(f"Invalid graph line: {line}")
            node, neighbors = line.split(':', 1)
            node = node.strip()
            if not node:
                raise ValueError(f"Invalid node name in line: {line}")
            graph[node] = [n.strip() for n in neighbors.split(',') if n.strip()]
        return graph

    def _search(self, graph, start, goal, algorithm):
        if algorithm == "BFS":
            queue = collections.deque([(start, [start])])
            visited = set([start])
            order = [start]
            while queue:
                node, path = queue.popleft()
                if node == goal:
                    return order, path
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        order.append(neighbor)
                        queue.append((neighbor, path + [neighbor]))
            return order, None

        stack = [(start, [start])]
        visited = set([start])
        order = [start]
        while stack:
            node, path = stack.pop()
            if node == goal:
                return order, path
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    visited.add(neighbor)
                    order.append(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        return order, None
