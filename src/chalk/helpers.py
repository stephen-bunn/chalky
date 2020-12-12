# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

import os
import platform
import subprocess


def supports_posix() -> bool:

    return platform.system().lower() in (
        "darwin",
        "linux",
    )


def supports_truecolor() -> bool:

    colorterm = os.getenv("COLORTERM")
    if colorterm:
        return "truecolor" in colorterm.lower()

    term = os.getenv("TERM")
    if term:
        term = term.lower()
        return any(
            value in term
            for value in (
                "256color",
                "24bit",
            )
        )

    if supports_posix():
        tput = subprocess.run(["tput", "colors"], capture_output=True)
        if tput and len(tput.stdout) > 0:
            return "256" in tput.stdout.decode("utf-8").split("\n")[0].lower()

    return False
