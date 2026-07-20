from hexp_core import INIT_ENV
from hexp_lang import evaluate, read_expr_string

# Check if the result of evaluating something is what we expect
def test_expected(expr, expected_output):
    parsed = read_expr_string(expr)
    output = evaluate(parsed, INIT_ENV)
    if output == expected_output:
        return True
    else:
        return (expr, parsed, output, expected_output)

# Just check if we can evaluate something without throwing
def test_evaluate(expr):
    evaluate(read_expr_string(expr), INIT_ENV)

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

def run():
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
        except:
            failures.append(t)
            print(RED + "F" + GREEN, end='')
    print(ENDC)
    print("Ran " + str(len(TESTS)) + " tests")
    if len(failures) > 0:
        print("\n" + str(len(failures)) + " Failure(s):")
        for f in failures:
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
    
TESTS = [
    ["42", 42],
    ["'blah'", "blah"],
    ['true', True],
    ['my_var', 11],
    ['+'],
    ['(+ 11 23)', 34],
    ['(+ 100 my_var)', 111],
    ['(+ 1 2 3 4 5 6 7 8)', 36],
    ['(+ 4 (+ 40 40))', 84],
    ['(if true 1 2)', 1],
    ['(if false 1 2)', 2],
    ['(if (= 5 6) 1 2)', 2],
    ['(if (= 5 5) 1 2)', 1],
    ['(if (= 5) 1 2)', 1],
    ['(if (= 5 5 5 5) 1 2)', 1],
    ['(if (= 5 5 5 6) 1 2)', 2],
    ['(quote 100)', 100],
    ['(quote (1 2 3))', [1, 2, 3]],
    ['(quote (1 (2 3 ())))', [1, [2, 3, []]]],
    ['(quote (quote (1 2 3)))'],
    ['(fn (a) a)'],
    ['((fn (a) a) 400)', 400],
    ['((fn () 32))', 32],
    ['((fn (a b) (+ a a b)) 200 20)', 420],
    ['(let (a 1) a)', 1],
    ['(let (a 1 b 2) (+ a b))', 3],
    ['(let (a 1 b a) b)', 1],
    ['(let (a 1 b (+ a 1)) (+ a b))', 3],
    ['(let (a 10) (let (b 20) (+ a b)))', 30],
    ['(let (a 10) (let (a 20) a))', 20],
    ['(let (inc (fn (n) (+ n 1))) (inc 41))', 42]
]

run()
