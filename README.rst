💯 versy: Update the version number of your Python git project 💯
====================================================================

A command line utility that finds the current version number of your Python
repository.

On request, ``versy`` will update that version number, and also update your
CHANGELOG with the date and new version number and a custom message, or a list
of the commits since the last version release if no message is supplied.

.. code-block:: python

    usage: versy [-h] [--changelog CHANGELOG] [--dry-run] [--message MESSAGE]
                 [--path PATH] [--verbose]
                 [action]

    Update the version number and CHANGELOG of the program

    positional arguments:
      action

    optional arguments:
      -h, --help            show this help message and exit
      --changelog CHANGELOG, -c CHANGELOG
      --dry-run, -d         Don't actually make the changes, just print the diffs
      --message MESSAGE, -m MESSAGE
      --path PATH, -p PATH
      --verbose, -v
