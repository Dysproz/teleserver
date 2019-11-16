# teleserver CLI

This package is CLI tool to teleserver project - a remote way to control your office TV.

Project's page:
[teleserver](https://github.com/Dysproz/teleserver)

## Idea

This CLI allows user to send API requests without need of providing service principal token to request.

## Usage

First, install this package with pip
```
pip install teleserver
```

In order to execute any command, please log in first:
```
teleserver log in --username <username to GUI> --server <IP of the teleserver>
```

You'll be prompted to enter password and afterwards you're logged in!

Once logged in, feel free to use API commands.

In order to log out execute:
```
teleserver log out
```

## Additional Features

### Server Lookup
Sometimes it's hard to find teleserver's IP.
It's possible to scan specific network, networks attached to specific interface or all networks in the system.
With `teleserver log lookup_server` command you can find IP address to your teleserver.
Possible flags:
* `--network` - Networks that should be searched for teleserver
* `--interface` - Name of the interface to search for networks to lookup.

This feature works only for IPv4 addreses.
