import argparse


def lb_search(search,area):
    print(search)
    print(area)


parser = argparse.ArgumentParser(description="search <search_string>", add_help=False)
#group = parser.add_mutually_exclusive_group()
# group.add_argument("search")
# group.add_argument("id")

parser.add_argument("search", help="Search for a bike position")
parser.add_argument("area", help="Area to look for")
parser.add_argument("id")

# parser.add_argument("search", help="hello")
# parser.add_argument("id")

args = parser.parse_args()
#print(args.search)

if args.search:
    lb_search(args.search, args.area)
