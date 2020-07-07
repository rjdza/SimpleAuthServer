Commandline Interface (CLI)
===========================

Authentication Functions
------------------------

- Authorise IP
- Authorise Subnet

##### Authorise IP
`--authip IP_ADDRESS`

Add single IP_ADDRESS to list of authorised IP addresses.

##### Authorise IP Subnet
`--authsubnet IP_SUBNET`

Add IP_SUBNET [CIDR](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) subnet to list of authorised IP addresses.

User Functions
--------------

- List users
- Add user(s)
- Delete user(s)
- Modify User
- Disable / Enable User

##### General Options
`--username`
 
 `--userpattern`
 
 `--password`

##### List Users
`-l, --list`

##### Add Users
`-a, --adduser`

##### Delete Users
`-d, --deluser`

###### Depends on 
Modify users account options

##### Modify Users
`-m, --modify`    
`--set-pass`  
`--set-email`  
`--set-group`  
`--set-fname`   
`--set-lname`   
`--set-desc`   


TODO: what other options are needed?

##### Disable / Enable User
Toggle: `-x`  
Enable: `--enable`  
Disable: `--disable`  


Ardparse Notes
--------------
### Positional / Subparsers

### Argument Groups
(https://docs.python.org/3/library/argparse.html#argument-groups)



```grp_auth = parser.add_argument_group("Auth Functions")
grp_users = parser.add_argument_group("User Functions")

grp_auth.add_argument('-i', '--ip', dest="action", action="store_const", const="auth.ip",
                      help="Authorise IP Address")

grp_users.add_argument('-l', '--list', dest="action", action="store_const", const="users.list",
                       help="List users")

grp_users.add_argument('-a', '--adduser',dest="action", action="store_const", const="users.add",
                       help="Add user")

grp_users.add_argument('-d', '--deluser',dest="action", action="store_const", const="users.del",
                       help="Delete user")

grp_users.add_argument('--setpass',dest="action", action="store_const", const="users.setpass",
                       help="Change User Password")

```