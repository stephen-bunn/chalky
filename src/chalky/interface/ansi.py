# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the ANSI interface implementation."""

import time
from typing import Optional, Set

from ..color import Color, Color_T, TrueColor
from ..helpers import int_to_bytes
from ..style import Style
from .base import BaseInterface

ESC = b"\x1b"
CSI = ESC + b"["
OSC = ESC + b"]"
BEL = b"\a"

MODE_KEEP_HEAD = 0
MODE_KEEP_TAIL = 1
MODE_KEEP_NONE = 2

FOREGROUND_COLOR_MAP = {
    Color.BLACK: b"30",
    Color.RED: b"31",
    Color.GREEN: b"32",
    Color.YELLOW: b"33",
    Color.BLUE: b"34",
    Color.MAGENTA: b"35",
    Color.CYAN: b"36",
    Color.WHITE: b"37",
    Color.BRIGHT_BLACK: b"90",
    Color.BRIGHT_RED: b"91",
    Color.BRIGHT_GREEN: b"92",
    Color.BRIGHT_YELLOW: b"93",
    Color.BRIGHT_BLUE: b"94",
    Color.BRIGHT_MAGENTA: b"95",
    Color.BRIGHT_CYAN: b"96",
    Color.BRIGHT_WHITE: b"97",
}

BACKGROUND_COLOR_MAP = {
    Color.BLACK: b"40",
    Color.RED: b"41",
    Color.GREEN: b"42",
    Color.YELLOW: b"43",
    Color.BLUE: b"44",
    Color.MAGENTA: b"45",
    Color.CYAN: b"46",
    Color.WHITE: b"47",
    Color.BRIGHT_BLACK: b"100",
    Color.BRIGHT_RED: b"101",
    Color.BRIGHT_GREEN: b"102",
    Color.BRIGHT_YELLOW: b"103",
    Color.BRIGHT_BLUE: b"104",
    Color.BRIGHT_MAGENTA: b"105",
    Color.BRIGHT_CYAN: b"106",
    Color.BRIGHT_WHITE: b"107",
}

STYLE_MAP = {
    Style.RESET: b"0",
    Style.BOLD: b"1",
    Style.DIM: b"2",
    Style.ITALIC: b"3",
    Style.UNDERLINE: b"4",
    Style.SLOW_BLINK: b"5",
    Style.RAPID_BLINK: b"6",
    Style.REVERSED: b"7",
    Style.CONCEAL: b"8",
    Style.STRIKETHROUGH: b"9",
    Style.NORMAL: b"22",
}


def build_escape_sequence(code: bytes) -> bytes:
    """Build the escape sequence for some given sequence code.

    Args:
        code (bytes):
            The sequence code to build.

    Returns:
        bytes:
            The built escape sequence.
    """

    return CSI + code + b"m"


def build_style(style: Style) -> bytes:
    """Build the appropriate escape sequence for a given style.

    Args:
        style (:class:`~style.Style`):
            The style to build the escape sequence for.

    Returns:
        bytes:
            The proper escape sequence for styling text with the given style.
    """

    style_code = STYLE_MAP.get(style)
    if style_code is None:
        return b""

    return build_escape_sequence(style_code)


def build_truecolor(color: TrueColor, background: bool = False) -> bytes:
    """Build the appropriate escape sequence for a given truecolor.

    Args:
        color (:class:`~color.TrueColor`):
            The color to build the escape sequence for.
        background (bool, optional):
            True if the color should bve used as a background color.
            Defaults to False.

    Returns:
        bytes:
            The proper escape sequence for coloring text with the given truecolor.
    """

    red, green, blue = color.to_bytes()
    truecolor_code = (
        (b"48" if background else b"38") + b";2;" + red + b";" + green + b";" + blue
    )

    return build_escape_sequence(truecolor_code)


def build_color(color: Color_T, background: bool = False) -> bytes:
    """Build the appropriate escape sequence for a given color.

    Args:
        color (:attr:`~color.Color_T`):
            The color to build the escape sequence for.
        background (bool, optional):
            True if the color should be used as a background color.
            Defaults to False.

    Returns:
        bytes:
            The proper escape sequence for coloring text with the given color.
    """

    if isinstance(color, TrueColor):
        return build_truecolor(color, background=background)

    color_map = BACKGROUND_COLOR_MAP if background else FOREGROUND_COLOR_MAP
    color_code = color_map.get(color)
    if color_code is None:
        return b""

    return build_escape_sequence(color_code)


def get_clear_mode(keep_head: bool, keep_tail: bool) -> Optional[int]:
    """Get the appropriate clear mode for the ``keep_head`` and ``keep_tail`` params.

    Args:
        keep_head (bool):
            True if you would like to keep the head content behind the cursor.
        keep_tail (bool):
            True if you would like to keep the tail content after the cursor.

    Returns:
        Optional[int]:
            The appropriate clear mode if available.
            If ``None`` is provided, consider skipping clearing.
    """

    if keep_head and keep_tail:
        return None

    if keep_head:
        return MODE_KEEP_HEAD
    elif keep_tail:
        return MODE_KEEP_TAIL
    else:
        return MODE_KEEP_NONE


def build_clear_screen(mode: int) -> bytes:
    """Build the escape sequence to clear the entire screen.

    Various modes are available for clearing the current line in the terminal.
    These are more appropriately derived from :func:`~ansi.get_clear_mode`.

    * 0 - Clear from cursor to end of screen
    * 1 - Clear from cursor to beginning of screen
    * 2 - Clear entire screen

    Args:
        mode (int):
            The mode to use for clearing the entire screen.

    Returns:
        bytes:
            The proper escape sequence to clear the entire screen.
    """

    return CSI + int_to_bytes(mode) + b"J"


def build_clear_line(mode: int) -> bytes:
    """Build the escape sequence to clear the current line.

    Various modes are available for clearing the current line in the terminal.
    These are more appropriately derived from :func:`~ansi.get_clear_mode`.

    * 0 - Clear from cursor to end of line
    * 1 - Clear from cursor to beginning of line
    * 2 - Clear entire line

    Args:
        mode (int):
            The mode to use for clearing the current line.

    Returns:
        bytes:
            The proper escape sequence to clear the current line.
    """

    return CSI + int_to_bytes(mode) + b"K"


def build_reset() -> bytes:
    """Build the escape sequence to reset the current text style and color.

    Returns:
        bytes:
            The proper escape sequence to reset the terminal text style and color.
    """

    return build_escape_sequence(STYLE_MAP.get(Style.RESET, b"0"))


def build_position_cursor(x: int, y: int) -> bytes:
    """Build the appropriate escape sequence to control the terminal cursor position.

    Args:
        x (int):
            The new column position of the cursor (1-indexed).
        y (int):
            The new row position of the cursor (1-indexed).

    Raises:
        ValueError:
            When either the given row or column positions are less than or equal to 0.

    Returns:
        bytes:
            The appropriate escape sequence to move the terminal cursor.
    """

    if x <= 0 or y <= 0:
        raise ValueError(f"Cursor positions are 1-indexed, received x={x}, y={y}")

    return CSI + int_to_bytes(y) + b";" + int_to_bytes(x) + b"H"


def build_video(normal: bool) -> bytes:
    """Build the appropriate escape sequence to control the terminal video state.

    Args:
        normal (bool):
            True if the terminal video should be normal, False if it should be reversed.

    Returns:
        bytes:
            The proper escape sequence to control terminal video state.
    """

    return CSI + b"?5" + (b"l" if normal else b"h")


def build_cursor(show: bool) -> bytes:
    """Build the appropriate escape sequence to control the visibility of the cursor.

    Args:
        show (bool):
            True if the cursor should be visible, False if it should be hidden.

    Returns:
        bytes:
            The proper escape sequence to control cursor visibility.
    """

    return CSI + b"?25" + (b"h" if show else b"l")


def build_set_title(title: str) -> bytes:
    """Build the appropriate escape sequence for setting the terminal title.

    Args:
        title (str):
            The new title to set.

    Returns:
        bytes:
            The proper escape sequence to set the terminal title.
    """

    return OSC + b"2;" + title.encode("utf-8") + BEL


class AnsiInterface(BaseInterface):
    """The interface to control ANSI terminals."""

    def _write(self, content: bytes):
        """Write the given bytes and immediately flush them.

        Args:
            content (bytes):
                The bytes to write to the ANSI text io.
        """

        self.io.write(content.decode(self.io.encoding))
        self.io.flush()

    def clear_screen(
        self,
        reset_position: bool = True,
        keep_head: bool = False,
        keep_tail: bool = False,
    ):
        """Clear the current screen of the terminal.

        Args:
            reset_position (bool, optional):
                If True, will also reset the cursor position to the start.
                Defaults to True.
            keep_head (bool, optional):
                If True, will retain the text before the cursor position.
                Defaults to False.
            keep_tail (bool, optional):
                If True, will retain the text after the cursor position.
                Defaults to False.
        """

        mode = get_clear_mode(keep_head, keep_tail)
        if not mode:
            return

        clear_screen = build_clear_screen(mode)
        if reset_position:
            clear_screen += build_position_cursor(1, 1)

        self._write(clear_screen)

    def clear_line(
        self,
        keep_head: bool = False,
        keep_tail: bool = False,
    ):
        """Clear the current line of the terminal.

        Args:
            keep_head (bool, optional):
                If True, will retain the text before the cursor position.
                Defaults to False.
            keep_tail (bool, optional):
                If True, will retain the text after the cursor position.
                Defaults to False.
        """

        mode = get_clear_mode(keep_head, keep_tail)
        if not mode:
            return

        self._write(build_clear_line(mode))

    def set_title(self, title: str):
        """Set the current title of the terminal to the given value.

        Args:
            title (str): The new title of the terminal.
        """

        self._write(build_set_title(title))

    def reset(self):
        """Reset the current style of printed terminal text."""

        self._write(build_reset())

    def hide_cursor(self):
        """Hide the current terminal cursor."""

        self._write(build_cursor(False))

    def show_cursor(self):
        """Show the current terminal cursor."""

        self._write(build_cursor(True))

    def reverse_video(self):
        """Reverse the current terminal colors."""

        self._write(build_video(False))

    def normal_video(self):
        """Normalize the current terminal colors."""

        self._write(build_video(True))

    def flash(self, duration: float):
        """Flash the terminal by inverting the current terminal colors.

        .. important::
            This is a blocking call.
            Whatever duration you specify for the flash, the runtime will be blocked for
            that time.
            Unless, of course, you decide to handle making the command async yourself.

        Args:
            duration (float):
                The delay in seconds the flash should last.
        """

        self.reverse_video()
        time.sleep(duration)
        self.normal_video()

    def apply(
        self,
        value: str,
        style: Set[Style],
        background: Optional[Color_T],
        foreground: Optional[Color_T],
    ) -> str:
        """Apply some style and color to a string for ANSI terminals.

        Args:
            value (str):
                The string value to apply styles to.
            style (Set[:class:`~style.Style`]):
                The set of styles to apply to the given string.
            background (Optional[:class:`~color.Color_T`]):
                The background color to apply to the given string.
            foreground (Optional[:class:`~color.Color_T`]):
                The foreground color to apply to the given string.

        Returns:
            str: The styled string value.
        """

        escape_sequence = b"".join(map(build_style, style))
        if background:
            escape_sequence += build_color(background, background=True)
        if foreground:
            escape_sequence += build_color(foreground)

        return (
            escape_sequence.decode(self.io.encoding)
            + value
            + build_reset().decode(self.io.encoding)
        )
