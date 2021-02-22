from telethon import events
from telethon.tl.types import MessageMediaPhoto
from Demotivator import make_demotivator
import logging
from Photo import *
from Common import *
from Fonts import get_font_path
from time import time
import re


BOTNAME = 'CreateDemotivatorBot'

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


@bot.on(events.NewMessage(pattern=fr'(?i)^/make({BOTNAME}|)(\s.*|$)', incoming=True))
async def reply(event):
    id = event.chat_id
    message = event.message
    reply = await event.get_reply_message()
    if reply is None or not isinstance(reply.media, MessageMediaPhoto) or reply.media.photo is None:
        await bot.send_message(id, 'To create demotivator, **reply** to a message with a **photo** and add command'
                                   ' `/make` with text.\nCommand example: `/make What? :: It\'s magic`')
        return
    photo = await save_photo(reply.media.photo)
    text = message.raw_text
    match = re.search(fr'(?i)^/make({BOTNAME}|)(|\s+(.*?)(|::(.*)))$', text, re.DOTALL)
    title = match.group(3)
    caption = match.group(5)
    if title is None:
        title = ''
    if caption is None:
        caption = ''
    title = title.strip()
    caption = caption.strip()
    demotivator = make_demotivator(photo, title=title, caption=caption,
                                   font=get_font_path("ThamesC"),
                                   font_caption=get_font_path("Verdana"))
    my_message = await bot.send_message(id, file=get_path(demotivator))
    link_photo_id(my_message.media.photo.id, demotivator)
