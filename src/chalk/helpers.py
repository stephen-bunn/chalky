# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains some miscellaneous helpers for the rest of the package."""

import os
import platform
import subprocess


def supports_posix() -> bool:
    """Check if the current machine supports basic posix.

    Returns:
        bool:
            True if the current machine is MacOSX or Linux.
    """

    return platform.system().lower() in (
        "darwin",
        "linux",
    )


def supports_truecolor() -> bool:
    """Attempt to check if the current terminal supports truecolor.

    Returns:
        bool:
            True if the current terminal supports truecolor, otherwise False.
    """

    colorterm = os.getenv("COLORTERM")
    if colorterm:
        return "truecolor" in colorterm.lower()

    term = os.getenv("TERM")
    if not term:
        return False

    term = term.lower()
    term_supported = any(
        value in term
        for value in (
            "256color",
            "24bit",
        )
    )
    if term_supported:
        return True

    if supports_posix():
        tput = subprocess.run(["tput", "colors"], capture_output=True)
        if tput and len(tput.stdout) > 0:
            return "256" in tput.stdout.decode("utf-8").split("\n")[0].lower()

    return False


def int_to_bytes(value: int) -> bytes:
    """Convert a given number to its representation in bytes.

    Args:
        value (int):
            The value to convert.

    Returns:
        bytes:
            The representation of the given number in bytes.
    """

    return bytes(str(value), "utf-8")
