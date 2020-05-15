from datetime import date
import safer
import sys

NAMES = 'CHANGELOG', 'CHANGES', 'changelog', 'HISTORY', 'NEWS'
SUFFIXES = {'', '.rst', '.txt', '.md'}


def _find(path):
    for name in NAMES:
        for f in path.iterdir():
            if f.stem == name and f.suffix in SUFFIXES:
                return f


def _update(filename, old_version, new_version, commits):
    def add(print):
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

    with safer.printer(filename) as print:
        printed = False
        for line in filename.read_text().splitlines():
            if not printed and old_version in line:
                add(print)
                printed = True

            print(line)


def update(path, old_version, new_version, commits):
    file = _find(path)
    if file:
        _update(file, old_version, new_version, commits)
    else:
        print('No changelog found', file=sys.stderr)
