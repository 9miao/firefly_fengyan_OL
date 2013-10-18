#coding:utf8
'''
Created on 2012-5-18
装备镶嵌
@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

def GetXiangQianPackInfo2110(dynamicId,characterId,curpage):
    '''获取镶嵌装备包裹
    @param characterId: int 角色的ID
    @param curpage: int 包裹分页
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data  = player.pack.getMosaicItemPackage(curpage)
    return data 

def GetXiangQianStoreInfo2111(dynamicId,characterId,curpage):
    '''获取镶嵌镶嵌石包裹
    @param characterId: int 角色的ID
    @param curpage: int 包裹分页
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data  = player.pack.getMosaicGemPackage(curpage)
    return data

def XiangQian2112(dynamicId,characterId,equipId,sId,packageType,position):
    '''装备镶嵌
    @param characterId: int 角色的ID
    @param equipId: int 装备的ID
    @param sId: int 镶嵌石的ID
    @param packageType: int 装备的位置  1装备栏 2包裹
    @param position: int 镶嵌的位置
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data  = player.pack.ItemMosaic(packageType,equipId,sId,position)
    msg = data.get('message',u'')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return data

def UnloadXiangQian2113(dynamicId,characterId,equipId,packageType,position):
    '''摘除宝石
    @param characterId: int 角色的ID
    @param equipId: int 装备的ID
    @param packageType: int 装备的位置 
    @param position: int 摘除的位置
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data  = player.pack.ItemRemoval(packageType,equipId,position)
    msg = data.get('message',u'')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return data


