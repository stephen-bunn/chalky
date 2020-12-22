# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from hypothesis import given
from hypothesis.strategies import booleans, integers

from chalk.chalk import Chalk
from chalk.color import TrueColor
from chalk.shortcuts import hex, rgb

from .test_color import hex_color


@given(hex_color(), booleans())
def test_hex(hex_color: str, background: bool):
    chalk = hex(hex_color, background=background)
    assert isinstance(chalk, Chalk)
    assert getattr(
        chalk, "background" if background else "foreground"
    ) == TrueColor.from_hex(hex_color)


@given(
    integers(min_value=0, max_value=255),
    integers(min_value=0, max_value=255),
    integers(min_value=0, max_value=255),
    booleans(),
)
def test_rgb(red: int, green: int, blue: int, background: bool):
    chalk = rgb(red, green, blue, background=background)
    assert isinstance(chalk, Chalk)
    assert getattr(chalk, "background" if background else "foreground") == TrueColor(
        red, green, blue
    )
