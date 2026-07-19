import re
from app import App
from app_components import Menu, Notification, clear_background
from typing import Literal
from .palette import *
from .util import *

bools = {
    "true": True,
    "false": False
}

class Symbol:
    def __init__(self, s):
        self.name = s

def read_atom(s):
    # is it a number
    if re.match("\d+\.?\d*", s):
        return float(s)    
    # is it a boolean?
    elif s in bools.keys():
        return bools[s]
    # is it a string?
    elif re.match("\'.+\'", s):
        return s[1:-1]
    # otherwise it's a variable name, wrap it in a Symbol
    else:
        return Symbol(s)
    
# we have a string which starts with an open paren, we want to take chars till it matching close, then return this sublist along with the remaining (or maybe just this sublist)
def take_sublist(s):
    out = "("
    remaining = s[1:]
    level = 1
    while level > 0:
        c = remaining[0]
        if (c == ")"):
            level = level - 1
        elif (c == "("):
            level = level + 1
        remaining = remaining[1:]
        out = out + c
    return out
        
# we want to split by spaces, but not if we're inside a paren
# if we find a paren, we should slurp till parens are balanced

# then for each sub expression string we want to call the parent
# read_expr_string on it, this should recursively get all our
# sublists
def read_list(s):
    inner = s[1:-1]
    sub_exprs = []
    current_expr = ""
    remaining = inner
    while len(remaining) >= 1:
        c = remaining[0]
        step = 1
        if (c == "("):
            sublist = take_sublist(remaining)
            step = len(sublist)
            sub_exprs.append(read_list(sublist))
        elif (c == " ") and len(current_expr) > 0:
            sub_exprs.append(read_atom(current_expr))
            current_expr = ""
        elif (c != " "):
            current_expr = current_expr + c
        remaining = remaining[step:]
    if len(current_expr) > 0:
        sub_exprs.append(read_atom(current_expr))
    return sub_exprs

def read_expr_string(s):
    # is it a list?
    if re.match("\(.*\)", s):
        return read_list(s)
    # it must be an atom
    else:
        return read_atom(s)

def is_atom(expr):
    return not isinstance(expr, list)

def is_symbol(expr):
    return isinstance(expr, Symbol)

def evaluate(expr, env):
    if is_atom(expr):
        if is_symbol(expr):
            return env[expr.name]
        else:
            return expr
    else:
        # @TODO: check for special forms        
        f_exp, *arg_exprs = expr
        f = evaluate(f_exp, env)
        args = (evaluate(arg, env) for arg in arg_exprs)
        return f(args)

# @TODO: move to a `core` module
def plus(args):
    a, b = args
    return a + b

INIT_ENV = {
    "my_var": 11,
    "+": plus
}

# test evaluate
def tev(expr):
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
        tev('(+ 11 23)')
        tev('(+ 4 (+ 40 40))')
        # tev('(list 42 33 11)')
        # tev('(quote (1 2 3))')
        

    def update(self, delta):
        self.foo = 42

    def draw(self, ctx):
        clear_background(ctx)
        colour(ctx, FOREST_GREEN)
        ctx.rectangle(-120, -120, 240, 240).fill()

__app_export__ = HexpApp
