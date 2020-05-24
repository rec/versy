from . import changelog
from . import git
from . import version_file
import argparse
import semver
import sys

PREFIX = '__version__ = '
VERSION = 'VERSION'
ACTIONS = 'patch', 'minor', 'major', 'new', 'version'


def versy(action, path):
    vfile, version = version_file.read(path)
    version = semver.VersionInfo.parse(version)

    if action == 'version':
        print(version, 'in', vfile)
    elif action == 'new':
        changelog.new(vfile, version)
    else:
        new_version = getattr(version, 'bump_' + action)()
        new = str(new_version)

        print('Version', version, '->', new, 'in', vfile)
        cl = changelog.update(path, version, new)
        version_file.write(vfile, new)
        git.commit([vfile, cl], 'New version v%s' % new)


def main(arg=None):
    p = argparse.ArgumentParser(description=_DESCRIPTION)
    p.add_argument(
        'action', choices=ACTIONS, default='version', help=_ACTION_HELP
    )
    p.add_argument('directory', default='.', help=_DIRECTORY_HELP)
    args = p.parse_args(arg)
    try:
        versy(args.action, args.directory)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(-1)


_DESCRIPTION = """Update the version number and CHANGELOG of the program"""
_ACTION_HELP = """"""
_DIRECTORY_HELP = """"""


if __name__ == '__main__':
    sys.exit(main())
