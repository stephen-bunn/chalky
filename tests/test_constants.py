# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from string import printable

from hypothesis import given
from hypothesis.strategies import text

from chalky.chalk import Chalk
from chalky.color import Color
from chalky.constants import configure, is_disabled


@given(text(printable))
def test_configure_disable(value: str):
    assert not is_disabled()
    configure(disable=True)
    assert is_disabled()

    applied = Chalk(foreground=Color.RED) | value
    assert isinstance(applied, str)
    assert len(applied) == len(value)

    configure(disable=False)
    assert not is_disabled()
    applied = Chalk(foreground=Color.RED) | value
    assert isinstance(applied, str)
    assert len(applied) > len(value)
