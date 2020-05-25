import wolk

PREFIX = '__version__ = '
VERSION = 'VERSION'


class VersionFile:
    def __init__(self, root, printer):
        self.printer = printer

        results = []
        for file in wolk.python(root):
            version = _get_version(file)
            if version:
                results.append((file, version))

        if not results:
            raise ValueError('No version files found')

        if len(results) > 1:
            raise ValueError('More than one version file found', str(results))

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

        print('Rewrote', self.file)


def _get_version(file):
    if file.name == VERSION:
        return file.read_text().strip()

    if not file.suffix == '.py':
        return

    lines = [s for s in file.read_text().splitlines() if s.startswith(PREFIX)]

    if lines:
        if len(lines) > 1:
            raise ValueError('More than one line starting "%s"' % PREFIX)

        line = lines[0]
        line = line[len(PREFIX) :]
        line = line.split('#')[0].strip()

        for quote in '"', "'":
            if len(line) > 2 and line[0] == line[-1] == quote:
                line = line[1:-1]

        return line
