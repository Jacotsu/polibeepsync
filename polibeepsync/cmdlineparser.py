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


def create_parser():
    debug_levels = ['debug', 'info', 'warning', 'error', 'critical']

    parser = argparse.ArgumentParser(description='Sync files from BeeP.')
    parser.add_argument('--hidden', action='store_true',
                        help="Don't show the main window, just the icon"
                             " in the system tray")
    parser.add_argument('--debug', action='store', choices=debug_levels,
                        help="Show debug information.")
    parser.add_argument('-s', '--use_theme',
                        action='store_true', default=False,
                        help="Choose Qt theme over gtk")

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()
