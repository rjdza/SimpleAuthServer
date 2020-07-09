#!/usr/bin/python3

import database as db
import sys
import getpass

import argparse

# <editor-fold desc="Argument Parser">
argsMain= ""

# <editor-fold desc="Parser Vars">
# <editor-fold desc="Parser Main">
ParserMain = argparse.ArgumentParser(
    description='Commandline tool for the Simple Auhentication Server.',
    epilog="Don't forget to backup the database."
)
subparsersMain = ParserMain.add_subparsers(prog="SimpleAuthServer-CLI", dest='rootaction')
parserAdd = subparsersMain.add_parser("add", help="Add user")
parserDel = subparsersMain.add_parser("del", help="Delete user")
parserMod = subparsersMain.add_parser("mod", help="Modify user")
parserList = subparsersMain.add_parser("list", help="List users")
parserPasswd = subparsersMain.add_parser("passwd", help="Change Password for user")
parserCheckAuth = subparsersMain.add_parser("checkauth", help="Change Password for user")
# </editor-fold>

# <editor-fold desc="Add User">
parserAdd.add_argument('--email', help="Email address of new user (Username)")
parserAdd.add_argument('--passwd', help="Password for new user")
parserAdd.add_argument('--fname', help="User's first name(s)")
parserAdd.add_argument('--lname', help="User's last name / surname")
parserAdd.add_argument('--desc', help="User description")
parserAdd.add_argument('--note', help="Additional info (note)")
parserAdd.add_argument('--groupid', help="Group membership")
# </editor-fold>

# <editor-fold desc="Delete User">
parserDelGrp=parserDel.add_mutually_exclusive_group(required=True)
parserDelGrp.add_argument('--email', help="Email address of user to delete")
parserDelGrp.add_argument('--uid', help="User ID of user to delete")
# </editor-fold>

# <editor-fold desc="Modify User">
parserModUserIDGroup=parserMod.add_mutually_exclusive_group(required=True)
parserModUserIDGroup.add_argument('--email', help="Email address of user to modify")
parserModUserIDGroup.add_argument('--uid', help="User ID of user to modify")
parserMod.add_argument('--newemail', help="New email address (Username)")
parserMod.add_argument('--passwd', help="New password")
parserMod.add_argument('--fname', help="User's first name(s)")
parserMod.add_argument('--lname', help="User's last name / surname")
parserMod.add_argument('--desc', help="User description")
parserMod.add_argument('--note', help="New note / info")
parserMod.add_argument('--addnote', help="Additional note")
parserMod.add_argument('--groupid', help="Group membership")
# </editor-fold>

# <editor-fold desc="Set Password">
parserSetPassIDGroup=parserPasswd.add_mutually_exclusive_group(required=True)
parserSetPassIDGroup.add_argument('--email', help="Email address of user to modify")
parserSetPassIDGroup.add_argument('--uid', help="User ID of user to modify")
parserPasswd.add_argument('--passwd', help="New Password")
# </editor-fold>

# <editor-fold desc="Check Auth">
parserCheckAuthIDGroup=parserCheckAuth.add_mutually_exclusive_group(required=True)
parserCheckAuthIDGroup.add_argument('--email', help="Email address of user to modify")
parserCheckAuthIDGroup.add_argument('--uid', help="User ID of user to modify")
parserCheckAuth.add_argument('--passwd', help="Password to test")
parserCheckAuth.add_argument('-d', '--showdetails', action='count', default=0, help="Show password data. Use multiple times to show more data.")
# </editor-fold>

# <editor-fold desc="List Users">
parserList.add_argument('--query', help="Query string")
parserList.add_argument('-e', '--exact', action='store_true', help="Query string must match exactly.  Without this option, all records matching any part of the string will be shown. Use the asterisk (*) as a wiuldcard")
parserList.add_argument('-n', '--shownotes', action='store_true', help="Show notes")
parserList.add_argument('-o', '--out', dest="outputstyle", help="Show notes", choices={"csv", "html", "formattedtext", "text"})
# </editor-fold>

# <editor-fold desc="Switcher - Functions">
def addUser():
    global parserAdd
    print("** Adding User **")
    EMAIL = getMissingValue("--email", argsMain.email, "Email address (Used as username)", False)
    PASSWD = getMissingValue("--passwd", argsMain.passwd, "Password", True)
    FNAME = getMissingValue("--fname", argsMain.fname, "First name(s)", False)
    LNAME = getMissingValue("--lname", argsMain.lname, "Last name / Surname", False)
    DESC = getMissingValue("--desc", argsMain.desc, "Description of user", False)
    NOTE = getMissingValue("--note", argsMain.note, "User Notes", False)
    # GROUPID = getMissingValue("--groupid", argsMain.groupid, "Group ID", False)
    GROUPID = 0
    RES = db.addUser(EMAIL, PASSWD, FNAME, LNAME, DESC, NOTE, int(GROUPID))

def delUser():
    global parserDel
    print("** Deleting User **")
    if argsMain.uid:
        db.delUser(argsMain.uid)
    else:
        ROWS = db.listUsers(argsMain.email, True)
        if len(ROWS) == 1:
            UUID = ROWS[0][0]
            print(f"Deleting user [{ROWS[0][1]}]")
            db.delUser(UUID)
        else:
            print("Too many results.  Choose one and try again:")
            for USER in ROWS:
                print(f"UserID: {USER[0]}, Email: {USER[1]}, Name: {USER[3]} {USER[4]}")

def modUser():
    global parserMod
    print("** Modifying User **")
    USERINFO = False
    if argsMain.uid:
        print("Mod by UUID")
        USERINFO = db.getUserInfo(argsMain.uid)
    else:
        ROWS = db.listUsers(argsMain.email, True)
        print(ROWS)
        if ROWS:
            if len(ROWS) == 1:
                USERID = ROWS[0][0]
                print("Mod by Email Address")
                USERINFO = db.getUserInfo(USERID)
            else:
                print("Too many results.  Choose one and try again:")
                for USER in ROWS:
                    print(f"UserID: {USER[0]}, Email: {USER[1]}, Name: {USER[3]} {USER[4]}")
        else:
            print("No results.")

    if USERINFO:
        USERID, EMAIL, PASSWD, FNAME, LNAME, DESC, NOTE, GROUPID = USERINFO
        print("Updating info for user [", EMAIL, "]")
        EMAIL = argsMain.newemail if argsMain.newemail else EMAIL
        FNAME = argsMain.fname if argsMain.fname else FNAME
        LNAME = argsMain.lname if argsMain.lname else LNAME
        DESC = argsMain.desc if argsMain.desc else DESC
        NOTE = argsMain.note if argsMain.note else NOTE
        NOTE = NOTE + "//" + argsMain.addnote if argsMain.addnote else NOTE
        GROUPID = argsMain.groupid if argsMain.groupid else GROUPID
        if argsMain.passwd:
            PASSWD = db.securePassword.NewPass(argsMain.passwd)

        SQLString = """
        UPDATE UserInfo SET 
            email_address = ?, 
            password = ?, 
            first_names = ?, 
            last_name = ?, 
            description = ?, 
            notes = ?, 
            group_id = ?
        WHERE
            id = ?
        """
        SQLVars = (EMAIL, PASSWD, FNAME, LNAME, DESC, NOTE, GROUPID, USERID)
        db.sqlExec(SQLString, SQLVars, "Update record")

def setPass():
    USERID = False
    if argsMain.uid:
        print("SetPass by UUID")
        USERID = argsMain.uid
    else:
        ROWS = db.listUsers(argsMain.email, True)
        if len(ROWS) == 1:
            USERID = ROWS[0][0]
            print("SetPass by Email Address")
        else:
            print("Too many results.  Choose one and try again:")
            for USER in ROWS:
                print(f"UserID: {USER[0]}, Email: {USER[1]}, Name: {USER[3]} {USER[4]}")
    if USERID:
        PASSWD = getMissingValue("", argsMain.passwd, "New Password", True)
        STOREDPASSWD = db.securePassword.NewPass(PASSWD)
        SQLString = """
        UPDATE UserInfo SET 
            password = ?
        WHERE
            id = ?
        """
        SQLVars = (STOREDPASSWD, USERID)
        RET = db.sqlExec(SQLString, SQLVars, "Update record")
        if RET:
            print("Password successfully changed")

def checkAuth():
    print("\nChecking authentication...\n")
    USERID = False
    if argsMain.uid:
        print("CheckAuth by UUID")
        USERID = argsMain.uid
    else:
        ROWS = db.listUsers(argsMain.email, True)
        if len(ROWS) == 1:
            USERID = ROWS[0][0]
            print("CheckAuth by Email Address")
        else:
            print("Too many results.  Choose one and try again:")
            for USER in ROWS:
                print(f"UserID: {USER[0]}, Email: {USER[1]}, Name: {USER[3]} {USER[4]}")
    if USERID:
        # print(argsMain.showdetails)
        PASSWD = getMissingValue("", argsMain.passwd, "Password", True)
        SHOWDETAILS = True if argsMain.showdetails > 0 else False
        SHOWPWDSTRING = True if argsMain.showdetails > 1 else False
        RET = db.checkAuth(USERID, PASSWD, showdetails=SHOWDETAILS, showpwdstring=SHOWPWDSTRING)
        if RET:
            print("Authentication successful")
        else:
            print("Authentication failed")

def listUsers():
    '''
    Get a list of users from the DB, potentially filtered by a query satring.
    :return:
    '''
    global parserList
    print("** Listing Users **")
    # print(argsMain)
    ROWS=db.listUsers(argsMain.query, argsMain.exact)
    # print(ROWS)
    # print("---")
    USERID, EMAIL, FNAME, LNAME, DESC, NOTE, GROUPID = "UserID", "Email", "First Name", "Last Name", "Description", "Note", "GroupID"
    SEP=" |"
    FIELDSTART=""
    FIELDEND = ""
    if argsMain.outputstyle == "csv":
        SEP = ","
        FIELDSTART = ""
        FIELDEND = ""
    elif argsMain.outputstyle == "text":
        SEP = ""
        FIELDSTART = ""
        FIELDEND = ""

    print(f"{FIELDSTART}{USERID:<7}{SEP} {EMAIL:<30}{SEP} {FNAME:<10}{SEP} {LNAME:<10}{SEP} {DESC:<10}{SEP} {GROUPID:<7}{FIELDEND}")
    for x in ROWS:
        # print(x[1])
        USERID=x[0]
        EMAIL=x[1][:31]
        FNAME=x[3][:11]
        LNAME = x[4][:11]
        DESC = x[5][:11]
        NOTE = x[6][:71]
        GROUPID = str(x[7])
        print(f"{FIELDSTART}{USERID:<7}{SEP} {EMAIL:<30}{SEP} {FNAME:<10}{SEP} {LNAME:<10}{SEP} {DESC:<10}{SEP} {GROUPID:<7}{FIELDEND}")
        if argsMain.shownotes:
            print(f"Notes: {NOTE:<70}")

def getMissingValue(switchDesc, switchVal, helpString, isPassword):
    '''
    Checks is option is set, and prompts for value if it isn't.
    :param switchDesc:
    :param switchVal:
    :param helpString:
    :param isPassword:
    :return:
    '''
    switchVal = "" if switchVal == None else switchVal
    while switchVal == "":
        if isPassword:
            switchVal = getpass.getpass("  " + switchDesc + "    " + helpString + ": ")
            switchVal2 = getpass.getpass("  " + switchDesc + "    " + helpString + "(confirm): ")
            if switchVal != switchVal2:
                switchVal = ""
                print("Values do not match.")

        else:
            switchVal = input("  " + switchDesc + "    " + helpString + ": ")
    return switchVal

# </editor-fold>

# <editor-fold desc="Switcher - Main">
switcherMain = {
    'add': addUser,
    'del': delUser,
    'mod': modUser,
    'list': listUsers,
    'passwd': setPass,
    'checkauth': checkAuth
}
# </editor-fold>


# txt = input("Type something to test this out: ")
# print("Is this what you just said? ", txt)

argsMain, argsUnknown = ParserMain.parse_known_args()
db.connect()

# print("##################")
# print(argsMain.rootaction)
# print("##################")

# RES = switcherMain.get(argsMain.rootaction, lambda: "Unknown Option")
# RES = switcherMain.get(argsMain.rootaction, ParserMain.print_help())
RES = switcherMain.get(argsMain.rootaction)
RES()


# print("##################")
# print(RES)
db.close_connections()