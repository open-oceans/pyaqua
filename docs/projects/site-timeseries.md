# Time Series data for Site

This allows to get the most daily data for a site based on a site ID from the idlist. The tool exports the time series data for both NOAA and spotter datasets as CSV to a given folder. It attaches the site_id to the CSV filename **spotter_dhw_siteid** for example **spotter_dhw_1113**

![site_timeseries](https://user-images.githubusercontent.com/6677629/145728547-c724f911-4301-4887-a9e8-dbbce4b28174.gif)

```
pyaqua site-timeseries -h
usage: pyaqua site-timeseries [-h] --sid SID --fpath FPATH [--months MONTHS]
                              [--dtype DTYPE]

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --sid SID        Site ID
  --fpath FPATH    Folder path for export

Optional named arguments:
  --months MONTHS  Total number of months from today
  --dtype DTYPE    Data type: wind/wave/temp/sat_temp/alert/anomaly/dhw
```
