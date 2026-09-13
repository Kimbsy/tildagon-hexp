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

init = [
    "(def empty (fn (s) 'NOT FOUND'))",
    "(def extend (fn (blahenv sym val) (fn (lookup-sym) (if (= lookup-sym sym) val (blahenv lookup-sym)))))",
    "(def initial (extend (extend (extend (extend empty (quote -) -) (quote *) *) (quote =) =) (quote +) +))",
    "(def hexp++ (fn (e env) (if (not (coll? e)) (if (symbol? e) (env e) e) (let (head (first e) tail (rest e)) (if (= head (quote quote)) (nth e 1) (if (= head (quote if)) (if (recur (nth e 1) env) (recur (nth e 2) env) (recur (nth e 3) env)) (if (= head (quote λ)) (fn (val) (recur (nth e 2) (extend-env env (nth e 1) val))) ((recur (first e) env) (recur (nth e 1) env)))))))))"
]

for expr in init:
    print(expr)
    print(session.evaluate(expr))

while True:
    expr = input("> ")
    if len(expr) > 0:
        print(session.evaluate(expr))
