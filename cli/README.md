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
