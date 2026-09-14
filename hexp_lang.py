# Hexp language evaluator and utils

import re

BOOLS = {
    "true": True,
    "false": False
}

# MicroPython regex sucks, we can't just re.sub(r";;.*", "", s)
# So we split by lines, then remove comment lines, then patch it back together
def remove_comments(s):
    lines = s.split("\n")
    out = ""
    for line in lines:
        if not line.strip().startswith(";;"):
            out = out + line
    return out

# We need to handle reading whole files and multi-line input better, we should parse a file while tracking parens, not _require_ two newlines between expressions

def read_atom(s, is_string):
    if is_string:
        return s
    
    # @TODO: handle negative number literals
    # is it a number
    if re.match(r"\d+\.?\d*", s):
        return float(s)    
    # is it a boolean?
    elif s in BOOLS.keys():
        return BOOLS[s]
    # is it a special form? wrap it in a Special
    elif s in SPECIAL_FORMS.keys():
        return Special(s)
    # otherwise it's a variable name, wrap it in a Symbol
    else:
        return Symbol(s)

# s is a single expression, some lines may be comments (starting with ;;)
def read_expr_string(s):
    s = remove_comments(s)
    s = s.replace(',', ' ').strip()

    incomplete_containers = []
    container = None
    map_key = None
    token = ""
    token_is_string = False
    in_string = False
    in_map = False

    for c in s:
        if c == "'":
            if in_string:
                in_string = False
            else:
                in_string = True
                token_is_string = True
        elif in_string:
            token += c

        elif c == '(':
            if token:
                if in_map:
                    if map_key is None:
                        map_key = read_atom(token, token_is_string)
                    else:
                        container[map_key] = read_atom(token, token_is_string)
                        map_key = None
                else:
                    container.append(read_atom(token, token_is_string))
                token = ""
                token_is_string = False

            incomplete_containers.append(
                (container, map_key, in_map)
            )
            container = []
            map_key = None
            in_map = False

        elif c == '{':
            if token:
                if in_map:
                    if map_key is None:
                        map_key = read_atom(token, token_is_string)
                    else:
                        container[map_key] = read_atom(token, token_is_string)
                        map_key = None
                else:
                    container.append(read_atom(token, token_is_string))
                token = ""
                token_is_string = False

            incomplete_containers.append(
                (container, map_key, in_map)
            )
            container = {}
            map_key = None
            in_map = True

        elif c == ')' or c == '}':
            if token:
                if in_map:
                    if map_key is None:
                        map_key = read_atom(token, token_is_string)
                    else:
                        container[map_key] = read_atom(token, token_is_string)
                        map_key = None
                else:
                    container.append(read_atom(token, token_is_string))
                token = ""
                token_is_string = False

            completed_container = container
            container, map_key, in_map = incomplete_containers.pop()

            # if there is no parent, this was the top level and we're done
            if container is None:
                return completed_container

            if in_map:
                container[map_key] = completed_container
                map_key = None
            else:
                container.append(completed_container)

        elif c.isspace():
            if token:
                if in_map:
                    if map_key is None:
                        map_key = read_atom(token, token_is_string)
                    else:
                        container[map_key] = read_atom(token, token_is_string)
                        map_key = None
                else:
                    container.append(read_atom(token, token_is_string))
                token = ""
                token_is_string = False
        else:
            token += c

    if token:
        if container is not None:
            if in_map:
                container[map_key] = read_atom(token, token_is_string)
            else:
                container.append(read_atom(token, token_is_string))
            return container
        else:
            return read_atom(token, token_is_string)

    raise ValueError('Unclosed expression: ' + s)

def is_atom(expr):
    return not isinstance(expr, list)

# @NOTE! mutating env dict!!!
def extend_env(env, bindings):
    for param, arg in bindings:
        env[param.name] = arg
    return env

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
    new_env = env.copy()
    f = lambda *arg_list: reduce_eval(bodies, extend_env(new_env, zip(params, arg_list)), ctx)[0]
    new_env["recur"] = f
    return (f, env)

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
    scoped_env = env.copy()
    syms = raw_bindings[0::2]
    val_exprs = raw_bindings[1::2]

    for sym, val_expr in zip(syms, val_exprs):
        val = evaluate(val_expr, scoped_env, ctx)[0]
        scoped_env[sym.name] = val
    
    return (reduce_eval(bodies, scoped_env, ctx)[0], env)

# With `quote` we just return the expression data structure unevaluated
def handle_quote(arg_exprs, env, ctx):
    return (arg_exprs[0], env)

# With def we expect a `name` symbol, then a body to evaluate to a value, we return an updated env
def handle_def(arg_exprs, env, ctx):
    name_sym, body_expr = arg_exprs
    res = evaluate(body_expr, env, ctx)[0]
    new_env = env.copy()
    return (res, extend_env(new_env, zip([name_sym], [res])))

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
    def __eq__(self, other):
        return isinstance(other, Special) and self.name == other.name

class Symbol:
    def __init__(self, s):
        self.name = s
    def __repr__(self):
        return "<sym: " + self.name + " >"
    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

def is_special(expr):
    return isinstance(expr, Special)

def is_symbol(expr):
    return isinstance(expr, Symbol)

# @TODO: might be a nicer way to know when to inject ctx, at a minimum this feels like ti should live in core, with the function definitions
REQUIRES_CTX = [
    "background",
    "draw-rect",
    "fill-rect",
    "draw-tri",
    "fill-tri",
    "draw-text"
]

def evaluate(expr, env, ctx=None):
    stack = [("eval", [expr, env])]
    result = None

    while stack:
        op, work = stack.pop()

        if op == "eval":
            expr, env = work

            if isinstance(expr, dict):
                stack.append(("map", [env, {}, list(expr.items()), 0]))
            
            elif is_atom(expr):
                # lookup a symbol in the environment
                if is_symbol(expr):
                    result = (env[expr.name], env)
                else:
                    # a literal value
                    result = (expr, env)

            else:
                f_exp, *arg_exprs = expr
                
                # appending backwards to ensure function is evaluated before it's applied
                stack.append(("apply", [f_exp, arg_exprs, env]))
                stack.append(("eval", [f_exp, env]))

        elif op == "apply":
            f_exp, arg_exprs, env = work
            # f is the result of the eval immediately preceding this
            f = result[0]

            if is_special(f_exp):
                result = f.handler(arg_exprs, env, ctx)

            else:
                # we're going to evaluate each arg one at a time,
                # collecting them in the args `[]` till this arg_index
                # 0 is at the length of arg_exprs
                stack.append(("arguments", [f, f_exp, arg_exprs, env, [], 0]))

                if arg_exprs:
                    stack.append(("eval", [arg_exprs[0], env]))

        elif op == "arguments":
            f, f_exp, arg_exprs, env, args, arg_index = work

            # add the arg value from the eval immediately preceding
            # this (except the first one which is the function to
            # apply)
            if arg_index > 0:
                args.append(result[0])
            
            if arg_index < len(arg_exprs):
                stack.append(("arguments", [f, f_exp, arg_exprs, env, args, arg_index + 1]))
                stack.append(("eval", [arg_exprs[arg_index], env]))
            else:
                if is_symbol(f_exp) and f_exp.name in REQUIRES_CTX:
                    args.insert(0, ctx)

                result = (f(*args), env)

        elif op == "map":
            env, result_map, items, item_index = work

            if item_index < len(items):
                key, value_expr = items[item_index]

                stack.append(("map", [env, result_map, items, item_index + 1]))
                stack.append(("map-value", [key, result_map]))
                stack.append(("eval", [value_expr, env]))

            else:
                result = (result_map, env)

        elif op == "map-value":
            key, result_map = work
            result_map[key] = result[0]

    return result
