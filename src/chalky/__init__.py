# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Chalky.

Simple ANSI terminal text coloring.
Compose multiple of the included chalk instances to produce a style that can be applied
directly to strings.

Examples:
    Compose multiple chalk instances together with ``&`` and apply it to a string
    using ``|``:

    from chalky import sty, fg
    print(sty.bold & fg.green | "Hello, World!")
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
