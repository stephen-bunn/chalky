# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from typing import Optional, Set

from ..color import Color, Color_T, TrueColor
from ..style import Style
from .base import BaseInterface

ESC = b"\x1b"
CSI = ESC + b"["
OSC = ESC + b"]"
BEL = b"\a"

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


class AnsiInterface(BaseInterface):
    def _build_escape_sequence(self, code: bytes) -> bytes:
        return CSI + code + b"m"

    def _build_style(self, style: Style) -> bytes:
        style_code = STYLE_MAP.get(style)
        if style_code is None:
            return b""

        return self._build_escape_sequence(style_code)

    def _build_truecolor(self, color: TrueColor, background: bool = False) -> bytes:
        red, green, blue = color.to_bytes()
        truecolor_code = (
            (b"48" if background else b"38") + b";2;" + red + b";" + green + b";" + blue
        )

        return self._build_escape_sequence(truecolor_code)

    def _build_color(self, color: Color_T, background: bool = False) -> bytes:
        if isinstance(color, TrueColor):
            return self._build_truecolor(color, background=background)

        color_map = BACKGROUND_COLOR_MAP if background else FOREGROUND_COLOR_MAP
        color_code = color_map.get(color)
        if color_code is None:
            return b""

        return self._build_escape_sequence(color_code)

    def _build_clear(self) -> bytes:
        # TODO: currently assuming CLEAR_ALL (2J) all the time
        return CSI + b"2J"

    def _build_reset_position(self) -> bytes:
        return CSI + b"H"

    def _build_clear_line(self) -> bytes:
        return CSI + b"2K"

    def _build_set_title(self, title: str) -> bytes:
        return OSC + b"2;" + title.encode("utf-8") + BEL

    def _build_reset(self) -> bytes:
        return self._build_escape_sequence(STYLE_MAP.get(Style.RESET, b"0"))

    def clear_screen(self, reset_position: bool = True):
        self.io.write(self._build_clear().decode(self.io.encoding))
        if reset_position:
            self.io.write(self._build_reset_position().decode(self.io.encoding))

    def clear_line(self):
        self.io.write("\r")
        self.io.write(self._build_clear_line().decode(self.io.encoding))

    def set_title(self, value: str):
        self.io.write(self._build_set_title(value).decode(self.io.encoding))

    def reset(self):
        self.io.write(self._build_reset().decode(self.io.encoding))

    def build_reset(self) -> bytes:
        return self._build_reset()

    def build(
        self,
        style: Set[Style],
        background: Optional[Color_T],
        foreground: Optional[Color_T],
    ) -> bytes:
        escape_sequence = b"".join(map(self._build_style, style))
        if background:
            escape_sequence += self._build_color(background, background=True)
        if foreground:
            escape_sequence += self._build_color(foreground)

        return escape_sequence
