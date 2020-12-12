# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Optional, Set, Union, overload

from .color import Color_T
from .interface import get_interface
from .style import Style


@dataclass
class Chalk:

    style: Set[Style] = field(default_factory=set)
    foreground: Optional[Color_T] = field(default=None)
    background: Optional[Color_T] = field(default=None)

    def __and__(self, other: Chalk) -> Chalk:

        return Chalk(
            style=self.style.union(other.style),
            foreground=other.foreground or self.foreground,
            background=other.background or self.background,
        )

    def __or__(self, value: str) -> str:
        interface = get_interface(sys.stdout)

        escape_sequence = interface.build(
            style=self.style,
            background=self.background,
            foreground=self.foreground,
        ).decode("utf-8")
        reset = interface.build_reset().decode("utf-8")

        return f"{escape_sequence!s}{value}{reset!s}"

    @overload
    def __add__(self, other: Chalk) -> Chalk:
        ...

    @overload
    def __add__(self, other: str) -> str:
        ...

    def __add__(self, other: Union[Chalk, str]) -> Union[Chalk, str]:
        if isinstance(other, Chalk):
            return self & other

        return self | other

    @property
    def reverse(self) -> Chalk:
        return self & Chalk(style={Style.REVERSED})
