import os
import re
import time
from app import App
from app_components import Menu, Notification, TextDialog, clear_background
from events.emote import EmotePositiveEvent, EmoteNegativeEvent
from display import get_ctx
from system.eventbus import eventbus
from typing import Literal
from .hexp_core import INIT_ENV
from .hexp_lang import evaluate, read_expr_string, remove_comments
from .hexp_repl import HexpRepl
from .palette import *
from .session import *

# App states
MAIN_MENU = "Main Menu"
REPL = "REPL"
LOAD_PROGRAM = "Load program"
SAVE_PROGRAM = "Save program"
DELETE_ALL = "Delete all programs"

MENUS = [MAIN_MENU, LOAD_PROGRAM, SAVE_PROGRAM]

MAIN_MENU_OPTIONS = [
    REPL,
    LOAD_PROGRAM,
    SAVE_PROGRAM,
    DELETE_ALL
]

APP_NAME = 'Kimbsy_tildagon_hexp'
APP_DIR = 'apps/' + APP_NAME
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

    def _find_programs(self):
        self.programs = [f for f in os.listdir(PROG_STORE_PATH) if re.match(r".*\.hxp", f)]

    # Ensure the program store directory exists
    def _init_prog_store(self):
        if APP_NAME not in os.listdir('apps'):
            os.mkdir(APP_DIR)
        if 'prog' not in os.listdir(APP_DIR):
            os.mkdir(PROG_STORE_PATH)
        self._find_programs()
        self.load_options = ['<none>']
        if len(self.programs) > 0:
            self.load_options = self.programs

    def _init_repl(self):
        self.repl = HexpRepl(
            self,
            self.session,
            self.repl_complete_callback,
            self.repl_cancel_callback
        )

    def session_error_handler(self, expr, error):
        print(repr(expr))
        print(repr(error))
        print(self.session.env)
        print(self.session.read_fn)
        self.notification = Notification(repr(error))
        eventbus.emit(EmoteNegativeEvent())

    def main_menu_select_handler(self, item, idx):
        # hack to ensure the font sizes for the menu are properly recalculated for each menu
        self.menu.focused_item_font_size_arr = []
        
        if item == LOAD_PROGRAM:
            self._find_programs()
            self.menu.menu_items = self.load_options
            self.menu.position = 0
        elif item == SAVE_PROGRAM:
            self._find_programs()
            self.menu.menu_items = self.programs + ['<new>']
            self.menu.position = 0

        if item == DELETE_ALL:
            self._delete_all()

        # REPL option implicitly handled
        self.state = item
        
    def main_menu_back_handler(self):
        if self.state != MAIN_MENU:
            self.state = MAIN_MENU
        else:
            self.minimise()

    # @TODO: we're getting evaluation errors while reading files, probably just an empty string or something.
    def load_menu_select_handler(self, item, idx):
        if item == '<none>':
            return
        f = open(PROG_STORE_PATH + "/" + item)
        prog = f.read()
        print(prog)
        exprs = prog.split("\n\n")
        for expr in exprs:
            if len(expr.strip()) > 0:
                self.session.evaluate(expr)
        self.notification = Notification("Loaded: " + item)
        # Don't emit a positive emote, in case the program crashes immediately, it gets mixed up with the negative emote from a failed evaluate
        # eventbus.emit(EmotePositiveEvent())

    def _back_to_main(self):
        self.menu.menu_items = MAIN_MENU_OPTIONS
        self.menu.position = 0
        self.state = MAIN_MENU

    def load_menu_back_handler(self):
        self._back_to_main()

    def save_menu_select_handler(self, item, idx):

        # Need to write to a file when they select '<new>'
        # We'll need to open a dialog to get the new filename, for now let's just use a static name to get one in there.

        # Then once we've got files I'm pretty sure we an either dump the whole history in there (separated by double newlines) or if loading the file didn't add o the session history then we can just append to the file.

        # appending will be weird if we load multiple files, the resulting file won't work like our current session.

        # yeah writing to the file overwrites the whole thing, loading does add to history so should be ok
        
        fname = item
        if fname == "<new>":
            fname = str(time.time()) + ".hxp"
        f = open(PROG_STORE_PATH + "/" + fname, 'wt')
        for h in self.session.history:
            expr, res = h
            f.write(expr + "\n\n")
        f.close()
        self.notification = Notification("Saved")
        eventbus.emit(EmotePositiveEvent())

        # reset the save menu
        self._init_prog_store()
        self.menu.position = 0
        self.menu.menu_items = self.programs + ['<new>']        

    def save_menu_back_handler(self):
        self._back_to_main()
        
    def repl_select_handler(self, item, idx):
        print("REPL SELECT NOOP")

    def repl_back_handler(self):
        self.repl = None
        self._back_to_main()

    def _delete_all(self):
        print("Deleting all")
        for f in self.programs:
            print("deleting " + PROG_STORE_PATH + "/" + f)
            os.remove(PROG_STORE_PATH + "/" + f)
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
            SAVE_PROGRAM: self.save_menu_select_handler
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

__app_export__ = HexpApp
