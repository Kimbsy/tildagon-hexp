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
    "(def empty (fn (sym) 'NOT FOUND'))",
    "(def extend (fn (env sym val) (fn (lookup-sym) (if (= lookup-sym sym) val (env lookup-sym)))))",
    "(def initial (extend (extend (extend (extend empty (quote -) -) (quote *) *) (quote =) =) (quote +) +))",
    """(def hexp++
  (fn (e env)
    (let (hexp++ recur)
      (if (not (coll? e))
        (if (symbol? e)
          (env e)
          e)
        (let (head (first e)
                   tail (rest e))
          (if (= head (quote quote))
            (nth e 1)
            (if (= head (quote if))
              (if (recur (nth e 1) env)
                (hexp++ (nth e 2) env)
                (hexp++ (nth e 3) env))
              (if (= head (quote fun))
                (fn (val)
                  (hexp++ (nth e 2) (extend env (first (nth e 1)) val)))
                (apply
                 (hexp++ (first e) env)
                 (map (fn (arg-exp)
                        (hexp++ arg-exp env))
                      (rest e)))))))))))"""
]

for expr in init:
    print(expr)
    print(session.evaluate(expr))

while True:
    expr = input("> ")
    if len(expr) > 0:
        print(session.evaluate(expr))
