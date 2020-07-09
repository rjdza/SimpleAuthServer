import sqlite3
from sqlite3 import Error
import hashlib, binascii
import os

DBUserDetailsFile = r"database/dbu_userdetails.sqlite3"
connDBUserDetails = ""
DEBUG=False

class clsSecurePassword:
    """
    Password management Class.

    NOTE: Changing vars. If you change these variables, previously stored passwords will no longer work.
    :var SaltLength: INT - System default length for salt.
    :var SecurityIterations: INT - Number of hash iterations used to make brute forcing take longer.
    """
    SaltLength = 32
    SecurityIterations = 100000

    def MakeSalt(self, SaltLength):
        """
        Create a string to be used to salt the password. DOES NOT use the built-in SaltLength var!

        :param SaltLength: INT - The length of the salt to create.
        :return: Returns a string.
        """
        salt = os.urandom(SaltLength)
        RET=binascii.b2a_hex(salt).decode("utf-8")
        return RET

    def NewPass(self,myPassword):
        """
        Create a NEW secure password hash with embedded salt
        :param myPassword: STR - The password to use for the hash.
        :return: STR - Retrurns a string that contains both the salt and the key, in that order.
        """
        salt = self.MakeSalt(self.SaltLength)
        PASSWDSTRING = self.MakePass(salt, myPassword)
        return PASSWDSTRING

    def MakePass(self, salt, myPassword):
        """
        Create a secure password with embedded salt.
        :param myPassword: STR - The plain text password to use for the hash.
        :param salt: STR - Salt used to ensure password uniqueness.
        :return:
        """
        salt_bin = binascii.a2b_hex(salt)
        key_bin = hashlib.pbkdf2_hmac('sha256', myPassword.encode('utf-8'), salt_bin, self.SecurityIterations)
        key = binascii.b2a_hex(key_bin).decode("utf-8")
        return salt + key

    def CheckPass(self, myPassword, StoredPassword, *args, **kwargs):
        """
        Compares the plain text password provided with the hashed hex password stored in the database.
        :param myPassword: STR - Plain text password
        :param StoredPassword: STR Salt + Password string
        :param args:
        :param kwargs: showdetails - BOOL - Display some internal vars
        :param kwargs: showpwdstring - BOOL - Display the entire stored password string
        :return: BOOL - Returns True is passwords match, False if they do not.
        """
        # print(kwargs)
        SHOWDETAILS = kwargs.get("showdetails", False)
        SHOWPWDSTRING = kwargs.get("showpwdstring", False)
        salt   =StoredPassword[:(self.SaltLength * 2)]
        oldKey = StoredPassword[(self.SaltLength * 2):]
        salt_bin = binascii.a2b_hex(salt)
        newKey = binascii.b2a_hex(hashlib.pbkdf2_hmac('sha256', myPassword.encode('utf-8'), salt_bin, self.SecurityIterations)).decode("utf-8")
        PWDMATCH = "Passwords MATCH" if oldKey == newKey else "Passwords DO NOT MATCH"

        if self.SaltLength == (len(salt)/2):
            LENCHK = "Salt matches system length of " + str(self.SaltLength)
        else:
            LENCHK = "Salt does NOT match system length.  System = " + str(self.SaltLength) + " while stored is " + str((len(salt)/2))

        if SHOWPWDSTRING:
            print("")
            print("-----START OF STORED PASSWORD STRING-----")
            print(StoredPassword)
            print("-----END OF STORED PASSWORD STRING-----")

        if SHOWDETAILS:
            print("")
            print("  PWD check str: " + myPassword)
            print(" PWD check hash: " + newKey)
            print("Stored PWD hash: " + oldKey)
            print("PWD comparisson: " + PWDMATCH)
            print("           Salt: " + salt)
            print("    Salt Length: " + LENCHK)
            print("")

        RET=True if oldKey == newKey else False
        return RET

securePassword = clsSecurePassword()

def dprint(PrintStr):
    if DEBUG:
        print(PrintStr)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    global connDBUserDetails
    # conn = None
    try:
        connDBUserDetails = sqlite3.connect(db_file)
        dprint("DB>SQLite Version: " + sqlite3.version)
        SQL_Cursor = connDBUserDetails.cursor()

        SQL='''CREATE TABLE IF NOT EXISTS UserInfo(
            id integer PRIMARY KEY AUTOINCREMENT,
            email_address text NOT NULL UNIQUE,
            password text,
            first_names text NOT NULL,
            last_name text NOT NULL,
            description text,
            notes text,
            group_id integer NOT NULL
        )'''
        SQL_Cursor.execute(SQL)
        connDBUserDetails.commit()

        # addUser('admin', 'bob', 'Admin', 'User', 'Auto-created admin user', 'Do not delete', 0)

        SQL='''CREATE TABLE IF NOT EXISTS GroupInfo(
            id integer PRIMARY KEY AUTOINCREMENT,
            group_name text UNIQUE,
            group_description text,
            group_notes text
        )
        '''
        SQL_Cursor.execute(SQL)
        connDBUserDetails.commit()

    except Error as e:
        dprint(e)
    finally:
        dprint("DB>Connected to Database File: " + db_file)
        # if connDBUserDetails:
        #     connDBUserDetails.close()

def close_connections():
    global connDBUserDetails
    if connDBUserDetails:
        connDBUserDetails.close()

def close():
    close_connections()

def connect():
    create_connection(DBUserDetailsFile)

def listUsers(searchQuery, searchExact):
    global connDBUserDetails
    if searchQuery == None:
        searchQuery = "%"
    if searchExact:
        dprint("Search EXACT")
        SQL = "SELECT * FROM UserInfo where email_address like '" + searchQuery + "'"
    else:
        dprint("Search loose")
        SQL = "SELECT * FROM UserInfo where email_address like '%" + searchQuery + "%'"
    dprint(SQL)
    SQL_Cursor = connDBUserDetails.cursor()
    SQL_Cursor.execute(SQL)
    return SQL_Cursor.fetchall()

def getUserInfo(UserID):
    global connDBUserDetails
    SQLString = "SELECT * FROM UserInfo where id = " + str(int(UserID))
    # print(SQLString)
    SQL_Cursor = connDBUserDetails.cursor()
    SQL_Cursor.execute(SQLString)
    RET = SQL_Cursor.fetchall()
    RET = False if len(RET) != 1 else RET[0]
    return RET

def addUser(email, passwd, fname, lname, desc, note, groupid):
    passwd = securePassword.NewPass(passwd)
    SQLString = "INSERT INTO UserInfo (email_address, password, first_names, last_name, description, notes, group_id) values(?, ?, ?, ?, ?, ?, ?)"
    SQLVars = (email, passwd, fname, lname, desc, note, groupid)
    RET = sqlExec(SQLString, SQLVars, "Add User")
    return RET

def delUser(UserID):
    SQLString = "DELETE FROM UserInfo WHERE id = ?"
    SQLVars = (str(UserID))
    RET=sqlExec(SQLString, SQLVars, "Delete User")
    return RET

def sqlExec(SQLString, SQLVars, actionDescription):
    global connDBUserDetails
    SQL_Cursor = connDBUserDetails.cursor()
    dprint(actionDescription)
    dprint(SQLString)
    dprint(SQLVars)
    try:
        RET=True
        SQL_Cursor.execute(SQLString, SQLVars)
        connDBUserDetails.commit()
    except sqlite3.Error as error:
        RET=False
        print(actionDescription + " - FAILED")
        print(error )
    return RET

def checkAuth(UserID, myPasswd, *args, **kwargs):
    SHOWDETAILS = kwargs.get("showdetails", False)
    SHOWPWDSTRING = kwargs.get("showpwdstring", False)
    # print(kwargs)
    USERINFO = getUserInfo(UserID)
    # print(USERINFO)
    if USERINFO:
        storedPasswd = USERINFO[2]
        RET = securePassword.CheckPass(myPasswd, storedPasswd, showdetails=SHOWDETAILS, showpwdstring=SHOWPWDSTRING)
    else:
        RET=False
    return RET

if __name__ == '__main__':
    # create_connection(r"C:\sqlite\db\pythonsqlite.db")
    create_connection(DBUserDetailsFile)

# create_connection(DBUserDetailsFile)