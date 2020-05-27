from . import git
from datetime import date
from pathlib import Path

NAMES = 'CHANGELOG', 'CHANGELIST', 'CHANGES', 'changelog'
SUFFIXES = {'', '.rst', '.txt', '.md'}


class ChangeLog:
    def __init__(self, root, version, file, printer, message):
        self.root = Path(root)
        self.version = version
        self.printer = printer
        self.file = file
        self.message = message

        if not self.file:
            files = []
            for name in NAMES:
                for f in self.root.iterdir():
                    if f.stem == name and f.suffix in SUFFIXES:
                        files.append(f)
            if len(files) > 1:
                raise ValueError('Multiple changelogs: ' + ' '.join(files))
            if files:
                self.file = files[0]

    def new(self):
        file = Path(self.file or self.root / NAMES[0])
        if file.exists():
            raise ValueError('File %s already exists' % file.absolute())

        with self.printer(file) as print:
            self._entry(self.version, [], print)
            print('* %s' % (self.message or 'First release'))

        self.file = file

    def update(self, new_version):
        if not self.file:
            msg = 'Couldn\'t find a CHANGE file in %s' % self.root
            raise FileNotFoundError(msg)

        if self.message:
            messages = [self.message]
        else:
            messages = git.get_commits(str(self.version), self.root)

        printed = False
        needs_empty_line = False
        with self.printer(self.file) as print:
            for line in self.file.read_text().splitlines():
                if not printed and self.version in line:
                    printed = True
                    if needs_empty_line:
                        print()
                    self._entry(new_version, messages, print)
                    if messages:
                        print()
                print(line)
                needs_empty_line = bool(line.strip())

            if not printed:
                if needs_empty_line:
                    print()
                self._entry(new_version, messages, print)

    def _entry(self, version, messages, print):
        today = date.today().strftime('%y/%m/%d')
        title = 'v%s - %s' % (version, today)
        if self.file == '.rst':
            print(title)
            print('=' * len(title))
        else:
            print('##', title)
        print()
        for message in messages:
            print('*', message)
