# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from string import printable
from typing import Optional, Union

from hypothesis import given
from hypothesis.strategies import (
    SearchStrategy,
    booleans,
    composite,
    integers,
    none,
    one_of,
    text,
)
from hypothesis.strategies._internal.core import sampled_from

from chalky.chain import Chain
from chalky.chalk import Chalk
from chalky.color import Color, Color_T, TrueColor
from chalky.style import Style

from .test_chalk import chalk
from .test_color import hex_color, true_color


@composite
def chain(
    draw,
    chalk_strategy: Optional[SearchStrategy[Chalk]] = None,
) -> SearchStrategy[Chain]:
    return Chain(chalk=draw(chalk_strategy if chalk_strategy else chalk()))


@given(chain(), one_of(chalk(), chain()))
def test_Chain_composable_by_and(chain: Chain, value: Union[Chalk, Chain]):
    composed = chain & value
    assert isinstance(composed, Chain)


@given(chain(), one_of(chalk(), chain()))
def test_Chain_composable_by_add(chain: Chain, value: Union[Chalk, Chain]):
    composed = chain + value
    assert isinstance(composed, Chain)


@given(chain(), text(printable))
def test_Chain_applied_by_or(chain: Chain, value: str):
    applied = chain | value
    assert isinstance(applied, str)
    assert len(applied) > len(value)


@given(chain(), text(printable))
def test_Chain_applied_by_add(chain: Chain, value: str):
    applied = chain + value
    assert isinstance(applied, str)
    assert len(applied) > len(value)


@given(chain(), text(printable))
def test_Chain_callable(chain: Chain, value: str):
    applied = chain(value)
    assert isinstance(applied, str)
    assert len(applied) > len(value)


@given(
    chain(chalk_strategy=chalk(foreground_strategy=none())),
    integers(min_value=0, max_value=255),
    integers(min_value=0, max_value=255),
    integers(min_value=0, max_value=255),
)
def test_Chain_rgb(chain: Chain, red: int, green: int, blue: int):
    updated = chain.rgb(red, green, blue)
    assert isinstance(updated.chalk.foreground, TrueColor)
    assert updated.chalk.foreground.red == red
    assert updated.chalk.foreground.green == green
    assert updated.chalk.foreground.blue == blue


@given(chain(chalk_strategy=chalk(foreground_strategy=none())), hex_color())
def test_Chain_hex(chain: Chain, color: str):
    updated = chain.hex(color)
    assert isinstance(updated.chalk.foreground, TrueColor)


@given(chain())
def test_Chain_bg(chain: Chain):
    chain.fg

    updated = chain.bg
    assert updated._background


@given(chain())
def test_Chain_fg(chain: Chain):
    chain.bg

    updated = chain.fg
    assert updated._background == False


@given(chain(), sampled_from(Style))
def test_Chain_applies_Style(chain: Chain, style: Style):
    updated = chain._handle_style(style)
    assert style in updated.chalk.style


@given(chain(), one_of(sampled_from(Color), true_color()), booleans())
def test_Chain_applies_Color(chain: Chain, color: Color_T, background: bool):
    if background:
        chain.bg
    else:
        chain.fg

    updated = chain._handle_color(color)

    if background:
        assert updated.chalk.background == color
    else:
        assert updated.chalk.foreground == color
