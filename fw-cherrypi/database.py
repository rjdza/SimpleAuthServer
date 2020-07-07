import sqlite3
from sqlite3 import Error
import hashlib
import os

DBUserDetailsFile = r"database/dbu_userdetails.sqlite3"
connDBUserDetails = ""
DEBUG=False

class clsSecurePassword:
    SaltLength = 32
    SecurityIterations = 100000
    def MakePass(self,myPassword):
        salt = os.urandom(self.SaltLength)
        key = hashlib.pbkdf2_hmac('sha256', myPassword.encode('utf-8'), salt, self.SecurityIterations)
        # if self.CheckPass(myPassword,salt+key):
        #     print("Password checks out OK!")
        # else:
        #     print("Password NOT OK!")
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

def addUser(email, passwd, fname, lname, desc, note, groupid):
    global connDBUserDetails
    global securePassword
    SQL_Cursor = connDBUserDetails.cursor()
    dprint((email, passwd, fname, lname, desc, note, groupid))
    passwd = securePassword.MakePass(passwd)
    try:
        SQL_Cursor.execute("INSERT INTO UserInfo (email_address, password, first_names, last_name, description, notes, group_id) values(?, ?, ?, ?, ?, ?, ?)", (email, passwd, fname, lname, desc, note, groupid))
        connDBUserDetails.commit()
        RET=True
    except sqlite3.Error as error:
        RET=False
        print("Failed to add user.")
        print(error )
    SQL_Cursor.close
    return RET

def delUser(UserID):
    # global connDBUserDetails
    # SQL_Cursor = connDBUserDetails.cursor()
    # SQL = "DELETE FROM UserInfo WHERE id = " + str(UserID)
    # try:
    #     RET=True
    #     SQL_Cursor.execute(SQL)
    #     connDBUserDetails.commit()
    # except sqlite3.Error as error:
    #     RET=False
    #     print("Failed to delete user.")
    #     print(error )
    # return RET
    SQL = "DELETE FROM UserInfo WHERE id = " + str(UserID)
    RET=sqlExec(SQL, "Delete User")
    return RET

def sqlExec(SQL, actionDescription):
    global connDBUserDetails
    SQL_Cursor = connDBUserDetails.cursor()
    try:
        RET=True
        SQL_Cursor.execute(SQL)
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