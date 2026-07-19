from app import App
from app_components import Menu, Notification, clear_background
from typing import Literal
from .hexp_core import INIT_ENV
from .hexp_lang import evaluate, read_expr_string
from .palette import *
from .util import *

# test evaluate
def tev(expr):
    print(evaluate(read_expr_string(expr), INIT_ENV))

class HexpApp(App):
    def __init__(self):
        self.foo = 42
        print(read_expr_string("42"))
        print(read_expr_string("'bar'"))
        print(read_expr_string("true"))
        v = read_expr_string("my_var")
        print(v)
        print(v.name)

        print("\n\n--------------")
        tev("42")
        tev("'blah'")
        tev('true')
        tev('my_var')
        tev('+')
        tev('(+ 11 23)')
        tev('(+ 4 (+ 40 40))')
        # tev('(list 42 33 11)')
        # tev('(quote (1 2 3))')
        

    def update(self, delta):
        self.foo = 42

    def draw(self, ctx):
        clear_background(ctx)
        colour(ctx, FOREST_GREEN)
        ctx.rectangle(-120, -120, 240, 240).fill()

__app_export__ = HexpApp
