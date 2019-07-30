"""
Bailer

Usage: 
    bailer add <flower-name> <watering-interval>
    bailer getall
    bailer remove <flower-name>
    bailer water <flower-name> [--force]
    bailer -h | -help

Options:
  -h --help     Show this screen.
"""

from docopt import docopt

import bailer
from storage import FileStorage


def main():
    args = docopt(__doc__)
    
    storage = FileStorage("entries.txt")
    bailer.init_storage(storage)

    if args.get('getall'):
        print(bailer.get_all_flowers())
    elif args.get('add'):
        print(bailer.add_flower(args.get('<flower-name>'), args.get('<watering-interval>')))
    elif args.get('remove'):
        print(bailer.remove_flower(args.get('<flower-name>')))
    elif args.get('water'):
        if args.get('--force'):
            print(bailer.water_flower_force(args.get('<flower-name>')))
        else:
            print(bailer.water_flower(args.get('<flower-name>')))


if __name__ == '__main__':
    main()

