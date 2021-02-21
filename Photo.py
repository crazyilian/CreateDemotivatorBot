import os
from Common import *


id_to_name = {}


async def save_photo(photo):
    id = photo.id
    if id not in id_to_name:
        name = str(id)
        id_to_name[id] = name
        await bot.download_media(photo, get_path(name))
    else:
        name = id_to_name[id]
    return name


def link_photo_id(id, dst):
    id_to_name[id] = dst


def get_name(path):
    return os.path.splitext(os.path.basename(path))[0]


def get_path(name):
    return os.path.join('tmp', name + '.jpg')


def next_photo_name(filename):
    if filename is None:
        return random_sequence(20)
    filename += '_'
    prefixes = (name[len(filename):] for name in id_to_name.values() if name.startswith(filename))
    matched = (name for name in prefixes if '_' not in name)
    numbers = (0,) + tuple(int(name) for name in matched if name.isdigit())
    last = max(numbers)
    filename += str(last + 1)
    if len(filename) > 64:
        print(filename)
        filename = random_sequence(20)
    return filename


def clear_tmp():
    id_to_name.clear()
    for filename in os.listdir('tmp'):
        os.remove(os.path.join('tmp', filename))


def fix_tmp():
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if len(os.listdir('tmp')) > 200:
        clear_tmp()
