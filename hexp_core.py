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

def hexp_or(args):
    a, b = args
    return a or b

# other booleans

def colour(ctx, c):
    r, g, b = c
    return ctx.rgb(r, g, b)

def multiply(args):
    if len(args) == 1:
        return args[0]
    elif len(args) == 2:
        return args[0] * args[1]
    else:
        a = args[0]
        for val in args[1:]:
            a = a * val
        return a

def minus(args):
    if len(args) == 1:
        return 0 - args[0]
    elif len(args) == 2:
        return args[0] - args[1]
    else:
        a = args[0]
        for val in args[1:]:
            a = a - val
        return a

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

def less_than(args):
    if len(args) == 2:
        a, b = args
        return a < b
    else:
        a = args[0]
        for val in args[1:]:
            if val >= a:
                return False
        return True

def append(args):
    xs, x = args
    return xs + [x]

def concat(args):
    xs, ys = args
    return xs + ys

def nth(args):
    coll, n = args
    return coll[int(n)]

def rand_nth(args):
    return args[0][randint(0, len(args[0]) - 1)]

# map

# reduce

# filter

# remove

def get(args):
    hashmap, key = args
    return hashmap[key]

def put(args):
    hashmap, key, val = args
    hashmap[key] = val
    return hashmap

def update(args):
    hashmap, key, f = args
    old_v = hashmap[key]
    new_v = f([old_v])
    hashmap[key] = new_v
    return hashmap

def background(args):
    ctx, colour_hex = args
    colour(ctx, parse_hex(colour_hex)).rectangle(-120, -120, 240, 240).fill()

def draw_rect(args):
    ctx, pos, size, colour_hex = args
    x, y = pos
    w, h = size
    colour(ctx, parse_hex(colour_hex)).rectangle(x, y, w, h).stroke()

def fill_rect(args):
    ctx, pos, size, colour_hex = args
    x, y = pos
    w, h = size
    colour(ctx, parse_hex(colour_hex)).rectangle(x, y, w, h).fill()

def draw_tri(args):
    ctx, points, colour_hex = args
    ctx.save()
    colour(ctx, parse_hex(colour_hex)).begin_path()
    lx, ly = points[-1]
    ctx.move_to(lx, ly)
    for x, y in points:
        ctx.line_to(x, y)
    ctx.close_path()
    ctx.stroke()
    ctx.restore()

def fill_tri(args):
    ctx, points, colour_hex = args
    ctx.save()
    colour(ctx, parse_hex(colour_hex)).begin_path()
    lx, ly = points[-1]
    ctx.move_to(lx, ly)
    for x, y in points:
        ctx.line_to(x, y)
    ctx.close_path()
    ctx.fill()
    ctx.restore()

def draw_text(args):
    ctx, pos, content, colour_hex = args
    x, y = pos
    ctx.save()
    colour(ctx, parse_hex(colour_hex))
    ctx.move_to(x, y).text(content)
    ctx.restore()
    
# @TODO: continue expanding initial env
INIT_ENV = {
    "or": hexp_or,
    "list": lambda args: args,
    "append": append,
    "concat": concat,
    "first": lambda args: args[0][0],
    "last": lambda args: args[0][-1],
    "rest": lambda args: args[0][1:],
    "nth": nth,
    "rand-nth": rand_nth,
    "get": get,
    "put": put,
    "update": update,
    "+": sum,
    "-": minus,
    "*": multiply,
    "=": equal,
    "<": less_than,
    "parse-hex": lambda s: parse_hex(s[0]),

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
