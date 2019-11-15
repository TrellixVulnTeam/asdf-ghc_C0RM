import re
import urllib.request

def list_all():
    versions = list_versions()
    print(' '.join(versions))

def list_versions():
    url = 'https://downloads.haskell.org/~ghc/'
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
        return re.findall('\"(\d+\.\d+\.\d+)/\"', content)

if __name__ == '__main__':
    list_all()
