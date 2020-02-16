import re
import math
import random

class Bot:

    def __init__(self, command_dict):
        self.command_dict = command_dict
    
    def check_priv(self, cmd_name, user):
        if self.command_dict[cmd_name].priv == 'root':
            if user.priv != 'root':
                return False
        if self.command_dict[cmd_name].priv == 'admin':
            if user.priv == 'gene':
                return False
        return True
    
    def cond_cmd(self, cmd_name, user, params):
        if self.check_priv(cmd_name, user):
            return self.command_dict[cmd_name].command(params)
        else:
            return "error: 此用户无权限"
    
    
help_dict = {
    'all' : '''输入.help [指令名(不加.)]查询相应指令的语法
    .mkchar 生成COC7角色
    .r[计算式] 投掷和计算
    .rd 默认骰1D100
    文档网站正在制作，报bug请联系QQ1412893630''',
    'help':'帮助指令。输入.help查看全部可以使用的指令，输入.help [指令名(不加.)]查询相应指令的语法。',

    'coc':'COC7指令：\n.makechar .rd 默认骰，投掷1d100',
    'r':'.r[计算式] [tag]，如.rd6, .r2d6, .rd4+d6，支持四则运算和乘方(^)',
    'rd':'.rd [tag]，投掷一个100面骰（默认）',
    'ra':'.ra[数值/属性名] [tag]，属性名支持中文，英文和英文缩写，不区分大小写',
    'mkchar':'输入.mkchar [个数,默认1]生成COC7规则基础人物属性',
    'lschar':'输入.lschar 查看自己拥有的所有人物卡',
    'swchar':'.swchar [角色卡名]，切换到对应的角色卡', # Terry named the command
    'stchar':'.set [角色卡名] <赋值语句>，例如.set thomas str90 体质90 DEX90，支持中文，英文和英文缩写，不区分大小写',
    'pwc':'.pwc(print working character)，显示目前操作的人物卡名称(区分大小写！)',
    'dispchar':'.dispchar [属性] 显示指定人物卡的指定属性，-all显示所有属性',
    'usrn':'.usrn [名字]设置您在bot上的全局用户名，默认值为您的QQ昵称',
    'grpn':'.grpn [名字]设置您在本群的局域用户名，默认值为您的群名片',
    }

class Help:
    
    def __init__(self, name, priv, helpinfo):
        self.name = name
        self.priv = priv
        self.helpinfo = helpinfo
    def command(self, params):
        # cmd = 指令名称，需要在helpList里
        cmd = params[0]
        msg = 'error: 未找到指令，请检查指令是否输入正确'
        if cmd in help_dict.keys():
            msg = help_dict[cmd]
        if cmd == '':
            msg = help_dict['all']
        return msg
cmd_help = Help('help', 'gene', help_dict['help'])

class RollDice:
    
    def __init__(self, name, priv, helpinfo):
        self.name = name
        self.priv = priv
        self.helpinfo = helpinfo
    
    def re_dice(self, matched):
        if matched.group(2) == '':
            dice = 100
        else:
            dice = int(matched.group(2))
        if matched.group(1) in ['', '1']:
            return str(math.ceil(random.uniform(0,dice)))
        else:
            send = '('
            for i in range(int(matched.group(1))):
                send += str(math.ceil(random.uniform(0,dice)))
                if i + 1 < int(matched.group(1)):
                    send += '+'
            send += ')'
            return send

    def command(self, params):
        algbr1 = params[0]
        tag = params[1]
        algbr1 = re.sub('\\s', '', algbr1)
        algbr2 = re.sub('(\\d*)d(\\d*)', self.re_dice, algbr1)
        send = "投掷 %s: %s=%s"%(tag, algbr1, algbr2)
        if not re.match('\\d*', algbr2):
            send += '='
            send += eval(algbr2)
        return send
cmd_roll_dice = RollDice('r', 'gene', help_dict['r'])

class MkChar:
    
    def __init__(self, name, priv, helpinfo):
        self.name = name
        self.priv = priv
        self.helpinfo = helpinfo
    
    def rd6(self):
        return math.ceil(random.uniform(0,6))
    def command(self, params):
        if params[0] == '':
            num = 1
        else:
            num = int(params[0])
        if num < 1:
            num = 1
        if num > 5:
            num = 5
        msg = 'COC7规则人物属性:'
        for i in range(num):
            strength = 3*self.rd6()*5 #好气啊str和int是python函数名
            con = 3*self.rd6()*5
            siz = (2*self.rd6() + 6)*5
            dex = 3*self.rd6()*5
            app = 3*self.rd6()*5
            intelligence = (2*self.rd6() + 6)*5
            pow = 3*self.rd6()*5
            edu = (2*self.rd6() + 6)*5
            luc = (2*self.rd6()+6)*5
            sum1 = strength + con + siz + dex + app + intelligence + pow +edu
            sum2 = sum1 + luc
            msg = msg + '\n力量:'+str(strength)+' 体质:'+str(con)+' 体型:'+str(siz)+' 敏捷:'+str(dex)+' 外貌:'+str(app)+' 智力:'+str(intelligence)+' 意志:'+str(pow)+' 教育:'+str(edu)+' 幸运:'+str(luc)+' 共计:'+str(sum1)+'('+str(sum2)+')'
        return msg

cmd_mkchar = MkChar('mkchar', 'gene', help_dict['mkchar'])

cmd_dict = {
    'help' : cmd_help,
    'mkchar' : cmd_mkchar,
    'r' : cmd_roll_dice,
}

bot = Bot(cmd_dict)

def msg_to_cmd(msg0):
    # 正则处理:QQmsg --> {'cmd_name': , 'params': }
    # 是否为指令(.开头)
    pattern = re.compile("^[\\.|。](.*)$",re.M|re.I)
    result = pattern.match(msg0)
    if result == None:
        return None
    
    # 辨别指令类型
    m1 = result.group(1)
    pattern_dict = {
        'help' : 'help\\s?(.*)',
        'mkchar' : 'mkchar\\s*(\\d*)',
        'r' : 'r([\\d\\+\\-\\*\\/\\^\\(\\)d\\s]*)(.*)'
    }
    for key in pattern_dict.keys():
        result = re.match(pattern_dict[key], m1, re.M|re.I)
        if result:
            result_dict = {
                'cmd_name' : key,
                'params' : result.groups()
            }
            return result_dict
    # 全部指令正则匹配失败
    return "error: 不存在指令或不是合法指令，输入.help[指令名]查看使用方法"
    

geneHelpList = {
    "":".help 全部可用指令列表\n.cochelp coc_trpg指令列表",
    "help":"帮助指令。输入.help查看全部可以使用的指令，输入.help [指令名(不加.)]查询相应指令的语法。",
    "coc":".coc .rd 默认骰，投掷1d100"
}

adminHelpList = {
    'on':'.on 打开bot'
}

rootAdminHelpList = {
    "addadmin":"添加bot全局管理员。输入.addadmin [QQ_id]",
    "deladmin":"删除bot全局管理员。输入.deladmin [QQ_id]",
    "showadmin":"显示全部bot全局管理员。输入.showadmin [QQ_id]",
    "addtestgroup":"添加bot测试群。输入.addtestgroup [QQ_id]",
    "deltestgroup":"删除bot测试群。输入.deltestgroup [QQ_id]",
    "showtestgroup":"显示全部bot测试群。输入.showtestgroup [QQ_id]"
}





