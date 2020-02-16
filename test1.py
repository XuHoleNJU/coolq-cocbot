import usersql
import init
import re
import json
import sqlite3

group_list = [{"group_id": 634501249, "group_name": "\u5168\u7403\u6700\u5927\u4e8c\u6b21\u5143\u7231\u597d\u8005"}, {"group_id": 781480453, "group_name": "\u673a\u5668\u4eba\u7ad9\u8d77\u6765\u4e86\uff01"}, {"group_id": 853186266, "group_name": "\u82cf\u5317\u4eba"}, {"group_id": 1030618409, "group_name": "bot\u6d4b\u8bd5\u7fa4"}, {"group_id": 1034137605, "group_name": "\u7b28\u6bd4\u8dd1\u56e2\u7fa4"}]
mem_list1 = [{"age": 20, "area": "", "card": "\u7b28\u6bd4", "card_changeable": False, "group_id": 634501249, "join_time": 1558802532, "last_sent_time": 1581661502, "level": "", "nickname": "\u75f0\u5410\u6b62\u7981", "role": 1, "sex": 0, "title": "", "title_expire_time": 0, "unfriendly": False, "user_id": 1412893630}, {"age": 21, "area": "", "card": "Sebastian", "card_changeable": False, "group_id": 634501249, "join_time": 1546087051, "last_sent_time": 1579961467, "level": "", "nickname": "\u5929\u8f6e", "role": 3, "sex": 0, "title": "", "title_expire_time": 0, "unfriendly": False, "user_id": 1461275735}, {"age": 30, "area": "", "card": "\u81ea\u9002\u5e94NPC", "card_changeable": False, "group_id": 634501249, "join_time": 1579952427, "last_sent_time": 1581661502, "level": "", "nickname": "\u9f99\u7389\u6d9b", "role": 1, "sex": 0, "title": "", "title_expire_time": 0, "unfriendly": False, "user_id": 1747975784}, {"age": 17, "area": "", "card": "", "card_changeable": False, "group_id": 634501249, "join_time": 1550205100, "last_sent_time": 1579961114, "level": "", "nickname": "\u661f\u7a7a\u308a\u3093", "role": 1, "sex": 1, "title": "", "title_expire_time": 0, "unfriendly": False, "user_id": 2389648900}]
mem_list2 = [{"age": 0, "area": "", "card": "", "card_changeable": False, "group_id": 1030618409, "join_time": 1580880096, "last_sent_time": 1581680644, "level": "", "nickname": "\u8fbe", "role": 1, "sex": 0, "title": "", "title_expire_time": 0, "unfriendly": False, "user_id": 719034161}, {"age": 20, "area": "", "card": "\u7b28\u6bd4", "card_changeable": False, "group_id": 1030618409, "join_time": 1579189048, "last_sent_time": 1581681362, "level": "", "nickname": "\u75f0\u5410\u6b62\u7981", "role": 3, "sex": 0, "title": "", "title_expire_time": 0, "unfriendly": False, "user_id": 1412893630}, {"age": 30, "area": "", "card": "", "card_changeable": False, "group_id": 1030618409, "join_time": 1579189048, "last_sent_time": 1581680437, "level": "", "nickname": "\u9f99\u7389\u6d9b", "role": 2, "sex": 0, "title": "", "title_expire_time": 0, "unfriendly": False, "user_id": 1747975784}, {"age": 17, "area": "", "card": "", "card_changeable": False, "group_id": 1030618409, "join_time": 1579189048, "last_sent_time": 1581252096, "level": "", "nickname": "\u661f\u7a7a\u308a\u3093", "role": 2, "sex": 1, "title": "", "title_expire_time": 0, "unfriendly": False, "user_id": 2389648900}, {"age": 0, "area": "", "card": "", "card_changeable": False, "group_id": 1030618409, "join_time": 1579189048, "last_sent_time": 1579189048, "level": "", "nickname": "\u4e0d\u60f3\u8df3\u821e", "role": 1, "sex": 255, "title": "", "title_expire_time": 0, "unfriendly": False, "user_id": 3232943587}]
user_dict_dict = {}

for group in group_list:
    if group["group_id"] == 634501249:
        mem_list = mem_list1
    if group["group_id"] == 1030618409:
        mem_list = mem_list2
    for member in mem_list:
        if member['user_id'] not in user_dict_dict.keys():
            user_dict = {
                'qqid' : member['user_id'],
                'username' : member['nickname'],
                'priv' : 'gene',
                'char' : [usersql.default_char_dict],
            }
            if member['card']:
                user_dict['groupinfo'] = {group['group_id'] : member['card']}
            else:
                user_dict['groupinfo'] = {group['group_id'] : member['nickname']}
            user_dict_dict[member['user_id']] = user_dict
        else:
            if member['card']:
                user_dict_dict[member['user_id']]['groupinfo'][group['group_id']] = member['card']
            else:
                user_dict_dict[member['user_id']]['groupinfo'][group['group_id']] = member['nickname']
        for admin_id in init.admin_list:
            user_dict_dict[admin_id]['priv'] = 'admin'
        for root_id in init.root_admin:
            user_dict_dict[root_id]['priv'] = 'root'

#print(user_dict_dict)
sql = usersql.UserSQL('user.db')

for key in user_dict_dict.keys():
    user = usersql.User(user_dict_dict[key])
    result = sql.sql_insert_user(user)
    if result == True:
        print("成功添加%d"%(user.qqid)) 
    else: 
        print(result+"qq:%d"%(user.qqid))    
send = "刷新数据库成功，共导入%d名用户"%(len(user_dict_dict))

# txt1 = '''
#     [{"age": 20, "area": "", "card": "\u7b28\u6bd4", "card_changeable": false, "group_id": 634501249, "join_time": 1558802532, "last_sent_time": 1581661502, "level": "", "nickname": "\u75f0\u5410\u6b62\u7981", "role": 1, "sex": 0, "title": "", "title_expire_time": 0, "unfriendly": false, "user_id": 1412893630}, {"age": 21, "area": "", "card": "Sebastian", "card_changeable": false, "group_id": 634501249, "join_time": 1546087051, "last_sent_time": 1579961467, "level": "", "nickname": "\u5929\u8f6e", "role": 3, "sex": 0, "title": "", "title_expire_time": 0, "unfriendly": false, "user_id": 1461275735}, {"age": 30, "area": "", "card": "\u81ea\u9002\u5e94NPC", "card_changeable": false, "group_id": 634501249, "join_time": 1579952427, "last_sent_time": 1581661502, "level": "", "nickname": "\u9f99\u7389\u6d9b", "role": 1, "sex": 0, "title": "", "title_expire_time": 0, "unfriendly": false, "user_id": 1747975784}, {"age": 17, "area": "", "card": "", "card_changeable": false, "group_id": 634501249, "join_time": 1550205100, "last_sent_time": 1579961114, "level": "", "nickname": "\u661f\u7a7a\u308a\u3093", "role": 1, "sex": 1, "title": "", "title_expire_time": 0, "unfriendly": false, "user_id": 2389648900}]
# '''
# memlist1 = json.loads(txt1)
# print('txt1')
# txt2 = re.sub('false','False',txt1)
# mem_list2 = json.loads(txt2)
# print('txt2')

# dict1 = {"a":True,"b":False,"c":"True","d":"text"}
# str1 = json.dumps(dict1)
# print(str1)