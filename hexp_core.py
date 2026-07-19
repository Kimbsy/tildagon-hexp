# Initial environment and core functions

def equal(args):
    if len(args) == 1:
        return True
    elif len(args) == 2:
        a, b = args
        return a == b
    else:
        a = args[0]
        for val in args[1:]:
            if val != a:
                return False
        return True

INIT_ENV = {
    "my_var": 11,
    "+": sum,
    "=": equal
}
