import gzip
import os
import platform
import re
import urllib.request

def install(path, version):
    urls = assets_urls(version)
    print(list(foo(urls)))
    os.mkdir(f"{path}/bin")
    return f"{path}/bin"

def assets_urls(version):
    url = f"https://downloads.haskell.org/~ghc/{version}/"
    with urllib.request.urlopen(url) as res:
        content = gzip.decompress(res.read()).decode()
        return map(
            lambda name: f"{url}{name}",
            re.findall('\"(ghc-.*\.tar\.xz)\"', content)
        )

def foo(urls, system = platform.system(), machine = platform.machine()):
    return filter(
        lambda url: system.lower() in url and machine.lower() in url,
        urls
    )
