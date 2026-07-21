# tildagon-hexp

A programming language for the tildagon badge!

@TODO: make much better docs, explain what were doing, why and where we're at

## Setup and run on badge

install pipx
``` shell
sudo apt install pipx
```

install mpremote with pipx
``` shell
# in tildagon-hexp/ dir
pipx install mpremote
```
create metadata.json

connect badge

create folders

``` shell
mpremote mkdir apps
mpremote mkdir apps/hexp
```

copy app files over and connect to the badge

``` shell
./upload.sh
```

`ctrl-d` to reboot while connected

> [!CAUTION]
> Note to self: Update app version in `tildagon.toml` before we make a release!
