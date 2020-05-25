from . import git
from . import semver
from .changelog import ChangeLog
from .version_file import VersionFile
import contextlib
import safer

PREFIX = '__version__ = '
VERSION = 'VERSION'
ACTIONS = 'patch', 'minor', 'major', 'new', 'show'


def versy(action, changelog, dry_run, message, path):
    printer = _dry_printer if dry_run else safer.printer

    vfile = VersionFile(path, printer)
    version = semver.semver(vfile.version)

    if action == 'show':
        print(version, 'in', vfile.path)
        return

    cl = ChangeLog(path, version, changelog, printer)

    if action == 'new':
        cl.new()
    else:
        new_version = str(semver.bump(version, action))
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
