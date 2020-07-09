#!/usr/bin/python3
import database as db
from database import securePassword as pwdTool
import sys

PASSWD=sys.argv[1]
SALT=False
try:
    SALT=sys.argv[2]
except:
    pass

if not SALT:
    print("Generating new salt...")
    SALT=pwdTool.MakeSalt(pwdTool.SaltLength)

STOREDPWD=pwdTool.MakePass(SALT,PASSWD)
ENCPWD=STOREDPWD[(pwdTool.SaltLength*2):]

# print(sys.argv)
print("  Password: " + PASSWD)
print("      Salt: " + str(SALT))
print("   Enc Pwd: " + ENCPWD)
print("Stored PWD: " + STOREDPWD)