from . import git
from .changelog import ChangeLog
from .version_file import VersionFile
import argparse
import contextlib
import safer
import semver
import sys

PREFIX = '__version__ = '
VERSION = 'VERSION'
ACTIONS = 'patch', 'minor', 'major', 'new', 'show'


def _semver(s):
    try:
        return semver.VersionInfo.parse(s)
    except Exception:
        raise ValueError('"%s" was not a valid version number' % s)


def versy(action, changelog, dry_run, message, path):
    printer = _dry_printer if dry_run else safer.printer

    vfile = VersionFile(path, printer)
    version = _semver(vfile.version)

    if action == 'show':
        print(version, 'in', vfile.path)
        return

    cl = ChangeLog(path, version, changelog, printer)

    if action == 'new':
        cl.new()
    else:
        new_version = str(_bump(version, action))
        print('Version', version, '->', new_version, 'in', vfile.path)

        cl = cl.update(new_version)
        vfile.write(new_version)
        git.commit([vfile.path, cl.file], 'New version v%s' % new_version)


@contextlib.contextmanager
def _dry_printer(file):
    def _print(*args, **kwds):
        print(' ', *args, **kwds)

    print('%s:' % file)
    yield _print


def _bump(version, action):
    if action == 'patch':
        return version.bump_patch()
    elif action == 'minor':
        return version.bump_minor()
    elif action == 'major':
        return version.bump_major()
    try:
        v = _semver(action)
    except ValueError:
        raise ValueError('Unknown action %s' % action)

    if v <= version:
        raise ValueError('%s <= current version %s' % (v, version))

    return v


def main(args=None):
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('action', default='show', help=_ACTIONS_HELP)
    p.add_argument('--changelog', '-c', default=None, help=_CHANGELOG_HELP)
    p.add_argument('--dry-run', '-d', action='store_true', help=_DRY_RUN_HELP)
    p.add_argument('--message', '-m', help=_MESSAGE_HELP)
    p.add_argument('--path', '-p', default='.', help=_PATH_HELP)

    a = p.parse_args(args)
    try:
        versy(**vars(a))
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(-1)


_DESCRIPTION = """Update the version number and CHANGELOG of the program"""
_ARGUMENT_HELP = """"""
_ACTIONS_HELP = """, choices=ACTIONS"""
_CHANGELOG_HELP = """"""
_MESSAGE_HELP = """"""
_PATH_HELP = """"""
_DRY_RUN_HELP = """Don't actually make the changes, just print the diffs"""


if __name__ == '__main__':
    sys.exit(main())
