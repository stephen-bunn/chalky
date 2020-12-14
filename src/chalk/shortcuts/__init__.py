# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains shortcuts for quickly utilizing chalk.

Simply combine colors and styles using ``&`` or ``+`` to produce a style that can used
to format a string with ``|`` or ``+``.

Examples:
    >>> from chalk import bg, fg, sty
    >>> my_style = bg.red & fg.black & sty.bold
    >>> print(my_style | "I'm bold black on red text")
    I'm bold black on red text

Many chalk styles can be combined together:

Examples:
    >>> from chalk import sty
    >>> my_style = sty.bold & sty.underline
    >>> print(my_style | "I'm bold and underlined")
    I'm bold and underlined

The last applied foreground or background color will be used when applied to a string:

Examples:
    >>> from chalk import bg
    >>> my_style = bg.red & bg.blue  # BLUE will override RED when styling the string
    >>> print(my_style | "My background is BLUE")
    My background is BLUE
"""

import sys
from typing import Tuple

from ..chalk import Chalk
from ..color import TrueColor
from ..interface import get_interface
from . import bg, fg, sty

interface = get_interface(sys.stdout)


def clear_line():
    """Completely clear the line the cursor is currently on."""

    interface.clear_line()


def clear_screen(reset_position: bool = True):
    """Completely clear the screen.

    Args:
        reset_position (bool):
            If ``True``, will reset the prompt position to the top of the screen.
    """

    interface.clear_screen(reset_position=reset_position)


def set_title(title: str):
    """Set the title of the terminal window.

    Args:
        title (str): The title to set.
    """

    interface.set_title(title)


def rgb(red: int, green: int, blue: int, background: bool = False) -> Chalk:
    """Generate a new truecolor chalk from an RGB tuple.

    Args:
        red (int):
            The intensity of red (0-255).
        green (int):
            The intensity of green (0-255).
        blue (int):
            The intensity of blue (0-255).
        background (bool, optional):
            If ``True`` will generate the new chalk to be applied as a background color.
            Defaults to False.

    Returns:
        :class:`~.chalk.Chalk`:
            The new chalk instance.
    """

    color = TrueColor(red, green, blue)
    return Chalk(background=color) if background else Chalk(foreground=color)


def hex(hexcolor: str, background: bool = False) -> Chalk:
    """Generate a new truecolor chalk from a HEX color (``#ffffff``) string.

    Args:
        hexcolor (str):
            The hex color string.
        background (bool, optional):
            If ``True`` will generate the new chalk to be applied as background color.
            Defaults to False.

    Returns:
        :class:`~.chalk.Chalk`:
            The new chalk instance.
    """

    color = TrueColor.from_hex(hexcolor)
    return Chalk(background=color) if background else Chalk(foreground=color)


__all__ = [
    "fg",
    "bg",
    "sty",
    "rgb",
    "hex",
    "clear_line",
    "clear_screen",
    "set_title",
]
