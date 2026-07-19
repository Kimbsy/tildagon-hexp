from app import App
from app_components import Menu, Notification, clear_background
from typing import Literal
from .hexp_core import INIT_ENV
from .hexp_lang import evaluate, read_expr_string
from .palette import *
from .util import *

# test evaluate
def tev(expr):
    print("\n\n" + expr + ":")
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
        print("\n\n---------------")
        tev('(+ 11 23)')
        tev('(+ 100 my_var)')
        tev('(+ 1 2 3 4 5 6 7 8)')
        tev('(+ 4 (+ 40 40))')
        print("\n\n---------------")
        tev('(if true 1 2)')
        tev('(if false 1 2)')
        tev('(if (= 5 6) 1 2)')
        tev('(if (= 5 5) 1 2)')
        tev('(if (= 5) 1 2)')
        tev('(if (= 5 5 5 5) 1 2)')
        tev('(if (= 5 5 5 6) 1 2)')
        print("\n\n---------------")
        tev('(quote 100)')
        tev('(quote (1 2 3))')
        tev('(quote (1 (2 3 ())))')
        tev('(quote (quote (1 2 3)))')
        print("\n\n---------------")
        tev('(fn (a) a)')
        tev('((fn (a) a) 400)')
        tev('((fn () 32))')
        tev('((fn (a b) (+ a a b)) 200 20)')
        
        # tev('(list 1 2 3)')
        

    def update(self, delta):
        self.foo = 42
        # @TODO: if we find an `update` function in the env, we should call it!

    def draw(self, ctx):
        clear_background(ctx)
        colour(ctx, FOREST_GREEN)
        ctx.rectangle(-120, -120, 240, 240).fill()
        # @TODO: if we find a draw function in the env we should draw it!

__app_export__ = HexpApp
