# pyspotter: Simple CLI for SofarOcean API

[![Twitter URL](https://img.shields.io/twitter/follow/samapriyaroy?style=social)](https://twitter.com/intent/follow?screen_name=samapriyaroy)
![](https://tokei.rs/b1/github/samapriya/pyspotter?category=code)
![](https://tokei.rs/b1/github/samapriya/pyspotter?category=files)
[![CI pyspotter](https://github.com/samapriya/pyspotter/actions/workflows/package_ci.yml/badge.svg)](https://github.com/samapriya/pyspotter/actions/workflows/package_ci.yml)
![PyPI - License](https://img.shields.io/pypi/l/pyspotter)
[![Downloads](https://pepy.tech/badge/pyspotter)](https://pepy.tech/project/pyspotter)
![PyPI](https://img.shields.io/pypi/v/pyspotter)


## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [pyspotter Simple CLI for Sofarocean API](#pyspotter-simple-cli-for-sofarocean-api)
    * [pyspotter auth](#pyspotter-auth)
    * [pyspotter reset](#pyspotter-reset)
    * [pyspotter devlist](#pyspotter-devlist)
    * [pyspotter spotcheck](#pyspotter-spotcheck)
    * [pyspotter spotdata](#pyspotter-spotdata)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

**pyspotter only support Python v3.4 or higher**

To install **pyspotter: Simple CLI for SofarOcean API** you can install using two methods.

```pip install pyspotter```

or you can also try

```
git clone https://github.com/samapriya/pyspotter.git
cd pyspotter
python setup.py install
```
For Linux use sudo or try ```pip install pyspotter --user```.

I recommend installation within a virtual environment. Find more information on [creating virtual environments here](https://docs.python.org/3/library/venv.html).

## Getting started

As usual, to print help:

```
pyspotter -h
usage: pyspotter [-h] {auth,reset,devlist,spot-check,spot-data} ...

Simple CLI for Sofarocean API

positional arguments:
  {auth,reset,devlist,spot-check,spot-data}
    auth                Authenticates and saves your API token
    reset               Regenerates your API token
    devlist             Print lists of devices available under your account
    spot-check          Spot check a Spotter location and time
    spot-data           Export Spotter Data based on Spotter ID & grouped by date

optional arguments:
  -h, --help            show this help message and exit
```

To obtain help for specific functionality, simply call it with _help_ switch, e.g.: `pyspotter spot-check -h`. If you didn't install pyspotter, then you can run it just by going to *pyspotter* directory and running `python pyspotter.py [arguments go here]`

## pyspotter Simple CLI for Sofarocean API
The tool is designed to interact with the SofarOcean API, for now this is focused only on the spotter endpoints.

### pyspotter auth
This allows you to save your authentication token, this is then used for authentication for requests. This uses your email and your password to fetch the token.

``` pyspotter auth```

### pyspotter reset
For some reason if you need to reset your token , this will allow you to use your current authentication to reset and fetch your new token. This requires no user input

```pyspotter reset```

### pyspotter devlist
This will simply print the names of all devices to which you have access, instead of trying to remember the list. This tool requires no user input.

```
usage: pyspotter devlist [-h]

optional arguments:
  -h, --help  show this help message and exit

```

usage is simply

```pyspotter devlist```


### pyspotter spotcheck
This tool is built to fetch simply the latest information from the spotter including battery, humidity, power and lat long. Since these spotter can move across multiple time zones, it uses the lat long to estimate the time zone and converts the UTC time to local time for the spotter.

```
pyspotter spot-check -h

usage: pyspotter spot-check [-h] --sid SID

optional arguments:
  -h, --help  show this help message and exit

Required named arguments.:
  --sid SID   Spotter ID
```

Example usage would be

```
pyspotter spot-check --sid 0320
```


### pyspotter spotdata
This tool was designed to get the datasets out of the spotter. It seems that API currently limited temporal data, and the best way to group seemed to be using dates. This script uses the result JSON objects, and adds a date field from the timestamp to make the grouping easy, since timestamps are unique. This then writes these CSV file with column headers and can export both wind and wave data as needed.

```
usage: pyspotter spot-data [-h] --sid SID --dtype DTYPE --folder FOLDER

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --sid SID        Spotter ID
  --dtype DTYPE    Data type: wind/wave/sst
  --folder FOLDER  Folder to export CSV data

```

Sample setup would be

```
pyspotter spot-data --sid 1234 --dtype wave --folder "full path to folder"
```


## Changelog

#### v0.0.5
- added sea surface temperature parsing for spot data
- minor general improvements

#### v0.0.4
- added spot id to spot data export and metadata
- gracefully handles missing data and better error handling
- general improvements

#### v0.0.3
- added spot check tool to get latest info about spotter
- spot data now exports CSV after grouping by date
- general improvements

#### v0.0.2
- added time zone parser from spotter lat long
- now prints UTC and local time for spotter
- pretty prints output
