import psutil
import os
from telethon import TelegramClient
import random
from string import ascii_lowercase, digits


def random_sequence(size):
    return ''.join(random.choices(ascii_lowercase + digits, k=size))



bot = TelegramClient('bot', int(os.environ['API_ID']), os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])


def showmem():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss
    print(mem / 1024 / 1024, 'MB')
