# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the actual implementation of interacting with a type of terminal buffer."""


import sys
from functools import lru_cache
from typing import Optional, TextIO

from .ansi import AnsiInterface
from .base import BaseInterface


@lru_cache()
def get_interface(io: Optional[TextIO] = None) -> BaseInterface:
    """Get the appropriate interface to interact with some terminal buffer.

    Examples:
        Get the default interface for interacting with the terminal buffer.
        This defaults to using :data:`sys.stdout`

        >>> from chalky.interface import get_interface
        >>> interface = get_interface()

        To get an interface using a different text io buffer, pass it in:

        >>> import sys
        >>> stderr_interface = get_interface(sys.stderr)

    Args:
        io (Optional[:class:`~typing.TextIO`], optional):
            The io to build an interface for.
            Defaults to :data:`sys.stdout`.

    Returns:
        :class:`~interface.base.BaseInterface`:
            The created interface for the given io buffer.
    """

    if not io:
        io = sys.stdout

    return AnsiInterface(io)


__all__ = ["get_interface"]
