from app import App
from app_components import Menu, Notification, TextDialog, clear_background
from typing import Literal
from .hexp_core import INIT_ENV
from .hexp_lang import evaluate, read_expr_string
from .palette import *
from .util import *

class HexpApp(App):
    def __init__(self):
        self.code = ""
        self.result = ""
        self.dialog = None
        self.displayed = False

    def _complete_handler(self):
        self.code = self.dialog.text
        self.result = str(evaluate(read_expr_string(self.code), INIT_ENV))
        self.dialog._cleanup()
        self.dialog = None

    def _cancel_handler(self):
        self.dialog._cleanup()
        self.dialog = None

    # @TODO: if we find an `update` function in the env, we should call it!
    def update(self, delta):
        if not self.displayed:
            self.displayed = True
            self.dialog = TextDialog(
                "Enter code plz:",
                self,
                masked=False,
                on_complete=self._complete_handler,
                on_cancel=self._cancel_handler)

    # @TODO: if we find a draw function in the env we should draw it!
    def draw(self, ctx):
        clear_background(ctx)
        colour(ctx, FOREST_GREEN)
        ctx.rectangle(-120, -120, 240, 240).fill()

        if self.result:
            ctx.save()
            ctx.text_align = ctx.CENTER
            colour(ctx, WHITE).move_to(0, -20).text(self.code)
            ctx.move_to(0, 20).text(self.result)
            ctx.restore()

        if self.dialog:
            self.dialog.draw(ctx)

__app_export__ = HexpApp
