# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

import sys
from string import printable
from typing import Optional
from unittest.mock import patch

import pytest
from hypothesis import given
from hypothesis.strategies import (
    binary,
    booleans,
    floats,
    integers,
    none,
    one_of,
    sampled_from,
    text,
)

from chalk.chalk import Chalk
from chalk.color import Color, Color_T, TrueColor
from chalk.interface.ansi import (
    MODE_KEEP_HEAD,
    MODE_KEEP_NONE,
    MODE_KEEP_TAIL,
    AnsiInterface,
    build_clear_line,
    build_clear_screen,
    build_color,
    build_cursor,
    build_escape_sequence,
    build_position_cursor,
    build_reset,
    build_set_title,
    build_style,
    build_truecolor,
    build_video,
    get_clear_mode,
)
from chalk.style import Style

from ..test_chalk import chalk
from ..test_color import true_color


def get_interface() -> AnsiInterface:
    return AnsiInterface(sys.stdout)


@given(binary(min_size=1, max_size=1))
def test_build_escape_sequence(code: bytes):
    escape_sequence = build_escape_sequence(code)
    assert isinstance(escape_sequence, bytes)
    assert len(escape_sequence) > len(code)


@given(one_of(sampled_from(Style), none()))
def test_build_style(style: Optional[Style]):
    style_sequence = build_style(style)  # type: ignore
    assert isinstance(style_sequence, bytes)
    if style is not None:
        assert len(style_sequence) > 0


@given(true_color(), booleans())
def test_build_truecolor(color: TrueColor, background: bool):
    with patch(
        "chalk.interface.ansi.build_escape_sequence", wraps=build_escape_sequence
    ) as mocked_build_escape_sequence:
        color_sequence = build_truecolor(color, background=background)

        layer_code = b"48" if background else b"38"
        assert mocked_build_escape_sequence.call_args.args[0].startswith(layer_code)

        assert isinstance(color_sequence, bytes)
        assert len(color_sequence) > 0


@given(one_of(sampled_from(Color), true_color(), none()), booleans())
def test_build_color(color: Optional[Color_T], background: bool):
    escape_sequence = build_color(color, background=background)  # type: ignore
    assert isinstance(escape_sequence, bytes)
    if color is not None:
        assert len(escape_sequence) > 0


@given(booleans(), booleans())
def test_get_clear_mode(keep_head: bool, keep_tail: bool):
    # XXX: this test is testing the explicit implementation of this function
    clear_mode = get_clear_mode(keep_head, keep_tail)
    if keep_head and keep_tail:
        assert clear_mode is None
        return

    if keep_head:
        assert clear_mode == MODE_KEEP_HEAD
    elif keep_tail:
        assert clear_mode == MODE_KEEP_TAIL
    else:
        assert clear_mode == MODE_KEEP_NONE


@given(integers(min_value=0))
def test_build_clear_screen(mode: int):
    escape_sequence = build_clear_screen(mode)
    assert isinstance(escape_sequence, bytes)
    assert len(escape_sequence) > 0


@given(integers(min_value=0))
def test_build_clear_line(mode: int):
    escape_sequence = build_clear_line(mode)
    assert isinstance(escape_sequence, bytes)
    assert len(escape_sequence) > 0


def test_build_reset():
    escape_sequence = build_reset()
    assert isinstance(escape_sequence, bytes)
    assert len(escape_sequence) > 0


@given(integers(max_value=0), integers(max_value=0))
def test_build_position_cursor_raises_ValueError(x: int, y: int):
    with pytest.raises(ValueError):
        build_position_cursor(x, y)


@given(integers(min_value=1), integers(min_value=1))
def test_build_position_cursor(x: int, y: int):
    escape_sequence = build_position_cursor(x, y)
    assert isinstance(escape_sequence, bytes)
    assert len(escape_sequence) > 0


@given(booleans())
def test_build_video(normal: bool):
    escape_sequence = build_video(normal)
    assert isinstance(escape_sequence, bytes)
    assert len(escape_sequence) > 0

    assert escape_sequence.endswith(b"l" if normal else b"h")


@given(booleans())
def test_build_cursor(show: bool):
    escape_sequence = build_cursor(show)
    assert isinstance(escape_sequence, bytes)
    assert len(escape_sequence) > 0

    assert escape_sequence.endswith(b"h" if show else b"l")


@given(text(printable))
def test_build_set_title(title: str):
    escape_sequence = build_set_title(title)
    assert isinstance(escape_sequence, bytes)
    assert len(escape_sequence) > 0


def test_write():
    with patch("sys.stdout", wraps=sys.stdout) as mocked_stdout:
        mocked_stdout.encoding = "utf-8"

        interface = get_interface()
        interface._write(b"test")

        mocked_stdout.write.assert_called_with("test")
        mocked_stdout.flush.assert_called()


@given(booleans())
def test_clear_screen(reset_position: bool):
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write:
        interface = get_interface()
        interface.clear_screen(reset_position=reset_position)

        mocked_write.assert_called()


def test_clear_screen_does_nothing_if_no_mode():
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write:
        interface = get_interface()
        interface.clear_screen(keep_head=True, keep_tail=True)

        mocked_write.assert_not_called()


def test_clear_line():
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write:
        interface = get_interface()
        interface.clear_line()

        mocked_write.assert_called()


def test_clear_line_does_nothing_if_no_mode():
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write:
        interface = get_interface()
        interface.clear_line(keep_head=True, keep_tail=True)

        mocked_write.assert_not_called()


@given(text(printable))
def test_set_title(title: str):
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write:
        interface = get_interface()
        interface.set_title(title)

        mocked_write.assert_called()


def test_reset():
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write:
        interface = get_interface()
        interface.reset()

        mocked_write.assert_called()


def test_hide_cursor():
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write:
        interface = get_interface()
        interface.hide_cursor()

        mocked_write.assert_called()


def test_show_cursor():
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write:
        interface = get_interface()
        interface.show_cursor()

        mocked_write.assert_called()


def test_reverse_video():
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write:
        interface = get_interface()
        interface.reverse_video()

        mocked_write.assert_called()


def test_normal_video():
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write:
        interface = get_interface()
        interface.normal_video()

        mocked_write.assert_called()


@given(floats(min_value=0, max_value=1))
def test_flash(duration: float):
    with patch("chalk.interface.ansi.AnsiInterface._write") as mocked_write, patch(
        "time.sleep"
    ) as mocked_sleep:

        interface = get_interface()
        interface.flash(duration)

        assert mocked_sleep.called_with(duration)
        assert len(mocked_write.mock_calls) == 2
