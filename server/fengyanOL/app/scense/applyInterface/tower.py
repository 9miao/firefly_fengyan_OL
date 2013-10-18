#coding:utf8
'''
Created on 2012-7-18
爬塔
@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.applyInterface.playerInfo import CanDoServer
from app.scense.core.language.Language import Lg

def GetCurLevelInfo4200(dynamicId,characterId):
    '''获取当前塔层的信息
    @param dynamicId: int 客户端的连接ID
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    res = CanDoServer(characterId)
    if not res['result']:
        pushOtherMessage(905, res.get('message',u''), [dynamicId])
        return res
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.tower.getTowerInfo()
    msg = data.get('message')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return {'result':True,'data':data}

def RefreshInfo4201(dynamicId,characterId):
    '''刷新爬塔信息
    @param dynamicId: int 客户端的连接ID
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    res = CanDoServer(characterId)
    if not res['result']:
        pushOtherMessage(905, res.get('message',u''), [dynamicId])
        return res
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.tower.flushTowerRecord()
    msg = data.get('message')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return data

def AutoPaTa4202(dynamicId,characterId):
    '''开始爬塔
    @param dynamicId: int 客户端的连接ID
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    res = CanDoServer(characterId)
    if not res['result']:
        pushOtherMessage(905, res.get('message',u''), [dynamicId])
        return res
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.tower.autoclimb()
    msg = result.get('message')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return result
    
def TowerBattle_4203(dynamicId,characterId):
    '''爬塔战斗
    @param dynamicId: int 客户端的连接ID
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    res = CanDoServer(characterId)
    if not res['result']:
        pushOtherMessage(905, res.get('message',u''), [dynamicId])
        return res
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.tower.climb()
    msg = result.get('message')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return result
    
