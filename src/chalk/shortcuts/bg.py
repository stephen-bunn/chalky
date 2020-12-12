# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Predefined background (bg) chalk colors."""

from ..chalk import Chalk
from ..color import Color

black = Chalk(background=Color.BLACK)
red = Chalk(background=Color.RED)
green = Chalk(background=Color.GREEN)
yellow = Chalk(background=Color.YELLOW)
blue = Chalk(background=Color.BLUE)
magenta = Chalk(background=Color.MAGENTA)
cyan = Chalk(background=Color.CYAN)
white = Chalk(background=Color.WHITE)

bright_black = Chalk(background=Color.BRIGHT_BLACK)
bright_red = Chalk(background=Color.BRIGHT_RED)
bright_green = Chalk(background=Color.BRIGHT_GREEN)
bright_yellow = Chalk(background=Color.BRIGHT_YELLOW)
bright_blue = Chalk(background=Color.BRIGHT_BLUE)
bright_magenta = Chalk(background=Color.MAGENTA)
bright_cyan = Chalk(background=Color.BRIGHT_CYAN)
bright_white = Chalk(background=Color.BRIGHT_WHITE)
