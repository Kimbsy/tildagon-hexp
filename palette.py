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

def colour(ctx, c):
    r, g, b = c
    return ctx.rgb(r, g, b)
