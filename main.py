from PIL import Image, ImageDraw, ImageFont
import Template
import time



def add_image(template, areas, img):
    rect = areas['image']
    img = img.resize((rect[2] - rect[0] + 1, rect[3] - rect[1] + 1))
    template.paste(img, (rect[0], rect[1]))


def add_text(template, areas, area_name, text, font_path, min_size=10, max_size=70):
    if not text:
        return
    rect = areas[area_name]
    font = get_font(font_path, text, rect[2] - rect[0], rect[3] - rect[1], min_size, max_size)
    draw = ImageDraw.Draw(template)
    center_x = (rect[0] + rect[2]) // 2
    center_y = (rect[1] + rect[3]) // 2
    text_width, text_height = get_text_size(font, text)
    h = center_y - text_height // 2
    lines = text.split('\n')
    if 'thamesc' not in font_path and 'uni-sans' not in font_path:
        h -= 14
    for line in lines:
        draw.text((center_x, h), line, 'white', font=font, anchor='ma')
        h += min(font.getsize(line)[1], font.size)


def make_demotivator(img=None, title=None, caption=None, font=None, font_caption=None):
    if not img:
        template, areas = Template.get_template_areas(Template.IMAGE_MAX_HEIGHT)
    else:
        new_height = img.height * Template.IMAGE_WIDTH // img.width
        new_height = max(new_height, Template.IMAGE_MIN_HEIGHT)
        new_height = min(new_height, Template.IMAGE_MAX_HEIGHT)
        template, areas = Template.get_template_areas(new_height)
    if img:
        add_image(template, areas, img)
    if caption:
        if title:
            add_text(template, areas, 'title', title, font)
        add_text(template, areas, 'caption', caption, font_caption, max_size=29)
    else:
        if title:
            add_text(template, areas, 'text', title, font)
        template = template.crop((0, 0, template.width, template.height - (areas['caption'][3] - areas['caption'][1])))
    return template


def get_text_size(font, text):
    w, h = 0, 0
    for line in text.split('\n'):
        ww, hh = font.getsize(line)
        h += min(hh, font.size)
        w = max(w, ww)
    return w, h


def get_font(path, text, w, h, min, max):
    l, r = min, max + 1
    while r - l > 1:
        m = (l + r) // 2
        font = ImageFont.truetype(path, m)
        fw, fh = get_text_size(font, text)
        if fw > w or fh > h:
            r = m
        else:
            l = m
    return ImageFont.truetype(path, l)


font = "fonts/thamesc-regular.ttf"
font_caption = "fonts/verdana-regular.ttf"

tic = time.time()
img = make_demotivator(img=Image.open('megumin.jpg'),
                       title='Кто?',
                       caption='Не знаю',
                       font=font, font_caption=font_caption)

img = make_demotivator(img=img,
                       title='Мегумин',
                       font=font, font_caption=font_caption)

img = make_demotivator(img=img,
                       title='А Мегумакс?',
                       # caption='ахахахпхахапахпхапапахп',
                       font=font, font_caption=font_caption)

img = make_demotivator(img=img,
                       title='Ладно',
                       caption='Прохладно',
                       font=font, font_caption=font_caption)

print('time:', time.time() - tic)
Template.showmem()

img.save('temp.png')
time.sleep(300)
