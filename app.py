from app import App
from app_components import Menu, Notification, TextDialog, clear_background
from display import get_ctx
from typing import Literal
from .hexp_core import INIT_ENV
from .hexp_lang import evaluate, read_expr_string
from .hexp_repl import HexpRepl
from .palette import *
from .session import *
from .util import *

MAIN_MENU = "Main Menu"
REPL = "REPL"
LOAD_PROGRAM = "Load program"
SAVE_PROGRAM = "Save program"

main_menu_options = [
    REPL,
    LOAD_PROGRAM,
    SAVE_PROGRAM
]

class HexpApp(App):
    def __init__(self):
        super().__init__()
        self.session = Session(
            INIT_ENV,
            read_expr_string,
            evaluate,
            self.session_error_handler,
            get_ctx())
        self.main_menu = Menu(
            self,
            main_menu_options,
            select_handler = self.main_menu_select_handler,
            back_handler = self.main_menu_back_handler
        )
        self.menu = self.main_menu
        self.notification = None
        self.state = MAIN_MENU
        # for some reason we don't seem to be able to create a TextDialog in the init function? it displays but is frozen?
        self.repl = None

    def _init_repl(self):
        self.repl = HexpRepl(
            self,
            self.session,
            self.repl_complete_callback,
            self.repl_cancel_callback
        )

    def session_error_handler(self, e):
        self.notification = Notification(repr(e))

    def main_menu_select_handler(self, item, idx):
        if self.state == MAIN_MENU:
            self.state = REPL

    def main_menu_back_handler(self):
        if self.state != MAIN_MENU:
            self.state = MAIN_MENU
        else:
            self.minimise()

    def repl_complete_callback(self):
        self.repl = None

    def repl_cancel_callback(self):
        self.repl = None
        self.state = MAIN_MENU

    def update(self, delta):
        # @TODO: split these state updates out into separate functions
        if self.state == MAIN_MENU:
            self.menu.update(delta)
        elif self.state == REPL:
            if not self.repl:
                self._init_repl()
        # elif self.state == LOAD_PROGRAM:
        #     pass
        # elif self.state == SAVE_PROGRAM:
        #     pass

        # :@TODO: do we need a `running-program` state?
        # if `hexp-update` is defined, invoke it
        self.session.update()

        # update any error notifications
        if self.notification:
            self.notification.update(delta)

    def draw(self, ctx):
        clear_background(ctx)

        if self.state == MAIN_MENU:
            self.menu.draw(ctx)
        elif self.state == REPL:
            if self.repl:
                self.repl.draw(ctx)
        # elif self.state == LOAD_PROGRAM:
        #     pass
        # elif self.state == SAVE_PROGRAM:
        #     pass

        # if `hexp-draw` is defined, invoke it
        self.session.draw()

        # draw any error notifications
        if self.notification:
            self.notification.draw(ctx)

    # @TODO: we need to exit the app when we hit the back button, I guess we _could_ try and write new version of each of the button handling methods an app can override?

__app_export__ = HexpApp
