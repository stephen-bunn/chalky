# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from __future__ import annotations

import ctypes
import sys
import warnings
from ctypes import wintypes
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Optional, Set, TextIO, Tuple

from ..color import Color_T
from ..style import Style
from .base import BaseInterface

STDOUT_HANDLE = -11
STDERR_HANDLE = -12


class WinStyle:

    NORMAL = 0x00
    BRIGHT = 0x08
    BRIGHT_BACKGROUND = 0x80


@dataclass
class ConsoleState:

    foreground: int
    background: int
    style: int
    light: bool = False

    @classmethod
    def from_attributes(cls, attributes: int) -> ConsoleState:
        return ConsoleState(
            foreground=attributes & 7,
            background=(attributes >> 4) & 7,
            style=attributes & (WinStyle.BRIGHT | WinStyle.BRIGHT_BACKGROUND),
        )

    @classmethod
    def from_default(cls) -> ConsoleState:
        return ConsoleState(foreground=7, background=0, style=0)

    def to_attributes(self) -> int:
        return self.foreground + (self.background * 16) + (self.style | int(self.light))


class ConsoleScreenBufferInfo(ctypes.Structure):

    _fields_ = [
        ("dwSize", wintypes._COORD),
        ("dwCursorPosition", wintypes._COORD),
        ("wAttributes", wintypes.WORD),
        ("srWindow", wintypes.SMALL_RECT),
        ("dwMaximumWindowSize", wintypes._COORD),
    ]

    def __str__(self) -> str:
        return (
            f"<{self.__class__.__qualname__!s} "
            f"dwSize={{Y: {self.dwSize.Y}, X: {self.dwSize.X}}}, "
            f"dwCursorPosition={{Y: {self.dwCursorPosition.Y}, "
            f"X: {self.dwCursorPosition.X}}}, "
            f"wAttributes={self.wAttributes}, "
            f"srWindow={{Top: {self.srWindow.Top}, Left: {self.srWindow.Left}, "
            f"Bottom: {self.srWindow.Bottom}, Right: {self.srWindow.Right}}}, "
            f"dwMaximumWindowSize={{Y: {self.dwMaximumWindowSize.Y}, "
            f"X: {self.dwMaximumWindowSize.X}}}"
            ">"
        )


class Win32Interface(BaseInterface):
    def __init__(self, io: TextIO):
        super().__init__(io)

        self.windll: Optional[ctypes.LibraryLoader] = None
        try:
            # ctypes.WinDLL is only available when running on Windows
            self.windll = ctypes.LibraryLoader(ctypes.WinDLL)  # type: ignore
            self.default_console_state = self._get_console_state(self.io)
        except (AttributeError, ImportError) as exc:
            warnings.warn(
                f"Initializing the {self.__class__.__qualname__!s} failed, {exc!r}",
                UserWarning,
            )

    def _noop(self, *args, **kwargs) -> None:
        return None

    @lru_cache(maxsize=1)
    def _build_get_std_handle(self) -> Callable[[int], Optional[wintypes.HANDLE]]:
        if not self.windll:
            return self._noop

        service = self.windll.kernel32.GetStdHandle
        service.argtypes = [wintypes.DWORD]
        service.restype = wintypes.HANDLE

        return service

    @lru_cache(maxsize=1)
    def _build_get_console_screen_buffer_info(
        self,
    ) -> Callable[[wintypes.HANDLE, ctypes.pointer], Optional[wintypes.BOOL]]:
        if not self.windll:
            return self._noop

        service = self.windll.kernel32.GetConsoleScreenBufferInfo
        service.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(ConsoleScreenBufferInfo),
        ]
        service.restype = wintypes.BOOL

        return service

    @lru_cache(maxsize=1)
    def _build_fill_console_output_character(
        self,
    ) -> Callable[
        [
            wintypes.HANDLE,
            ctypes.c_char,
            wintypes.DWORD,
            wintypes._COORD,
            ctypes.pointer,
        ],
        Optional[wintypes.BOOL],
    ]:
        if not self.windll:
            return self._noop

        service = self.windll.kernel32.FillConsoleOutputCharacterA
        service.argtypes = [
            wintypes.HANDLE,
            ctypes.c_char,
            wintypes.DWORD,
            wintypes._COORD,
            ctypes.POINTER(wintypes.DWORD),
        ]
        service.restype = wintypes.BOOL

        return service

    @lru_cache(maxsize=1)
    def _build_fill_console_output_attribute(
        self,
    ) -> Callable[
        [
            wintypes.HANDLE,
            wintypes.WORD,
            wintypes.DWORD,
            wintypes._COORD,
            ctypes.pointer,
        ],
        Optional[wintypes.BOOL],
    ]:
        if not self.windll:
            return self._noop

        service = self.windll.kernel32.FillConsoleOutputAttribute
        service.argtypes = [
            wintypes.HANDLE,
            wintypes.WORD,
            wintypes.DWORD,
            wintypes._COORD,
            ctypes.POINTER(wintypes.DWORD),
        ]
        service.restype = wintypes.BOOL

        return service

    @lru_cache(maxsize=1)
    def _build_set_console_text_attribute(
        self,
    ) -> Callable[[wintypes.HANDLE, wintypes.WORD], Optional[wintypes.BOOL]]:
        if not self.windll:
            return self._noop

        service = self.windll.kernel32.SetConsoleTextAttribute
        service.argtypes = [wintypes.HANDLE, wintypes.WORD]
        service.restype = wintypes.BOOL

        return service

    @lru_cache(maxsize=1)
    def _build_set_console_cursor_position(
        self,
    ) -> Callable[[wintypes.HANDLE, wintypes._COORD], Optional[wintypes.BOOL]]:
        if not self.windll:
            return self._noop

        service = self.windll.kernel32.SetConsoleCursorPosition
        service.argtypes = [wintypes.HANDLE, wintypes._COORD]
        service.restype = wintypes.BOOL

        return service

    @lru_cache(maxsize=1)
    def _build_set_title(self) -> Callable[[wintypes.LPCWSTR], Optional[wintypes.BOOL]]:
        if not self.windll:
            return self._noop

        service = self.windll.kernel32.SetConsoleTitleW
        service.argtypes = [wintypes.LPCWSTR]
        service.restype = wintypes.BOOL

        return service

    def _get_std_handle(self, io: TextIO) -> Optional[wintypes.HANDLE]:
        is_stderr = io.fileno() == sys.stderr.fileno()
        return self._build_get_std_handle()(
            STDERR_HANDLE if is_stderr else STDOUT_HANDLE
        )

    def _get_console_screen_buffer_info(
        self, io: TextIO
    ) -> Optional[ConsoleScreenBufferInfo]:
        handle = self._get_std_handle(io)
        if not handle:
            return None

        buffer_info = ConsoleScreenBufferInfo()
        success = self._build_get_console_screen_buffer_info()(
            handle, ctypes.byref(buffer_info)  # type: ignore
        )

        if not success:
            return None

        return buffer_info

    def _fill_console_output_character(
        self,
        io: TextIO,
        char: str,
        to_erase: int,
        from_coord: wintypes._COORD,
    ) -> Optional[int]:
        handle = self._get_std_handle(io)
        if not handle:
            return None

        written_chars = wintypes.DWORD(0)
        self._build_fill_console_output_character()(
            handle,
            ctypes.c_char(char.encode("utf-8")),
            wintypes.DWORD(to_erase),
            from_coord,
            ctypes.byref(written_chars),  # type: ignore
        )

        return written_chars.value

    def _fill_console_output_attribute(
        self,
        io: TextIO,
        attributes: int,
        to_erase: int,
        from_coord: wintypes._COORD,
    ) -> Optional[bool]:
        handle = self._get_std_handle(io)
        if not handle:
            return None

        written_chars = wintypes.DWORD(0)
        return self._build_fill_console_output_attribute()(
            handle,
            wintypes.WORD(attributes),
            wintypes.DWORD(to_erase),
            from_coord,
            ctypes.byref(written_chars),  # type: ignore
        )

    def _set_console_cursor_position(
        self,
        io: TextIO,
        position: Tuple[int, int],
        auto_adjust: bool = True,
    ) -> Optional[bool]:
        coord = wintypes._COORD(*position)
        if coord.Y <= 0 or coord.X <= 0:  # type: ignore
            return None

        handle = self._get_std_handle(io)
        if not handle:
            return None

        adjusted_coord = wintypes._COORD(coord.Y - 1, coord.X - 1)  # type: ignore
        if auto_adjust:
            screen_buffer = self._get_console_screen_buffer_info(io)
            if not screen_buffer:
                return None

            adjusted_coord.Y += screen_buffer.srWindow.Top
            adjusted_coord.X += screen_buffer.srWindow.Left

        return bool(self._build_set_console_cursor_position()(handle, adjusted_coord))

    def _set_console_text_attribute(
        self, io: TextIO, attributes: int
    ) -> Optional[bool]:
        handle = self._get_std_handle(io)
        if not handle:
            return None

        return bool(
            self._build_set_console_text_attribute()(
                handle,
                wintypes.WORD(attributes),
            )
        )

    def _get_console_state(self, io: TextIO) -> Optional[ConsoleState]:
        screen_buffer = self._get_console_screen_buffer_info(io)
        if not screen_buffer:
            return None

        return ConsoleState.from_attributes(screen_buffer.wAttributes)

    def _set_console_state(self, io: TextIO, state: ConsoleState) -> Optional[bool]:
        return self._set_console_text_attribute(io, state.to_attributes())

    def _set_title(self, title: str) -> Optional[bool]:
        return bool(self._build_set_title()(wintypes.LPCWSTR(title)))

    def clear_screen(self, reset_position: bool = True):
        # Writing an extra newline prior to clearing the screen assures that we are
        # considering the whole screen buffer in case someone is continually writing to
        # the same line
        self.io.write("\n")

        screen_buffer = self._get_console_screen_buffer_info(self.io)
        if not screen_buffer:
            return

        total_cells = screen_buffer.dwSize.X * screen_buffer.dwSize.Y
        # written_cells = (
        #     screen_buffer.dwSize.X * screen_buffer.dwCursorPosition.Y
        # ) + screen_buffer.dwCursorPosition.X

        to_erase = total_cells
        from_coord = wintypes._COORD(0, 0)

        self._fill_console_output_character(self.io, " ", to_erase, from_coord)
        self._fill_console_output_attribute(
            self.io,
            screen_buffer.wAttributes,
            to_erase,
            from_coord,
        )

        if reset_position:
            self._set_console_cursor_position(self.io, (1, 1))

    def clear_line(self):
        self.io.write("\r")
        screen_buffer = self._get_console_screen_buffer_info(self.io)
        if not screen_buffer:
            return

        to_erase = screen_buffer.dwSize.X
        from_coord = wintypes._COORD(0, screen_buffer.dwCursorPosition.Y)
        self._fill_console_output_character(self.io, " ", to_erase, from_coord)
        self._fill_console_output_attribute(
            self.io,
            screen_buffer.wAttributes,
            to_erase,
            from_coord,
        )

    def set_title(self, value: str):
        self._set_title(value)

    def reset(self):
        self._set_console_state(
            self.io,
            self.default_console_state or ConsoleState.from_default(),
        )

    def build_reset(self) -> bytes:
        return b""

    def build(
        self,
        style: Set[Style],
        background: Optional[Color_T],
        foreground: Optional[Color_T],
    ) -> bytes:

        # TODO: no implementation yet
        pass
