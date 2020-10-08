from pathlib import Path
import wolk

PREFIX = '__version__ = '
VERSION = 'VERSION'


class VersionFile:
    def __init__(self, root, printer, file=None):
        self.printer = printer
        if file:
            self.file = Path(file)
            self.version = _get_version(self.file)
        else:
            results = []
            for f in wolk.python(root):
                f = Path(f)
                version = _get_version(f)
                if version:
                    results.append((f, version))

            if not results:
                raise ValueError('No version files found')

            if len(results) > 1:
                res = ', '.join('{1} in {0}'.format(*r) for r in results)
                raise ValueError('More than one version file found: ' + res)

            self.file, self.version = results[0]

    def write(self, version):
        with self.printer(self.file) as _print:
            if self.file.name == VERSION:
                _print(version)

            else:
                for line in self.file.read_text().splitlines():
                    if line.startswith(PREFIX):
                        line = "%s'%s'" % (PREFIX, version)
                    _print(line)


def _get_version(f):
    if f.name == VERSION:
        return f.read_text().strip()
    if f.suffix != '.py':
        return

    lines = [s for s in f.read_text().splitlines() if s.startswith(PREFIX)]

    if not lines:
        return

    if len(lines) > 1:
        raise ValueError('More than one line starting "%s"' % PREFIX)

    line = lines[0]
    line = line[len(PREFIX) :]
    line = line.split('#')[0].strip()

    for quote in '"', "'":
        if len(line) > 2 and line[0] == line[-1] == quote:
            line = line[1:-1]

    return line
