families = ['thamesc', 'uni-sans', 'verdana']
single = ['impact', 'lobster', 'comic-sans']


def get_font_path(name, bold=False, italic=False):
    name = name.lower().replace(' ', '-')
    if name in single:
        return f'fonts/{name}.ttf'
    if name in families:
        suffix = ''
        if bold:
            suffix += '-bold'
        if italic:
            suffix += '-italic'
        if not suffix:
            suffix += '-regular'
        return f'fonts/{name + suffix}.ttf'
    raise Exception(f'Unknown font name: {name}')
