from dataclasses import dataclass

import gzip
import os
import platform
import re
import subprocess
import sys
import urllib.request

ARCH = platform.machine()
BASE_URL = 'https://downloads.haskell.org/~ghc/'
OS = sys.platform


@dataclass(init=False)
class Distro:
  name: str
  version: float

  def __init__(self, distro):
    values = next(iter(re.findall('([a-z]+)(.+)', distro)))
    self.name = values[0]
    self.version = float(values[1])

@dataclass(init=False)
class Filename:
  filename: str
  distro: Distro

  def __init__(self, filename):
    values = filename.replace('.tar.xz', '').split('-')
    self.filename = filename
    self.distro = Distro(values[3]) if len(values) >= 2 else None
    print(values)



def install(install_dir, version):
    filenames = __get_filenames(version)
    print(list(filenames))
    return None


def __get_filenames(version):
    def is_tarball(filename):
      return ARCH in filename and OS in filename and filename.endswith('.tar.xz')

    with urllib.request.urlopen(f'{BASE_URL}{version}/') as resp:
        content = gzip.decompress(resp.read()).decode('utf-8')
        return map(
          Filename,
          filter(is_tarball, re.findall('(?<=href=")(ghc-.*)(?=")', content))
        )


def __filename(filename):
  values = filename.split('-')
  print(values)
  if len(values) >= 2:
    return {
      'filename': filename,
      'distro': __distro(values[3]),
    }

  return {
    'filename': filename,
    'distro': None,
  }


def __distro(distro):
  values = next(iter(re.findall('([a-z]+)(\d+)', distro)), None)
  if values:
    return { 'name': values[0], 'version': int(values[1]) }

  return None


if __name__ == '__main__':
    install_dir = os.environ['ASDF_INSTALL_PATH']
    version = os.environ['ASDF_INSTALL_VERSION']
    install(install_dir, version)
