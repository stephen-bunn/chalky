# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains shortcuts for quickly utilizing chalk.

Simply combine colors and styles using ``&`` or ``+`` to produce a style that can used
to format a string with ``|`` or ``+``.

Examples:
    >>> from chalky import bg, fg, sty
    >>> my_style = bg.red & fg.black & sty.bold
    >>> print(my_style | "I'm bold black on red text")
    I'm bold black on red text

Many chalk styles can be combined together:

Examples:
    >>> from chalky import sty
    >>> my_style = sty.bold & sty.underline
    >>> print(my_style | "I'm bold and underlined")
    I'm bold and underlined

The last applied foreground or background color will be used when applied to a string:

Examples:
    >>> from chalky import bg
    >>> my_style = bg.red & bg.blue  # BLUE will override RED when styling the string
    >>> print(my_style | "My background is BLUE")
    My background is BLUE
"""

from ..chalk import Chalk
from ..color import TrueColor
from . import bg, fg, sty


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
    "chain",
]
