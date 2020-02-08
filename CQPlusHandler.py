# -*- coding:utf-8 -*-

import cqplus
import random
import re
import cmd

import init # add,show, and delete admins and groups
#import order # order list

class MainHandler(cqplus.CQPlusHandler):
    def handle_event(self, event, params):

        def repeat(params):
            if params['from_group'] in init.testGruopList:
                self.api.send_group_msg(params['from_group'],params['msg'])
            return 

        if event == "on_private_msg":
            #msg_id = params['msg_id']
            from_qq = params['from_qq']
            msg = params['msg']

            if from_qq == 1412893630: # qq=xdt
                self.api.send_private_msg(1412893630, "Hello")
        if event == "on_group_msg":
            #msg_id = params['msg_id']
            from_qq = params['from_qq']
            from_group = params['from_group']
            msg = params['msg']
            is_anonymous = params['is_anonymous']
            anonymous = params['anonymous']

            repeat(params)
            
        