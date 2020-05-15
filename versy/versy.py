import semver
import sys
from . import changelog
from . import commits
from . import version_file

PREFIX = '__version__ = '
VERSION = 'VERSION'


def main(action='patch', path='.'):
    vfile, version = version_file.read(path)

    old = semver.VersionInfo.parse(version)
    new = getattr(old, 'bump_' + action)()

    print('Version', old, '->', new)

    version_file.write(vfile, new)
    cnames = commits.get_commits(version, path)
    changelog.update(path, old, new, cnames)


if __name__ == '__main__':
    main(*sys.argv[1:])
