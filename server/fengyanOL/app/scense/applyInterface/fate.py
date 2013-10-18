#coding:utf8
'''
Created on 2012-6-7

@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.FateShop import FateShop
from app.scense.core.language.Language import Lg

def GetXingYunList(dynamicId,characterId):
    '''获取星运信息
    @param dynamicId: int 客户端的动态ID
    @param characterId: int 角色的ID 
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.fate.getZhanXingInfo()
    return result

def ZhanXing(dynamicId,characterId,fatelevel):
    '''开始占星
    @param dynamicId: int 客户端的动态ID
    @param characterId: int 角色的ID 
    @param fatelevel: int 占星的等级
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.fate.ZhanXing(fatelevel)
    msg = result.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return result

def YiJianObtainAndDrop(dynamicId,characterId,opearType):
    '''一键拾取或卖出
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if opearType:
        result = player.fate.SellAll()
    else:
        result = player.fate.PickUpAll()
    return result

def YiJianZhanXing(dynamicId,characterId):
    '''一键占星
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.fate.AutoZhanXing()
    return result

def GetPackXingYunListInfo(dynamicId,characterId):
    '''获取占星包裹信息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.fate.getZhanXingPack()
    return {'result':True,'data':data}

def YiJianHeCheng(dynamicId,characterId):
    '''一键合成
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.fate.HeChengAll()
    return result

def GetRoleAndPetList(dynamicId,characterId):
    '''获取角色和宠物的星运装备栏信息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.fate.GetRoleAndPetFateList()
    return {'result':True,'data':data}
    
def MoveXingYun(dynamicId,characterId,opear,opeType,frompos,topos):
    '''移动星运
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.fate.MoveFate(opeType,opear,frompos,topos)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return data

def GetJiFengShopInfo(dynamicId,characterId,page):
    '''获取星运积分商城信息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    info = FateShop().getShopInfo(page)
    info['score'] = player.fate.score
    return {'result':True,'data':info}
    
def QueRenExchange(dynamicId,characterId,fateId):
    '''积分兑换星运'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.fate.ExchangeFate(fateId)
    msg = result.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return result
    
    