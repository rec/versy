from pathlib import Path
import os
import semver
import sys
from . import commits
from . import version_file

PREFIX = '__version__ = '
VERSION = 'VERSION'


def main(action='patch', path='.'):
    all_files = list(_all_files(path))

    path, version = version_file.read(all_files)

    old = semver.VersionInfo.parse(version)
    new = getattr(old, 'bump_' + action)()

    print('Version', old, '->', new)
    version_file.write(path, str(new))
    commits.get_commits(version, path)


def _all_files(root):
    root = Path(root)
    for directory, sub_dirs, files in os.walk(root):
        path = Path(directory)
        if path == root:
            sub_dirs[:] = (i for i in sub_dirs if i not in ('build', 'dist'))

        sub_dirs[:] = (i for i in sub_dirs if not i.startswith('.'))
        files[:] = (i for i in files if not i.startswith('.'))

        yield from (path / f for f in files)


if __name__ == '__main__':
    main(*sys.argv[1:])
