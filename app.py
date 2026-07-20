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
        self.code = ""

    def update(self, delta):
        self.foo = 42
        # @TODO: if we find an `update` function in the env, we should call it!

    def draw(self, ctx):
        clear_background(ctx)
        colour(ctx, FOREST_GREEN)
        ctx.rectangle(-120, -120, 240, 240).fill()
        # @TODO: if we find a draw function in the env we should draw it!

__app_export__ = HexpApp
