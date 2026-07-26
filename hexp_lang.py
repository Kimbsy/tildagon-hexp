# Hexp language evaluator and utils

import re

BOOLS = {
    "true": True,
    "false": False
}

def read_atom(s):
    # is it a number
    if re.match(r"\d+\.?\d*", s):
        return float(s)    
    # is it a boolean?
    elif s in BOOLS.keys():
        return BOOLS[s]
    # is it a string?
    elif re.match(r"\'.*\'", s):
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

    # @TODO: we need to also keep track of if we're inside single quotes so we can have spaces in strings!!!!

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
    s = s.replace('\n', ' ').strip()
    # is it a list?
    if re.match(r"\(.*\)", s):
        return read_list(s)
    # it must be an atom
    else:
        return read_atom(s)

def is_atom(expr):
    return not isinstance(expr, list)

def extend_env(env, bindings):
    scoped_env = env
    for param, arg in bindings:
        # print(type(param))
        # print(param)
        # print(type(arg))
        # print(arg)
        scoped_env[param.name] = arg
    return scoped_env

# Evaluate multiple expressions,allowing update to env each time (for `def` etc), returns the value of the final expression and the final env
def reduce_eval(exprs, env, ctx):
    res = None
    for expr in exprs:
        res, env = evaluate(expr, env, ctx)
    return (res, env)

# With a `fn` we expect a list of params, then any number of `(body1) (body2)` expressions
def handle_fn(arg_exprs, env, ctx):
    params, *bodies = arg_exprs
    # Python only allows single line lambdas !!!?!
    return (lambda arg_list: reduce_eval(bodies, extend_env(env, zip(params, arg_list)), ctx)[0], env)

# With an `if`, we expect a `(consequent)` and `(alternative)` body expressions, we should only evaluate one
def handle_if(arg_exprs, env, ctx):
    pred, consequent, alternative = arg_exprs
    if evaluate(pred, env)[0]:
        return (evaluate(consequent, env, ctx)[0], env)
    else:
        return (evaluate(alternative, env, ctx)[0], env)

# With `let` we expect a set of `(a 1 b 2)` bindings and any number of `(body1) (body2)` expressions
def handle_let(arg_exprs, env, ctx):
    raw_bindings, *bodies = arg_exprs
    names = raw_bindings[0::2]
    # @TODO: do we not need to evaluate these one by one and extend the env each time?
    vals = map(lambda v: evaluate(v, env)[0], raw_bindings[1::2])
    scoped_env = extend_env(env, zip(names, vals))
    return (reduce_eval(bodies, scoped_env, ctx)[0], env)

# With `quote` we just return the expression data structure unevaluated
def handle_quote(arg_exprs, env, ctx):
    return (arg_exprs[0], env)

# With def we expect a `name` symbol, then a body to evaluate to a value, we return an updated env
def handle_def(arg_exprs, env, ctx):
    name_sym, body_expr = arg_exprs
    return (None, extend_env(env, zip([name_sym], [evaluate(body_expr, env, ctx)[0]])))

SPECIAL_FORMS = {
    "fn": handle_fn,
    "if": handle_if,
    "let": handle_let,
    "quote": handle_quote,
    "def": handle_def
}

class Special:
    def __init__(self, s):
        self.name = s
        self.handler = SPECIAL_FORMS[s]
    def __repr__(self):
        return "<spf: " + self.name + " >"

class Symbol:
    def __init__(self, s):
        self.name = s
    def __repr__(self):
        return "<sym: " + self.name + " >"

def is_special(expr):
    return isinstance(expr, Special)

def is_symbol(expr):
    return isinstance(expr, Symbol)

# @TODO: would be nice to do this better
requires_ctx = ["draw-rect"]

# @TODO: need to return the new env from each call?
def evaluate(expr, env, ctx=None):
    if is_atom(expr):
         # lookup a symbol in the environment
        if is_symbol(expr):
            return (env[expr.name], env)
        else:
            # return a literal value
            return (expr, env)
    else:
        f_exp, *arg_exprs = expr
        f = evaluate(f_exp, env, ctx)[0]
        # handle special forms
        if is_special(f):
            return f.handler(arg_exprs, env, ctx)
        # function application
        else:
            args = list(map(lambda arg: evaluate(arg, env, ctx)[0], arg_exprs))
            if is_symbol(f_exp) and f_exp.name in requires_ctx:
                args.insert(0, ctx)
            # print("!!!!!!!1")
            # print(f)
            # print(args)
            return (f(args), env)
