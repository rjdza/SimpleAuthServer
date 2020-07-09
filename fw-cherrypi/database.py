import sqlite3
from sqlite3 import Error
import hashlib
import binascii
import os

# dbfile_userdetails = r"database/dbu_userdetails.sqlite3"
# dbconn_userdetails = ""
DEBUG = False
#TODO: Do I need to have better error handling?


class ClassSecurePassword:
    """
    Password management Class.

    NOTE: Changing vars. If you change these variables, previously stored passwords will no longer work.
    :var salt_length: INT - System default length for salt.
    :var security_iterations: INT - Number of hash iterations used to make brute forcing take longer.
    """
    salt_length = 32
    security_iterations = 100000

    def make_salt(self, salt_length):
        """
        Create a string to be used to salt the password. DOES NOT use the built-in salt_length var!

        :param salt_length: INT - The length of the salt to create.
        :return: Returns a string.
        """
        salt = os.urandom(salt_length)
        return_value=binascii.b2a_hex(salt).decode("utf-8")
        return return_value

    def make_new_password(self, myPassword):
        """
        Create a NEW secure password hash with embedded salt
        :param myPassword: STR - The password to use for the hash.
        :return: STR - Retrurns a string that contains both the salt and the key, in that order.
        """
        salt = self.make_salt(self.salt_length)
        PASSWDSTRING = self.make_password(salt, myPassword)
        return PASSWDSTRING

    def make_password(self, salt, myPassword):
        """
        Create a secure password with embedded salt.
        :param myPassword: STR - The plain text password to use for the hash.
        :param salt: STR - Salt used to ensure password uniqueness.
        :return:
        """
        salt_bin = binascii.a2b_hex(salt)
        key_bin = hashlib.pbkdf2_hmac('sha256', myPassword.encode('utf-8'), salt_bin, self.security_iterations)
        key = binascii.b2a_hex(key_bin).decode("utf-8")
        return salt + key

    def check_password(self, my_password, stored_password_string, *args, **kwargs):
        """
        Compares the plain text password provided with the hashed hex password stored in the database.
        :param my_password: STR - Plain text password
        :param stored_password_string: STR - Salt + Password string
        :param args:
        :param kwargs: showdetails - BOOL - Display some internal vars
        :param kwargs: showpwdstring - BOOL - Display the entire stored password string
        :return: BOOL - Returns True is passwords match, False if they do not.
        """
        # print(kwargs)
        show_details = kwargs.get("showdetails", False)
        show_password_string = kwargs.get("showpwdstring", False)
        salt   = stored_password_string[:(self.salt_length * 2)]
        stored_password = stored_password_string[(self.salt_length * 2):]
        salt_bin = binascii.a2b_hex(salt)
        new_password = binascii.b2a_hex(hashlib.pbkdf2_hmac('sha256', my_password.encode('utf-8'), salt_bin, self.security_iterations)).decode("utf-8")
        password_match = "Passwords MATCH" if stored_password == new_password else "Passwords DO NOT MATCH"

        if self.salt_length == (len(salt) / 2):
            LENCHK = "Salt matches system length of " + str(self.salt_length)
        else:
            LENCHK = "Salt does NOT match system length.  System = " + str(self.salt_length) + " while stored is " + str((len(salt) / 2))

        if show_password_string:
            print("")
            print("-----START OF STORED PASSWORD STRING-----")
            print(stored_password_string)
            print("-----END OF STORED PASSWORD STRING-----")

        if show_details:
            print("")
            print("  PWD check str: " + my_password)
            print(" PWD check hash: " + new_password)
            print("Stored PWD hash: " + stored_password)
            print("PWD comparisson: " + password_match)
            print("           Salt: " + salt)
            print("    Salt Length: " + LENCHK)
            print("")

        return_value=True if stored_password == new_password else False
        return return_value

class ClassDBUserManagement:
    """
    Functions to easily manage users.
    """
    dbfile_userdetails = r"database/dbu_userdetails.sqlite3"
    dbconn_userdetails = ""
    sec_pwd_tool = ClassSecurePassword()

    def dbadmin_connect(self):
        """
        Connect to the database
        :return:
        """
        dprint("")
        dprint("###################")
        dprint("# dbAdmin Connect #")
        dprint("###################")
        dprint("")

        try:
            self.dbconn_userdetails = sqlite3.connect(self.dbfile_userdetails)
            dprint("DB>SQLite Version: " + sqlite3.version)
            self.dbconn_userdetails.commit()

        except Error as e:
            dprint(e)
        finally:
            dprint("DB>Connected to Database File: " + self.dbfile_userdetails)

        self.dbadmin_create_tables()

    def dbadmin_close(self):
        """
        Close all connections to the database
        :return:
        """
        dprint("")
        dprint("#################")
        dprint("# dbAdmin Close #")
        dprint("#################")
        dprint("")

    def dbadmin_create_tables(self):
        """
        Create the default tables and populate with default information.
        :return:
        """
        dprint("")
        dprint("#########################")
        dprint("# dbAdmin Create Tables #")
        dprint("#########################")
        dprint("")
        sql_string = '''CREATE TABLE IF NOT EXISTS UserInfo(
            id integer PRIMARY KEY AUTOINCREMENT,
            email_address text NOT NULL UNIQUE,
            password text,
            first_names text NOT NULL,
            last_name text NOT NULL,
            description text,
            notes text,
            group_id integer NOT NULL
        )'''
        sql_result = self.dbadmin_exec(sql_string)

        sql_string = '''CREATE TABLE IF NOT EXISTS GroupInfo(
            id integer PRIMARY KEY AUTOINCREMENT,
            group_name text UNIQUE,
            group_description text,
            group_notes text
        )
        '''
        sql_result = self.dbadmin_exec(sql_string)

    def dbadmin_exec(self, sql_string, *args, **kwargs):
        action_description = kwargs.get("descriptption", "SQL Exec")
        sql_vars = kwargs.get("sql_vars", False)
        sql_cursor = self.dbconn_userdetails.cursor()

        dprint("")
        dprint("################")
        dprint("# dbAdmin Exec #")
        dprint("################")
        dprint("")

        dprint("-- START " + action_description + "--")
        dprint("SQL String: " + sql_string)
        dprint("SQL Vars: " + repr(sql_vars))
        dprint(type(sql_vars))
        dprint("-- END --")
        try:
            return_value = True
            if sql_vars is False:
                dprint("No SQL Vars")
                sql_cursor.execute(sql_string)
                dprint("No Vars End")
            else:
                dprint("Using SQL Vars: " + repr(sql_vars))
                sql_cursor.execute(sql_string, sql_vars)
                dprint("With Vars END")
            self.dbconn_userdetails.commit()

        except sqlite3.Error as error:
            return_value = False
            print(action_description + " - FAILED")
            print(error)
        #TODO: Return cursor with result so that results can be passed.
        return return_value

    def users_list(self, query_string, query_exact, *args, **kwargs):
        """
        Returns a list of users matching the criteria given below.
        :param query_string: STR - String that will be used in the SELECT statement
        :param query_exact: BOOL - Do we require a full match, or are partial matches OK?
        :param kwargs: altfield - STR - Search a database field otrher than email address. !!TODO!!
        :return: Returns a list of records that match the search query
        """
        dprint("")
        dprint("##############")
        dprint("# Users List #")
        dprint("##############")
        dprint("")

        if query_string is None:
            query_string = "%"

        if query_exact:
            dprint("Search EXACT")
            sql_string = "SELECT * FROM UserInfo where email_address like '" + query_string + "'"
        else:
            dprint("Search loose")
            sql_string = "SELECT * FROM UserInfo where email_address like '%" + query_string + "%'"

        dprint(sql_string)
        sql_cursor = self.dbconn_userdetails.cursor()
        sql_cursor.execute(sql_string)
        return sql_cursor.fetchall()

    def users_get_info(self, user_id):
        """
        Returns a single record representing a single user.  Fails is no records or more than one record.
        :param user_id: INT - An integer that corresponds to the unique id field in the UserInfo table.
        :return: Returns a record for a single user, or False.
        """
        dprint("")
        dprint("##################")
        dprint("# Users Get Info #")
        dprint("##################")
        dprint("")

        sql_string = "SELECT * FROM UserInfo where id = " + str(int(user_id))
        dprint(sql_string)
        sql_cursor = self.dbconn_userdetails.cursor()
        sql_cursor.execute(sql_string)
        return_value = sql_cursor.fetchall()
        return_value = False if len(return_value) != 1 else return_value[0]
        return return_value

    def user_add(self, email, passwd, fname, lname, desc, note, groupid):
        """
        Add a new user to the database.
        :param passwd: STR - Plain text password
        :param fname: STR - First Name for the user
        :param lname: STR - Last name (surname) for the user
        :param desc: STR - Description of the user.
        :param note: STR - Notes relating to the user.
        :param groupid: INT - Integer that corresponds to a group in the group table. !!NOT USED!!
        :return:
        """
        dprint("")
        dprint("############")
        dprint("# User Add #")
        dprint("############")
        dprint("")

        passwd = self.sec_pwd_tool.make_new_password(passwd)
        sql_string = "INSERT INTO UserInfo (email_address, password, first_names, last_name, description, notes, group_id) values(?, ?, ?, ?, ?, ?, ?)"
        sql_vars = (email, passwd, fname, lname, desc, note, groupid)
        return_value = self.dbadmin_exec(sql_string, sql_vars=sql_vars, descriptption="Add User")
        return return_value

    def user_del(self, user_id):
        """
        Deletes a user from the database.
        :param user_id: INT - The unique id of the user as contained in the id field of the UserInfo table
        :return: BOOL - Returns True of delete was successful, otherwise it returns False
        """
        dprint("")
        dprint("###############")
        dprint("# User Delete #")
        dprint("###############")
        dprint("")

        sql_string = "DELETE FROM UserInfo WHERE id = ?"
        sql_vars = (user_id,)
        return_value = self.dbadmin_exec(sql_string, sql_vars=sql_vars, descriptption="Delete User")
        return return_value

    def users_check_auth(self, user_id, my_password, *args, **kwargs):
        """
        Chewcks if the my_password var matches the stored password details for the user given by user_id
        :param user_id: INT - An integer that corresponds to the unique id field in the UserInfo table
        :param my_password: A clear text password that matches what the user would enter
        :param args:
        :param kwargs:
        :return:
        """
        show_details = kwargs.get("show_details", False)
        show_pwdstring = kwargs.get("show_pwdstring", False)
        # print(kwargs)
        # user_info = getUserInfo(UserID)
        user_info = self.users_get_info(user_id)
        # print(user_info)
        if user_info:
            stored_passwd = user_info[2]
            # RET = securePassword.check_password(myPasswd, stored_passwd, showdetails=show_details, showpwdstring=show_pwdstring)
            RET = self.sec_pwd_tool.check_password(my_password, stored_passwd, showdetails=show_details, showpwdstring=show_pwdstring)
        else:
            RET = False
        return RET

def dprint(print_string):
    if DEBUG:
        print(print_string)

if __name__ == '__main__':
    # dbUserManagement.dbadmin_connect()
    pass
