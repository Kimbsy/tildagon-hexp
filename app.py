import os
import re
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

# App states
MAIN_MENU = "Main Menu"
REPL = "REPL"
LOAD_PROGRAM = "Load program"
SAVE_PROGRAM = "Save program"

MENUS = [MAIN_MENU, LOAD_PROGRAM, SAVE_PROGRAM]

MAIN_MENU_OPTIONS = [
    REPL,
    LOAD_PROGRAM,
    SAVE_PROGRAM
]

APP_DIR = 'apps/hexp'
PROG_STORE_PATH = APP_DIR + '/prog'

class HexpApp(App):
    def __init__(self):
        super().__init__()
        self.session = Session(
            INIT_ENV,
            read_expr_string,
            evaluate,
            self.session_error_handler,
            get_ctx())
        self.menu = Menu(
            self,
            MAIN_MENU_OPTIONS,
            select_handler = self.multi_menu_select_handler,
            back_handler = self.multi_menu_back_handler
        )
        self._init_prog_store()

        self.notification = None
        self.state = MAIN_MENU
        # for some reason we don't seem to be able to create a TextDialog in the init function? it displays but is frozen?
        self.repl = None

    # Ensure the program store directory exists
    def _init_prog_store(self):
        if 'prog' not in os.listdir(APP_DIR):
            os.mkdir(PROG_STORE_PATH)
        self.programs = [f for f in os.listdir(PROG_STORE_PATH) if re.match(r".*\.hxp", f)]
        self.load_options = ['<no programs found>']
        if len(self.programs) > 0:
            self.load_options = self.programs

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
        if item == LOAD_PROGRAM:
            self.menu.menu_items = self.load_options
            self.menu.position = 0
        elif item == SAVE_PROGRAM:
            self.menu.menu_items = self.programs + ['<new file>']
            self.menu.position = 0

        # REPL option implicitly handled
        self.state = item
        
    def main_menu_back_handler(self):
        if self.state != MAIN_MENU:
            self.state = MAIN_MENU
        else:
            self.minimise()

    # @TODO: THIS THIS THIS!!!!
    def load_menu_select_handler(self, item, idx):
        print("LOAD")
        print(item)

    def _back_to_main(self):
        self.menu.menu_items = MAIN_MENU_OPTIONS
        self.menu.position = 0
        self.state = MAIN_MENU

    def load_menu_back_handler(self):
        self._back_to_main()

    # @TODO: THIS THIS THIS!!!!
    def save_menu_select_handler(self, item, idx):
        print("SAVE")
        print(item)

    def save_menu_back_handler(self):
        self._back_to_main()
        
    def repl_select_handler(self, item, idx):
        print("REPL SELECT NOOP")

    def repl_back_handler(self):
        self.repl = None
        self._back_to_main()

    # All the menus seem to have their handlers triggered, so we really just want a single menu object
    # THIS is probably why the menus still move when they're not displayed if you press buttons
    # Can also lead to an error when you move past the last index of the menu you're about to load.
    def multi_menu_select_handler(self, item, idx):
        if self.state not in MENUS:
            return
        menu_handlers = {
            MAIN_MENU: self.main_menu_select_handler,
            LOAD_PROGRAM: self.load_menu_select_handler,
            SAVE_PROGRAM: self.save_menu_select_handler,
        }
        menu_handlers[self.state](item, idx)

    def multi_menu_back_handler(self):
        menu_handlers = {
            MAIN_MENU: self.main_menu_back_handler,
            REPL: self.repl_back_handler,
            LOAD_PROGRAM: self.load_menu_back_handler,
            SAVE_PROGRAM: self.save_menu_back_handler,
        }
        menu_handlers[self.state]()
        
    def repl_complete_callback(self):
        print("whoops")
        self.repl = None

    def repl_cancel_callback(self):
        print("whoopsie")
        self.repl = None
        self.state = MAIN_MENU

    def update(self, delta):
        # @TODO: split these state updates out into separate functions
        if self.state in [MAIN_MENU, LOAD_PROGRAM, SAVE_PROGRAM]:
            self.menu.update(delta)
        elif self.state == REPL:
            if not self.repl:
                self._init_repl()

        # :@TODO: do we need a `running-program` state?
        # if `hexp-update` is defined, invoke it
        self.session.update()

        # update any error notifications
        if self.notification:
            self.notification.update(delta)

    def draw(self, ctx):
        clear_background(ctx)

        if self.state in MENUS:
            self.menu.draw(ctx)
        elif self.state == REPL:
            if self.repl:
                self.repl.draw(ctx)

        # if `hexp-draw` is defined, invoke it
        self.session.draw()

        # draw any error notifications
        if self.notification:
            self.notification.draw(ctx)

    # @TODO: we need to exit the app when we hit the back button, I guess we _could_ try and write new version of each of the button handling methods an app can override?

__app_export__ = HexpApp
