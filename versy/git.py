from . import DRY_RUN
import subprocess

SUB = {'stderr': subprocess.DEVNULL, 'encoding': 'utf8'}
CMD = 'git log --pretty=format:%s HEAD~{end}..HEAD~{begin}'


def get_commits(version, cwd, max_commits=256, commit_block=2):
    commits = []

    begin = 0
    end = commit_block
    while True:
        cmd = CMD.format(begin=begin, end=end)
        try:
            out = subprocess.check_output(cmd.split(), cwd=cwd, **SUB)
        except subprocess.CalledProcessError:
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


def commit(files, message):
    cmd = ('git', 'commit') + tuple(files) + ('-m', message)
    if DRY_RUN:
        print('$', *cmd)
    else:
        print('$', *cmd)
        subprocess.check_output(cmd, encoding='utf8')


if __name__ == '__main__':
    import sys

    for line in get_commits(sys.argv[1], '.'):
        print(line)
