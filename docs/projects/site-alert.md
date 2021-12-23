# Site alert for sites

The site alert tool parses data from the [heat stress collection page of aqualink](https://aqualink.org/collections/heat-stress). Since the tool is focused on spotter only sites it only picks those sites that have active alerts and have spotters.

![site-alert](https://user-images.githubusercontent.com/6677629/147210423-1048b0d3-d53e-4338-822c-e27df865a343.gif)

```
pyaqua site-alert -h
usage: pyaqua site-alert [-h] [--level {0,1,2,3,4}]

optional arguments:
  -h, --help           show this help message and exit

Optional named arguments:
  --level {0,1,2,3,4}  Level 0-4 no-alert|watch|warning|Level-1|Level-2
```
