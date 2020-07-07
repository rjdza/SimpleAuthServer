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
parserAuth = subparsersMain.add_parser("authip", help="Authorise IP address.")
parserAuth.add_argument('--ip', help="IP Address")

parserUser = subparsersMain.add_parser("authiprange", help="Authorise CIDR IP subnet.")
parserUser.add_argument('--iprange', help="CIDR IP Address range")

argsMain, argsUnknown = ParserMain.parse_known_args()