# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

import sys

from chalky.interface import get_interface
from chalky.interface.ansi import AnsiInterface


def test_get_interface():
    interface = get_interface()
    assert interface.io == sys.stdout
    assert isinstance(interface, AnsiInterface)

    stderr_interface = get_interface(sys.stderr)
    assert stderr_interface.io == sys.stderr
    assert isinstance(stderr_interface, AnsiInterface)
