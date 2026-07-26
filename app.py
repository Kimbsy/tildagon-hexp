from app import App
from app_components import Menu, Notification, TextDialog, clear_background
from display import get_ctx
from typing import Literal
from .hexp_core import INIT_ENV
from .hexp_lang import evaluate, read_expr_string
from .palette import *
from .session import *
from .util import *

class HexpApp(App):
    def __init__(self):
        self.session = Session(INIT_ENV, read_expr_string, evaluate, get_ctx())
        print(self.session.evaluate("(def thingy 300)"))
        print(self.session.evaluate("(def whatsit 99)"))
        print(self.session.evaluate("(+ thingy whatsit)"))
    #     self.code = """
    #     (let (a 1)
    #       (draw-rect (list x 0) (list 30 30) '#ff00ff')
    #       (draw-rect (list 0 x) (list 30 30) '#00ffff'))
    #     """
    #     self.env = INIT_ENV | {'x': 0}
    #     self.bg_colour = DARK_BLUE


    # # @TODO: if we find an `update` function in the env, we should call it!
    # def update(self, delta):

    #     # @TODO: we need a better way of updating the state? maybe?

    #     self.env['x'] = self.env['x'] + 1
    #     if self.env['x'] > 120:
    #         self.env['x'] = -120

    # # @TODO: if we find a draw function in the env we should draw it!
    # def draw(self, ctx):
    #     clear_background(ctx)
    #     colour(ctx, self.bg_colour)
    #     ctx.rectangle(-120, -120, 240, 240).fill()

    #     evaluate(read_expr_string(self.code), self.env, ctx)

__app_export__ = HexpApp
