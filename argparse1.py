import argparse
import os
import sys

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
