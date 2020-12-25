# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains package constants that modify the global functions of the package."""


DISABLED = False


def is_disabled() -> bool:
    """Callable to evaluate the disabled conditional.

    Returns:
        bool:
            True if chalky is disabled, otherwise False.
    """

    return DISABLED


def configure(disable: bool = False):
    """Configure the global state of the chalky module.

    Args:
        disable (bool, optional):
            If True, will disable all future application of colors and styles.
            Defaults to False.
    """

    global DISABLED

    DISABLED = disable
