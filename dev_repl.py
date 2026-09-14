#!/usr/bin/python3

from hexp_core import INIT_ENV
from hexp_lang import evaluate, read_expr_string
from session import *

session = Session(
    INIT_ENV,
    read_expr_string,
    evaluate,
    None,
    None
)

# For convenience you can list expression to be evaluated when the dev
# REPL starts.
init = [
    "(def foo 42)",
    "(def bar 67)",
]

for expr in init:
    print(expr)
    print(session.evaluate(expr))

while True:
    expr = input("> ")
    if len(expr) > 0:
        print(session.evaluate(expr))
