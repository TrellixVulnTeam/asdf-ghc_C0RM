from lib.distro import get_distro
from lib.filename import parse_filename

import os
import platform
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

ARCH = platform.machine()
BASE_URL = 'https://downloads.haskell.org/~ghc'
OS = sys.platform


def main(install_dir, version):
    filename = __downloadable_filename(
      __sort_by_distro_version(__filter_by_distro(__get_filenames(version)))
    )
    return __install(
      install_dir,
      version,
      '%s/%s/%s' % (BASE_URL, version, filename['filename'])
    )


def __downloadable_filename(filenames):
    def no_extras(filename):
        return len(filename['extras']) == 0

    return next(filter(no_extras, filenames))


def __sort_by_distro_version(filenames):
    def by_distro_version(filename):
        return filename['distro']['version']

    return sorted(filenames, key=by_distro_version, reverse=True)


def __filter_by_distro(filenames):
    distro = get_distro()

    def by_distro(filename):
        is_name = distro['name'] == filename['distro']['name']
        is_version = distro['version'] >= filename['distro']['version']
        return is_name and is_version

    return filter(by_distro, filenames)


def __get_filenames(version):
    def is_tarball(filename):
        is_arch = ARCH in filename
        is_os = OS in filename
        return is_arch and is_os and filename.endswith('tar.xz')

    with urllib.request.urlopen('%s/%s/' % (BASE_URL, version)) as resp:
        content = resp.read().decode('utf-8')
        return map(
          parse_filename,
          filter(is_tarball, re.findall('(?<=href=")(ghc-.*)(?=")', content))
        )


def __install(install_dir, version, url):
    with tempfile.TemporaryDirectory() as download_dir:
        path, _ = urllib.request.urlretrieve(
            url,
            '%s/ghc.tar.xz' % download_dir
        )
        with tarfile.open(path) as tar:
            tar.extractall(download_dir)
            working_dir = '%s/ghc-%s' % (download_dir, version)
            subprocess.run(
                ['./configure', '--prefix=%s' % install_dir],
                cwd=working_dir
            )
            subprocess.run(
                ['make', 'install'],
                cwd=working_dir
            )


if __name__ == '__main__':
    install_dir = os.environ['ASDF_INSTALL_PATH']
    version = os.environ['ASDF_INSTALL_VERSION']
    main(install_dir, version)
