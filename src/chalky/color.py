# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the available tools to define the colors that can be used for chalk."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Union

from .helpers import int_to_bytes


class Color(Enum):
    """Enum of the available colors that can be used to color some printable text.

    Attributes:
        BLACK
        RED
        GREEN
        YELLOW
        BLUE
        MAGENTA
        CYAN
        WHITE
        BRIGHT_BLACK:
            Otherwise known as gray.
        BRIGHT_RED
        BRIGHT_GREEN
        BRIGHT_YELLOW
        BRIGHT_BLUE
        BRIGHT_MAGENTA
        BRIGHT_CYAN
        BRIGHT_WHITE:
            Otherwise known as actual white.
    """

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
    """Describes a true color that can be displayed on compatible terminals.

    Parameters:
        red (int):
            The value of red (0-255).
        green (int):
            The value of green (0-255).
        blue (int):
            The value of blue (0-255).
    """

    red: int
    green: int
    blue: int

    def __hash__(self) -> int:
        """Generate a comparable hash for the current instance.

        Returns:
            int:
                The appropriate hash of the current instance.
        """

        return hash(f"{self.red}{self.green}{self.blue}")

    @classmethod
    def from_hex(cls, color: str) -> TrueColor:
        """Create an instance from a given hex color string.

        Args:
            color (str):
                The hex color string of the color to create.

        Raises:
            ValueError:
                If the given hex color string is not a length of 3 or 6

        Returns:
            TrueColor:
                The created instance.
        """

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
        """Convert the current color to a tuple of RGB bytes.

        Returns:
            Tuple[bytes, bytes, bytes]:
                The corresponding bytes of the current instance (red, green, blue).
        """

        return (
            int_to_bytes(self.red),
            int_to_bytes(self.green),
            int_to_bytes(self.blue),
        )


Color_T = Union[Color, TrueColor]
