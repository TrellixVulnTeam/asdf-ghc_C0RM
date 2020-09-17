from distutils.version import StrictVersion

import gzip
import re
import urllib.request

URL = 'https://downloads.haskell.org/~ghc/'


def list_all(printer=print):
    versions = sorted(__extract_versions(__downloads_page()))
    printer(' '.join(__versions_to_string(versions)))


def __versions_to_string(versions):
    return map(lambda version: str(version), versions)


def __extract_versions(page):
    return map(
        lambda version: StrictVersion(version),
        re.findall('(?<=href=")([0-9]+.[0-9]+.[0-9]+)(?=/")', page)
    )


def __downloads_page():
    with urllib.request.urlopen(URL) as resp:
        return resp.read().decode('utf-8')


if __name__ == '__main__':
    list_all()
