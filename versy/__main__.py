from versy import versy
import argparse
import sys
import traceback


def main(args=None):
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('action', nargs='?', default='show', help=_ACTIONS_HELP)
    p.add_argument('--changelog', '-c', default=None, help=_CHANGELOG_HELP)
    p.add_argument('--dry-run', '-d', action='store_true', help=_DRY_RUN_HELP)
    p.add_argument('--message', '-m', help=_MESSAGE_HELP)
    p.add_argument('--path', '-p', default='.', help=_PATH_HELP)
    p.add_argument('--verbose', '-v', action='store_true', help=_VERBOSE_HELP)

    args = p.parse_args(args)
    try:
        versy.versy(**vars(args))
    except Exception as e:
        print(e, file=sys.stderr)
        if args.verbose:
            traceback.print_exc()
        sys.exit(-1)


_DESCRIPTION = """Update the version number and CHANGELOG of the program"""
_ACTIONS_HELP = """"""
_CHANGELOG_HELP = """"""
_MESSAGE_HELP = """"""
_PATH_HELP = """"""
_VERBOSE_HELP = """"""
_DRY_RUN_HELP = """Don't actually make the changes, just print the diffs"""


if __name__ == '__main__':
    sys.exit(main())
