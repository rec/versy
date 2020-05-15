from pathlib import Path
import safer

PREFIX = '__version__ = '
VERSION = 'VERSION'


def read(all_files):
    results = []
    for filepath in all_files:
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


def _write_file(path, version):
    Path(path).write_text('%s\n' % version)
    print('Rewrote', path)


def _write_python(path, version):
    lines = Path(path).read_text().splitlines()
    found_line = -1
    with safer.printer(path, 'w') as _print:
        for i, line in enumerate(lines):
            first, *rest = line.strip().split(PREFIX)
            if first:
                _print(line)
            else:
                if found_line >= 0:
                    raise ValueError('More than one version was found')
                found_line = i + 1
                _print("%s'%s'" % (PREFIX, version))
        if found_line < 0:
            raise ValueError('No version found')

    print('Rewrote %s:%d' % (path, found_line))