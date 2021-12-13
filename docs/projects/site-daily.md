# Daily Data for Site

This allows to get the most daily data for a site based on a site ID from the idlist. The tool parses the daily output as an indented JSON and you can specify months since today as well as data type like wind/wave/temp.

![site_daily](https://user-images.githubusercontent.com/6677629/145728380-11b0acaf-8a9c-4c90-904a-675f8364a5f6.gif)

```
pyaqua site-daily -h
usage: pyaqua site-daily [-h] --sid SID [--months MONTHS] [--dtype DTYPE]

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --sid SID        Site ID

Optional named arguments:
  --months MONTHS  Total number of months from today
  --dtype DTYPE    Data type: wind/wave/temp
```
