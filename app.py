from app import App
from app_components import Menu, Notification, TextDialog, clear_background
from typing import Literal
from .hexp_core import INIT_ENV
from .hexp_lang import evaluate, read_expr_string
from .palette import *
from .util import *

class HexpApp(App):
    def __init__(self):
        self.code = "(draw-rect (list x 0) (list 30 30) '#ff00ff')"
        self.env = INIT_ENV | {'x': 0}
        self.bg_colour = DARK_BLUE

    # @TODO: if we find an `update` function in the env, we should call it!
    def update(self, delta):

        # @TODO: we need a better way of updating the state? maybe?

        self.env['x'] = self.env['x'] + 1
        if self.env['x'] > 120:
            self.env['x'] = -120

    # @TODO: if we find a draw function in the env we should draw it!
    def draw(self, ctx):
        clear_background(ctx)
        colour(ctx, self.bg_colour)
        ctx.rectangle(-120, -120, 240, 240).fill()

        evaluate(read_expr_string(self.code), self.env, ctx)

__app_export__ = HexpApp
