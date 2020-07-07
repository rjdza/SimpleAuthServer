import sqlite3
from sqlite3 import Error
import hashlib, binascii
import os

DBUserDetailsFile = r"database/dbu_userdetails.sqlite3"
connDBUserDetails = ""
DEBUG=False

class clsSecurePassword:
    SaltLength = 32
    SecurityIterations = 100000
    def MakeSalt(self, SaltLength):
        salt = os.urandom(SaltLength)
        return salt

    def MakePass(self,myPassword):
        """
        Create a secure password with embedded salt
        :param myPassword:
        :return:
        """
        salt = self.MakeSalt(self.SaltLength)
        key = hashlib.pbkdf2_hmac('sha256', myPassword.encode('utf-8'), salt, self.SecurityIterations)
        return salt + key

    def CheckPass(self, myPassword, StoredPassword):
        salt = StoredPassword[:self.SaltLength]
        oldKey = StoredPassword[self.SaltLength:]
        newKey = hashlib.pbkdf2_hmac('sha256', myPassword.encode('utf-8'), salt, self.SecurityIterations)
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
    dprint(SQLString)
    SQL_Cursor = connDBUserDetails.cursor()
    SQL_Cursor.execute(SQLString)
    return SQL_Cursor.fetchall()[0]

def addUser(email, passwd, fname, lname, desc, note, groupid):
    passwd = securePassword.MakePass(passwd)
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


if __name__ == '__main__':
    # create_connection(r"C:\sqlite\db\pythonsqlite.db")
    create_connection(DBUserDetailsFile)

# create_connection(DBUserDetailsFile)