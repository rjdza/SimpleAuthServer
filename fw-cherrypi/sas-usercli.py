#!/usr/bin/python3
# import sys
import getpass
import argparse

import database as db

dbUserManager = db.ClassDBUserManagement()
securePassword = db.ClassSecurePassword

# <editor-fold desc="Argument Parser">
# args_main = ""

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
def add_user():
    global parserAdd
    print("** Adding User **")
    email_address = get_missing_value("--email", args_main.email, "Email address (Used as username)", False)
    password = get_missing_value("--passwd", args_main.passwd, "Password", True)
    first_name = get_missing_value("--fname", args_main.fname, "First name(s)", False)
    last_name = get_missing_value("--lname", args_main.lname, "Last name / Surname", False)
    user_description = get_missing_value("--desc", args_main.desc, "Description of user", False)
    user_notes = get_missing_value("--note", args_main.note, "User Notes", False)
    # group_id = get_missing_value("--groupid", args_main.groupid, "Group ID", False)
    group_id = 0
    result = dbUserManager.user_add(email_address, password, first_name, last_name, user_description, user_notes, int(group_id))
    return result

def delete_user():
    global parserDel
    print("** Deleting User **")
    if args_main.uid:
        dbUserManager.user_del(args_main.uid)
    else:
        query_rows = dbUserManager.users_list(args_main.email, True)
        if len(query_rows) == 1:
            user_id = query_rows[0][0]
            print(f"Deleting user [{query_rows[0][1]}]")
            dbUserManager.user_del(int(user_id))
        else:
            print("Too many results.  Choose one and try again:")
            for USER in query_rows:
                print(f"user_id: {USER[0]}, Email: {USER[1]}, Name: {USER[3]} {USER[4]}")

def modUser():
    global parserMod
    print("** Modifying User **")
    user_info = False
    if args_main.uid:
        print("Mod by UUID")
        user_info = dbUserManager.users_get_info(args_main.uid)
        
    else:
        query_rows = dbUserManager.users_list(args_main.email, True)
        print(query_rows)
        if query_rows:
            if len(query_rows) == 1:
                user_id = query_rows[0][0]
                print("Mod by Email Address")
                user_info = dbUserManager.users_get_info(user_id)
            else:
                print("Too many results.  Choose one and try again:")
                for user in query_rows:
                    print(f"user_id: {user[0]}, Email: {user[1]}, Name: {user[3]} {user[4]}")
        else:
            print("No results.")

    if user_info:
        user_id, email_address, password, first_name, last_name, description, note, group_id = user_info
        print("Updating info for user [", email_address, "]")
        email_address = args_main.newemail if args_main.newemail else email_address
        first_name = args_main.fname if args_main.fname else first_name
        last_name = args_main.lname if args_main.lname else last_name
        description = args_main.desc if args_main.desc else description
        note = args_main.note if args_main.note else note
        note = note + "//" + args_main.addnote if args_main.addnote else note
        group_id = args_main.groupid if args_main.groupid else group_id
        if args_main.passwd:
            password = dbUserManager.sec_pwd_tool.make_new_password(args_main.passwd)

        sql_string = """
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
        sql_vars = (email_address, password, first_name, last_name, description, note, group_id, user_id)
        dbUserManager.dbadmin_exec(sql_string, sql_vars, "Update record")

def change_password():
    user_id = False
    if args_main.uid:
        print("SetPass by UUID")
        user_id = args_main.uid
    else:
        # query_rows = dbUserManager.users_list(args_main.email, True)
        query_rows = dbUserManager.users_list(args_main.email, True)
        if len(query_rows) == 1:
            user_id = query_rows[0][0]
            print("SetPass by Email Address")
        else:
            print("Too many results.  Choose one and try again:")
            for USER in query_rows:
                print(f"user_id: {USER[0]}, Email: {USER[1]}, Name: {USER[3]} {USER[4]}")
    if user_id:
        password = get_missing_value("", args_main.passwd, "New Password", True)
        stored_password = dbUserManager.sec_pwd_tool.make_new_password(password)
        sql_string = """
        UPDATE UserInfo SET 
            password = ?
        WHERE
            id = ?
        """
        sql_vars = (stored_password, user_id)
        return_value = dbUserManager.dbadmin_exec(sql_string, sql_vars=sql_vars, descriptption="Update record")
        
        if return_value:
            print("Password successfully changed")
        else:
            print("Problem while changing password")

def check_auth():
    print("\nChecking authentication...\n")
    user_id = False
    if args_main.uid:
        print("CheckAuth by User ID")
        user_id = args_main.uid
    else:
        # query_rows = dbUserManager.users_list(args_main.email, True)
        query_rows = dbUserManager.users_list(args_main.email, True)
        if len(query_rows) == 1:
            user_id = query_rows[0][0]
            print("CheckAuth by Email Address")
        else:
            print("Too many results.  Choose one and try again:")
            for user in query_rows:
                print(f"user_id: {user[0]}, Email: {user[1]}, Name: {user[3]} {user[4]}")
    if user_id:
        # print(args_main.show_details)
        passwd = get_missing_value("", args_main.passwd, "Password", True)
        show_details = True if args_main.showdetails > 0 else False
        show_pwd_string = True if args_main.showdetails > 1 else False
        # return_value = db.check_auth(user_id, passwd, showdetails=show_details, showpwdstring=show_pwd_string)
        return_value = dbUserManager.users_check_auth(user_id, passwd, showdetails=show_details, showpwdstring=show_pwd_string)
        if return_value:
            print("Authentication successful")
        else:
            print("Authentication failed")

def list_users():
    '''
    Get a list of users from the DB, potentially filtered by a query satring.
    :return:
    '''
    global parserList
    print("** Listing Users **")
    # ROWS=dbUserManager.users_list(args_main.query, args_main.exact)
    ROWS=dbUserManager.users_list(args_main.query, args_main.exact)
    USERID, EMAIL, FNAME, LNAME, DESC, NOTE, GROUPID = "user_id", "Email", "First Name", "Last Name", "Description", "Note", "GroupID"
    SEP=" |"
    FIELDSTART=""
    FIELDEND = ""
    if args_main.outputstyle == "csv":
        SEP = ","
        FIELDSTART = ""
        FIELDEND = ""
    elif args_main.outputstyle == "text":
        SEP = ""
        FIELDSTART = ""
        FIELDEND = ""

    print(f"{FIELDSTART}{USERID:<7}{SEP} {EMAIL:<30}{SEP} {FNAME:<10}{SEP} {LNAME:<10}{SEP} {DESC:<10}{SEP} {GROUPID:<7}{FIELDEND}")
    for x in ROWS:
        USERID=x[0]
        EMAIL=x[1][:31]
        FNAME=x[3][:11]
        LNAME = x[4][:11]
        DESC = x[5][:11]
        NOTE = x[6][:71]
        GROUPID = str(x[7])
        print(f"{FIELDSTART}{USERID:<7}{SEP} {EMAIL:<30}{SEP} {FNAME:<10}{SEP} {LNAME:<10}{SEP} {DESC:<10}{SEP} {GROUPID:<7}{FIELDEND}")
        if args_main.shownotes:
            print(f"Notes: {NOTE:<70}")

def get_missing_value(switchDesc, switchVal, helpString, isPassword):
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
    'add': add_user,
    'del': delete_user,
    'mod': modUser,
    'list': list_users,
    'passwd': change_password,
    'checkauth': check_auth,
    None: ParserMain.print_help
}
# </editor-fold>


args_main, argsUnknown = ParserMain.parse_known_args()
dbUserManager.dbadmin_connect()

switcher_result = switcherMain.get(args_main.rootaction)
switcher_result()

dbUserManager.dbadmin_close()