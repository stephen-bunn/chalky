# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Chalk.

Simple portable terminal text coloring.
"""

from .chalk import Chalk
from .color import Color, TrueColor
from .shortcuts import bg, fg, hex, rgb, sty
from .style import Style

__all__ = [
    "Chalk",
    "Color",
    "TrueColor",
    "Style",
    "fg",
    "bg",
    "sty",
    "rgb",
    "hex",
]
