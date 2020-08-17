from functools import reduce

import csv
import glob
import gzip
import os
import platform
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

NAMES = {
  'debian': 'deb'
}

def install(install_dir, version):
  urls = __compatible_urls(__downloadable_urls(version))
  info = __distro()
  url = __specific_url(urls, info)
  return __install_from_url(install_dir, version, url)

def __specific_url(urls, info):
  filtered_urls = filter(lambda url: f'{info[0]}{info[1]}' in url and url.endswith('tar.xz'), urls)
  return next(filtered_urls, None)

def __install_from_url(install_dir, version, url):
  with tempfile.TemporaryDirectory() as download_dir:
    path, _ = urllib.request.urlretrieve(url, f"{download_dir}/ghc.tar.xz")
    with tarfile.open(path) as tar:
      tar.extractall(download_dir)
      working_dir = f'{download_dir}/ghc-{version}'
      subprocess.run(['./configure', f'--prefix={install_dir}'], cwd=working_dir)
      subprocess.run(['make', 'install'], cwd=working_dir)
      return True

def __distro():
  info = __os_release()
  return (NAMES[info['ID']], int(info['VERSION_ID']))

def __os_release():
  def row_to_info(info, row):
    info[row[0]] = row[1]
    return info

  with open('/etc/os-release') as f:
    return reduce(row_to_info, csv.reader(f, delimiter='='), {})

def __compatible_urls(urls):
  arch = platform.machine()
  os = sys.platform
  return filter(lambda url: arch in url and os in url, urls);

def __downloadable_urls(version):
  base_url = f'https://downloads.haskell.org/~ghc/{version}/'
  with urllib.request.urlopen(base_url) as resp:
    html = gzip.decompress(resp.read()).decode('utf-8')
    targets = re.findall('href="(.*)"', html)
    return map(
      lambda filename: f'{base_url}{filename}',
      filter(__is_downlodable(version), targets)
    )

def __is_downlodable(version):
  def zoo(target):
    return target.startswith(f'ghc-{version}') and not target.endswith('.sig')

  return zoo

if __name__ == '__main__':
  install_dir = os.environ['ASDF_INSTALL_PATH']
  version = os.environ['ASDF_INSTALL_VERSION']
  install(install_dir, version)
