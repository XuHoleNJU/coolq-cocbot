# -*- coding:utf-8 -*-

import cqplus
import random
import re
import cmd
import json
import time

import usersql
import init # add,show, and delete admins and groups
#import order # order list

class MainHandler(cqplus.CQPlusHandler):
    def handle_event(self, event, params):
        
        if event == "on_private_msg":
            #msg_id = params['msg_id']
            from_qq = params['from_qq']
            msg = params['msg']
            if from_qq == 1412893630: # qq=xdt
                self.api.send_private_msg(1412893630, "I am alive.")
        
        if event == "on_group_msg":
            #msg_id = params['msg_id']
            from_qq = params['from_qq']
            from_group = params['from_group']
            msg = params['msg']
            #is_anonymous = params['is_anonymous']
            #anonymous = params['anonymous']
            if from_group in init.test_group_list:
                if cmd.msg_to_cmd(msg):
                    tmp = cmd.msg_to_cmd(msg)
                    if type(tmp) == str:
                        self.api.send_group_msg(from_group, tmp)
                    else:
                        sql = usersql.UserSQL('user.db')
                        user = sql.sql_get_user(from_qq)
                        send = cmd.bot.cond_cmd(tmp['cmd_name'], user, tmp['params'])
                        self.api.send_group_msg(from_group, send)
                if from_qq in init.admin_list:
                    if msg == 'lsgrp':
                        group_list = self.api.get_group_list()
                        bot_qq = self.api.get_login_user_id()
                        send = "%d加入的QQ群如下：\n" %(bot_qq)
                        for dict in group_list:
                            send += '%s(%d)\n' %(dict['group_name'], dict['group_id'])
                        self.api.send_group_msg(from_group, send)
                if msg == 'rfrdb':
                    group_list = self.api.get_group_list()
                    
                    bot_qq = self.api.get_login_user_id()
                    user_dict_dict = {} # key = qq_id, content = user_dict\
                    
                    for group in group_list:
                        mem_list = self.api.get_group_member_list(group['group_id'])
                        for member in mem_list:
                            if member['user_id'] not in user_dict_dict.keys():
                                user_dict = {
                                    'qqid' : member['user_id'],
                                    'username' : member['nickname'],
                                    'priv' : 'gene',
                                    'char' : [usersql.default_char_dict]
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
                            
                    sql = usersql.UserSQL('user.db')
                    count = 0

                    for key in user_dict_dict.keys():
                        user = usersql.User(user_dict_dict[key])
                        result = sql.sql_insert_user(user)
                        if result == True:
                            count += 1
                            self.api.send_group_msg(from_group, "成功添加%d"%(user.qqid))    
                    send = "刷新数据库成功，共导入%d名新用户，现有%d名用户"%(count, len(user_dict_dict))
                    self.api.send_group_msg(from_group, send)

                if msg == "lsusr":
                    sql = usersql.UserSQL('user.db')
                    data = sql.sql_select_user()
                    usernum = len(data)
                    bot_qq = self.api.get_login_user_id()
                    send = "%d共有%d个用户：(最多显示5个)\n" %(bot_qq, usernum)
                    count = 0
                    for row in data:
                        if count == 5:
                            break
                        qq_id = row[0]
                        username = row[1]
                        priv = row[2]
                        charnum = len(json.loads(row[4]))
                        send += "%s(%d),权限：%s, 人物卡数量：%d\n" %(username, qq_id, priv, charnum)
                        count += 1
                    self.api.send_group_msg(from_group, send)

        if event == 'on_group_member_increase':
            from_qq = params['from_qq']
            from_group = params['from_group']
            mem_info = self.api.get_group_member_info(from_group, from_qq, True)
            send = "欢迎%s进群~~输入.help查看可用指令列表"%(mem_info['nickname'])
            self.api.send_group_msg(from_group, send)

        if event == 'on_group_member_decrease':
            from_qq = params['from_qq']
            from_group = params['from_group']
            send = "呜呜呜，%d离开了我们"%(from_qq)
            self.api.send_group_msg(from_group, send)

