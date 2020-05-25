from . import git
from datetime import date
from pathlib import Path

NAMES = 'CHANGELOG', 'CHANGELIST', 'CHANGES', 'changelog'
SUFFIXES = {'', '.rst', '.txt', '.md'}


class ChangeLog:
    def __init__(self, path, version, file, printer, message):
        self.path = path
        self.version = version
        self.printer = printer
        self.file = file
        self.message = message

        if not self.file:
            files = []
            for name in NAMES:
                for f in Path(path).iterdir():
                    if f.stem == name and f.suffix in SUFFIXES:
                        files.append(f)
            if len(files) > 1:
                raise ValueError('Multiple changelogs: ' + ' '.join(files))
            if files:
                self.file = files[0]

    def new(self):
        file = Path(self.file or NAMES[0])
        if file.exists():
            raise ValueError('File %s already exists' % file.absolute())

        with self.printer(file) as print:
            self._entry(self.version, [], print)
            print('* %s' % (self.message or 'First release'))

    def update(self, new_version):
        if not self.file:
            msg = 'Couldn\'t find a CHANGE file in %s' % self.path
            raise FileNotFoundError(msg)

        commits = git.get_commits(self.version, self.path)
        printed = False
        with self.printer(self.file) as print:
            for line in self.file.read_text().splitlines():
                if not printed and self.version in line:
                    printed = True
                    self._entry(new_version, commits, print)
                print(line)

            if not printed:
                self._entry(new_version, commits, print)

    def _entry(self, version, commits, print):
        today = date.today().strftime('%y/%m/%d')
        title = 'v%s - %s' % (version, today)
        if self.file == '.rst':
            print(title)
            print('=' * len(title))
        else:
            print('##', title)
        print()
        for commit in commits:
            print('*', commit)
        if commits:
            print()
