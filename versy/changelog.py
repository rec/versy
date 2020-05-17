from datetime import date
from pathlib import Path
import safer
import sys

NAMES = 'CHANGELOG', 'CHANGELIST', 'CHANGES', 'changelog', 'HISTORY', 'NEWS'
SUFFIXES = {'', '.rst', '.txt', '.md'}


def find(path):
    for name in NAMES:
        for f in Path(path).iterdir():
            if f.stem == name and f.suffix in SUFFIXES:
                return f


def updated(filename, old_version, new_version, commits, print=print):
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


def rewrite(file, old_version, new_version, commits):
    if file:
        with safer.printer(file) as print:
            updated(file, old_version, new_version, commits, print)
    else:
        print('No changelog found', file=sys.stderr)
