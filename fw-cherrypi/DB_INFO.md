Database Info
=============

UserInfo
--------
    CREATE TABLE IF NOT EXISTS UserInfo(
            id integer PRIMARY KEY AUTOINCREMENT,
            email_address text NOT NULL UNIQUE,
            password text,
            first_names text NOT NULL,
            last_name text NOT NULL,
            description text,
            notes text,
            group_id integer NOT NULL
`id`: User ID - Integer, unique, and auto-increment  
`email_address`: Email address of user  
`password`: User password, hased with TODO:Hash Algo  
`first_names`: First Name(s)  
`last_name`: Last Name
`description`: User description  
`notes`: User notes
`group_id`: Group ID - Integer that links to groupinfo DB.

GroupInfo
---------
    CREATE TABLE IF NOT EXISTS GroupInfo(
            id integer PRIMARY KEY AUTOINCREMENT,
            group_name text UNIQUE,
            group_description text,
            group_notes text
        )
`id`: Group ID - Integer, unique, and auto-increment  
`group_name`: Name of group.  No spaces, use underscores instead  
`group_description`: Description of group
`group_notes`: Group notes