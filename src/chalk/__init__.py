# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Chalk.

Simple portable terminal text coloring.
"""

from .shortcuts import bg, clear_line, clear_screen, fg, set_title, sty

__all__ = ["fg", "bg", "sty", "clear_line", "clear_screen", "set_title"]
