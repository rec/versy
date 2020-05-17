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
    if path.name == VERSION:
        _write_file(path, version)
    else:
        _write_python(path, version)


def _all_files(root):
    root = Path(root)
    for directory, sub_dirs, files in os.walk(root):
        path = Path(directory)
        if path == root:
            sub_dirs[:] = (i for i in sub_dirs if i not in ('build', 'dist'))

        sub_dirs[:] = (i for i in sub_dirs if not i.startswith('.'))
        files[:] = (i for i in files if not i.startswith('.'))

        yield from (path / f for f in files)


def _get_version(filepath):
    if filepath.name == VERSION:
        return filepath.read_text().strip()

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


def _write_file(path, version):
    Path(path).write_text('%s\n' % version)
    print('Rewrote', path)


def _write_python(path, version):
    lines = Path(path).read_text().splitlines()
    found_line = -1
    with safer.printer(path, 'w') as _print:
        for i, line in enumerate(lines):
            first, *rest = line.strip().split(PREFIX)
            if first or not rest:
                _print(line)
            else:
                print('FOUND', i, line)
                if found_line >= 0:
                    raise ValueError(
                        'More than one version was found',
                        str(found_line),
                        str(i),
                    )
                found_line = i + 1
                _print("%s'%s'" % (PREFIX, version))
        if found_line < 0:
            raise ValueError('No version found')

    print('Rewrote %s:%d' % (path, found_line))
