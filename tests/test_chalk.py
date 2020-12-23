# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from string import printable
from typing import Optional, Set

from chalky.chalk import Chalk
from chalky.color import Color, Color_T
from chalky.style import Style
from hypothesis import given
from hypothesis.strategies import (
    SearchStrategy,
    composite,
    none,
    nothing,
    one_of,
    sampled_from,
    sets,
    text,
)

from .test_color import true_color


@composite
def chalk(
    draw,
    style_strategy: Optional[SearchStrategy[Set[Style]]] = None,
    foreground_strategy: Optional[SearchStrategy[Color_T]] = None,
    background_strategy: Optional[SearchStrategy[Color_T]] = None,
) -> SearchStrategy[Chalk]:
    default_style_strategy = sets(sampled_from(Style))
    default_color_strategy = one_of(none(), sampled_from(Color), true_color())

    return Chalk(
        style=draw(style_strategy if style_strategy else default_style_strategy),
        foreground=draw(
            foreground_strategy if foreground_strategy else default_color_strategy
        ),
        background=draw(
            background_strategy if background_strategy else default_color_strategy
        ),
    )


def test_Chalk_composition_overrides():
    overridden_foreground = Chalk(foreground=Color.BLUE) & Chalk(foreground=Color.RED)
    assert overridden_foreground.foreground == Color.RED

    overridden_background = Chalk(background=Color.RED) & Chalk(background=Color.BLUE)
    assert overridden_background.background == Color.BLUE


def test_Chalk_composition_unions():
    unioned_style = Chalk(style={Style.BOLD}) & Chalk(style={Style.BOLD, Style.ITALIC})
    assert unioned_style.style == {Style.BOLD, Style.ITALIC}


@given(chalk(), chalk())
def test_Chalk_composable_by_and(chalk_a: Chalk, chalk_b: Chalk):
    assert isinstance(chalk_a & chalk_b, Chalk)


@given(chalk(), chalk())
def test_Chalk_composable_by_add(chalk_a: Chalk, chalk_b: Chalk):
    assert isinstance(chalk_a + chalk_b, Chalk)


@given(chalk(), text(printable, min_size=1))
def test_Chalk_applied_by_or(chalk: Chalk, value: str):
    assert isinstance(chalk | value, str)


@given(chalk(), text(printable, min_size=1))
def test_Chalk_applied_by_add(chalk: Chalk, value: str):
    assert isinstance(chalk + value, str)


@given(chalk(style_strategy=sets(nothing(), max_size=0)))
def test_Chalk_reverse(chalk: Chalk):
    assert Style.REVERSED not in chalk.style
    assert Style.REVERSED in chalk.reverse.style
