#coding:utf8
'''
Created on 2011-4-13

@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.character.PlayerCharacter import PlayerCharacter
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.utils import dbaccess
import datetime
import time
from app.scense.core.shop.PublicShop import PublicShop
from app.scense.core.shop.mall import Mall
from app.scense.core.shop.shopmanager import ShopManager
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.language.Language import Lg


def getShopInfo(dynamicId,characterId,shopCategory):
    '''获取商店信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param shopType: int 商店类型  1武器 2防具 3材料 4 杂货
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    package = player.shop.getShopPackage(shopCategory)
    result = package.getPackageItemInfo()
    refreshShopTime = player.shop.getRefreshShopTime()
    data = {'shopCategory':shopCategory,'refreshShopTime':refreshShopTime,'packageItemInfo':result}
    return {'result':True,'data':data}

def buyItemInMyshop(dynamicId,characterId,itemTemplateId):
    '''获取商城信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param itemTemplateId: int 物品的模板Id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data  = player.shop.buyItemInMyshop(itemTemplateId)
    return data
    
def getMallItemInfo(dynamicId,characterId,page,tag):
    '''获取商城信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param page: int 页面号
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = Mall().getPageItems(page,tag)
    maxpage = Mall().getMaxPageByType(tag)
    cx=Mall().getCXItemInfo()
    data = {'maxpage':maxpage,'items':result,'page':page,'cx':cx}
    return {'result':True,'data':data}

def buyItemInMall(dynamicId,characterId,itemTemplateId,count,priceType,buyType,presentName):
    '''购买商城中的物品
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param itemTemplateId: 物品的模板id
    @param priceType: int 1为钻价格 2为绑定钻价格
    @param butType: int 购买类型 0购买1赠送
    @param presentName: string 赠送角色的名称
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    tocid=0 #送给谁的
    if buyType==1:
        data=dbaccess.getCharecterInfoByNickName(presentName)
        if not data:
            return{'result':False,'message':Lg().g(188)%presentName}
        else:
            tocid=data.get('id',0)
    mall_item=Mall().getItemInfoById(itemTemplateId) #获取商城物品
    if not mall_item:
        return {'result':False,'message':Lg().g(189)}
    return buyService(player, itemTemplateId, count, mall_item,tocid)
        
        
def buyService(player,itemTemplateId,count,mall_item,tocid):
    '''购买商城商品
    @param player: object 角色实例
    @param itemTemplateId: int 物品模板id
    @param count: int 购买物品的数量
    @param mall_item: object 商城中的物品信息
    @param tocid: int 送给角色的id 0为没有赠送人
    '''
    if player.finance.getGold()>=(mall_item['gold']*count):
        flg= buyServicepack(player,mall_item,tocid)
        if flg.get('result'):
            player.daily.noticeDaily(9,0,1)
        return flg
    else:
        data={'recharge':True,'priceType':1,'itemTemplateId':itemTemplateId,'count':count}
        return {'result':False,'message':Lg().g(190),'data':data}


def buyServicepack(player,mall_item,toid):
    '''把物品放入包裹中并扣除角色钱
    @param player: object 购买者的实例
    @param mall_item: 商城中的物品信息
    @param isGold: bool  是否是钻支付  ture 钻支付   false 绑定钻支付
    @param toid: int 送给角色的id 0为没有赠送人
    '''
    zhekou = player.attribute.getMallrebate()#VIP折扣
    gold= int(mall_item['gold']*1.0*zhekou)
    if mall_item['cx']>0:
        gold=mall_item['cx']
    newitem = mall_item['templateid']
    count = mall_item['count']
    itemTemplateId = newitem
    value=player.finance.getGold()-gold

    if value<0:
        data={'recharge':True,'priceType':1,'itemTemplateId':itemTemplateId,'count':count}
        return {'result':False,'message':Lg().g(190),'data':data}
    if toid>0:
        result=PlayerCharacter(toid).pack.putNewItemsInPackage(newitem,count)
        if not result:
            data={'recharge':False,'priceType':1,'itemTemplateId':itemTemplateId,'count':count}
            return {'result':False,'message':Lg().g(191),'data':data}
    else:
        result=player.pack.putNewItemsInPackage(newitem,count)
    if not result:
        data={'recharge':False,'priceType':1,'itemTemplateId':itemTemplateId,'count':count}
        return {'result':False,'message':Lg().g(16),'data':data}
    player.finance.updateGold(value)
    player.finance.consGold(gold,2,itemId=newitem)
    
    player.schedule.noticeSchedule(12,goal = gold)
    data={'recharge':False,'priceType':1,'itemTemplateId':itemTemplateId,'count':count}
    pushObjectNetInterface.pushUpdatePlayerInfo(player.dynamicId)
    if toid>0:
        return {'result':True,'message':Lg().g(192),'data':data}
    return {'result':True,'message':Lg().g(193),'data':data}

            
def getMallByItemtemplateid(itemid):
    '''根据物品模板Id获取特价商品剩余时间'''
    info = dbaccess.getMallItemById(itemid)
    if info:
        if info['tag'].find('1')!=-1:
            nowtime=datetime.datetime.fromtimestamp(time.time()) #系统当前时间
            down=info['cheapend']
            s1=(down-nowtime).days*24*3600
            s2=(down-nowtime).seconds
#            hours=s2//3600
#            m=s2%3600
#            m1=m//60
#            s=m%60
            return {'result':True,'message':u'返回数据','daga':s1+s2}
        else:
            return {'result':False,'message':Lg().g(194)}
    return {'result':False,'message':Lg().g(189)}

def getNpcShopInfo(dynamicId,characterId,npcId,shopCategory,curPage):
    '''获取公共商店信息'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    publicshop = ShopManager().getShopByID(npcId)
    if not publicshop:
        publicshop = PublicShop(npcId)
        ShopManager().addShop(publicshop)
    if shopCategory ==0:
        data = publicshop.getPublicShopInfo(curPage)
    else:
        data = publicshop.getRepurchaseInfo(characterId)
    return {'result':True,'data':data}
        
def NpcShopSellItem(dynamicId,characterId,itemPos,packageType,curpage,stack):
    '''出售物品
    @param itemPos: int 
    @param packageType: int 背包标签页 1道具 2任务物品
    @param curpage: int 当前页数
    @param stack: int 出售数量
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.pack.sellItemInpack(itemPos,packageType,curpage,stack)
    pushOtherMessage(905, data.get('message',''), [dynamicId])
    return data

def NpcShopBuyItem(dynamicId,characterId,itemId,opeType,buyNum,npcId):
    '''购买，回购商品
    @param opeType: int 操作类型 0购买1购回
    @param buyNum: int 购买的数量
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if opeType==0:
        data  = player.shop.buyItemInMyshop(itemId,buyNum,npcId)
    else:
        data = player.shop.RepurchaseItem(itemId)
    if data.get('result',False):
        if opeType == 0:
            pushOtherMessage(905, Lg().g(193), [dynamicId])
        else:
            pushOtherMessage(905, Lg().g(195), [dynamicId])
    return data


