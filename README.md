# tildagon-hexp

A programming language for the Tildagon badge!

> What? what on Earth are you talking about?

A couple of things:
- I don't much care for Python
- I do much care for Lisps
- Implementing tiny languages is a fun coding problem, and a great learning opportunity

Also you gave us a gosh-darned _keyboard_ for the thing, what was I supposed to do? _Not write a programming language_???

So I've written a language called `Hexp` which runs on the badge (it's an interpreted language running in MicroPython inside the `HexpLang` badge app).

As far as I can tell it is the first full programming language written specifically for Tildagon OS :tada:

## The Hexp REPL

The simplest way to get writing Hexp is using the built-in REPL of the HexpLang app. Launch the app and select REPL from the main menu.

From here you can evaluate Hexp expressions in an interactive session.

```Clojure
;; comments start with ;;

;; numbers evaluate to themselves
42
=> 42

;; so do strings (single quotes)
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

;; bind lexically-scoped variables with `let`
(let (a 1
      b 2
      c (+ a b))
  (list a b c))
=> [1, 2, 3]

;; create a function with `fn`
(def inc (fn (n) (+ n 1)))
=> <closure ... >
(inc 68)
=> 69
```

## Saving and loading programs

After evaluating code in the REPL you can exit to the main menu with the `F` button (your REPL state is safe until a reboot), then select `Save program` to write the session to the Tildagon's filesystem.

> [!NOTE]
> Currently a random number will be used for the filename, sorry

From the main menu you can also select `Load program` to load a previously saved program into the REPL.

Saving again will contain the whole history of the session (including any loaded programs).

You can also sideload a program onto the Tildagon by copying it directly into the pogram store directory:

``` shell
mpremote mkdir apps/Kimbsy_tildagon_hexp/prog
mpremote cp my-program.hxp :/apps/Kimbsy_tildagon_hexp/prog/
```

Take a look at the [example programs](/examples).

> [!NOTE]
> Make sure your program file ends with the `.hxp` Hexp file extension so it is recognised by the Hexp program loader

## Writing programs in Hexp

When writing a Hexp program, make sure that each top-level expression is separated by an empty line, also make sure that there are no empty lines inside an expression (comment lines are ok though). This is basically because I wrote a pretty crappy program loader :sweat_smile:

As a general tip, try and keep functions small and reuse them, partly because this is good Lisp style, but also because the recursion used by special forms like `fn`, `let`, `if` eventually exhaust the MicroPython call stack.

> [!IMPORTANT]
> Did you know that the MicroPython recursion limit is 17? _SEVENTEEN_??? S.E.V.E.N.T.E.E.N. Almost all of the complexity in writing Hexp is in order to get around this.

The full list of functions available to you in Hexp (not including the ones you write yourself!) is declared in `INIT_ENV` in [hexp_core.py](hexp_core.py)

## Writing a Tildagon OS badge app in Hexp

Ok so this one is a bit of a stretch, but you _can_ _TECHNICALLY_ "write a "badge app" in hexp".

If you write a program which defines the `hexp-update` and `hexp-draw` functions, the Hexp IDE app will immediately start executing those functions in it's own `update` and `draw` functions.

So as soon as your program is evaluated Hexp will be able to draw to the screen and update it's own internal state every frame.

Currently there are functions for drawing/filling triangles/rectangles and drawing text.

I don't think we'll be running Doom anytime soon, but a bouncing DVD logo? That's absolutely achievable.

Check out the following example programs:

- draw-text.hxp : draws text to the screen
- draw-tri.hxp : draws triangles to the screen
- updating state : draws squares to the screen, updates their positions each frame
- dvd-demo.hxp : I did it! the Bouncing DVD logo of your 90s nostaglia dreams is here on the badge, running entirely in Hexp.

## Contributing to Hexp

If you have any idea for ways in which Hexp can be improved (if such a thing is even _possible_) issues and pull requests on this repo are more than welcome :heart:

If you run into any of the _completely incomprehensible_ errors that Hexp throws when something goes wrong (this happens a lot) feel free to raise an issue with your error and the code that threw it, I'll do my best to help out. For this reason it's very helpful to have a laptop connected to you Tildagon while doing intense Hexp development, and connecting with:

``` shell
mpremote connect auto
```

That way you can copy from the terminal which will show the current input as well as the error stack trace.

Example programs (even trivial ones) are more than welcome.

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
