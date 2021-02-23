from telethon import events
from telethon.tl.types import MessageMediaPhoto
from telethon.tl.custom import Button
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from Demotivator import make_demotivator
import logging
from Photo import *
from Common import *
from Fonts import get_font_path
from time import time
import re
import traceback
import asyncio


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
    if title is None:
        title = ''
    if caption is None:
        caption = ''
    title = title.strip()
    caption = caption.strip()
    demotivator = make_demotivator(photo, title=title, caption=caption,
                                   font=get_font_path("ThamesC"),
                                   font_caption=get_font_path("Verdana"))
    my_message = await event.respond(file=get_path(demotivator))
    link_photo_id(my_message.media.photo.id, demotivator)


def text_wordwrap(text_type, chosen):
    def button(text, data):
        return Button.inline(
            '✅ ' * (chosen.lower() == data.lower()) + text,
            text_type + '/wordwrap/' + data
        )

    text = f'**Word wrap settings for {text_type}**\n' \
           '• **Custom** - only your new lines are used\n' \
           '• **Auto wrap** - only auto new lines are used\n' \
           '• **Mixed** - your new lines are used but auto wrap can add more new lines\n\n' \
           '__Auto wrap will add new lines if text size reaches minimum size limit__'
    buttons = [
        [button('Custom', 'custom'), button('Auto wrap', 'auto'), button('Mixed', 'mixed')],
        [button('Back', 'back')]
    ]
    return text, buttons


user_data = {'404377069': {
    'title': {'font': 'thamesc', 'bold': False, 'italic': False, 'size': {'type': 'auto', 'auto': [10, 80], 'fixed': 80},
              'wordwrap': 'mixed'},
    'caption': {'font': 'verdana', 'bold': False, 'italic': False, 'size': {'type': 'auto', 'auto': [10, 29], 'fixed': 29},
                'wordwrap': 'mixed'},
    'image': {}
}}


def message_by_path(id, path):
    parts = path.split('/')
    if path in ('title', 'caption'):
        pass


# @bot.on(events.NewMessage(pattern=fr'(?i)^/text({BOTNAME}|)(\s|$)', incoming=True))
# async def settings(event):
#     text, buttons = text_wordwrap('title', 'mixed')
#     await event.respond(text, buttons=buttons)


processing_callbacks = set()


@bot.on(events.CallbackQuery())
async def callbackhandler(event):
    id = event.chat_id
    if id in processing_callbacks:
        await event.answer()
        print('oh')
        return
    processing_callbacks.add(id)

    # # # # # # # # # # # # # # # #

    path = event.data.decode().split('/')
    val = path[-1]
    if val == 'back':
        text = 'lol'
        buttons = None
    elif path[1] == 'wordwrap':
        text, buttons = text_wordwrap(path[0], val)

    # # # # # # # # # # # # # # # #

    try:
        await event.edit(text, buttons=buttons)
    except MessageNotModifiedError:
        print(f'Message Not Modified: too more queries from {id}')
        await asyncio.sleep(2)
    except Exception as e:
        traceback.print_exc()
        await asyncio.sleep(2)
    processing_callbacks.remove(id)
