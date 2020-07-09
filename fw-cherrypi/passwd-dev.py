#!/usr/bin/python3
import database as db
import sys
import binascii

def main():
    sec_pwd_tool = db.ClassSecurePassword()

    password = sys.argv[1]
    salt = False
    try:
        salt = sys.argv[2]
    except:
        pass

    if not salt:
        print("Generating new salt...")
        print("System Salt Length: ", str(sec_pwd_tool.salt_length))
        try:
            salt = sec_pwd_tool.make_salt(sec_pwd_tool.salt_length)
        except binascii.Error as error:
            print("Error creating salt: ", error)

    try:
        stored_password = sec_pwd_tool.make_password(salt, password)
    except binascii.Error as error:
        print("Error hashing password: ", error)
        print(" - Is your salt a proper hexadecimal string?")
        print(" - Is your password properly quoted?")
        quit(127)

    encrypted_password = stored_password[(sec_pwd_tool.salt_length * 2):]

    # print(sys.argv)
    print("  Password: " + password)
    print("      Salt: " + str(salt))
    print("   Enc Pwd: " + encrypted_password)
    print("Stored PWD: " + stored_password)

def help():
    print("""
This tool creates a password string that includes both the salt and the hashed password in HEX format. It takes two arguments - The password, and the seed.

The first argument is the password to hash.  This can be plain, but if it contains spaces it needs to be quoted. If it contains special characters, it may need to be quoted in single quotes, eg: 'password !'.

The second argument is the seed, and may be omitted.  If omitted, a new seed is generated.  If provided, the given seed is used.  
    """)

    pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            main()
        except Exception as error:
            print(repr(error))
    else:
        help()


