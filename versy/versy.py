from . import git
from . import semver
from .changelog import ChangeLog
from .version_file import VersionFile
import contextlib
import safer

PREFIX = '__version__ = '
VERSION = 'VERSION'
ACTIONS = 'patch', 'minor', 'major', 'new', 'show'
__version__ = '0.9.0'


def versy(action, changelog, dry_run, message, path):
    printer = _dry_printer if dry_run else safer.printer

    vfile = VersionFile(path, printer)
    version = semver.semver(vfile.version)

    if action == 'show':
        print('Version', version, 'found in', vfile.file)
        return

    cl = ChangeLog(path, version, changelog, printer, message)

    if action == 'new':
        cl.new()
        msg = 'First release version v%s' % version
        git.commit([cl.file], msg, dry_run)
    else:
        new_version = str(semver.bump(version, action))
        print('Version', version, '->', new_version, 'in', vfile.file)

        cl = cl.update(new_version)
        vfile.write(new_version)
        msg = 'New version v%s' % new_version
        git.commit([vfile.file, cl.file], msg, dry_run)


@contextlib.contextmanager
def _dry_printer(file):
    def _print(*args, **kwds):
        print(' ', *args, **kwds)

    print('%s:' % file)
    yield _print
