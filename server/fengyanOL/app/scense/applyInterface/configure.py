#coding:utf8
'''
Created on 2012-3-16
配置文件 配置各种变量
@author: jt
'''

from twisted.python import log
import random,datetime,time
import math
from app.scense.core.language.Language import Lg

formatNobility=None

def shuxingbianliang():
    global formatNobility
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


def NumbToBool(num):
    '''数字转布尔'''
    if num>=1:
        return True
    if num<1:
        return False

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
        
        
def getAttributeByZyAndWqTypeid(zyid,wqtype,qh,baseQuality):
    '''根据角色职业类型和装备类型获取增加的属性
    @param zyid: int 职业限制      #1战士 2 法师 3 游侠 4 牧师   0无属性限制
    @param wqtype: int 武器类型       #0=衣服#1=裤子 #2=头盔#3=手套#4=靴子#5=护肩#6=项链#7=戒指#8=主武器#9=副武器#10=双手
    @param qh: int 物品当前强化等级

    '''
    wlgjqh=10 #物理攻击倍数
    mfgjqh=11 #魔法攻击倍数
    wlfyqh=3  #物理防御倍数
    mffyqh=4  #魔法防御倍数
    gsqh=2    #攻速倍数
    smqh=30   #生命倍数
    if baseQuality==1:#绿色
        mffyqh=12  
        wlfyqh=10  
        smqh=50
        wlgjqh=10 
        mfgjqh=11
    elif baseQuality==2:#蓝色
        mffyqh=13  
        wlfyqh=11  
        smqh=53   
        wlgjqh=11 
        mfgjqh=12
    elif baseQuality==3:#紫色
        mffyqh=13
        wlfyqh=11  
        smqh=53   
        wlgjqh=11 
        mfgjqh=12
    elif baseQuality==4:#金色
        mffyqh=14
        wlfyqh=12  
        smqh=59   
        wlgjqh=12 
        mfgjqh=13
    elif baseQuality==5:#橙色
        mffyqh=15
        wlfyqh=12  
        smqh=62   
        wlgjqh=12 
        mfgjqh=14
    elif baseQuality==6:#红色
        mffyqh=16
        wlfyqh=13
        smqh=65
        wlgjqh=13
        mfgjqh=14
    elif baseQuality==7:#神佑红
        mffyqh=16
        wlfyqh=14
        smqh=68   
        wlgjqh=14 
        mfgjqh=15
    
    wg=qh*wlgjqh#攻击
    mg=qh*mfgjqh#魔法攻击
    wf=qh*wlfyqh#物理防御d
    mf=qh*mffyqh#魔法防御
    sm=qh*smqh#生命
    sd=qh*gsqh#攻速
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
        return [[Lg().g(35),wf]]
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
        return int(3*round(qh**2.9+60))
    
    elif wqtype==8:#主手
        return int(3*round(qh**2.9+60))
    
    elif wqtype==7:#戒指
        return int(3*round(qh**2.9+60))
    
    elif wqtype==6:#项链
        return int(3*round(0.6*qh**2.9+30))
    
    elif wqtype==4:#鞋子
        return int(3*round(0.9*qh**2.9+50))
    
    elif wqtype==1:#裤子
        return int(3*round(0.8*qh**2.9+45))
    
    elif wqtype==3:#护手
        return int(3*round(0.9*qh**2.9+50))
    
    elif wqtype==0:#衣服
        return int(3*round(0.4*qh**2.9+30))
    
    elif wqtype==5:#护肩
        return int(3*round(0.8*qh**2.9+45))
    
    elif wqtype==2:#头盔
        return int(3*round(0.4*qh**2.9+30))
    return -1


def getzizhidengji(count):
    '''根据四个属性获取资质等级, 1高级宠物  2中级宠物  3低级宠物
    @param count: int 宠物资质  1=普通（绿）2=优秀（蓝）3=精良（紫）
    '''
    if count==1:
        return 3  #1高级宠物  2中级宠物  3低级宠物
    elif count==2:
        return 2
    elif count==3:
        return 1
    else:
        return 0
    
def getpetshopsuiji():
    '''宠物商店随机'''
    abss=random.randint(1,100)
    if abss<=90:
        return 3 #  3低级宠物
    elif abss>90 and abss<=99:
        return 2 #  2中级宠物
    else:
        return 1 #  1高级宠物
        

def qdShuliang(t,gold):
    '''根据祈祷随机出来的类型和花费钻石数量获取奖励数量
    @param t: int  祈祷类 ( 1金币奖励    2经验奖励   3声望奖励    4活力)
    @param gold: int 花费钻石数量
    '''
    if t==1:#金币奖励
        return int(math.ceil((600*gold+(gold/0.1)**2.2)/2+1000))
    elif t==2:#经验奖励
        return int(math.ceil((100*gold+(gold/0.1)**2.3)/2+1000))
    elif t==3:#声望奖励
        return gold*2
    else:#活力奖励
        return gold
    
def qd(gold):
    '''祈祷类型随机    1金币奖励    2经验奖励   3声望奖励    4活力
    @return: [奖励类型，奖励数量，奖励倍数]
    '''
    if gold==0:
        gold=1
    abss=random.randint(1,10000)
    v=0#获得奖励数量
    t=0#奖励类型
    
    if abss<=8000:
        t=1#金币奖励
        v=qdShuliang(t, gold)
#    elif abss>9982 and abss<=9992:
#        t=2#经验奖励
#        v=qdShuliang(t, gold)
    elif abss>8000 and abss<=9500:
        t=3#声望奖励
        v=qdShuliang(t, gold)
    else:
        t=4#活力奖励
        v=qdShuliang(t, gold)
    b=qdMultiple()
    v=v*b
    return[t,v,b]
    
def qdMultiple():
    '''祈祷倍数'''
    b=0#奖励倍数
    v=random.randint(1,10000)
    if v<=8500:
        b=1
    elif v>8500 and v<=9500:
        b= 2
    elif v>9500 and v<=9850:
        b= 4
    else:
        b= 10
    sj=time.strftime("%w%H")
    sj=int(sj)
    if sj>=210 and sj<=214:
        b*=2
    elif sj>=510 and sj<=514:
        b*=2
    return b

def isteamInstanceTime(level):
    '''多人副本是否可以开启'''
    sj=int(time.strftime("%H%M"))
    if  level<17:
        return False
    if sj>=1230 and sj<=1330:
        return True
    elif sj>=1930 and sj<=2030:
        return True
    else:
        return False
