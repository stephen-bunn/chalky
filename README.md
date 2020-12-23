# Chalky

[![Supported Versions](https://img.shields.io/pypi/pyversions/chalky.svg)](https://pypi.org/project/chalky/)
[![Test Status](https://github.com/stephen-bunn/chalky/workflows/Test%20Package/badge.svg)](https://github.com/stephen-bunn/chalky)
[![Documentation Status](https://readthedocs.org/projects/chalky/badge/?version=latest)](https://chalky.readthedocs.io/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

> Simple ANSI terminal text coloring

```python
from chalky import sty, fg

my_style = sty.bold & fg.red
print(my_style | "This is red on black")
print(my_style.reverse | "This is black on red")
```

![Basic Colors](docs/source/_static/assets/img/basic.png)

```python
from chalky import rgb, sty, hex

print(rgb(23, 255, 122) & sty.italic | "Truecolor as well")
print(sty.bold & hex("#ff02ff") | "More and more colors")
```

![True Colors](docs/source/_static/assets/img/truecolor.png)
