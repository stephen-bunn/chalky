# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""


from functools import lru_cache
from typing import TextIO

from .ansi import AnsiInterface
from .base import BaseInterface


@lru_cache()
def get_interface(io: TextIO) -> BaseInterface:
    return AnsiInterface(io)


__all__ = ["get_interface"]
