# Site list and ID

This allows you to get existing sites with spotters or hobo sensors and print Site Name and ID. These could be in different status of application including maintenance, deployed, lost, shipped and so on. The tool also applies a fuzzy search and allows you to look for a specific site to get site id. You can now filter using status as well so status types like maintenance, deployed, shipped or lost

![site_list](https://user-images.githubusercontent.com/6677629/168004255-968e5320-c53d-460c-b230-3a6dc75dfa6e.gif)


```
pyaqua site-list -h
usage: pyaqua site-list [-h] [--name NAME] [--status STATUS]

optional arguments:
  -h, --help       show this help message and exit

Optional named arguments:
  --name NAME      Pass site name
  --status STATUS  Site status from maintenance|deployed|shipped|lost
```
