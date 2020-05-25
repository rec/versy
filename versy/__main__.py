from versy import versy
import argparse
import sys


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
