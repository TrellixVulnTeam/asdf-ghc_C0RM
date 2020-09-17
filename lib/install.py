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


def install(install_dir, version):
    filenames = __filter_by_distro(__get_filenames(version))
    print(list(filenames))
    return None

def __filter_by_distro(filenames):
    distro = __normalize_distro(subprocess.check_output(['lsb_release', '-irs']))
    def by_distro(filename):
      return distro['name'] == filename['distro']['name'] and distro['version'] >= filename['distro']['version']

    return filter(by_distro, filenames)

def __normalize_distro(distro):
  values = distro.decode('utf-8').split()
  if values[0] == 'Debian':
    return { 'name': 'deb', 'version': float(values[1]) }

  return { 'name': values[0], 'version': float(values[1]) }

def __get_filenames(version):
    def is_tarball(filename):
      return ARCH in filename and OS in filename and filename.endswith('.tar.xz')

    with urllib.request.urlopen(f'{BASE_URL}{version}/') as resp:
        content = resp.read().decode('utf-8')
        return map(
          __parse_filename,
          filter(is_tarball, re.findall('(?<=href=")(ghc-.*)(?=")', content))
        )


def __parse_filename(filename):
    values = filename.replace('.tar.xz', '').split('-')
    return {
      'filename': filename,
      'distro': __parse_distro(values[3]),
      'extras': values[5:]
    }


def __parse_distro(distro):
    values = next(iter(re.findall('([a-z]+)(\d+)', distro)))
    return { 'name': values[0], 'version': float(values[1]) }


if __name__ == '__main__':
    install_dir = os.environ['ASDF_INSTALL_PATH']
    version = os.environ['ASDF_INSTALL_VERSION']
    install(install_dir, version)
