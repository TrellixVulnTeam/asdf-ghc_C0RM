import gzip
import os
import platform
import re
import subprocess
import urllib.request

bar = {
  'Debian': 'deb'
}

def install(path, version):
    urls = assets_urls(version)
    print(list(urls))
    os.mkdir(f"{path}/bin")
    return f"{path}/bin"

def assets_urls(version, system = platform.system(), machine = platform.machine()):
    url = f"https://downloads.haskell.org/~ghc/{version}/"
    system = system.lower()
    machine = machine.lower()

    def url_and_tags(name):
        tags = name.replace('.tar.xz', '').split('-')[2::]
        tags.remove(system)
        tags.remove(machine)
        return (f"{url}{name}", tags)

    with urllib.request.urlopen(url) as res:
        content = res.read().decode('utf-8')
        return map(
            url_and_tags,
            filter(
                lambda url: system in url and machine in url,
                re.findall(f"\"(ghc-{version}-.*\.tar\.xz)\"", content)
            )
        )
