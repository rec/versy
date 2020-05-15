import subprocess

SUB = {'stderr': subprocess.DEVNULL, 'encoding': 'utf8'}
CMD = 'git log --pretty=format:%s HEAD~{end}..HEAD~{begin}'


def get_commits(version, cwd, max_commits=256, commit_block=32):
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
