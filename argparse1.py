import argparse
import os
import sys

# https://realpython.com/command-line-interfaces-python-argparse/

# EXAMPLE 1

# import os
# import sys
#
# if len(sys.argv) > 2:
#     print('You have specified too many arguments')
#     sys.exit()
#
# if len(sys.argv) < 2:
#     print('You need to specify the path to be listed')
#     sys.exit()
#
# input_path = sys.argv[1]
#
# if not os.path.isdir(input_path):
#     print('The path specified does not exist')
#     sys.exit()
#
# print('\n'.join(os.listdir(input_path)))

# EXAMPLE 2

# create the parser
# explicitly set the name of the program

# my_parser = argparse.ArgumentParser(prog='argparse1',
#                                     usage='\n%(prog)s [options] path',
#                                     description='List the content of a folder',
#                                     epilog='Enjoy the program!',
#                                     prefix_chars='/')
#
# # add the arguments
# my_parser.add_argument('Path',
#                        metavar='path',
#                        type=str,
#                        help='the path to list')
#
# # execute the parse_args() method
# args = my_parser.parse_args()
#
# input_path = args.Path
#
# if not os.path.isdir(input_path):
#     print('The path specified does not exist')
#     sys.exit()
#
# print('\n'.join(os.listdir(input_path)))

# EXAMPLE 3

# store -  stores the input value to the Namespace object. (This is the default action.)
# store_const - stores a constant value when the corresponding optional arguments are specified.
# store_true - stores the Boolean value True when the corresponding optional argument is specified and stores a False elsewhere.
# store_false - stores the Boolean value False when the corresponding optional argument is specified and stores True elsewhere.
# append - stores a list, appending a value to the list each time the option is provided.
# append_const - stores a list appending a constant value to the list each time the option is provided.
# count - stores an int that is equal to the times the option has been provided.
# help - shows a help text and exits.
# version - shows the version of the program and exits.

# my_parser = argparse.ArgumentParser()
# my_parser.version = '1.0'
# my_parser.add_argument('-a', action='store')
# my_parser.add_argument('-b', action='store_const', const=42)
# my_parser.add_argument('-c', action='store_true')
# my_parser.add_argument('-d', action='store_false')
# my_parser.add_argument('-e', action='append')
# my_parser.add_argument('-f', action='append_const', const=42)
# my_parser.add_argument('-g', action='count')
# my_parser.add_argument('-i', action='help')
# my_parser.add_argument('-j', action='version')
#
# args = my_parser.parse_args()
#
# # vars takes an object as a parameter and returns the dict objects
# print(vars(args))

# EXAMPLE 4

# - nargs keyword can also accept the following:

# ?: a single value, which can be optional
# *: a flexible number of values, which will be gathered into a list
# +: like *, but requiring at least one value


# my_parser = argparse.ArgumentParser()
# #my_parser.add_argument('input', action='store', type=int, nargs=3)
# my_parser.add_argument('search', action='store', nargs='+')
# #my_parser.add_argument('id', action='store', type=int, nargs=1)
# args = my_parser.parse_args()

# print(args.search)

# EXAMPLE 5

# my_parser = argparse.ArgumentParser()
# my_parser.add_argument('search', action='store', type=str, nargs=2, help='search <search_string>')
# #my_parser.add_argument('params', action='store', nargs=argparse.REMAINDER)
# #my_parser.add_argument('id', action='store', type=str, nargs=1)
#
# args = my_parser.parse_args()
# print(args.search)

# print('first = %r' % args.search)
# print('others = %r' % args.params)
# print('id = %r' % args.id)

# EXAMPLE 6

# mutually exclusive args must be optional
my_parser = argparse.ArgumentParser()
my_group = my_parser.add_mutually_exclusive_group(required=True)

my_group.add_argument('search', action='store')
my_group.add_argument('id', action='store')

args = my_parser.parse_args()
print(vars(args))