from pathlib import Path
import json
import wolk

PREFIX = '__version__ = '
VERSION = 'VERSION'
DOTFILE = '.versy.json'


class VersionFile:
    def __init__(self, root, printer, version_file=None):
        self.printer = printer
        self.file, self.version = _get_version(version_file, root)

    def write(self, version):
        with self.printer(self.file) as print:
            if self.file.name == VERSION:
                print(version)
                return

            for line in self.file.read_text().splitlines():
                if line.startswith(PREFIX):
                    line = "%s'%s'" % (PREFIX, version)
                print(line)


def _get_version(version_file, root):
    if not version_file:
        df = Path(root) / DOTFILE
        if df.exists():
            version_file = json.loads(df.read_text()).get('version_file')
    files = [version_file] if version_file else wolk.python(root)

    results = []
    for f in files:
        f = Path(f)

        if f.name == VERSION:
            results.append((f, f.read_text().strip()))

        elif f.suffix == '.py':
            for line in f.read_text().splitlines():
                if line.startswith(PREFIX):
                    value = line[len(PREFIX) :]
                    value = value.split('#')[0].strip()

                    for quote in '"', "'":
                        if len(value) > 2 and value[0] == value[-1] == quote:
                            value = value[1:-1]

                    results.append((f, value))

    if not results:
        raise ValueError('No version files found')

    if len(results) > 1:
        res = ', '.join('{1} in {0}'.format(*r) for r in results)
        raise ValueError('More than one version file found: ' + res)

    assert len(results[0]) == 2, str(len(results[0]))
    return results[0]
