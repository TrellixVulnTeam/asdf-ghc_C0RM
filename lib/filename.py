import re


def parse_filename(filename):
    values = filename.replace('.tar.xz', '').split('-')
    return {
        'filename': filename,
        'distro': __parse_distro(values[3]),
        'extras': values[5:]
    }


def __parse_distro(distro):
    values = next(iter(re.findall('([a-z]+)(.*)', distro)))
    if values[1]:
        return {'name': values[0], 'version': float(values[1])}

    return {'name': values[0], 'version': 0}
