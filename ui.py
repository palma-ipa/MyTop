import curses
import time
import psutil
from process_manager import ProcessManager


class TUI:
    """Text User Interface for process management using curses."""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.process_manager = ProcessManager()
        self.selected_idx = 0
        self.scroll_offset = 0
        self.status_message = ""
        self.status_time = 0

    def draw_header(self):
        """Display navigation instructions at the top of the screen."""
        header = "UP/DOWN: Navigate | K: Kill Process | Q: Quit"
        self.stdscr.addstr(0, 0, header, curses.A_REVERSE)
        self.stdscr.clrtoeol()

    def draw_process_table(self, processes):
        """
        Display the process table with fixed-width columns.
        Implements scrolling for processes exceeding terminal height.
        """
        height, width = self.stdscr.getmaxyx()
        start_y = 2

        col_widths = [8, 25, 10, 12, 15]
        headers = ["PID", "Name", "CPU%", "MEM%", "User"]
        header_line = ""
        for i, header in enumerate(headers):
            header_line += header.ljust(col_widths[i])
        self.stdscr.addstr(start_y, 0, header_line)

        visible_rows = height - start_y - 2
        if self.selected_idx >= self.scroll_offset + visible_rows:
            self.scroll_offset = self.selected_idx - visible_rows + 1
        elif self.selected_idx < self.scroll_offset:
            self.scroll_offset = self.selected_idx

        for i in range(visible_rows):
            proc_idx = self.scroll_offset + i
            if proc_idx >= len(processes):
                break
            proc = processes[proc_idx]
            y = start_y + 1 + i
            attr = curses.A_REVERSE if proc_idx == self.selected_idx else curses.A_NORMAL
            line = ""
            line += str(proc['pid']).ljust(col_widths[0])
            line += proc['name'][:col_widths[1]-1].ljust(col_widths[1])
            line += f"{proc['cpu_percent']:.1f}".ljust(col_widths[2])
            line += f"{proc['memory_percent']:.1f}".ljust(col_widths[3])
            line += str(proc['username'] or '').ljust(col_widths[4])
            try:
                self.stdscr.addstr(y, 0, line[:width-1], attr)
            except curses.error:
                pass

        for i in range(visible_rows):
            y = start_y + 1 + i
            if processes and y >= start_y + 1 + len(processes) - self.scroll_offset:
                try:
                    self.stdscr.addstr(y, 0, " " * (width - 1))
                except curses.error:
                    pass

    def draw_status_bar(self):
        """Display status messages at the bottom of the screen for 2 seconds."""
        height, width = self.stdscr.getmaxyx()
        if self.status_message and time.time() - self.status_time < 2:
            try:
                self.stdscr.addstr(height - 1, 0, self.status_message[:width-1], curses.A_REVERSE)
            except curses.error:
                pass

    def run(self):
        """Main event loop with auto-refresh every 2 seconds and non-blocking input."""
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.stdscr.timeout(2000)

        self.process_manager._init_cpu_monitoring()

        while True:
            processes = self.process_manager.get_processes()
            if self.selected_idx >= len(processes):
                self.selected_idx = max(0, len(processes) - 1)
            self.stdscr.erase()

            self.draw_header()
            if processes:
                self.draw_process_table(processes)
            self.draw_status_bar()

            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key == curses.KEY_DOWN and self.selected_idx < len(processes) - 1:
                self.selected_idx += 1
            elif key == curses.KEY_UP and self.selected_idx > 0:
                self.selected_idx -= 1
            elif key in (ord('k'), ord('K')):
                if processes:
                    pid = processes[self.selected_idx]['pid']
                    success, msg = self.process_manager.kill_process(pid)
                    self.status_message = msg
                    self.status_time = time.time()
                    self.selected_idx = min(self.selected_idx, len(processes) - 2) if len(processes) > 1 else 0
            elif key in (ord('q'), ord('Q')):
                break