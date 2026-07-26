#!/usr/bin/python3

from hexp_core import INIT_ENV
from hexp_lang import evaluate, read_expr_string
from session import *

session = Session(INIT_ENV, read_expr_string, evaluate)

while True:
    expr = input("> ")
    print(session.evaluate(expr))
