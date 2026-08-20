# tildagon-hexp

A programming language for the Tildagon badge!

> What? what on Earth are you talking about?

A couple of things:
- I don't much care for Python
- I do much care for Lisps
- Implementing tiny languages is a fun coding problem, and a great learning opportunity

So I've written a new language called `Hexp` which runs on the badge (it's an interpreted language running in MicroPython inside the `Hexp IDE` badge app).

As far as I can tell it is the first full programming language written specifically for Tildagon OS :tada:

## The Hexp REPL

The simplest way to get writing Hexp is using the built-in REPL of the Hexp IDE app. Luanch the IDE app and select REPL from the main menu.

From here you can evaluate Hexp expressions in an interactive session.

```Clojure
;; numbers evaluate to themselves
42
=> 42

;; so do strings
'hello'
=> hello

;; invoke a function by wrapping it in parens with it's args
(+ 1 2)
=> 3

;; define a variable with `def`
(def foo 67)
=> 67

;; variables evaluate to their values
foo
=> 67
```

## Saving and loading programs

## Writing a Tildagon OS badge app in Hexp

Ok so this one is a bit of a stretch, but you _can_ _TECHNICALLY_ "write a "badge app" in hexp".

If you write a program which defines the `hexp-update` and `hexp-draw` functions, the Hexp IDE app will immediately start executing those functions in it's own `update` and `draw` functions.

So as soon as your program is evaluated Hexp will be able to draw to the screen and update it's own internal state every frame.

I don't think we'll be running Doom anytime soon, but a bouncing DVD logo? That's absolutely achievable.

Check out the `examples/*.hxp` programs (type it into the repl if you like!) for an example.

## Setup and run on badge for local development

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

copy example programs over

``` shell
mpremote mkdir apps/Kimbsy_tildagon_hexp/prog
mpremote cp examples/*.hxp :/apps/Kimbsy_tildagon_hexp/prog/
```

`ctrl-d` to reboot while connected

> [!CAUTION]
> Note to self: Update app version in `tildagon.toml` before we make a release!
