from PIL import ImageColor, Image, ImageDraw
import copy


IMAGE_WIDTH = 616
IMAGE_MAX_HEIGHT = 616
IMAGE_MIN_HEIGHT = 308

WIDTH = 750
HEIGHT_ZERO = 237
HEIGHT_MAX = HEIGHT_ZERO + IMAGE_MAX_HEIGHT
HEIGHT_MIN = HEIGHT_ZERO + IMAGE_MIN_HEIGHT

MIDDLE_POWS = 10
SAFE_CORNERS = (100, 100, 100, 200)  # left right up down
MEMOIZATION_LENGTH = 100


top = Image.open('templateMarkup/top.png')
bottom = Image.open('templateMarkup/bottom.png')
middles = [Image.open(f'templateMarkup/middle_{2 ** i}.png') for i in range(0, MIDDLE_POWS)]
explanation = {'lime': 'image', 'yellow': 'text', 'red': 'title', 'magenta': 'caption'}
memo_templates_areas = dict()


def middle_x(x):
    res = Image.new('RGB', (WIDTH, x))
    start = 0
    for i in range(0, MIDDLE_POWS):
        if (x >> i) & 1:
            res.paste(middles[i], (0, start))
            start += 2 ** i
    return res


def get_template(img_height):
    middle = middle_x(img_height)
    template = Image.new('RGB', (top.width, top.height + middle.height + bottom.height))
    template.paste(top, (0, 0))
    template.paste(middle, (0, top.height))
    template.paste(bottom, (0, top.height + middle.height))
    return template


def get_areas(img, explanation):
    areas = {ImageColor.getrgb(col): [None, None, None, None] for col in explanation}
    l, r, u, d = SAFE_CORNERS
    for x in list(range(0, l)) + list(range(img.width - r, img.width)):
        for y in list(range(0, u)) + list(range(img.height - d, img.height)):
            col = img.getpixel((x, y))
            if col not in areas:
                continue
            if areas[col][0] is None:
                areas[col][0] = x
                areas[col][1] = y
            areas[col][2] = x
            areas[col][3] = y
    return {explanation[col]: areas[ImageColor.getrgb(col)] for col in explanation}


# def fix_template(img):
#     colors = ['lime', 'yellow', 'magenta', 'red']
#     for x in range(img.width):
#         for y in range(img.height):
#             val = img.getpixel((x, y))
#             if val[0] == val[1] == val[2]:
#                 continue
#             diff = {}
#             for c in colors:
#                 col = ImageColor.getrgb(c)
#                 diff[col] = sum(abs(col[i] - val[i]) ** 3 for i in range(3))
#             mn = min(diff.values())
#             col = [c for c in diff if diff[c] == mn][0]
#             img.putpixel((x, y), col)


def calc_template_and_areas(img_height):
    img = get_template(img_height)
    areas = get_areas(img, explanation)
    draw = ImageDraw.Draw(img)
    draw.rectangle(areas['image'], 'white')
    draw.rectangle(areas['caption'], 'black')
    draw.rectangle(areas['text'], 'black')
    return img, areas


def get_template_and_areas(img_height):
    global memo_templates_areas
    if img_height not in memo_templates_areas:
        memo_templates_areas[img_height] = calc_template_and_areas(img_height)
    res = copy.deepcopy(memo_templates_areas[img_height])
    if len(memo_templates_areas) > MEMOIZATION_LENGTH:
        memo_templates_areas.clear()
        print('CLEARED')
    return res
