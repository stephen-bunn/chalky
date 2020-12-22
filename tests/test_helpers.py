# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

import os
from contextlib import contextmanager
from platform import system
from typing import Dict, Optional, Set
from unittest.mock import patch

import pytest
from hypothesis import given
from hypothesis.strategies import sampled_from

from chalk.helpers import supports_posix, supports_truecolor


def get_environment(exclude_keys: Optional[Set[str]] = None) -> Dict[str, str]:
    return {
        key: value
        for key, value in os.environ.items()
        if exclude_keys and key not in exclude_keys
    }


@given(sampled_from(("darwin", "linux")))
def test_supports_posix(supported_os: str):
    with patch("platform.system") as mocked_system:
        mocked_system.return_value = supported_os

        assert supports_posix()


@given(sampled_from(["truecolor"]))
def test_supports_truecolor_checks_COLORTERM(colorterm_value: str):
    with patch.dict(os.environ, {"COLORTERM": colorterm_value}):
        assert supports_truecolor()


@given(sampled_from(("256color", "24bit")))
def test_supports_truecolor_checks_TERM(term_value: str):
    with patch.dict(
        os.environ,
        {
            "TERM": term_value,
            **get_environment({"COLORTERM"}),
        },
        clear=True,
    ):
        assert supports_truecolor()


@pytest.mark.skipif(
    not supports_posix(),
    reason="os specific tests only works on posix",
)
def test_supports_truecolor_checks_tput():
    with patch.dict(
        os.environ,
        {"TERM": "test", **get_environment({"COLORTERM"})},
        clear=True,
    ):
        assert supports_truecolor()


def test_supports_truecolor_fails():
    with patch("chalk.helpers.supports_posix") as mocked_supports_posix:
        mocked_supports_posix.return_value = False
        with patch.dict(os.environ, get_environment({"TERM", "COLORTERM"}), clear=True):
            assert not supports_truecolor()
