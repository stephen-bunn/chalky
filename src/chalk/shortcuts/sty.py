# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Predefined style (sty) chalk styles."""

from ..chalk import Chalk
from ..style import Style

bold = Chalk(style={Style.BOLD})
dim = Chalk(style={Style.DIM})
italic = Chalk(style={Style.ITALIC})
underline = Chalk(style={Style.UNDERLINE})
slow_blink = Chalk(style={Style.SLOW_BLINK})
rapid_blink = Chalk(style={Style.RAPID_BLINK})
reversed = Chalk(style={Style.REVERSED})
conceal = Chalk(style={Style.CONCEAL})
strikethrough = Chalk(style={Style.STRIKETHROUGH})
normal = Chalk(style={Style.NORMAL})
