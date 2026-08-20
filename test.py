#!/usr/bin/python3

import time
from hexp_core import INIT_ENV
from hexp_lang import evaluate, read_expr_string

# Check if the result of evaluating something is what we expect
def test_expected(expr, expected_output):
    parsed = read_expr_string(expr)
    output = evaluate(parsed, INIT_ENV)[0]
    if output == expected_output:
        return True
    else:
        return (expr, parsed, output, expected_output)

# Just check if we can evaluate something without throwing
def test_evaluate(expr):
    evaluate(read_expr_string(expr), INIT_ENV)[0]

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

def run():
    start_ms = time.time() * 1000
    failures = []
    print(GREEN, end='')
    for t in TESTS:
        try:
            if len(t) == 1:
                test_evaluate(t[0])
            elif len(t) == 2:
                expr, expected = t
                result = test_expected(expr, expected)
                if result == True:
                    print(".", end='')
                else:
                    failures.append(result)
                    print(RED + "F" + GREEN, end='')
        except Exception as e:
            failures.append(t + [repr(e)])
            print(RED + "F" + GREEN, end='')
    print(ENDC)
    print("Ran " + str(len(TESTS)) + " tests")
    if len(failures) > 0:
        print("\n" + str(len(failures)) + " Failure(s):")
        for f in failures:
            print(f)
            if len(f) == 1:
                print("\nFailed evaluation: " + str(f[0]))
            elif len(f) == 4:
                expr, parsed, output, expected_output = f
                print("\nExpr:     " + str(expr))
                print("Parsed:   " + str(parsed))
                print("Output:   " + str(output))
                print("Expected: " + str(expected_output))
    else:
        print("All passed " + GREEN + "[OK]" + ENDC)
    print("{:.2f}".format(((time.time() * 1000) - start_ms)) + "ms")
    
TESTS = [
    ["42", 42],
    ["  42  ", 42],
    ["'blah'", "blah"],
    ["'blah blah blah'", "blah blah blah"],
    ["true", True],
    ["+"],
    ["(+ 11 23)", 34],
    ["(+ 1 2 3 4 5 6 7 8)", 36],
    ["(+ 4 (+ 40 40))", 84],
    ["(- 10 1)", 9],
    ["(- 10 1 2 3)", 4],
    ["(- 4)", -4],
    ["(* 2 2)", 4],
    ["(* 2 2 2)", 8],
    ["(* 2)", 2],
    ["(if true 1 2)", 1],
    ["(if false 1 2)", 2],
    ["(if (= 5 6) 1 2)", 2],
    ["(if (= 5 5) 1 2)", 1],
    ["(if (= 5) 1 2)", 1],
    ["(if (= 5 5 5 5) 1 2)", 1],
    ["(if (= 5 5 5 6) 1 2)", 2],
    ["(< 1 2)", True],
    ["(< 2 1)", False],
    ["(< 1 2 3)", True],
    ["(< 1 3 2)", False],
    ["(odd? 2)", False],
    ["(odd? 3)", True],
    ["(odd? 0)", False],
    ["(even? 2)", True],
    ["(even? 3)", False],
    ["(even? 0)", True],
    ["(complement odd?)"],
    ["((complement odd?) 1)", False],
    ["((complement odd?) 2)", True],
    ["(quote 100)", 100],
    ["(quote (1 2 3))", [1, 2, 3]],
    ["(quote (1 (2 3 ())))", [1, [2, 3, []]]],
    ["(quote (quote (1 2 3)))"],
    ["(fn (a) a)"],
    ["((fn (a) a) 400)", 400],
    ["((fn () 32))", 32],
    ["((fn (a b) (+ a a b)) 200 20)", 420],
    ["((fn (a b) a b) 1 2)", 2],
    ["((fn (a) (def b 30) (def c 40) (+ a b c)) 20)", 90],
    ["(let (a 1) a)", 1],
    ["(let (a 1 b 2) (+ a b))", 3],
    ["(let (a 1 b a) b)", 1],
    ["(let (a 1 b (+ a 1)) (+ a b))", 3],
    ["(let (a 10) (let (b 20) (+ a b)))", 30],
    ["(let (a 10) (let (a 20) a))", 20],
    ["(let (inc (fn (n) (+ n 1))) (inc 41))", 42],
    ["(let (a 1 b 2) (+ a b) 400)", 400],
    ["(let (a 1) (def foo 41) (+ foo a))", 42],
    ["(parse-hex '#ff00ff')", [1, 0, 1]],
    ["(list)", []],
    ["(list 1 2 3)", [1, 2, 3]],
    ["(list 1 (list 2) (list (list 3)))", [1, [2], [[3]]]],
    ["(append (list 1) 2)", [1, 2]],
    ["(concat (list 1 2) (list 3 4 5))", [1, 2, 3, 4, 5]],
    ["(first (list 1 2 3))", 1],
    ["(last (list 1 2 3))", 3],
    ["(rest (list 1 2 3))", [2, 3]],
    ["(rest (list 1))", []],
    ["(rest (list))", []],
    ["(nth (list 1 2 3) 1)", 2],
    ["(rand-nth (list 1))", 1],
    ["(rand-nth (list 'foo'))", "foo"],
    ["(map (fn (n) (+ n 1)) (list 1 2 3))", [2, 3, 4]],
    ["(map (fn (n) (+ n 1)) (list))", []],
    ["(reduce + 0 (list 1 2 3))", 6],
    ["(reduce + (list 1 2 3))", 6],
    ["(filter odd? (list 1 2 3 4 5))", [1, 3, 5]],
    ["(filter even? (list 1 2 3 4 5))", [2, 4]],
    ["(remove odd? (list 1 2 3 4 5))", [2, 4]],
    ["(remove even? (list 1 2 3 4 5))", [1, 3, 5]],
    ["(def foo 22)", 22],
    ["""(let (multi-line-works? true)
          (= true multi-line-works?))""", True],
    ["""(+ 1
    ;; this is a comment
     2)""", 3],
    [""";; this is a comment
    (+ 1 2)""", 3],
    ["{1 2}", {1: 2}],
    ["{'foo' 'bar'}", {'foo': 'bar'}],
    ["{'foo' {'bar' {'baz' 33}}}", {'foo': {'bar': {'baz': 33}}}],
    ["{'foo' 1 'bar' 2}", {'foo': 1, 'bar': 2}],
    ["(get {'foo' 1 'bar' 2} 'bar')", 2],
    ["(get (get {'foo' {'bar' {'baz' 33}}} 'foo') 'bar')", {'baz': 33}],
    ["(put {} 'foo' 1)", {'foo': 1}],
    ["(put {'foo' 1} 'bar' 2)", {'foo': 1, 'bar': 2}],
    ["(put {'foo' 1} 'foo' 2)", {'foo': 2}],
    ["(put {'foo' 1} 'bar' {'baz' 45})", {'foo': 1, 'bar': {'baz': 45}}],
    ["(update {'x' 10} 'x' (fn (x) (- x 1)))", {'x': 9}],
    ["""(let (inc (fn (n) (+ n 1)))
          (update {'x' 10} 'x' inc))""", {'x': 11}],
    ["(or true true)", True],
    ["(or true false)", True],
    ["(or false true)", True],
    ["(or false false)", False],
    ["(and true true)", True],
    ["(and true false)", False],
    ["(and false true)", False],
    ["(and false false)", False],
    ["(not true)", False],
    ["(not false)", True],
    
]

run()
