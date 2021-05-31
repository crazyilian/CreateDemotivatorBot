from telethon import events
from telethon.tl.types import MessageMediaPhoto
import logging
from Photo import save_photo, rename_to_id
from Common import *
from Fonts import get_font_path
import re
from Demotivator import make_demotivator


BOTNAME = 'CreateDemotivatorBot'

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


@bot.on(events.NewMessage(pattern=fr'(?i)^/make({BOTNAME}|)(\s|$)', incoming=True))
async def make(event):
    message = event.message
    reply = await event.get_reply_message()
    if reply is None or not isinstance(reply.media, MessageMediaPhoto) or reply.media.photo is None:
        await event.respond('To create demotivator, **reply** to a message with a **photo** and add command'
                            ' `/make` with text.\nCommand example: `/make What? :: It\'s magic`')
        return
    photo = await save_photo(reply.media.photo)
    text = message.raw_text
    match = re.search(fr'(?i)^/make({BOTNAME}|)(|\s+(.*?)(|::(.*)))$', text, re.DOTALL)
    title = match.group(3)
    caption = match.group(5)
    if title:
        title = title.strip()
    if caption:
        caption = caption.strip()
    demotivator = make_demotivator(photo, title=title, caption=caption,
                                   font_title=get_font_path("ThamesC"),
                                   font_caption=get_font_path("Verdana"))
    my_message = await event.respond(file=demotivator)
    rename_to_id(demotivator, my_message.media.photo.id)

# user_data = {'404377069': {
#     'title': {'font': 'thamesc', 'bold': False, 'italic': False, 'size': {'type': 'auto', 'auto': [50, 110], 'fixed': 100}},
#     'caption': {'font': 'verdana', 'bold': False, 'italic': False, 'size': {'type': 'auto', 'auto': [30, 40], 'fixed': 40}},
#     'image': {}
# }}
