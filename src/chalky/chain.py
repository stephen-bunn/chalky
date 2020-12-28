# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the chain class that can be used to quickly produce styles and colors."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union, overload

from .chalk import Chalk
from .color import Color, Color_T, TrueColor
from .style import Style


@dataclass
class Chain:
    """Quickly produce a chain of styles and colors that can be applied to a string.

    Parameters:
        chalk (Chalk):
            The container chalk instance that contains the current chain style.

    Examples:
        Chaining styles together should be fairly straightforward:

        >>> from chalk import chain
        >>> print(chain.bold.blue | "Bold blue text")
        >>> print(chain.black.bg.green.italic | "Italic black text on green background")

        Once a :class:`~.chain.Chain` instance is applied to a string, the styles are
        consumed and the chain instance is reset.
    """

    _chalk: Chalk = field(default_factory=Chalk)
    _background: bool = field(default=False)

    def __and__(self, other: Union[Chalk, Chain]) -> Chain:
        """Compose the chain with another chain or a chalk instance.

        Args:
            other (Union[Chalk, Chain]):
                Another :class:`~.shortcuts.chain.Chain` or :class:`~.chalk.Chalk`
                instance to compose with the current chain.

        Returns:
            :class:`~.shortcuts.chain.Chain`:
                The newly updated chain.
        """

        if isinstance(other, Chalk):
            self._chalk = self._chalk & other
            return self

        self._chalk = self._chalk & other._chalk
        return self

    @overload
    def __add__(
        self, other: Union[Chalk, Chain]
    ) -> Chain:  # noqa: D105 # pragma: no cover
        ...

    @overload
    def __add__(self, other: str) -> str:  # noqa: D105 # pragma: no cover
        ...

    def __add__(self, other: Union[Chalk, Chain, str]) -> Union[Chain, str]:
        """Handle applying chain instances to things.

        Args:
            other (Union[Chalk, Chain, str]):
                Either a chalk instance, a chain instance, or a string.

        Returns:
            Union[Chain, str]:
                The updated chain or the applied string.
        """

        if isinstance(other, str):
            return self | other

        return self & other

    def __or__(self, value: str) -> str:
        """Style some given string with the current chain.

        Args:
            value (str):
                THe string to apply the current chain to.

        Returns:
            str:
                The newly styled string.
        """

        applied = self._chalk | value
        self._reset()

        return applied

    def __call__(self, value: str) -> str:
        """Handle applying a chain to a strings.

        Args:
            value (str):
                The string to apply the current chain to.

        Returns:
            str:
                The newly styled string.
        """

        return self | value

    def _reset(self):
        self._chalk = Chalk()
        self._background = False

    def _handle_style(self, style: Style) -> Chain:
        self._chalk.style.add(style)

        return self

    def _handle_color(self, color: Color_T) -> Chain:
        if self._background:
            self._chalk.background = color
        else:
            self._chalk.foreground = color

        return self

    def rgb(self, red: int, green: int, blue: int) -> Chain:
        """Add a truecolor chalk from an RGB tuple.

        Args:
            red (int):
                The intensity of red (0-255).
            green (int):
                The intensity of green (0-255).
            blue (int):
                The intensity of blue (0-255).

        Returns:
            :class:`~.chain.Chain`:
                The newly updated chain.
        """

        return self._handle_color(TrueColor(red, green, blue))

    def hex(self, color: str) -> Chain:
        """Add a truecolor chalk from a hex string.

        Args:
            color (str):
                The hex color string (#ffffff)

        Returns:
            :class:`~.chain.Chain`:
                The newly updated chain.
        """

        return self._handle_color(TrueColor.from_hex(color))

    @property
    def chalk(self) -> Chalk:
        """Extract the currently built chalk instance.

        .. important::
            Consuming this property will reset the current chain's styles.
            We are assuming that if you need the :class:`~.chalk.Chalk`, you have
            finished constructing it through the chaining syntax.

        Returns:
            ~.chalk.Chalk:
                The current chalk instance from the chained styles and colors.
        """

        chalk = self._chalk
        self._reset()

        return chalk

    @property
    def bg(self) -> Chain:
        """Following colors will be applied as the background color."""

        self._background = True
        return self

    @property
    def fg(self) -> Chain:
        """Following colors will be applied as the foreground color."""

        self._background = False
        return self

    @property
    def bold(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_style(Style.BOLD)

    @property
    def dim(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_style(Style.DIM)

    @property
    def italic(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_style(Style.ITALIC)

    @property
    def underline(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_style(Style.UNDERLINE)

    @property
    def slow_blink(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_style(Style.SLOW_BLINK)

    @property
    def rapid_blink(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_style(Style.RAPID_BLINK)

    @property
    def reversed(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_style(Style.REVERSED)

    @property
    def conceal(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_style(Style.CONCEAL)

    @property
    def strikethrough(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_style(Style.STRIKETHROUGH)

    @property
    def normal(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_style(Style.NORMAL)

    @property
    def black(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.BLACK)

    @property
    def red(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.RED)

    @property
    def green(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.GREEN)

    @property
    def yellow(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.YELLOW)

    @property
    def blue(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.BLUE)

    @property
    def magenta(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.MAGENTA)

    @property
    def cyan(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.CYAN)

    @property
    def white(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.WHITE)

    @property
    def bright_black(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.BRIGHT_BLACK)

    @property
    def bright_red(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.BRIGHT_RED)

    @property
    def bright_green(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.BRIGHT_GREEN)

    @property
    def bright_yellow(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.BRIGHT_YELLOW)

    @property
    def bright_blue(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.BRIGHT_BLUE)

    @property
    def bright_magenta(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.BRIGHT_MAGENTA)

    @property
    def bright_cyan(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.BRIGHT_CYAN)

    @property
    def bright_white(self) -> Chain:  # noqa: D102 # pragma: no cover
        return self._handle_color(Color.BRIGHT_WHITE)


chain = Chain()
