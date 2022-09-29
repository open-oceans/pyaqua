# Time Series data for Site

This allows to get the most daily data for a site based on a site ID from the idlist. The tool exports the time series data for both NOAA and spotter datasets as CSV to a given folder. It attaches the site_id to the CSV filename **spotter_dhw_siteid** for example **spotter_dhw_1113**. It Now supports custom date ranges since v0.1.0

![site_timeseries](https://user-images.githubusercontent.com/6677629/192980552-56bc916a-6643-4d74-8523-232baaf28bbd.gif)

```
pyaqua site-timeseries -h
usage: pyaqua site-timeseries [-h] --sid SID --fpath FPATH [--months MONTHS] [--start START] [--end END] [--dtype DTYPE]

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --sid SID        Site ID
  --fpath FPATH    Folder path for export

Optional named arguments:
  --months MONTHS  Total number of months in the past from today (default=3)
  --start START    Start date for daily data in format YYYY-MM-DD
  --end END        End date for daily data in format YYYY-MM-DD
  --dtype DTYPE    Data type: wind/wave/temp/sat_temp/alert/anomaly/dhw
```
