#coding:utf8
'''
Created on 2012-5-7
角色日程表,每日目标
@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

def GetCalendarTaskListInfo(characterId):
    '''获取角色日程信息
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        return player.schedule.getScheduleInfo()
    return {'result':False,'message':Lg().g(18)}

def ReceivedCalendarBound(characterId,step):
    '''领取日程表的奖励
    @param step: int 奖励的步骤
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        return player.schedule.receiveBound(step)
    return {'result':False,'message':Lg().g(18)}

def GetTargetInfo(characterId):
    '''获取角色每日目标数据
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        return player.daily.getAllDailyInfo()
    return {'result':False,'message':Lg().g(18)}

def ObtainTargetReward(characterId,taskId):
    '''领取每日目标奖励
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data =  player.daily.receiveBound(taskId)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [player.dynamicId])
    return data
    


