.. _getting-started:

===============
Getting Started
===============

| **Welcome to Chalky!**
| This page should hopefully provide you with enough information to get you started using Chalky.

Installation and Setup
======================

Installing the package should be super duper simple as we utilize Python's setuptools.

.. code-block:: bash

   $ poetry add chalky
   $ # or if you're old school...
   $ pip install chalky

Or you can build and install the package from the git repo.

.. code-block:: bash

   $ git clone https://github.com/stephen-bunn/chalky.git
   $ cd ./chalky
   $ python setup.py install


Usage
=====

Now with Chalky installed we can start applying some styles to text.
Styles and colors are applied to text through a single :class:`~chalky.chalk.Chalk`
instance that contains the desired format for styling a string.
This instance is reusable and does not require the user to manually define when reset
escape sequences need to be sent.

Creating Chalk
--------------

The :class:`~chalky.chalk.Chalk` class is simply a container storing the basic styles
and colors that can be applied to a string.
The stored rules try as best as possible to be agnostic to the :mod:`~chalky.interfaces`
the styles are going to be built with.

Chalk instances can contain:

* A set of :class:`~chalky.style.Style`
* A foreground color (:class:`~chalky.color.Color` or :class:`~chalky.color.TrueColor`)
* A background color (:class:`~chalky.color.Color` or :class:`~chalky.color.TrueColor`)

Constructing instances is pretty straightforward:

.. code-block:: python
   :linenos:

   from chalky import Chalk
   from chalky.style import Style
   from chalky.color import Color

   my_chalk = Chalk(
      styles={Style.BOLD, Style.ITALIC},
      foreground=Color.GREEN,
      background=Color.WHITE
   )


Applying Chalk to Strings
-------------------------

Now that you have a :class:`~chalky.chalk.Chalk` instance to work with, you can apply it
to a string using either the ``|`` or ``+`` operators.
Or you can simply call the chalk instance with the desired string.

.. code-block:: python

   print(my_chalk | "Hello, World!")
   print(my_chalk + "Hello, World!")
   print(my_chalk("Hello, World!"))

When applying the chalk instance to a string, it will build the appropriate ANSI escape
sequences to style the string and automatically add the reset sequence to the end of the
string.


Composing Chalk
---------------

These :class:`~chalky.chalk.Chalk` instances can be composed together using the
``&`` or ``+`` operators.

.. code-block:: python
   :linenos:

   from chalky import Chalk
   from chalky.style import Style
   from chalky.color import Color

   my_chalk = Chalk(style={Style.BOLD}) & Chalk(foreground=Color.RED)
   my_chalk = Chalk(style={Style.BOLD}) + Chalk(foreground=Color.RED)

The styles provided in the instance **being** applied will override any existing styles
on the starting instance.

.. code-block:: python
   :linenos:

   my_chalk = Chalk(foreground=Color.RED) & Chalk(foreground=Color.BLUE)
   assert my_chalk.foreground == Color.BLUE


Chaining Chalk
--------------

Chaining together multiple styles and colors is another typical interface that people
like to use for text coloring.
We provide a :class:`~.chain.Chain` class that produces a :class:`~.chalk.Chalk` for
quick and easy production:

.. code-block:: python
   :linenos:

   from chalky import chain

   print(chain.green.bold | "I'm bold green text")
   print(chain.italic.white.bg.blue | "I'm italic white text on blue background")


Using :class:`~.chain.Chain` classes should be pretty similar to how you use
:class:`~.chalk.Chalk` instances.
You can compose them with other chains or chalks and apply them to strings just like
chalk instances.
They ultimately just provide a different interface for constructing the chalk instance
and quickly consuming it.

Chalk Shortcuts
---------------

Since it can be pretty darn tedious to create instances of :class:`~chalky.chalk.Chalk`
all the time, I threw in some pre-initialized chalk in the :mod:`~chalky.shortcuts`
module.

From this module we export :mod:`~chalky.shortcuts.fg` (foreground),
:mod:`~chalky.shortcuts.bg` (background), and :mod:`~chalky.shortcuts.sty` (style)
namespaces to make it easy and quick to compose custom chalk instances:

.. code-block:: python
   :linenos:

   from chalky import fg, bg, sty

   debug = sty.dim & fg.white
   success = fg.green & sty.bold
   error = fg.red & sty.bold
   critical = bg.red & fg.white


   print(debug | "This is a DEBUG message")
   print(success | "This is a SUCCESS message")
   print(error | "This is a ERROR message")
   print(critical | "This is a CRITICAL message")


You can quickly produce truecolor's as well (if your terminal supports them) by using
the :func:`~chalky.shortcuts.hex` or :func:`~chalky.shortcuts.rgb` functions to quickly
produce :class:`~chalky.color.TrueColor` instances:

.. code-block:: python
   :linenos:

   from chalky import hex, rgb

   custom_rgb = rgb(102, 102, 255) & sty.underline
   custom_hex = hex("#90ff9c", background=True) & fg.black & sty.bold

   print(custom_rgb | "Potential link text")
   print(custom_hex | "Black on green text")
