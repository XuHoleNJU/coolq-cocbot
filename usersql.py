import sqlite3
import json
import sys
# 两个类，角色卡信息和用户信息，都用dict初始化
class Character:
    char_dict = {}
    def __init__(self, char_dict):
        self.char_dict = char_dict
        self.label = char_dict['label']
        self.name = char_dict['name']
        self.gender = char_dict['gender']
        self.age = char_dict['age']
        self.strength = char_dict['strength']
        self.con = char_dict['con']
        self.siz = char_dict['siz']
        self.dex = char_dict['dex']
        self.app = char_dict['app']
        self.int = char_dict['int']
        self.pow = char_dict['pow']
        self.edu = char_dict['edu']
        self.luc = char_dict['luc']

    def disp_dict(self):
        return self.char_dict

class User:
    user_dict = {}
    def __init__(self, user_dict):
        self.user_dict = user_dict
        self.qqid = user_dict['qqid']
        self.username = user_dict['username']
        self.priv = user_dict['priv']
        self.char = user_dict['char']
        self.groupinfo = user_dict['groupinfo'] #群昵称等信息

    def refresh_nickname(self, qqid):
        pass

    def disp_user(self):
        return self.user_dict

user_dict0 = {
    'qqid' : 1,
    'username' : '',
    'priv' : 'gene',
    'char' : '',
    'groupinfo' : '',
}

default_char_dict = {
    'label' : 'default'
}

class UserSQL:
    def __init__(self, db):
        self.db = db

    def sql_insert_user(self, user):
        userinfo = (user.qqid, user.username, user.priv, json.dumps(user.groupinfo), json.dumps(user.char))
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('insert into user (qqid, username, privilege, groupinfo, character) \
                values (?, ?, ?, ?, ?)', userinfo)
            conn.commit()
            conn.close()
            return True
        except:
            return "error:" + str(sys.exc_info()[0]) + str(sys.exc_info()[1])

    def sql_select_user(self):
        cmd = "SELECT qqid, username, privilege, groupinfo, character from user"
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.execute(cmd)
            data = []
            for row in cursor:
                data.append(row)
            conn.close()
            return data
        except:
            return "error:" + str(sys.exc_info()[0]) + str(sys.exc_info()[1])

    def sql_get_user(self, qqid):
        data = self.sql_select_user()
        user_dict = user_dict0
        for row in data:
            if qqid == row[0]:
                user_dict = {
                    'qqid' : row[0],
                    'username' : row[1],
                    'priv' : row[2],
                    'groupinfo' : row[3],
                    'char' : row[4],
                }
        return User(user_dict)

    def sql_delete_user(self, user):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute("DELETE from user where qqid= ?;", (user.qqid,))
            conn.commit()
            conn.close()
            return True
        except:
            return "error:" + str(sys.exc_info()[0]) + str(sys.exc_info()[1])
    
    def sql_insert_char(self, user, char):
        user.char.append(char.disp_dict())
        update = (json.dumps(user.char), user.qqid)
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute("update user set char = ? where qqid = ? ", update)
            conn.commit()
            conn.close()
            return True
        except:
            return "error:" + str(sys.exc_info()[0]) + str(sys.exc_info()[1])

    def sql_delete_char(self, user, char):
        for i in range(len(user.char)):
            if user.char[i] == char.disp_dict():
                del user.char[i]
                break
        update = (json.dumps(user.char), user.qqid)
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute("update user set char = ? where qqid = ? ", update)
            conn.commit()
            conn.close()
            return True
        except:
            return "error:" + str(sys.exc_info()[0]) + str(sys.exc_info()[1])

    def sql_update_char(self, user, char_label, update_dict):
        for char_dict in user.char:
            if char_dict['label'] == char_label:
                for key in update_dict.keys:
                    char_dict[str(key)] = update_dict[str(key)]
        update = (json.dumps(user.char), user.qqid)
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute("update user set char = ? where qqid = ? ", update)
            conn.commit()
            conn.close()
            return True
        except:
            return "error:" + sys.exc_info()[0] + sys.exc_info()[1]


# conn = sqlite3.connect('user.db')
# print("successfully opened")
# c = conn.cursor()

# c.execute('''create table user
#     (qqid int primary key not null,
#     username    text not null,
#     privilege   text not null,
#     groupinfo   text not null,
#     character   text);
#     ''')
# print("table successfully created")
# conn.commit()

# c.execute(sql_insert_user(xuholeUser))
# c.execute(sql_insert_user(terryUser))

# print('succefully inserted')
# conn.commit()


# cursor = c.execute(sql_select_user())
# for row in cursor:
#     print("qqid = " + str(row[0]))
#     print("username = " + str(row[1]))
#     print("priv = " + str(row[2]))
#     char_dict_list = json.loads(row[3])
#     print(str(row[1]) + " has " + str(len(char_dict_list)) + " character(s):")
#     for i in range(len(char_dict_list)):
#         print(str(char_dict_list[i]))


# c.execute('''CREATE TABLE COMPANY
#        (ID INT PRIMARY KEY     NOT NULL,
#        NAME           TEXT    NOT NULL,
#        AGE            INT     NOT NULL,
#        ADDRESS        CHAR(50),
#        SALARY         REAL);''')
# print("Table created successfully")
# conn.commit()

# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (1, 'Paul', 32, 'California', 20000.00 )")
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
# conn.commit()
# print("Records created successfully")

# cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
# for row in cursor:
#    print( "ID = " + str(row[0]))
#    print("NAME = " + str(row[1]))
#    print("ADDRESS = " + str(row[2]))
#    print("SALARY = " + str(row[3]) + "\n")

# print("Operation done successfully")

# c.execute("DELETE from COMPANY where ID=2;")
# conn.commit()
# print("Total number of rows deleted :" + str(conn.total_changes))

# cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
# for row in cursor:
#    print( "ID = " + str(row[0]))
#    print("NAME = " + str(row[1]))
#    print("ADDRESS = " + str(row[2]))
#    print("SALARY = " + str(row[3]) + "\n")

# print("Operation done successfully")

# conn.close()