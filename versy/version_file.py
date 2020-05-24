from pathlib import Path
import os
import safer

PREFIX = '__version__ = '
VERSION = 'VERSION'


def read(root):
    results = []
    for filepath in _all_files(root):
        version = _get_version(filepath)
        if version:
            results.append((filepath, version))

    if not results:
        raise ValueError('No version files found')
    if len(results) > 1:
        raise ValueError('More than one version file found', str(results))

    return results[0]


def write(path, version):
    with safer.printer(path) as _print:
        if path.name == VERSION:
            _print(version)
        else:
            for line in Path(path).read_text().splitlines():
                if line.startswith(PREFIX):
                    line = "%s'%s'" % (PREFIX, version)
                _print(line)

    print('Rewrote', path)


def _all_files(root):
    root = Path(root)
    for directory, sub_dirs, files in os.walk(root):
        path = Path(directory)
        if path == root:
            sub_dirs[:] = (i for i in sub_dirs if i not in ('build', 'dist'))

        sub_dirs[:] = (i for i in sub_dirs if not i.startswith('.'))
        files[:] = (i for i in files if not i.startswith('.'))

        yield from (path / f for f in files)


def _get_version(path):
    if path.name == VERSION:
        return path.read_text().strip()

    if not path.suffix == '.py':
        return

    lines = [s for s in path.read_text().splitlines() if s.startswith(PREFIX)]

    if not lines:
        return
    if len(lines) > 1:
        raise ValueError('More than one __version__ = line')

    line = lines[0][len(PREFIX) :].split('#')[0].strip()

    for quote in '"', '\'':
        if len(line) > 2 and line[0] == line[-1] == quote:
            line = line[1:-1]

    return line
