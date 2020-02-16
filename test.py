import cmd
import usersql

test_dict = {
    'qqid' : 123456,
    'username' : 'test',
    'priv' : 'root',
    'char' : '',
    'groupinfo' : '',
}

user_test = usersql.User(test_dict)

while True:
    msg = input('输入QQbot指令:')
    if cmd.msg_to_cmd(msg):
        tmp = cmd.msg_to_cmd(msg)
        if type(tmp) == str:
            print(tmp)
        else:
            user = usersql.User(usersql.user_dict0)
            send = cmd.bot.cond_cmd(tmp['cmd_name'], user, tmp['params'])
            print(send)
    