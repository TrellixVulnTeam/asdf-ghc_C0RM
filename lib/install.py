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


def install(install_dir, version):
    filename = __downloadable_filename(
      __sort_by_distro_version(__filter_by_distro(__get_filenames(version)))
    )
    return __download_and_install(
      install_dir,
      version,
      f"{BASE_URL}/{version}/{filename['filename']}"
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
    distro = __normalize_distro(
        subprocess.check_output(['lsb_release', '-irs'])
    )

    def by_distro(filename):
        is_name = distro['name'] == filename['distro']['name']
        is_version = distro['version'] >= filename['distro']['version']
        return is_name and is_version

    return filter(by_distro, filenames)


def __normalize_distro(distro):
    values = distro.decode('utf-8').split()

    if values[0] == 'Debian':
        return {'name': 'deb', 'version': float(values[1])}

    return {'name': values[0], 'version': float(values[1])}


def __get_filenames(version):
    def is_tarball(filename):
        is_arch = ARCH in filename
        is_os = OS in filename
        return is_arch and is_os and filename.endswith('tar.xz')

    with urllib.request.urlopen(f'{BASE_URL}/{version}/') as resp:
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
    values = next(iter(re.findall('([a-z]+)(.+)', distro)))
    return {'name': values[0], 'version': float(values[1])}


def __download_and_install(install_dir, version, url):
    with tempfile.TemporaryDirectory() as download_dir:
        path, _ = urllib.request.urlretrieve(url, f"{download_dir}/ghc.tar.xz")
        with tarfile.open(path) as tar:
            tar.extractall(download_dir)
            working_dir = f'{download_dir}/ghc-{version}'
            subprocess.run(
                ['./configure', f'--prefix={install_dir}'],
                cwd=working_dir
            )
            subprocess.run(
                ['make', 'install'],
                cwd=working_dir
            )


if __name__ == '__main__':
    install_dir = os.environ['ASDF_INSTALL_PATH']
    version = os.environ['ASDF_INSTALL_VERSION']
    install(install_dir, version)
