#coding:utf8
'''
Created on 2011-9-27
强化
@author: SIOP_09
'''

from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface import pushObjectNetInterface
from app.scense.applyInterface import configure
#from utils.dbopera import dbStrengthen

from app.scense.serverconfig.chatnode import chatnoderemote 
from app.scense.core.language.Language import Lg
#import math

def isHaveQH(characterid,itemid):
    '''判断是否能够强化
    @param characterid: int 角色id
    @param itemid: int 物品1（item）表主键id
    '''
    item1=None#物品实例1
    player=PlayersManager().getPlayerByID(characterid)
    
    if itemid>0:#如果物品1存在

        if player.pack._package._PropsPagePack.getPositionByItemId(itemid)!=-1:#背包中没有此物品
            item1=player.pack._package._PropsPagePack.getItemInfoByItemid(itemid)#获取物品实例
        else:
            item1=player.pack._equipmentSlot.getItemInfoByItemid(itemid)
            
        if not item1:
            return {'result':False,'message':Lg().g(189),'data':None}

    wqtype=item1.getWQtype()#武器类型 #装备类型id   #0=衣服#1=裤子 #2=头盔#3=手套#4=靴子#5=护肩#6=项链#7=戒指#8=主武器#9=副武器#10=双手
    if wqtype<0 or wqtype>10: #装备类型id  
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(196), [player.getDynamicId()])
        return {'result':False,'message':Lg().g(197),'data':None}
   
    baseQuality=item1.baseInfo.getItemTemplateInfo().get("baseQuality",0)#基础品质 1灰 2白 3绿 4蓝 5紫 6橙 7红
    itemlevel=item1.baseInfo.getItemTemplateInfo().get("levelRequire",0) #装备等级
    qlevel=item1.attribute.getStrengthen() #物品当前的强化等级
    jinbi= coinCount(qlevel,baseQuality,wqtype,itemlevel)
    return qq(player, itemid,wqtype,baseQuality,jinbi,item1)
            
            
    
    
def qq(player,itemid,wqtype,baseQuality,jinbi,item):
    '''
    @param player: obj 角色实例
    @param itemid: int 物品id
    @param wqtype: int #装备类型id  1武器  2防具 3饰品  4强化石  0不是装备
    @param baseQuality: int 物品品质
    @param jinbi: int 需要花费多少金币
    @param item: obj 物品实例
    '''
#    item=player.pack._package._PropsPagePack.getItemInfoByItemid(itemid)#物品id
    qlevel=item.attribute.getStrengthen() #物品当前的强化等级
#    baseprobability=int(qhslevel/(qlevel/2.0+baseQuality*qhslevel)*5.0)#成功率百分比 x%    #(强化石Lv/(装备强化Lv/2+装备品质*强化石Lv))*5
    if qlevel>=player.level.getLevel():
        pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(198), [player.baseInfo.id])
        return {'result':False,'message':Lg().g(198),'data':None}
    if not player:
        return {'result':False,'message':Lg().g(199),'data':None}
#    flg=False#金币是否足够
#    playercoin=player.finance.getCoin()#角色的金币数量
#    if playercoin>=jinbi:
#        flg=True
    zyid=item.baseInfo.getItemProfession()#职业类型限制 1战士 2 法师 3 游侠 4 牧师
    arraylist=configure.getAttributeByZyAndWqTypeid(zyid, wqtype,qlevel+1,baseQuality)#根据角色职业类型和装备类型获取增加的属性
    arraylist=arraylist[0]
    itemTemplateId=item.baseInfo.getItemTemplateId()
    data={'syname':arraylist[0],'syvalue':arraylist[1],'coin':jinbi,'itemTemplateId':itemTemplateId,'qlevel':qlevel+1}
    return{'result':True,'message':Lg().g(166),'data':data}
    
def coinCount(qlevel,color,wqtype,level):
    '''强化物品需要多少钱
    @param qlevel: int 物品当前强化等级
    @param color: int 装备品质
    @param bodyTypeid: int 装备部位
    @param level: int 物品等级
    '''
    coin1=configure.getStrengthenIcon(qlevel, wqtype)
    return coin1

def coinCountObj(item1,qevels=0):
    '''强化物品需要多少钱
    @param item: obj 物品实例
    @param qevels: int 物品强化等级
    '''
#    color=item1.baseInfo.getItemTemplateInfo().get("baseQuality",0)#基础品质 1灰 2白 3绿 4蓝 5紫 6橙 7红
#    level=item1.baseInfo.getItemTemplateInfo().get("levelRequire",0) #装备等级
#    qlevel=item1.attribute.getStrengthen() #物品当前的强化等级
    wqtype=item1.getWQtype()#武器类型 #装备类型id   #0=衣服#1=裤子 #2=头盔#3=手套#4=靴子#5=护肩#6=项链#7=戒指#8=主武器#9=副武器#10=双手
    coin1=configure.getStrengthenIcon(qevels, wqtype)
    return coin1
    
    
def StrengthenItem(characterid,itemid):
    '''强化装备
    @param characterid: int 角色id
    @param itemid: int 装备id
    '''
    
    item=None #装备实例
    player=PlayersManager().getPlayerByID(characterid) #角色实例
    if not player:
        return {'result':False,'message':Lg().g(199),'data':None}
    if player.pack._package._PropsPagePack.getPositionByItemId(itemid)!=-1:#背包中没有此物品
        item=player.pack._package._PropsPagePack.getItemInfoByItemid(itemid)
    else:
        item=player.pack._equipmentSlot.getItemInfoByItemid(itemid)
    if not item:
        return {'result':False,'message':Lg().g(189),'data':None}
    qlevel=item.attribute.getStrengthen() #装备的强化等级
    plevel=player.level.getLevel()
    if qlevel>=plevel:
        pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(198), [player.baseInfo.id])
        return {'result':False,'message':Lg().g(198),'data':None}
#    sim=player.qhtime.isdraw()
#    if not sim:
#        pushObjectNetInterface.pushOtherMessageByCharacterId(u'冷却时间不足', [player.baseInfo.id])
#        return {'result':False,'message':u'冷却时间不足','data':None}
    
    baseQuality=item.baseInfo.getItemTemplateInfo().get("baseQuality",0)#基础品质 1灰 2白 3绿 4蓝 5紫 6橙 7红
    itemlevel=item.baseInfo.getItemTemplateInfo().get("levelRequire",0) #装备等级
    wqtype=item.getWQtype()#武器类型  #0=衣服#1=裤子 #2=头盔#3=手套#4=靴子#5=护肩#6=项链#7=戒指#8=主武器#9=副武器#10=双手
    if wqtype<0 or wqtype>10: #装备类型id
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(196), [player.getDynamicId()])
        return {'result':False,'message':Lg().g(197),'data':None}
    jinbi= coinCount(qlevel,baseQuality,wqtype,itemlevel)#强化所需金币
    if player.finance.getCoin()>=jinbi:
        player.finance.updateCoin(player.finance.getCoin()-jinbi)
    else:
        return {'result':False,'message':Lg().g(200),'data':None}
    
    result=__StrengthenOne(player,item,qlevel,characterid)    
    if result:
        return result
    return {'result':True,'message':Lg().g(166),'data':None}
    
def __StrengthenOne(player,item,qlevel,characterid):
    '''强化装备ing
    @param player: obj 角色
    @param itemid: obj 物品
    @param qlevel: int 强化等级
    '''
#    player.pack.delItemByItemId(item1id)
#    r=random.randint(1,100)
    if True: #如果强化成功
        
        item.attribute.updateStrengthen(item.attribute.getStrengthen()+1) #强化+1
#        sstime=player.qhtime.add(item.attribute.getStrengthen()-1)#增加冷却时间，返回增加后的剩余秒数
#        pushObjectNetInterface.StrengthenTime2120(player.baseInfo.id,sstime)#推送心冷却时间到客户端
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(201), [player.getDynamicId()])
        pushStrengthenSys(player,item,True)
#        msg=u'玩家['+player.baseInfo.getNickName()+u']强化'+item.baseInfo.getName()+'+'+str(item.attribute.getStrengthen())+' 成功'
        player.quest.specialTaskHandle(102)#特殊任务处理
        player.schedule.noticeSchedule(2,goal = 1)
        player.daily.noticeDaily(8,0,item.attribute.getStrengthen()+1)
        return {'result':True,'message':u'','data':None}
#        chat.sendAnnouncement(msg) #公告
#        chat.sendSysInfomation(msg1, player.baseInfo.id)#系统提示
    else: #如果强化失败
#        msg='玩家['+player.baseInfo.getNickName()+']强化'+item.baseInfo.getName()+'+'+str(item.attribute.getStrengthen())+' 失败'
#        chat.sendAnnouncement(msg) #公告
#        chat.sendSysInfomation(msg1, player.baseInfo.id)#系统提示
        pushStrengthenSys(player,item,False)
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(202), [player.getDynamicId()])
        return {'result':False,'message':u'','data':None}

def pushStrengthenSys(player,item,result):
    '''推送强化的系统消息
    @param player: PlayerCharacter
    '''
    strenlevel = item.attribute.getStrengthen()
    if strenlevel%10!=0 and strenlevel !=0:
        return
    UnionTypeStr = player.guild.getUnionTypeStr()
    palyername = player.baseInfo.getName()
    imterichname = item.baseInfo.getRichName()
    strenlevel = item.attribute.getStrengthen()
    if result:
        msg = Lg().g(203)%(UnionTypeStr,
                                         palyername,imterichname,strenlevel)
    else:
        msg = Lg().g(204)%(UnionTypeStr,
                                         palyername,imterichname,strenlevel)
    chatnoderemote.callRemote('pushSystemToInfo',msg)

def GetStrengthenPackageInfo(playerId,curPage):
    '''获取强化包裹中的数据
    @param playerId: int 角色的id
    @param curPage: int 包裹的ID
    '''
    player=PlayersManager().getPlayerByID(playerId) #角色实例
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.pack.GetStrengthenPackageInfo(curPage)
    return {'result':True,'data':data}

def getItemByplayer(player,itemid):
    '''根据角色实例和物品id获取物品实例
    @param palyer: obj 角色实例
    @param itemid: int 物品id
    '''
    item1=None
    if player.pack._package._PropsPagePack.getPositionByItemId(itemid)!=-1:#背包中没有此物品
        item1=player.pack._package._PropsPagePack.getItemInfoByItemid(itemid)#获取物品实例
    else:
        item1=player.pack._equipmentSlot.getItemInfoByItemid(itemid)
    return item1
            

def getSxzy(characterid,item1,item2):
    '''获取属性转移后的效果及其花费信息
    @param item1: int 物品id （转移后强化等级变成0的那个物品的id）
    @param item: int 物品id 
    '''
    if item1==item2:
        pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(206), [characterid])
        return {'result':False,'message':Lg().g(206),'data':None}
    player=PlayersManager().getPlayerByID(characterid) #角色实例
    if not player:
        return {'result':False,'message':Lg().g(199),'data':None}
    if player.level.getLevel()<30:
        return {'result':False,'message':Lg().g(205),'data':None}
    items1=getItemByplayer(player, item1)
    if not items1:
        return {'result':False,'message':Lg().g(189),'data':None}
    items2=getItemByplayer(player, item2)
    if not items2:
        return {'result':False,'message':Lg().g(189),'data':None}
    
    if items1.getWQtype()!=items2.getWQtype():
        return {'qh':None,'coin':0}

    level=Sxzy(items1, items2)
    zyyh=level+items2.attribute.getStrengthen()#转移以后装备的强化等级
    if player.level.getLevel()<zyyh:
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(207)%zyyh, [player.getDynamicId()])
    Zcion=getSxzyCoin(items1, items2)#转移花费金币
    
    
    return {'qh':level,'coin':Zcion}
        

def runningSxzy(characterid,item1,item2):
    '''执行属性转移'''
    if item1==item2:
        pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(206), [characterid])
        return {'result':False,'message':Lg().g(206),'data':None}
    player=PlayersManager().getPlayerByID(characterid) #角色实例
    if not player:
        return {'result':False,'message':Lg().g(199),'data':None}
    if player.level.getLevel()<30:
        return {'result':False,'message':Lg().g(205),'data':None}
    items1=None
    if player.pack._package._PropsPagePack.getPositionByItemId(item1)!=-1:#背包中没有此物品
        items1=player.pack._package._PropsPagePack.getItemInfoByItemid(item1)#获取物品实例
    else:
        items1=player.pack._equipmentSlot.getItemInfoByItemid(item1)
    if not items1:
        return {'result':False,'message':Lg().g(189),'data':None}
    items2=None
    if player.pack._package._PropsPagePack.getPositionByItemId(item2)!=-1:#背包中没有此物品
        items2=player.pack._package._PropsPagePack.getItemInfoByItemid(item2)#获取物品实例
    else:
        items2=player.pack._equipmentSlot.getItemInfoByItemid(item2)
    if not items2:
        return {'result':False,'message':Lg().g(189),'data':None}
    Zcion=getSxzyCoin(items1, items2)#转移花费金币
    if player.finance.getCoin()<Zcion:
        return {'result':False,'message':Lg().g(88),'data':None}
    level=Sxzy(items1, items2)#转移获得等级
    
    zyyh=level+items2.attribute.getStrengthen()#转移以后装备的强化等级
    if player.level.getLevel()<zyyh:
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(207)%zyyh, [player.getDynamicId()])
        return {'result':False,'message':Lg().g(207)%zyyh,'data':None}
    items1.attribute.updateStrengthen(0)
    if level !=0:
        items2.attribute.updateStrengthen(items2.attribute.getStrengthen()+level)
    player.finance.updateCoin(player.finance.getCoin()-Zcion)
    player.quest.specialTaskHandle(112)#特殊任务处理
    player.schedule.noticeSchedule(5,goal = 1)
    return {'result':True,'message':Lg().g(166),'data':None}
    
    
def Sxzy(items1,items2):
    '''根据两个物品实例获取转移后效果'''
    icon1=0#物品1总共花费
    for i in range(items1.attribute.strengthen):
        icon1+=coinCountObj(items1,i)
    icon2=coinCountObj(items2,items2.attribute.strengthen)#物品2花费
    level=0
    t=1
    while icon1-icon2>=0:
        level+=1
        icon1-=icon2
        icon2=coinCountObj(items2,t)
        t+=1
    return level

def getSxzyCoin(items1,items2):
    '''根据两个物品实例计算花费金币'''
    coin=(items1.attribute.getStrengthen()*2000)+(items2.attribute.getStrengthen()*1000)
    return coin

def getSYtime(pid):
    '''根据角色返回剩余冷却时间'''
    player=PlayersManager().getPlayerByID(pid) #角色实例
    if player:
        ss=player.qhtime.getTime()#获取剩余冷却时间
        return ss
    
def cleanCD(pid):
    '''清除角色强化冷却时间
    @param pid: int 角色id
    '''
    player=PlayersManager().getPlayerByID(pid) #角色实例
    if player:
        return player.qhtime.clearCd()
                
        