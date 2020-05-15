from pathlib import Path
import os
import safer
import semver
import subprocess
import sys

SUB = {'stderr': subprocess.DEVNULL, 'encoding': 'utf8'}
CMD = 'git log --pretty=format:%s HEAD~{end}..HEAD~{begin}'

PREFIX = '__version__ = '
VERSION = 'VERSION'


def main(action='patch', path='.'):
    all_files = list(_all_files(path))

    path, version = _version_files(all_files)

    old_semver = semver.VersionInfo.parse(version)
    new_semver = getattr(old_semver, 'bump_' + action)()

    print('Version', old_semver, '->', new_semver)

    if path.endswith(VERSION):
        _write_file_version(new_semver)
    else:
        _write_python_version(path, new_semver)


def _all_files(root):
    root = Path(root)
    for directory, sub_dirs, files in os.walk(root):
        path = Path(directory)
        if path == root:
            sub_dirs[:] = (i for i in sub_dirs if i not in ('build', 'dist'))

        sub_dirs[:] = (i for i in sub_dirs if not i.startswith('.'))
        files[:] = (i for i in files if not i.startswith('.'))

        yield from (path / f for f in files)


def _version_files(all_files):
    results = []
    for filepath in all_files:
        version = _get_version(filepath)
        if version:
            results.append((filepath, version))

    if not results:
        raise ValueError('No version files found')
    if len(results) > 1:
        raise ValueError('More than one version file found', str(results))
    return results[0]


def _get_version(filepath, filename):
    if filename == VERSION:
        return Path(filepath).read_text().strip()

    if not filepath.suffix == '.py':
        return

    lines = [i.strip() for i in filepath.read_text().splitlines() if i.strip()]
    for line in lines:
        first, *rest = line.split(PREFIX, maxsplit=1)
        if not first:
            body = rest[0].strip().split('#')[0]
            for quote in '"', '\'':
                if len(body) > 2 and body[0] == body[-1] == quote:
                    body = body[1:-1]
            return body


def _write_file_version(path, version):
    Path(path).write_text('%s\n' % version)
    print('Rewrote', path)


def _write_python_version(path, version):
    lines = Path(path).read_text().splitlines()
    found_line = -1
    with safer.printer(path, 'w') as _print:
        for i, line in enumerate(lines):
            first, *rest = line.strip().split(PREFIX)
            if first:
                _print(line)
            else:
                if found_line >= 0:
                    raise ValueError('More than one version was found')
                found_line = i + 1
                _print("%s'%s'" % (PREFIX, version))
        if found_line < 0:
            raise ValueError('No version found')

    print('Rewrote %s:%d' % (path, found_line))


def _get_commits(version, cwd, max_commits=256, commit_block=32):
    commits = []

    begin = 0
    end = commit_block + 1
    while True:
        cmd = CMD.format(begin=begin, end=end).split()
        try:
            out = subprocess.check_output(cmd, cwd=cwd, **SUB)
        except subprocess.Subprocess.CalledProcessError:
            return []

        for line in out.splitlines():
            if line:
                if version in line:
                    return commits
                if len(commits) >= max_commits:
                    return []
                commits.append(line)

        begin += commit_block
        end += commit_block

    return commits


if __name__ == '__main__':
    main(*sys.argv[1:])
