# Site information

The site info tool uses the site ID to get detailed information about the setup, location, time zone, status information to name a few. Historical means are dropped along with admin data for ease of parsing and since they do not add a large amount of value for general purpose users directly. The user does have the option to get to the complete admin or historical data if needed

![site-info](https://user-images.githubusercontent.com/6677629/145769759-9c09dab3-4b45-472a-a62c-2d327ea2255c.gif)

```
pyaqua site-info -h
usage: pyaqua site-info [-h] --sid SID [--extra EXTRA]

optional arguments:
  -h, --help     show this help message and exit

Required named arguments.:
  --sid SID      Site ID

Optional named arguments:
  --extra EXTRA  extra info keywords : historical/admins
```
