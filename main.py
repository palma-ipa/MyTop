#!/usr/bin/env python3
"""Entry point for the CLI task manager application."""

import curses
from ui import TUI


def main(stdscr):
    """Main function passed to curses.wrapper for safe terminal handling."""
    TUI(stdscr).run()


if __name__ == "__main__":
    curses.wrapper(main)