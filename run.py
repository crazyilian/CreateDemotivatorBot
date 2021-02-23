from Photo import fix_tmp, clear_tmp
import bot as bot_handlers
from Common import *


async def f():
    from datetime import datetime
    a = datetime.now()
    s = 'Current date\n' + a.strftime('%d %B %Y %H:%M:%S')
    await bot.send_message(404377069, s)



try:
    fix_tmp()
    clear_tmp()
    # bot.send_message()
    bot.loop.run_until_complete(f())
    bot.run_until_disconnected()
except Exception as e:
    clear_tmp()
