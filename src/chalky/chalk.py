# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the base chalk class that is used to group some style and colors."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Set, Union, overload

from .color import Color_T
from .constants import is_disabled
from .interface import get_interface
from .style import Style


@dataclass
class Chalk:
    """Describes the style and color to use for styling some printable text.

    Chalk can be composed using ``&`` and can be applied to strings with ``|``.
    You can create your own instance of chalk by setting your desired
    :class:`~style.Style` and :class:`~color.Color` when creating a new instance.

    Examples:
        Creating custom instances of chalk looks like the following:

        >>> my_chalk = Chalk(
        ...     style={Style.BOLD, Style.UNDERLINE},
        ...     foreground=Color.RED,
        ... )

        Composing two chalk instances can be done through either using ``&`` or ``+``:

        >>> bold_chalk = Chalk(style={Style.BOLD})
        >>> error_chalk = bold_chalk & Chalk(foreground=Color.RED)

        Using chalk instances to style strings can be done using either ``|`` or ``+``:

        >>> error_chalk | "Hello, World!"
        Hello, World!


    .. important::

        When composing two chalk instances together, the chalk *being* applied to the
        base chalk instance will override the foreground and background colors.
        This means that if you apply a new chalk with a different foreground color it
        will override the starting foreground color:

        >>> red = Chalk(foreground=Color.RED)
        >>> blue = Chalk(foreground=Color.BLUE)
        >>> assert blue == (red & blue)
    """

    style: Set[Style] = field(default_factory=set)
    foreground: Optional[Color_T] = field(default=None)
    background: Optional[Color_T] = field(default=None)

    def __and__(self, other: Chalk) -> Chalk:
        """Create a new chalk instance from the composition of two chalk.

        Args:
            other (:class:`~Chalk`):
                Another chalk to combine with the current chalk.

        Returns:
            :class:`~Chalk`:
                The newly created chalk instance.
        """

        return Chalk(
            style=self.style.union(other.style),
            foreground=other.foreground or self.foreground,
            background=other.background or self.background,
        )

    def __or__(self, value: Any) -> str:
        """Style some given string with the current chalk instance.

        .. tip::
            If a non-string value is provided, we will attempt to get the most
            appropriate string from the value by simply calling ``str(value)``.
            So if you are passing in an object, make sure to use an appropriate
            ``__str__`` or ``__repr__``.

        Args:
            value (~typing.Any):
                The value to apply the current chalk styles to.

        Returns:
            str:
                The newly styled string.
        """

        if is_disabled():
            return str(value)

        interface = get_interface()
        return interface.apply(
            value=str(value),
            style=self.style,
            background=self.background,
            foreground=self.foreground,
        )

    @overload
    def __add__(self, other: Chalk) -> Chalk:  # pragma: no cover
        """Handle applying chalk to other chalk instances.

        Args:
            other (:class:`~Chalk`):
                The chalk instance to apply to the current instance.

        Returns:
            :class:`~Chalk`:
                They newly created chalk instance.
        """

        ...

    @overload
    def __add__(self, other: str) -> str:  # pragma: no cover
        """Handle applying chalk to strings.

        Args:
            other (str):
                The string to style with the current chalk instance.

        Returns:
            str:
                They newly styled string.
        """

        ...

    def __add__(self, other: Union[Chalk, str]) -> Union[Chalk, str]:
        """Handle applying chalk instances to things.

        Args:
            other (Union[Chalk, str]):
                Either another chalk instance or a string.

        Returns:
            Union[Chalk, str]:
                The combined chalk instances or a styled string.
        """

        if isinstance(other, Chalk):
            return self & other

        return self | other

    def __call__(self, value: str) -> str:
        """Handle applying chalk instances to strings.

        Args:
            value (str):
                The string to apply the current styles to.

        Returns:
            str:
                The newly styled string.
        """

        return self | value

    @property
    def reverse(self) -> Chalk:
        """Color reverse of the current chalk instance.

        Returns:
            :class:`~Chalk`:
                The revsered chalk instance
        """

        return self & Chalk(style={Style.REVERSED})
