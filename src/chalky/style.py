# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the available styles we can use for chalk."""

from enum import Enum


class Style(Enum):
    """Enum of the available styles that can be applied to some printable text.

    Attributes:
        RESET:
            Resets all styles and colors to the original terminal style.
        BOLD:
            Emphasizes the text by increasing the font weight.
        DIM:
            Dims the text color and sometimes decreases font weight.
        ITALIC:
            Italicize the text.
        UNDERLINE:
            Underlines the text (works in most modern terminals).
        SLOW_BLINK:
            Flash the text slowly (doesn't work in most modern terminals).
        RAPID_BLINK:
            Flash the text very quickly (doesn't work in most modern terminals).
        REVERSED:
            Reversed the current style of the terminal for the text.
        CONCEAL:
            Hide the text.
        STRIKETHROUGH:
            Draw a line through the text (works in most modern terminals).
        NORMAL:
            Normalizes the text for the current terminal.
    """

    RESET = "reset"
    BOLD = "bold"
    DIM = "dim"
    ITALIC = "italic"
    UNDERLINE = "underline"
    SLOW_BLINK = "slow_blink"
    RAPID_BLINK = "rapid_blink"
    REVERSED = "reversed"
    CONCEAL = "conceal"
    STRIKETHROUGH = "strikethrough"
    NORMAL = "normal"
