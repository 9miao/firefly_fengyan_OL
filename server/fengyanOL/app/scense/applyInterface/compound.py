#coding:utf8
'''
Created on 2012-5-21
物品合成
@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

def GetAllHeChengInfos2114(dynamicId,characterId):
    '''获取所有的合成配方信息
    @param characterId: int 角色的ID
    ''' 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data  = player.pack.getCompoundsInfo()
    return data 

def GetOneItemHeChengInfo2115(dynamicId,characterId,itemId):
    '''获取单个物品的合成信息
    @param characterId: int 角色的ID
    @param itemId: int 物品的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data  = player.pack.getOneItemCompoundInfo(itemId)
    return data 

def Hecheng2116(dynamicId,characterId,itemId):
    '''物品合成
    @param characterId: int 角色的ID
    @param itemId: int 物品的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data  = player.pack.ItemCompound(itemId)
    msg = data.get('message',u'')
    if msg:
        pushOtherMessage(905, data.get('message',u''), [dynamicId])
    return data 
    
    
    