#coding:utf8
'''
Created on 2012-5-2
角色冥想（在线挂机）
@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

def StartUpGuaJi(dynamicId,characterId):
    '''角色开始挂机
    @param characterId: int 角色的ID
    '''
    from app.scense.core.campaign.FortressManager import FortressManager
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    #判断是否有冥想加成
    if player.baseInfo.getState()==1:  #如果角色在副本
        state = 0
    else:
        guildId = player.guild.getID()
        sceneId = player.baseInfo.getTown()
        fortress=  FortressManager().getFortressBySceneId(sceneId)
        if not fortress.isOccupied:
            state = 0
        else:
            if fortress.kimori==guildId and guildId!=0:
                state=1
            else:
                state = 0
    result = player.afk.startMeditation(state=state)
    if not result.get('result'):
        msg = result.get('message')
        sendId = player.getDynamicId()
        pushOtherMessage(905, msg, [sendId])
    return result

def CancelGuaJi(characterId):
    '''角色取消挂机
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.afk.stopMeditation()
    if not result.get('result'):
        msg = result.get('message')
        sendId = player.getDynamicId()
        pushOtherMessage(905, msg, [sendId])
    return result
    
def GetGuaJiInfo(characterId):
    '''获取挂机信息
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.afk.getMeditationInfo()
    return result
    
    
    
    