# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Predefined foreground (fg) chalk colors."""

from ..chalk import Chalk
from ..color import Color

black = Chalk(foreground=Color.BLACK)
red = Chalk(foreground=Color.RED)
green = Chalk(foreground=Color.GREEN)
yellow = Chalk(foreground=Color.YELLOW)
blue = Chalk(foreground=Color.BLUE)
magenta = Chalk(foreground=Color.MAGENTA)
cyan = Chalk(foreground=Color.CYAN)
white = Chalk(foreground=Color.WHITE)

bright_black = Chalk(foreground=Color.BRIGHT_BLACK)
bright_red = Chalk(foreground=Color.BRIGHT_RED)
bright_green = Chalk(foreground=Color.BRIGHT_GREEN)
bright_yellow = Chalk(foreground=Color.BRIGHT_YELLOW)
bright_blue = Chalk(foreground=Color.BRIGHT_BLUE)
bright_magenta = Chalk(foreground=Color.MAGENTA)
bright_cyan = Chalk(foreground=Color.BRIGHT_CYAN)
bright_white = Chalk(foreground=Color.BRIGHT_WHITE)
