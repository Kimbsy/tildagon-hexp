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
        self.bg_colour = DARK_BLUE
        self.session = Session(INIT_ENV, read_expr_string, evaluate, get_ctx())
        self.session.evaluate("(def x 0)")
        self.session.evaluate("(def inc (fn (n) (+ n 1)))")
        self.session.evaluate("""
        (def hexp-update
          (fn ()
            (if (< x 120)
               (def x (inc x))
               (def x (- 0 120)))))""")
        self.session.evaluate("""
        (def hexp-draw
          (fn ()
            (background '#002b36')
            (draw-rect (list x 0) (list 30 30) '#ff00ff')))""")

    def update(self, delta):
        self.session.update()

    def draw(self, ctx):
        self.session.draw()

    # @TODO: we need to exit the app when we hit the back button, I guess we _could_ try and write new version of each of the button handling methods an app can override?

__app_export__ = HexpApp
