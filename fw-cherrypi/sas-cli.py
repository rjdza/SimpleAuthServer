#!/usr/bin/python3

import database as db
import sys

import argparse

# <editor-fold desc="Argument Parser">
argsMain= ""

# <editor-fold desc="Parser Vars">
ParserMain = argparse.ArgumentParser(
    description='Commandline tool for the Simple Auhentication Server.',
    epilog="Don't forget to backup the database."
)
subparsersMain = ParserMain.add_subparsers(prog="SimpleAuthServer-CLI", dest='rootaction')
parserAuth = subparsersMain.add_parser("auth", help="IP Authentication services")
parserUser = subparsersMain.add_parser("user", help="User management services functions")

ParserAuth = argparse.ArgumentParser(
    description='Authentication Services.',
)
subparserAuth = ParserAuth.add_subparsers(prog="SimpleAuthServer-CLI", dest='rootaction')
subparserAuth.add_parser("ip", help="IP Authentication services")
subparserAuth.add_parser("iprange", help="IP Authentication services")


# </editor-fold>

def parser_main():
    global argsMain
    global ParserMain, subparsersMain, parserAuth, parserUser

    argsMain, argsUnknown = ParserMain.parse_known_args()
    if argsMain.rootaction == "auth":
        # sys.argv.remove("auth")
        sys.argv[1] = ""
        parser_auth()
    elif argsMain.rootaction == "user":
        # sys.argv.remove("user")
        sys.argv[1] = ""
        parser_user()
    else:
        ParserMain.print_help()
        ParserAuth.print_help()

    print("########################")
    print(sys.argv)
    print("########################")
    return

def parser_auth():
    global ParserAuth
    global parserAuth, subparserAuth

    argsMain, argsUnknown = ParserAuth.parse_args()

    print("IP auth Services")

def parser_user():
    global ParserUser
    ParserUser = argparse.ArgumentParser(
        description='Commandline tool for the Simple Auhentication Server - User Management Services.',
    )
    subparserUser = ParserUser.add_subparsers(prog="SimpleAuthServer-CLI", dest='rootaction')

    print("User management services")

# </editor-fold>

print("Simple Auth Server CLI")

parser_main()

db.connect()
