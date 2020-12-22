# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the base abstract interface to inherit from."""

import abc
from typing import Optional, Set, TextIO

from ..color import Color_T
from ..style import Style


class BaseInterface(abc.ABC):
    """The base abstract interface to inherit from."""

    def __init__(self, io: TextIO):
        """Initialize the interface with some text io buffer.

        Args:
            io (:class:`~typing.TextIO`):
                The text io buffer to write to.
        """

        self.io = io

    @abc.abstractmethod
    def clear_screen(
        self,
        reset_position: bool = True,
        keep_head: bool = False,
        keep_tail: bool = False,
    ):  # pragma: no cover
        """Clear the full screen of the terminal.

        Args:
            reset_position (bool, optional):
                If True, will set the cursor position to the starting point.
                Defaults to True.
            keep_head (bool, optional):
                If True, will retain the text before the cursor position.
                Defaults to False.
            keep_tail (bool, optional):
                If True, will reatin the text after the cursor position.
                Defaults to False.
        """

        ...

    @abc.abstractmethod
    def clear_line(
        self,
        keep_head: bool = False,
        keep_tail: bool = False,
    ):  # pragma: no cover
        """Clear the current line of the terminal.

        Args:
            keep_head (bool, optional):,
                If True, will retain the text before the cursor position.
                Defaults to False.
            keep_tail (bool, optional):
                If True, will retain the text after the cursor position.
                Defaults to False.
        """

        ...

    @abc.abstractmethod
    def set_title(self, value: str):  # pragma: no cover
        """Set the current title of the terminal.

        Args:
            value (str):
                The new title of the terminal.
        """

        ...

    @abc.abstractmethod
    def reset(self):  # pragma: no cover
        """Reset the current style of the terminal."""

        ...

    @abc.abstractmethod
    def hide_cursor(self):  # pragma: no cover
        """Hide the current terminal cursor."""

        ...

    @abc.abstractmethod
    def show_cursor(self):  # pragma: no cover
        """Show the current terminal cursor."""

        ...

    @abc.abstractmethod
    def flash(self, duration: float):  # pragma: no cover
        """Flash the terminal.

        Args:
            duration (float):
                The delay in seconds the flash should last.
        """

        ...

    @abc.abstractmethod
    def apply(
        self,
        value: str,
        style: Set[Style],
        background: Optional[Color_T],
        foreground: Optional[Color_T],
    ) -> str:  # pragma: no cover
        """Apply some styles and colors to a given string.

        Args:
            value (str):
                The string to apply styles and colors to.
            style (Set[:class:`~style.Style`]):
                The set of styles to apply to the string value.
            background (Optional[:class:`~color.Color_T`]):
                The background color to apply to the given string.
            foreground (Optional[:class:`~color.Color_T`]):
                The foreground color to apply to the given string.

        Returns:
            str:
                The newly styled string.
        """

        ...
