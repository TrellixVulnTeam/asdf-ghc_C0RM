import csv
import sys


def get_distro(os_name=sys.platform):
    if os_name == 'linux':
        release = os_release()
        if release['ID'] == 'debian':
            return {'name': 'deb', 'version': float(release['VERSION_ID'])}

        return {'name': release['ID'], 'version': float(release['VERSION_ID'])}

    return {'name': 'apple', 'version': 0.0}


def os_release():
    def not_empty(values):
        return len(values) == 2

    with open('/etc/os-release', 'r') as f:
        return dict(filter(not_empty, csv.reader(f, delimiter='=')))
