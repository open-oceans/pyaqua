# Daily Data for Site

This allows to get the most daily data for a site based on a site ID from the idlist. The tool parses the daily output as an indented JSON and you can specify months since today as well as data type like wind/wave/temp. It also supports export as CSV and custom date ranges since v0.1.0

![site_daily](https://user-images.githubusercontent.com/6677629/192980559-e58014a3-26ab-4519-a73e-9a9bdfb5ae69.gif)

```
pyaqua site-daily -h
usage: pyaqua site-daily [-h] --sid SID [--months MONTHS] [--start START] [--end END] [--dtype DTYPE] [--fpath FPATH]

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --sid SID        Site ID

Optional named arguments:
  --months MONTHS  Total number of months in the past from today (default=1)
  --start START    Start date for daily data in format YYYY-MM-DD
  --end END        End date for daily data in format YYYY-MM-DD
  --dtype DTYPE    Data type: wind/wave/temp
  --fpath FPATH    Full path to folder to export daily data as CSV
```
