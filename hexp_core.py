# Initial environment and core functions

from random import randint

def parse_hex(s):
    r = int("0x" + s[1:3], 16)
    g = int("0x" + s[3:5], 16)
    b = int("0x" + s[5:7], 16)
    return [r / 255, g / 255, b / 255]

WHITE = [1, 1, 1]
BLACK = [0, 0, 0]
GREY = [0.4, 0.4, 0.4]
LIGHT_GREY = [0.8, 0.8, 0.8]
CRAB_ORANGE = [1, 0.5, 0.1]
DARK_BLUE = [0.17, 0.26, 0.32]
ICE_BLUE = [0.75, 0.99, 0.98]
ELECTRIC_PINK = [0.9, 0.01, 0.35]
ELECTRIC_BLUE = [0.1, 1, 1]
RED = parse_hex("#E40303")
ORANGE = parse_hex("#FF8C00")
YELLOW = parse_hex("#FFED00")
GREEN = parse_hex("#008026")
BLUE = parse_hex("#004CFF")
PURPLE = parse_hex("#732982")
DESERT_YELLOW = parse_hex("#FFBF46")
FOREST_GREEN = parse_hex("#4F9D69")
BROWN = parse_hex("#504136")
DARK_PINK = parse_hex("#EF0AFF")
LIGHT_PINK = parse_hex("#FAADFF")

def _colour(ctx, c):
    r, g, b = c
    return ctx.rgb(r, g, b)

def hexp_or(a, b):
    return a or b

# @TODO: other booleans

def multiply(*args):
    if len(args) == 1:
        return args[0]
    elif len(args) == 2:
        return args[0] * args[1]
    else:
        a = args[0]
        for val in args[1:]:
            a = a * val
        return a

def minus(*args):
    if len(args) == 1:
        return 0 - args[0]
    elif len(args) == 2:
        return args[0] - args[1]
    else:
        a = args[0]
        for val in args[1:]:
            a = a - val
        return a

def equal(*args):
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

def less_than(*args):
    if len(args) == 2:
        a, b = args
        return a < b
    else:
        test = args[0]
        for val in args[1:]:
            if val <= test:
                return False
            test = val
        return True

def append(xs, x):
    return xs + [x]

def concat(xs, ys):
    return xs + ys

def nth(coll, n):
    return coll[int(n)]

def rand_nth(coll):
    return coll[randint(0, len(coll) - 1)]

# @TODO: map

# @TODO: reduce

# @TODO: filter

# @TODO: remove

def get(hashmap, key):
    return hashmap[key]

def put(hashmap, key, val):
    hashmap[key] = val
    return hashmap

def update(hashmap, key, f):
    old_v = hashmap[key]
    new_v = f(old_v)
    hashmap[key] = new_v
    return hashmap

def background(ctx, colour_hex):
    _colour(ctx, parse_hex(colour_hex)).rectangle(-120, -120, 240, 240).fill()

def draw_rect(ctx, pos, size, colour_hex):
    x, y = pos
    w, h = size
    _colour(ctx, parse_hex(colour_hex)).rectangle(x, y, w, h).stroke()

def fill_rect(ctx, pos, size, colour_hex):
    x, y = pos
    w, h = size
    _colour(ctx, parse_hex(colour_hex)).rectangle(x, y, w, h).fill()

def draw_tri(ctx, points, colour_hex):
    ctx.save()
    _colour(ctx, parse_hex(colour_hex)).begin_path()
    lx, ly = points[-1]
    ctx.move_to(lx, ly)
    for x, y in points:
        ctx.line_to(x, y)
    ctx.close_path()
    ctx.stroke()
    ctx.restore()

def fill_tri(ctx, points, colour_hex):
    ctx.save()
    _colour(ctx, parse_hex(colour_hex)).begin_path()
    lx, ly = points[-1]
    ctx.move_to(lx, ly)
    for x, y in points:
        ctx.line_to(x, y)
    ctx.close_path()
    ctx.fill()
    ctx.restore()

def draw_text(ctx, pos, content, colour_hex):
    x, y = pos
    ctx.save()
    _colour(ctx, parse_hex(colour_hex))
    ctx.move_to(x, y).text(content)
    ctx.restore()
    
# @TODO: continue expanding initial env
INIT_ENV = {
    "or": hexp_or,
    "list": lambda *args: list(args),
    "append": append,
    "concat": concat,
    "first": lambda coll: coll[0],
    "last": lambda coll: coll[-1],
    "rest": lambda coll: coll[1:],
    "nth": nth,
    "rand-nth": rand_nth,
    "get": get,
    "put": put,
    "update": update,
    "+": lambda *args: sum(args),
    "-": minus,
    "*": multiply,
    "=": equal,
    "<": less_than,
    "parse-hex": lambda s: parse_hex(s),

    # side effecting functions
    "print": lambda x: print(x[0]),

    # ctx graphics functions
    "background": background,
    "draw-rect": draw_rect,
    "fill-rect": fill_rect,
    "draw-tri": draw_tri,
    "fill-tri": fill_tri,
    "draw-text": draw_text,

    # Tildagon app lifecycle functions
    "hexp-update": None,
    "hexp-draw": None
}
