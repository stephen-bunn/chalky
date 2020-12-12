# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

import abc
from typing import Optional, Set, TextIO

from ..color import Color_T
from ..style import Style


class BaseInterface(abc.ABC):
    def __init__(self, io: TextIO):
        self.io = io

    @abc.abstractmethod
    def clear_screen(self, reset_position: bool = True):
        ...

    @abc.abstractmethod
    def clear_line(self):
        ...

    @abc.abstractmethod
    def set_title(self, value: str):
        ...

    @abc.abstractmethod
    def reset(self):
        ...

    @abc.abstractmethod
    def build_reset(self) -> bytes:
        ...

    @abc.abstractmethod
    def build(
        self,
        style: Set[Style],
        background: Optional[Color_T],
        foreground: Optional[Color_T],
    ) -> bytes:
        ...
