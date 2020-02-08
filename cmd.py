import re
import math
import random

class Bot:
    command_dict = {}
        
    def __init__(self, commands):
        for command in commands:
            self.command_dict[command['name']] = command['instance']
        self.command_dict['help'] = self.help
    
    def help(self):
        pass
        return
    
    def command(self, cmd, params):
        if cmd in self.command_dict:
            return self.command_dict[cmd].handle(params)

    def check_priv(self, cmd, usr):
        return True
    
    def rd6(self):
        return math.ceil(random.uniform(0,6))

    def commandMkChar(self, num = 1):
        if num < 1:
            num = 1
        if num > 5:
            num = 5
        msg = 'COC7规则人物属性：\n'
        for i in range(num):
            strength = 3*self.rd6()*5
            con = 3*self.rd6()*5
            siz = (2*self.rd6() + 6)*5
            dex = 3*self.rd6()*5
            app = 3*self.rd6()*5
            int = (2*self.rd6() + 6)*5
            pow = 3*self.rd6()*5
            edu = (2*self.rd6() + 6)*5
            luc = (2*self.rd6+6)*5
            sum1 = strength + con + siz + dex + app + int + pow +edu
            sum2 = sum1 + luc
            msg = msg + '力量:'+str(strength)+' 体质:'+str(con)+' 体型:'+str(siz)+' 敏捷:'+str(dex)+' 外貌:'+str(app)+' 智力:'+str(int)+' 意志:'+str(pow)+' 教育:'+str(edu)+' 幸运:'+str(luc)+' 共计:'+str(sum1)+'('+str(sum2)+')\n'
        return msg

bot = Bot([
    {'name' : 'r', 'instance' : CommandR },
    {'name' : 'pwc', 'instance' : CommandPWC },
    {'name' : 'mkchar', 'instance' : CommandMkChar }
    ])

#class somecmd:
#    name =  '' e.g.: roll_dice
#    priv =  '' gene, admin, root
#    helpinfo = helpList[name]
#    
#   def __init__(self, name, priv, helpinfo):
#        self.name = name
#        self.priv = priv
#        self.helpinfo = helpinfo
#    
#    def command():
helpList = {
    'help':'帮助指令。输入.help查看全部可以使用的指令，输入.help [指令名(不加.)]查询相应指令的语法。',

    'coc':'COC7指令：\n.makechar .rd 默认骰，投掷1d100',
    'r':'.r[计算式] [tag]，如.rd6, .r2d6, .rd4+d6，支持四则运算和乘方(^)',
    'rd':'.rd [tag]，投掷一个100面骰（默认）',
    'ra':'.ra[数值/属性名] [tag]，属性名支持中文，英文和英文缩写，不区分大小写',
    'mkchar':'输入.mkchar [个数,默认1]生成COC7规则基础人物属性',
    'swchar':'.swchar [角色卡名]，切换到对应的角色卡', # Terry named the command
    'setchar':'.set [角色卡名] <赋值语句>，例如.set thomas str90 体质90 DEX90，支持中文，英文和英文缩写，不区分大小写',
    'pwc':'.pwc(print working character)，显示目前操作的人物卡名称(区分大小写！)',
    'dispchar':'.dispchar [属性] 显示指定人物卡的指定属性，-all显示所有属性',
    'usrn':'.usrn [名字]设置您在bot上的全局用户名，默认值为您的QQ昵称',
    'grpn':'.grpn [名字]设置您在本群的局域用户名，默认值为您的群名片',
    }
class Help:
    name = 'help'
    priv = 'gene' # gene admin root
    helpinfo = helpList[name]

    def __init__(self, name, priv, helpinfo):
        self.name = name
        self.priv = priv
        self.helpinfo = helpinfo
    def command(self, cmd):
        # cmd = 指令名称，需要在helpList里
        msg = 'error: 未找到指令，请检查指令是否输入正确'
        if cmd in helpList:
            msg = helpList['cmd']
        return msg
class RollDice:
    name =  'rolldice'
    priv =  'gene'
    helpinfo = helpList['rd']
    
    def __init__(self, name, priv, helpinfo):
        self.name = name
        self.priv = priv
        self.helpinfo = helpinfo
    
    def command(self):
        pass

class MkChar:
    name =  'mkchar'
    priv =  'gene'
    helpinfo = helpList[name]
    
    def __init__(self, name, priv, helpinfo):
        self.name = name
        self.priv = priv
        self.helpinfo = helpinfo
    
    def rd6(self):
        return math.ceil(random.uniform(0,6))
    def command(self, num = 1):
        if num < 1:
            num = 1
        if num > 5:
            num = 5
        msg = 'COC7规则人物属性：\n'
        for i in range(num):
            strength = 3*self.rd6()*5
            con = 3*self.rd6()*5
            siz = (2*self.rd6() + 6)*5
            dex = 3*self.rd6()*5
            app = 3*self.rd6()*5
            int = (2*self.rd6() + 6)*5
            pow = 3*self.rd6()*5
            edu = (2*self.rd6() + 6)*5
            luc = (2*self.rd6()+6)*5
            sum1 = strength + con + siz + dex + app + int + pow +edu
            sum2 = sum1 + luc
            msg = msg + '力量:'+str(strength)+' 体质:'+str(con)+' 体型:'+str(siz)+' 敏捷:'+str(dex)+' 外貌:'+str(app)+' 智力:'+str(int)+' 意志:'+str(pow)+' 教育:'+str(edu)+' 幸运:'+str(luc)+' 共计:'+str(sum1)+'('+str(sum2)+')\n'
        return msg


def msg_to_cmd(m0):
    pattern = re.compile("^[\\.|。](.*)$",re.M|re.I)
    result = pattern.match(m0)
    if result == None:
        return None
    m1 = result.group(1)
    #r_result = re.compile('r(.*)',re.M|re.I)
    #rd_result = re.match('rd')
    help_result = re.match('help(.*)',m1,re.M|re.I)
    mkchar_result = re.match('mkchar[\s*]([0-9]*).*',m1,re.M|re.I)
    

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





