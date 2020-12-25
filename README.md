![Chalky](https://github.com/stephen-bunn/chalky/raw/master/docs/source/_static/assets/img/Chalky.png)

[![Supported Versions](https://img.shields.io/pypi/pyversions/chalky.svg)](https://pypi.org/project/chalky/)
[![Test Status](https://github.com/stephen-bunn/chalky/workflows/Test%20Package/badge.svg)](https://github.com/stephen-bunn/chalky)
[![Documentation Status](https://readthedocs.org/projects/chalky/badge/?version=latest)](https://chalky.readthedocs.io/)
[![Codecov](https://codecov.io/gh/stephen-bunn/chalky/branch/master/graph/badge.svg?token=G3KRpTeg5J)](https://codecov.io/gh/stephen-bunn/chalky)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

> Simple ANSI terminal text coloring

Yet another terminal text coloring library…

Why? Because, I like certain things and I hate certain things about the currently
available solutions.
This here is my attempt to build an interface for simply applying ANSI escape sequences
to strings that I enjoy and can update at my own free will.
That is it, there is nothing new or interesting that this packages adds.
Thanks 🎉

For more interesting details, please visit the
[documentation](https://chalky.readthedocs.io/).

## Style Composition

```python
from chalky import sty, fg

my_style = sty.bold & fg.red
print(my_style | "This is red on black")
print(my_style.reverse | "This is black on red")
```

![Basic Colors](https://github.com/stephen-bunn/chalky/raw/master/docs/source/_static/assets/img/basic.png)

## Style Chaining

```python
from chalky import chain

print(chain.bold.green | "I'm bold green text")
print(chain.white.bg.red.italic | "I'm italic white text on a red background")
```

![Style Colors](https://github.com/stephen-bunn/chalky/raw/master/docs/source/_static/assets/img/chaining.png)

## Truecolor

```python
from chalky import rgb, sty, hex

print(rgb(23, 255, 122) & sty.italic | "Truecolor as well")
print(sty.bold & hex("#ff02ff") | "More and more colors")
```

![True Colors](https://github.com/stephen-bunn/chalky/raw/master/docs/source/_static/assets/img/truecolor.png)

## Disable Colors

```python
from chalky import configure, fg

print(fg.red | "I am red text")
configure(disable=True)
print(fg.red | "I am NOT red text")
```

![Configure](https://github.com/stephen-bunn/chalky/raw/master/docs/source/_static/assets/img/configure.png)
