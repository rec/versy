from . import git
from datetime import date
from pathlib import Path
import safer

NAMES = 'CHANGELOG', 'CHANGELIST', 'CHANGES', 'changelog', 'HISTORY', 'NEWS'
SUFFIXES = {'', '.rst', '.txt', '.md'}


def update(path, old_version, new_version, commits, print=print):
    file = _find(path)
    commits = git.get_commits(old_version, path)
    with safer.printer(file) as print:
        _update(file, old_version, new_version, commits, print)

    return file


def new(path, version):
    pass


def _find(path):
    for name in NAMES:
        for f in Path(path).iterdir():
            if f.stem == name and f.suffix in SUFFIXES:
                return f
    raise FileNotFoundError('Couldn\'t find a CHANGE file in %s' % path)


def _update(filename, old_version, new_version, commits, print=print):
    def add():
        today = date.today().strftime('%y/%m/%d')
        title = 'v%s - %s' % (new_version, today)
        if filename.suffix == '.rst':
            print(title)
            print('=' * len(title))
        else:
            print('##', title)
        print()
        for commit in commits:
            print('*', commit)
        print()

    printed = False
    for line in filename.read_text().splitlines():
        if not printed and old_version in line:
            add()
            printed = True
        print(line)
