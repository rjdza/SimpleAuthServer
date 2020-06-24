import sqlite3
from sqlite3 import Error

DBUserDetailsFile = r"database/dbu_userdetails.sqlite3"
connDBUserDetails = ""

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    global connDBUserDetails
    # conn = None
    try:
        connDBUserDetails = sqlite3.connect(db_file)
        print(sqlite3.version)
        SQL_Cursor = connDBUserDetails.cursor()

        SQL='''CREATE TABLE IF NOT EXISTS UserInfo(
            id integer PRIMARY KEY AUTOINCREMENT,
            email_address text NOT NULL UNIQUE,
            first_names text NOT NULL,
            last_name text NOT NULL,
            description text,
            group_id integer NOT NULL
        )'''
        SQL_Cursor.execute(SQL)

        SQL='''CREATE TABLE IF NOT EXISTS GroupInfo(
            id integer PRIMARY KEY AUTOINCREMENT,
            group_name text UNIQUE,
            group_descrotion text
        )
        '''
        SQL_Cursor.execute(SQL)
        
    except Error as e:
        print(e)
    finally:
        print("Connected to Database File: " + db_file)
        # if connDBUserDetails:
        #     connDBUserDetails.close()

def close_connections():
    global connDBUserDetails
    if connDBUserDetails:
        connDBUserDetails.close()

def connect():
    create_connection(DBUserDetailsFile)

if __name__ == '__main__':
    # create_connection(r"C:\sqlite\db\pythonsqlite.db")
    create_connection(DBUserDetailsFile)

# create_connection(DBUserDetailsFile)