#!/usr/bin/python3

import database as db

import argparse
parser = argparse.ArgumentParser(
    description='Commandline tool for the Simple Auhentication Server.',
    epilog="Don't forget to backup the database."
)

# parser.add_argument('-u', '--users',dest='action',action='store_const', const='userfunc',
#                     help='User Functions')
# parser.add_argument('-a', '--auth',dest='action',action='store_const', const='authfunc',
#                     help='Auth Functions')

subparsers = parser.add_subparsers(help="User Functions Help")

parser_users = subparsers.add_parser('users', help="User functions")
parser_users.add_argument('-l', '--list', dest='useraction',action='store_const', const='list',
                          help='List users')

parser_users.add_argument('-a', '--adduser', dest='useraction',action='store_const', const='add',
                          help='List all users matching pattern (* is wildcard)')

parser_auth = subparsers.add_parser('auth', help="Auth Functions")
parser_auth.add_argument('bar', type=int, help='bar2 help')

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

args = parser.parse_args()

print("Simple Auth Server CLI")

print(args.action)

db.connect()
