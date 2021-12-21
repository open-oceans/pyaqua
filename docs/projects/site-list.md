# Site list and ID

This allows you to get existing sites with spotters attached and print Site Name and ID. These could be in different status of application including maintenance, deployed, lost, shipped and so on. The tool also applies a fuzzy search and allows you to look for a specific site to get site id. You can now filter using status as well so status types like maintenance, deployed, shipped or lost

![site-list](https://user-images.githubusercontent.com/6677629/146982428-a0263324-c6fb-4418-b20e-3b121986a8a4.gif)

```
pyaqua site-list -h
usage: pyaqua site-list [-h] [--name NAME] [--status STATUS]

optional arguments:
  -h, --help       show this help message and exit

Optional named arguments:
  --name NAME      Pass site name
  --status STATUS  Site status from maintenance|deployed|shipped|lost
```
