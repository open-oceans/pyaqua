#  Argofloat data for Site

This tool uses the argofloats CLI to get coincident argofloats data per site. It uses the start and end date specified and a search radius around the site latitude and longitude. Default search radius is a 1000 kilometers and the exports are in a CSV format with format **argofloats_profileID**

![pyaqua_site-argo](https://user-images.githubusercontent.com/6677629/152304351-0375871b-e80e-46f5-a74b-56c76f094c9a.gif)

```
pyaqua site-argo -h
usage: pyaqua site-argo [-h] --sid SID --start START --end END --fpath FPATH [--radius RADIUS]

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --sid SID        Site ID
  --start START    Start date in format YYYY-MM-DD
  --end END        End date in format YYYY-MM-DD
  --fpath FPATH    Folder path for export

Optional named arguments:
  --radius RADIUS  Search radius in kilometers
```
