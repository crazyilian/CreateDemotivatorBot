from Photo import fix_tmp, clear_tmp
import bot as bot_handlers
from Common import *


try:
    fix_tmp()
    clear_tmp()
    bot.run_until_disconnected()
except Exception as e:
    clear_tmp()
