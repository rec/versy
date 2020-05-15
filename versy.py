from pathlib import Path
import os
import safer
import semver
import sys

PREFIX = '__version__ = '
VERSION = 'VERSION'


def main(action='patch', path='.'):
    path = Path(path)
    version_files = list(_version_files(path))

    if not version_files:
        raise ValueError('No version files found')
    if len(version_files) > 1:
        raise ValueError('More than one version files found')

    path, version = version_files[0]

    ver = semver.VersionInfo.parse(version)
    new_ver = getattr(ver, 'bump_' + action)()

    if path.endswith(VERSION):
        Path(path).write_text('%s\n' % new_ver)
    else:
        lines = Path(path).read_text().splitlines()
        with safer.printer(path, 'w') as pr:
            for line in lines:
                first, *rest = line.strip().split(PREFIX)
                if first:
                    pr(line)
                else:
                    pr("%s'%s'" % (PREFIX, new_ver))


def _version_files(path):
    for directory, sub_dirs, files in os.walk(path):
        sub_dirs[:] = (i for i in sub_dirs if not i.startswith('.'))
        directory = Path(directory)
        if directory == path:
            sub_dirs[:] = (i for i in sub_dirs if i not in ('build', 'dist'))
        for filename in files:
            filepath = directory / filename
            version = _get_version(filepath, filename)
            if version:
                yield path, version


def _get_version(filepath, filename):
    if filename == VERSION:
        return Path(filepath).read_text().strip()

    if not filepath.suffix == '.py':
        return

    lines = [i.strip() for i in filepath.read_text().splitlines() if i.strip()]
    for line in lines:
        first, *rest = line.split(PREFIX, maxsplit=1)
        if not first:
            body = rest[0].strip().split('#')[0]
            for quote in '"', '\'':
                if len(body) > 2 and body[0] == body[-1] == quote:
                    body = body[1:-1]
            return body


if __name__ == '__main__':
    main(*sys.argv[1:])
