#coding:utf8
'''
Created on 2012-5-17
官爵
@author: jt
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.utils.dbopera import dbNobility
from app.scense.core.language.Language import Lg

def errors():
    lists=dbNobility.all
    for key,info in lists.items():
        try:
            if key==22:
                pass
            for item in [1,2,3,4,5,6]:
                strr="f%s"%item
                lli=eval(info[strr]) 
        except:
            print str(key)+"   "+str(item)+"  "

def getzuan(pid):
    '''返回客户端这次点击贡献应该花费多少钻'''
    player=PlayersManager().getPlayerByID(pid)
    if not player:
        return False
    counts=player.nobility.getzuans()#当前爵位信息   
    return counts

def getItemList(pid):
    '''获得威望任务信息'''
    player=PlayersManager().getPlayerByID(pid)
    if not player:
        return False
    info= player.nobility.getNowInfo()#当前爵位信息
    if not info:
        return False
    ist=[]
    for item in [1,2,3,4,5,6]:
        strr="f%s"%item
        try:
            lli=eval(info[strr]) #[0物品id,1物品名称,2物品数量，3获得贡献值数量,4是否可以上交物品，5，标志id,6魔钻是否足够]
        except:
            print "---------------%s"%str(info)
        issj=player.nobility.isSJWP(strr)#判断这个物品是否可以上交或者贡献钻
        if issj:#如果这个物品可以上交
            ct=player.pack._package._PropsPagePack.countItemTemplateId(lli[0])#物品的数量
            if ct>lli[2]:
                lli.append(True) #是否可上交
            else:
                lli.append(False) #是否可上交
            lli.append(strr) #标志id
            counts=player.nobility.getzuans()#获取贡献钻数量
            ncount=player.finance.getGold()#角色当前钻数量
            if ncount>counts:
                lli.append(True)#魔钻是否足够
            else:
                lli.append(False)#魔钻是否足够
        else:
            lli.append(False) #是否可上交
            lli.append(strr) #标志id
            lli.append(False)#魔钻是否足够
        ist.append(lli)
    return ist

def handin(pid,iid):
    '''上交物品获得贡献
    @param pid: int 角色id
    @param iid: str  f1 f2 f3...f6
    '''
    player=PlayersManager().getPlayerByID(pid)
    if not player:
        return {'result':False,'message':Lg().g(106)}
    data=player.nobility.handin(iid)
    return data

def drawDiamond(pid,iid):
    '''贡献钻换取威望
    @param iid: string 贡献物品唯一标识
    '''
    player=PlayersManager().getPlayerByID(pid)
    if not player:
        return {'result':False,'message':Lg().g(106)}
    data=player.nobility.drawZuanShi(iid)
    return data


def drawPromote(pid):
    '''升级爵位'''
    player=PlayersManager().getPlayerByID(pid)
    if not player:
        return False
    flg= player.nobility.promote()
    
    return flg


def drawSalary(pid):
    '''领取俸禄'''
    player=PlayersManager().getPlayerByID(pid)
    if not player:
        return False
    flg= player.nobility.draw()
    return flg

def getAllInfo(pid,page):
    '''获取爵位面板所有信息
    @param pid: int  角色id
    @param page: int 封爵史当前页数
    '''
    from app.scense.applyInterface import configure
    
    player=PlayersManager().getPlayerByID(pid)
    if not player:
        return False
    nobility= player.nobility#角色的爵位类
    data={}
    nowinfo= nobility.getNowInfo()#当前爵位信息
    nextinfo=nobility.getNextInfo()#下一爵位信息
    historylist=nobility.getHistory(pid,page)#封爵史
   
    
    data['hasGetSalary']=nobility.isdraw()#当前角色可否领取俸禄
    data['isjw']=nobility.ispromote()#是否可以升级爵位
    if historylist:
        data['totalpage']=historylist.get('zong',-1)
        data['curpage']=page
        data['fcontext']=historylist.get('context',[])
        data['ftime']=historylist.get('time',[])
    else:
        data['totalpage']=0
        data['curpage']=page
        data['fcontext']=[]
        data['ftime']=[]
    if nextinfo:
        addxj=configure.FormatNobilityAttribute(eval(nextinfo['attribute'])) #下级增加属性及其数值
        data['addxj']=addxj#下级增加属性及其数值
        data['nextDouqi']=nextinfo['morale']
        data['nextJinbi']=nextinfo['coin']
        data['nextWeiwang']=nextinfo['prestige']
        data['nextJuewei']=nextinfo['names']
        data['dengji']=nextinfo['dengji']#升级爵位限制等级
    else:
        data['addxj']=[Lg().g(143)]#下级增加属性及其数值
        data['nextDouqi']=0
        data['nextJinbi']=0
        data['nextWeiwang']=0
        data['dengji']=0
        data['nextJuewei']=Lg().g(157)
    
    data['currentDouqi']=nowinfo['morale']
    data['currentJinbi']=nowinfo['coin']
    data['weiwang']=player.finance.getPrestige()
    data['currentJuewei']=nowinfo['names']
    adddq=configure.FormatNobilityAttribute(eval(nowinfo['attribute'])) #当前增加属性及其数值
    data['adddq']=adddq##当前增加属性及其数值
    
    return data
    
    
    
