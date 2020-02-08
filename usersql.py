import sqlite3
import json

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

    def refresh_nickname(self, qqid):
        pass

    def disp_user(self):
        return self.user_dict

char1_dict = {
    'label' : 'Tom',
    'name' : 'Thomas Edison',
    'strength' : 90,
    'con' : 80,
    'siz' : 70,
    'dex' : 60,
    'app' : 50,
    'int' : 40,
    'pow' : 30,
    'edu' : 20,
    'luc' : 50,
    'age' : 20,
    'gender' : 'M'
}
char2_dict = {
    'label' : 'terry',
    'name' : 'Terry Geng',
    'strength' : 50,
    'con' : 50,
    'siz' : 65,
    'dex' : 45,
    'app' : 50,
    'int' : 75,
    'pow' : 40,
    'edu' : 70,
    'luc' : 30,
    'age' : 20,
    'gender' : 'M'
}
char3_dict = {
    'label' : 'lixi',
    'name' : 'Xi Li',
    'strength' : 40,
    'con' : 50,
    'siz' : 40,
    'dex' : 60,
    'app' : 60,
    'int' : 75,
    'pow' : 40,
    'edu' : 70,
    'luc' : 90,
    'age' : 20,
    'gender' : 'F'
}
default_char_dict = {
    'label' : 'default'
}

tomChar = Character(char1_dict)
terryChar = Character(char2_dict)
xiChar = Character(char3_dict)


user1_dict = {
    'qqid' : 1412893630,
    'username' : '痰吐止禁',
    'priv' :  'root',
    'char' : [tomChar.disp_dict()]
}

user2_dict = {
    'qqid' : 719034161,
    'username' : '达',
    'priv' :  'root',
    'char' : [terryChar.disp_dict(), xiChar.disp_dict()]
}

xuholeUser = User(user1_dict)
terryUser = User(user2_dict)

class UserSQL:
    def __init__(self):
        self.conn = sqlite3.connect('user.db')
        self.curs = self.conn.cursor
    
    def sql_insert_user(self, user):
        msg = ''' insert into user (qqid, username, privilege, character) \
            values (%d, %s, %s, %s); \
                ''' % (user.qqid, user.username, user.priv, json.dumps(user.char))
        self.curs.execute(msg)
        self.conn.commit()

    def sql_select_user(self):
        msg = "SELECT qqid, username, privilege, character from user"
        cursor = self.curs.execute(msg)
        return cursor
    
    def sql_delete_user(self, user):
        msg = "DELETE from user where qqid= %d ;" % (user.qqid)
        self.curs.execute(msg)
        self.conn.commit()
    
    def sql_insert_char(self, user, char):
        user.char.append(char.disp_dict())
        msg = '''update user set char = '%s' where qqid = %d 
            ''' % (json.dumps(user.char), user.qqid)
        self.curs.execute(msg)
        self.conn.commit()

    def sql_delete_char(self, user, char):
        for i in range(len(user.char)):
            if user.char[i] == char.disp_dict():
                del user.char[i]
                break
        msg = '''update user set char = '%s' where qqid = %d 
            ''' % (json.dumps(user.char), user.qqid)
        self.curs.execute(msg)
        self.conn.commit()

    def sql_update_char(self, user, char_label, update_dict):
        for char_dict in user.char:
            if char_dict['label'] == char_label:
                for key in update_dict.keys:
                    char_dict[str(key)] = update_dict[str(key)]
        msg = '''update user set char = '%s' where qqid = %d 
            ''' % (json.dumps(user.char), user.qqid)
        self.curs.execute(msg)
        self.conn.commit()

# conn = sqlite3.connect('user.db')
# print("successfully opened")
# c = conn.cursor()

# c.execute('''create table user
#     (qqid int primary key not null,
#     username    text not null,
#     privilege   text not null,
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