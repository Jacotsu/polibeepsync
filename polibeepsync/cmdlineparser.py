__copyright__ = """Copyright 2020 Davide Olianas (ubuntupk@gmail.com), Di
Campli Raffaele (dcdrj.pub@gmail.com)."""

__license__ = """This f is part of poliBeePsync.
poliBeePsync is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

poliBeePsync is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with poliBeePsync. If not, see <http://www.gnu.org/licenses/>.
"""

import argparse

"""
Thanks
https://stackoverflow.com/questions/14117415/in-python-using-argparse-allow
-only-positive-integers
"""


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            f"{value}: 0 and negative numbers are not allowed")
    return ivalue


def create_parser():
    debug_levels = ['debug', 'info', 'warning', 'error', 'critical']

    parser = argparse.ArgumentParser(description='Sync files from BeeP.')
    parser.add_argument('--hidden', action='store_true',
                        help="Don't show the main window, just the icon"
                             " in the system tray")
    parser.add_argument('--log-level', action='store', choices=debug_levels,
                        help='Choose logging report verbosity')
    parser.add_argument('-s', '--use_theme',
                        action='store_true', default=False,
                        help="Choose Qt theme over gtk")
    parser.add_argument(
        '--default-timeout',
        type=check_positive,
        action='store',
        default=10,
        help='[Non persistent override] Choose how long (in seconds) the '
        'connection should remain open before assuming that the server'
        ' is offline')

    parser.add_argument(
        '--sync-interval',
        type=check_positive,
        action='store',
        help='[Non persistent override] Choose how often (in minutes) the '
        'courses files should be synced')

    parser.add_argument(
        '--sync-on-startup',
        action='store_true',
        help='[Non persistent override] Synces the courses files on startup')

    return parser
