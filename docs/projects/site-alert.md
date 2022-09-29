# Site alert for sites

The site alert tool parses data from each device type or all sites keeping in consideration the temperature alert level data. You can now filter by device type spotters/hobo loggers.

![site_alert](https://user-images.githubusercontent.com/6677629/192980561-b8d69577-e434-4011-8716-368a21c0824d.gif)

```
pyaqua site-alert -h
usage: pyaqua site-alert [-h] [--level {0,1,2,3,4}] [--device DEVICE]

optional arguments:
  -h, --help           show this help message and exit

Optional named arguments:
  --level {0,1,2,3,4}  Level 0-4 no-alert|watch|warning|Level-1|Level-2
  --device DEVICE      spotter|hobo
```
