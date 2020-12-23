# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from string import printable
from typing import Optional

import pytest
from chalky.color import TrueColor
from hypothesis import given
from hypothesis.strategies import SearchStrategy, composite, from_regex, integers, text


@composite
def hex_color(draw) -> SearchStrategy[str]:
    return draw(from_regex(r"\A#?[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\Z"))


@composite
def true_color(
    draw,
    red_strategy: Optional[SearchStrategy[int]] = None,
    green_strategy: Optional[SearchStrategy[int]] = None,
    blue_strategy: Optional[SearchStrategy[int]] = None,
) -> SearchStrategy[TrueColor]:
    default_value_strategy = integers(min_value=0, max_value=255)
    return TrueColor(
        red=draw(red_strategy if red_strategy else default_value_strategy),
        green=draw(green_strategy if green_strategy else default_value_strategy),
        blue=draw(blue_strategy if blue_strategy else default_value_strategy),
    )


@given(true_color())
def test_TrueColor_hashable(color: TrueColor):
    assert hash(color)


@given(hex_color())
def test_TrueColor_from_hex(color_string: str):
    color = TrueColor.from_hex(color_string)
    assert isinstance(color, TrueColor)


@given(text(printable).filter(lambda x: len(x) not in (3, 6)))
def test_TrueColor_from_hex_raises_ValueError(color_string: str):
    with pytest.raises(ValueError):
        TrueColor.from_hex(color_string)


@given(true_color())
def test_TrueColor_to_bytes(color: TrueColor):
    color_bytes = color.to_bytes()
    assert len(color_bytes) == 3
    assert all(isinstance(value, bytes) for value in color_bytes)
