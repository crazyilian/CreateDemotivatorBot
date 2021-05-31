from PIL import Image, ImageDraw, ImageFont
import Fonts
from random import randint
from Photo import get_path


image_width = 616
image_max_height = 800
image_min_height = 400
demotivator_width = 750


class Demotivator:

    def __init__(self, imgW, imgH, font_title, font_caption):
        self.font_title = font_title
        self.font_caption = font_caption

        imgH = imgH * image_width // imgW
        imgW = image_width
        imgH = min(imgH, image_max_height)
        imgH = max(imgH, image_min_height)
        self.imgW = imgW
        self.imgH = imgH
        self.outline = 11
        self.outlineW = 3

        self.w = demotivator_width
        ident = (demotivator_width - image_width) // 2
        self.ident = ident

        self.textW = imgW + self.outline * 2
        self.textEndH = ident + imgH + self.outline + ident // 2
        self.h = self.textEndH + ident // 2

        self.imgStart = (ident, ident)
        self.imgEnd = (self.imgStart[0] + imgW, self.imgStart[1] + imgH)

        self.build()

    def build(self):
        self.img = Image.new('RGB', (self.w, self.h), 'black')
        self.imgd = ImageDraw.Draw(self.img)
        d1 = self.outline
        d2 = self.outline - self.outlineW
        self.imgd.rectangle(((self.imgStart[0] - d1, self.imgStart[1] - d1),
                             (self.imgEnd[0] + d1, self.imgEnd[1] + d1)), fill='white')
        self.imgd.rectangle(((self.imgStart[0] - d2, self.imgStart[1] - d2),
                             (self.imgEnd[0] + d2, self.imgEnd[1] + d2)), fill='black')

    def add_photo(self, photo=None):
        if photo:
            photo = photo.resize((self.imgW, self.imgH))
            self.img.paste(photo, self.imgStart)
        else:
            self.imgd.rectangle((self.imgStart, self.imgEnd), fill='white')

    def get_font_size(self, font, text):
        ascent, descent = font.getmetrics()
        text_width = font.getmask(text).getbbox()[2]
        text_height = font.getmask(text).getbbox()[3] + descent
        return (text_width, text_height)

    def get_max_font_size(self, font_path, text, min, max):
        l, r = min, max + 1
        while (r - l > 1):
            m = (l + r) // 2
            font = ImageFont.truetype(font_path, m)
            w, h = font.getsize(text)
            if w > self.textW:
                r = m
            else:
                l = m
        return l

    def get_font_start(self, font, text):
        w, h = font.getsize(text)
        cent = self.ident - self.outline + self.textW // 2
        start = cent - w // 2
        return (start, self.textEndH)

    def fix_width(self):
        new_h = self.textEndH + self.ident // 2
        self.h = new_h
        self.img = self.img.crop((0, 0, self.w, new_h))
        self.imgd = ImageDraw.Draw(self.img)

    def add_title(self, text):
        font_path = self.font_title
        sz = self.get_max_font_size(font_path, text, min=50, max=110)
        font = ImageFont.truetype(font_path, sz)
        start = self.get_font_start(font, text)
        self.textEndH += font.getsize(text)[1] + self.ident // 2
        self.fix_width()
        self.imgd.text(start, text, 'white', font=font)

    def add_caption(self, text):
        font_path = self.font_caption
        sz = self.get_max_font_size(font_path, text, min=30, max=40)
        font = ImageFont.truetype(font_path, sz)
        start = self.get_font_start(font, text)
        self.textEndH += font.getsize(text)[1]
        self.fix_width()
        self.imgd.text(start, text, 'white', font=font)

    def add_text(self, title=None, caption=None):
        if title:
            title = title.replace('\n', ' ')
            self.add_title(title)
        if caption:
            captions = caption.split('\n')
            for c in captions:
                self.add_caption(c)

    def save(self, path, *args, **kwargs):
        self.img.save(path, *args, **kwargs)


def make_demotivator(img_name, title=None, caption=None, font_title=None, font_caption=None):
    if not font_title:
        font_title = Fonts.get_font_path('ThamesC')
    if not font_caption:
        font_caption = Fonts.get_font_path('Verdana')
    img = Image.open(get_path(img_name)).convert('RGB')
    dem = Demotivator(*img.size, font_title, font_caption)
    dem.add_photo(img)
    dem.add_text(title=title, caption=caption)
    name = hex(randint(1, 2**128 - 1))[2:]
    dem.save(get_path(name))
    return get_path(name)
