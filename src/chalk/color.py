# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Union


class Color(Enum):

    BLACK = "black"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"

    BRIGHT_BLACK = "bright_black"
    BRIGHT_RED = "bright_red"
    BRIGHT_GREEN = "bright_green"
    BRIGHT_YELLOW = "bright_yellow"
    BRIGHT_BLUE = "bright_blue"
    BRIGHT_MAGENTA = "bright_magenta"
    BRIGHT_CYAN = "bright_cyan"
    BRIGHT_WHITE = "bright_white"


@dataclass
class TrueColor:

    red: int
    green: int
    blue: int

    def __hash__(self) -> int:
        return hash(f"{self.red}{self.green}{self.blue}")

    @classmethod
    def from_hex(cls, color: str) -> TrueColor:
        color = color.lstrip("#")
        if len(color) not in (3, 6):
            raise ValueError(f"Hex color #{color!s} is not of length 3 or 6")

        if len(color) == 3:
            color = "".join([element * 2 for element in color])

        red, green, blue = [
            int(color[index : index + 2], 16) for index in range(0, len(color), 2)
        ]

        return cls(red=red, green=green, blue=blue)

    def to_bytes(self) -> Tuple[bytes, bytes, bytes]:
        def _int_to_bytes(value: int) -> bytes:
            return bytes(str(value), "utf-8")

        return (
            _int_to_bytes(self.red),
            _int_to_bytes(self.green),
            _int_to_bytes(self.blue),
        )


Color_T = Union[Color, TrueColor]
