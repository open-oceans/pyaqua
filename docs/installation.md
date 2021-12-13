# General Installation

This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

**pyaqua only support Python v3.7 or higher**

To install **pyaqua: Simple CLI for Aqualink API** you can install using two methods.

```pip install pyaqua```

or you can also try

```
git clone https://github.com/samapriya/pyaqua.git
cd pyaqua
python setup.py install
```
For Linux use sudo or try ```pip install pyaqua --user```.

I recommend installation within a virtual environment. Find more information on [creating virtual environments here](https://docs.python.org/3/library/venv.html).

## Getting started

As usual, to print help:

```
usage: pyaqua [-h] {site-list,site-live,site-daily,site-timeseries} ...

Simple CLI for Aqualink API

positional arguments:
  {site-list,site-live,site-daily,site-timeseries}
    site-list           Print lists of Site Name and ID with spotters
    site-live           Get most recent/live info from a site
    site-daily          Print daily data info for a site
    site-timeseries     Print daily data info for a site

optional arguments:
  -h, --help            show this help message and exit
```

To obtain help for specific functionality, simply call it with _help_ switch, e.g.: `pyaqua site-live -h`. If you didn't install pyaqua, then you can run it just by going to *pyaqua* directory and running `python pyaqua.py [arguments go here]`
