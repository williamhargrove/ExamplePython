import argparse


def lb_search(search,area):
    print(search)
    print(area)


my_parser = argparse.ArgumentParser()
my_parser.add_argument('-search', action='store', type=str, nargs=2, help='search <search_string>')
my_parser.add_argument('-id', action='store', type=str, nargs=1)

args = my_parser.parse_args()
print(args.search)

print('search = %r' % args.search)

print('id = %r' % args.id)

if args.search:
    lb_search(args.search, args.area)
