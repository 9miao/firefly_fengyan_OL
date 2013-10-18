#coding:utf8
'''
Created on 2012-3-16
配置文件 配置各种变量
@author: jt
'''
from twisted.python import log
from app.chatServer.core.language.Language import Lg

formatNobility={'Str':Lg().g(27),'Dex':Lg().g(28),'Vit':Lg().g(29),'Wis':Lg().g(30),'Spi':Lg().g(31),'MaxHp':Lg().g(32),'MaxMp':Lg().g(33),
    'PhyAtt':Lg().g(34),'PhyDef':Lg().g(35),'MigAtt':Lg().g(36),'MigDef':Lg().g(37),'HitRate':Lg().g(38),
    'CriRate':Lg().g(39),'Squelch':Lg().g(40),'ExpEff':Lg().g(41),'power':Lg().g(42),'StrPercen':Lg().g(43),
    'DexPercen':Lg().g(44),'VitPercen':Lg().g(45),'WisPercen':Lg().g(46),'SpiPercen':Lg().g(47),
    'MaxHpPercen':Lg().g(48),'MaxMp':Lg().g(49),'PhyAttPercen':Lg().g(50),'PhyDefPercen':Lg().g(51),
    'MigAttPercen':Lg().g(52),'MigAttPercen':Lg().g(53),'Dodge':Lg().g(54),'Speed':Lg().g(55),'Ignore':Lg().g(56),
    'zhekou':Lg().g(57),'Block':Lg().g(58),'shjc':Lg().g(59),'shjm':Lg().g(60)}

def guanjueZuan(count):
    '''通过点击上交钻石次数，返回档次需要交纳的钻数量'''
    ct=count*10
    return ct

def m(m):
    '''分钟转秒数'''
    return m*60
def h(h):
    '''小时转秒'''
    return h*60*60
def date(d,h,m,s):
    '''返回秒数
    @param d: int 天数
    @param h: int 小时数
    @param m: int 分钟数
    @param s: int 秒数
    '''
    return d*24*3600+h*3600+m*60+s


instanceStatus=h(6)#副本状态药剂持续时间 (单位:小时 后副本状态增益效果取消)
instanceStatusPrompt=m(30)#副本状态药剂持剩余时间提醒 （30：剩余30秒的时候提醒,单位秒）

numbool={-1:False,0:False,1:True}

def NumbToBool(num):
    '''数字转布尔'''
    if num>1:
        num=1
    if num<-1:
        num=-1
    bo=numbool.get(num,False)
    return bo

def BoolToNumb(flg):
    '''1=true,-1=false'''
    if flg:
        return 1
    else:
        return -1
    



def FormatNobilityAttribute(lists):
    '''格式化爵位属性为字符串数组
    @param lists: {} 字典类型
    return []
    '''
    li=[]#格式化后的
    for item in lists.items():
        try:
            li.append(u'%s+%s'%(formatNobility.get(item[0]),item[1]))
        except:
            log.err(u"Configure->FormatNobilityAttribute formatNobility.get( %s )"%item[0])
    return li

def getchatimeTime(down,counts):
    '''获取两日期相差的时间,返回剩余秒数及其当前时间
    @param down: datetime 记录时间
    @param counts: int 间隔秒数
    '''
    import datetime
    nowtime=datetime.datetime.now() #系统当前时间
    if not down:
        return [0,nowtime]
   
    lin=down
    b=datetime.timedelta(seconds=counts)
    lin=lin+b#记录时间+间隔秒数
    if lin>nowtime:#如果冷却时间不为0
        s1=(lin-nowtime).days
        s1=s1*24*3600
        s2=(lin-nowtime).seconds
        s=s1+s2
        return [s,nowtime]
    else:
        return [0,nowtime]
    
    
def getchaTime(down,counts):
    '''获取两日期相差的时间,返回剩余秒数
    @param down: datetime 记录时间
    @param counts: int 间隔秒数
    '''
    import datetime
    lin=down
    nowtime=datetime.datetime.now() #系统当前时间
    b=datetime.timedelta(seconds=counts)
    lin=lin+b#记录时间+间隔秒数
    if lin>nowtime:#如果冷却时间不为0
        s1=(lin-nowtime).days
        s1=s1*24*3600
        s2=(lin-nowtime).seconds
        s=s1+s2
        return s
    else:
        return 0
        
        
def getAttributeByZyAndWqTypeid(zyid,wqtype,qh):
    '''根据角色职业类型和装备类型获取增加的属性
    @param zyid: int 职业限制      #1战士 2 法师 3 游侠 4 牧师
    @param wqtype: int 武器类型       #0=衣服#1=裤子 #2=头盔#3=手套#4=靴子#5=护肩#6=项链#7=戒指#8=主武器#9=副武器#10=双手
    @param qh: int 物品当前强化等级

    '''
    wg=qh*45#物理攻击
    mg=qh*48#魔法攻击
    wf=qh*12#物理防御
    mf=qh*15#魔法防御
    sm=qh*120#魔法防御
    sd=qh*6#攻速
    if wqtype==9:#副手
        if zyid==0:
            return [[Lg().g(36),mg],[Lg().g(34),wg]]
        elif zyid%2==0:#如果是魔法类装备
            return [[Lg().g(36),mg]]
        else:
            return [[Lg().g(34),wg]]
    elif wqtype==8:#主手
        if zyid==0:
            return [[Lg().g(36),mg],[Lg().g(34),wg]]
        elif zyid%2==0:
            return [[Lg().g(36),mg]]
        else:
            return [[Lg().g(34),wg]]
    elif wqtype==7:#戒指
        if zyid==0:
            return [[Lg().g(36),mg],[Lg().g(34),wg]]
        elif zyid%2==0:
            return [[Lg().g(36),mg]]
        else:
            return [[Lg().g(34),wg]]
    elif wqtype==6:#项链
        if zyid==0:
            return [[Lg().g(37),mf],[Lg().g(35),wf]]
        if zyid%2==0:
            return [[Lg().g(37),mf]]
        else:
            return [[Lg().g(35),wf]]
    elif wqtype==4:#鞋子
        return [[Lg().g(55),sd]]
    elif wqtype==1:#裤子
        return [[Lg().g(32),sm]]
    elif wqtype==3:#护手
        return [[Lg().g(55),sd]]
    elif wqtype==0:#衣服
        return [Lg().g(35),wf]
    elif wqtype==5:#护肩
        return [[Lg().g(32),sm]]
    elif wqtype==2:#头盔
        return [[Lg().g(37),mf]]
    return [['空',0]]
        



def getStrengthenIcon(qh,wqtype):
    '''获取强化花费，根据物品强化等级和物品装备部位
    @param qh: int 物品当前强化等级
    @param wqtype: int 武器类型       #0=衣服#1=裤子 #2=头盔#3=手套#4=靴子#5=护肩#6=项链#7=戒指#8=主武器#9=副武器#10=双手
    '''
    qh+=1
    if wqtype==9:#副手
        return int(round(qh**3.1+60))
    
    elif wqtype==8:#主手
        return int(round(qh**3.1+60))
    
    elif wqtype==7:#戒指
        return int(round(qh**3.1+60))
    
    elif wqtype==6:#项链
        return int(round(0.6*qh**3.1+30))
    
    elif wqtype==4:#鞋子
        return int(round(0.9*qh**3.1+50))
    
    elif wqtype==1:#裤子
        return int(round(0.8*qh**3.1+45))
    
    elif wqtype==3:#护手
        return int(round(0.9*qh**3.1+50))
    
    elif wqtype==0:#衣服
        return int(round(0.4*qh**3.1+30))
    
    elif wqtype==5:#护肩
        return int(round(0.8*qh**3.1+45))
    
    elif wqtype==2:#头盔
        return int(round(0.4*qh**3.1+30))
    return -1
    
