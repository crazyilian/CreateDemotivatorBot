from telethon import events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
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
    smth_wrong_msg = 'To create demotivator, **reply** to a message with a **photo** and add command `/make` with ' \
                     'text.\nCommand example: `/make What? :: It\'s magic` '
    if reply is None:
        await event.respond(smth_wrong_msg)
        return
    elif isinstance(reply.media, MessageMediaPhoto) and reply.media.photo is not None:
        photo = await save_photo(reply.media.photo)
    elif isinstance(reply.media, MessageMediaDocument) \
            and reply.media.document is not None \
            and reply.media.document.mime_type.startswith('image'):
        photo = await save_photo(reply.media.document)
    else:
        await event.respond(smth_wrong_msg)
        return
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
    print(event.chat.id, '::', event.chat.username)


@bot.on(events.NewMessage(pattern=fr'(?i)^/help({BOTNAME}|)(\s|$)', incoming=True))
async def help(event):
    await event.respond('''**Hello!**

🍉 This bot is designed to create demotivators from any picture you want.

🥥 To use this bot, just send here your picture. Then **reply** to it with the command:
```/make [title] :: [caption]```

🍍 To see this message again, send the `/help` command.

🍒 Enjoy!
''')


@bot.on(events.NewMessage(pattern=fr'(?i)^/start({BOTNAME}|)(\s|$)', incoming=True))
async def start(event):
    await help(event)

# user_data = {'404377069': {
#     'title': {'font': 'thamesc', 'bold': False, 'italic': False, 'size': {'type': 'auto', 'auto': [50, 110], 'fixed': 100}},
#     'caption': {'font': 'verdana', 'bold': False, 'italic': False, 'size': {'type': 'auto', 'auto': [30, 40], 'fixed': 40}},
#     'image': {}
# }}
