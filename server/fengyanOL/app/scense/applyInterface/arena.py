#coding:utf8
'''
Created on 2012-7-1
竞技场操作
@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.applyInterface.playerInfo import CanDoServer
from app.scense.core.language.Language import Lg

def GetJingJiInfo3700(dynamicId,characterId):
    '''获取竞技场信息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    res = CanDoServer(characterId)
    if not res['result']:
        pushOtherMessage(905, res.get('message',u''), [dynamicId])
        return res
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.arena.getArenaAllInfo()
    return {'result':True,'data':data}


def AddJingJiCount3703(dynamicId,characterId):
    '''添加竞技次数'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.arena.AddSurplustimes()
    msg = result.get('message',u'')
    if msg:
        pushOtherMessage(905, result.get('message',u''), [dynamicId])
    return result

def ArenaBattle_3704(dynamicId,characterId,tocharacterId):
    '''竞技场战斗
    '''
    player = PlayersManager().getPlayerByID(characterId)
    res = CanDoServer(characterId)
    if not res['result']:
        pushOtherMessage(905, res.get('message',u''), [dynamicId])
        return res
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.arena.doFight(tocharacterId)
    msg = result.get('message',u'')
    if msg:
        pushOtherMessage(905, result.get('message',u''), [dynamicId])
    return result
    
def JingJiCleanCD_2705(dynamicId,characterId):
    '''清除竞技场CD
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.arena.clearCD()
    msg = result.get('message',u'')
    if msg:
        pushOtherMessage(905, result.get('message',u''), [dynamicId])
    return result
    
    


