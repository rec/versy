import semver
import sys
from . import changelog
from . import git
from . import version_file

PREFIX = '__version__ = '
VERSION = 'VERSION'


def main(action='patch', path='.'):
    # TODO: create the changelist if there is none!
    vfile, old = version_file.read(path)

    version = semver.VersionInfo.parse(old)
    new_version = getattr(version, 'bump_' + action)()
    new = str(new_version)

    print('From', vfile)
    print('Version', old, '->', new)

    commits = git.get_commits(old, path)
    cl = changelog.find(path)
    version_file.write(vfile, new)
    if cl:
        changelog.rewrite(cl, old, new, commits)
        files = [vfile, cl]
    else:
        print('No CHANGELOG found', file=sys.stderr)
        files = [vfile]
    git.commit(files, 'New version v%s' % new)


if __name__ == '__main__':
    main(*sys.argv[1:])
