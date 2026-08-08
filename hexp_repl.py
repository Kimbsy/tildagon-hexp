# A Repl component based on the TextDialog class

from app_components import TextDialog
from app_components.tokens import label_font_size
from .palette import *

THEMES = {
    "dark": {
        "bg": DARK_BLUE,
        "text": WHITE,
        "comment": GREY
    },
    "light": {
        "bg": WHITE,
        "text": BLACK,
        "comment": GREY
    }
}

# @TODO: remove character selection stuff entirely, it still prints in the console

class HexpRepl(TextDialog):
    def __init__(self, app, session, app_on_complete_cb, app_on_cancel_cb):
        super().__init__(
            "",
            app,
            on_complete=self._on_complete,
            on_cancel=self._on_cancel
        )
        self.app = app
        self.theme = THEMES["dark"]
        self.session = session
        self.app_on_complete_cb = app_on_complete_cb
        self.app_on_cancel_cb = app_on_cancel_cb

    def _on_complete(self):
        print("repl-complete")
        if not self.app.state == 'REPL':
            return
        expr = self.text
        res = self.session.evaluate(expr)
        self._cleanup()
        self.app_on_complete_cb()

    def _on_cancel(self):
        print("repl-cancel")
        if not self.app.state == 'REPL':
            return
        self._cleanup()
        self.app_on_cancel_cb()

    def draw_history_item(self, ctx, h, idx):
        expr, res = h
        y_off = (-2 * idx * label_font_size) - label_font_size
        colour(ctx, self.theme["comment"])
        ctx.move_to(-100, int(y_off)).text(">")
        ctx.move_to(-100, int(y_off) + int(label_font_size)).text(">>")
        colour(ctx, self.theme["text"])
        ctx.move_to(-70, int(y_off)).text(expr.replace('\n', ' '))
        ctx.move_to(-70, int(y_off) + int(label_font_size)).text(res)

    def draw_history(self, ctx):
        ctx.font_size = label_font_size
        ctx.text_align = ctx.LEFT
        ctx.text_baseline = ctx.BOTTOM
        for idx, h in  enumerate(list(reversed(self.session.history))[0:3]):
            self.draw_history_item(ctx, h, idx)

    def draw_input(self, ctx):
        current_input = self.text
        ctx.text_align = ctx.CENTER
        x_off = 0
        
        # if it's a long line, align RIGHT and follow the input cursor
        if len(current_input) > 13:
            ctx.text_align = ctx.RIGHT
            x_off = 70
            
        ctx.font_size = label_font_size
        ctx.text_baseline = ctx.TOP
        colour(ctx, self.theme["text"])
        ctx.move_to(x_off, 15).text(current_input)
        if ctx.a11y:
            ctx.a11y.add_alt(self, current_input + ":")

    def draw(self, ctx):
        ctx.save()
        colour(ctx, self.theme["bg"])
        ctx.rectangle(-120, -120, 240, 240).fill()

        self.draw_input(ctx)
        self.draw_history(ctx)
        if ctx.a11y:
            ctx.a11y.add_alt(self, "Buttons:")
            for i in range(6):
                if self._keys[i]:
                    self.speak_keys(ctx, self._keys[i])

        ctx.restore()
