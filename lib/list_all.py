from distutils.version import StrictVersion

import gzip
import re
import urllib.request

URL = 'https://downloads.haskell.org/~ghc/'


def list_all(printer=print):
  print(list(map(lambda a: str(a), sorted(list(__bar(__foo()))))))


def __bar(html):
    return map(
        lambda version: StrictVersion(version),
        re.findall('(?<=href=")([0-9]+\.[0-9]+\.[0-9]+)(?=/")', html)
    )


def __foo():
    with urllib.request.urlopen(URL) as resp:
        return gzip.decompress(resp.read()).decode('utf-8')


if __name__ == '__main__':
    list_all()
