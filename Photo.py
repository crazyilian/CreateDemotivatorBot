from Common import *
import os


photos = set()


async def save_photo(photo):
    id = photo.id
    if id not in photos:
        await bot.download_media(photo, get_path(id))
        photos.add(id)
    return get_path(id)


def rename_to_id(name, id):
    os.rename(get_path(name), get_path(id))
    photos.add(id)


def get_id(path):
    return os.path.splitext(os.path.basename(path))[0]


def get_path(name):
    name = str(name)
    if name.startswith(os.path.join('tmp', '')):
        return name
    return os.path.join('tmp', name + '.jpg')


def clear_tmp():
    photos.clear()
    for filename in os.listdir('tmp'):
        os.remove(os.path.join('tmp', filename))


def fix_tmp():
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if len(os.listdir('tmp')) > 200:
        clear_tmp()
