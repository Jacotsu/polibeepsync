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
