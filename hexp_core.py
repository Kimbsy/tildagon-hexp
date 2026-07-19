# Initial environment and core functions

def plus(args):
    a, b = args
    return a + b

INIT_ENV = {
    "my_var": 11,
    "+": plus
}
