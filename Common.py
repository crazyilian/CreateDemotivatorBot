import psutil
import os
from telethon import TelegramClient


bot = TelegramClient('bot', int(os.environ['API_ID']), os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])


def showmem():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss
    print(mem / 1024 / 1024, 'MB')
