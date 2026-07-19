# Hexp language evaluator and utils

import re
from .hexp_core import INIT_ENV

BOOLS = {
    "true": True,
    "false": False
}

def read_atom(s):
    # is it a number
    if re.match("\d+\.?\d*", s):
        return float(s)    
    # is it a boolean?
    elif s in BOOLS.keys():
        return BOOLS[s]
    # is it a string?
    elif re.match("\'.+\'", s):
        return s[1:-1]
    # is it a special form? wrap it in a Special
    elif s in SPECIAL_FORMS.keys():
        return Special(s)
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

# @TODO: implement the special forms
def handle_fn(arg_exprs, env):
    print("handling fn")
    pass

# With an `if`, we expect a `(consequent)` and `(alternative)` body expressions, we should only evaluate one
def handle_if(arg_exprs, env):
    pred, consequent, alternative = arg_exprs
    if evaluate(pred, env):
        return evaluate(consequent, env)
    else:
        return evaluate(alternative, env)

def handle_let(arg_exprs, env):
    print("handling let")
    pass

def handle_quote(arg_exprs, env):
    return arg_exprs[0]

SPECIAL_FORMS = {
    "fn": handle_fn,
    "if": handle_if,
    "let": handle_let,
    "quote": handle_quote
}

class Special:
    def __init__(self, s):
        self.name = s
        self.handler = SPECIAL_FORMS[s]
    def __repr__(self):
        return self.name

class Symbol:
    def __init__(self, s):
        self.name = s
    def __repr__(self):
        return self.name

def is_special(expr):
    return isinstance(expr, Special)

def is_symbol(expr):
    return isinstance(expr, Symbol)

def evaluate(expr, env):
    if is_atom(expr):
         # lookup a symbol in the environment
        if is_symbol(expr):
            return env[expr.name]
        else:
            # return a literal value
            return expr
    else:
        f_exp, *arg_exprs = expr
        f = evaluate(f_exp, env)
        # handle special forms
        if is_special(f):
            return f.handler(arg_exprs, env)
        # function application
        else:
            args = list(map(lambda arg: evaluate(arg, env), arg_exprs))
            # print("!!!!!!!1")
            # print(f)
            # print(args)
            return f(args)
