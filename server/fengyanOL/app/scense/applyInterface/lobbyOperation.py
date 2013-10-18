#coding:utf8
'''
Created on 2011-5-23

@author: sean_lan
'''
from app.scense.utils import dbaccess
from app.scense.applyInterface.playerInfo import CanDoServer
from twisted.internet import reactor
from app.scense.core.PlayersManager import PlayersManager
import datetime ,time, math
from app.scense.core.language.Language import Lg
#from netInterface.pushObjectNetInterface import p
reactor = reactor

def doWhenLobbyOperateFinsihed(attrs, player):
    '''当大厅操作时间结束时'''
    now = datetime.datetime.now()
    lobbyRecord = dbaccess.getPlayerLobbyRecord(player.baseInfo.id)
    finishTime = lobbyRecord[3]
    if (not finishTime) or (finishTime > now):
        return
    dbaccess.updatePlayerInfo(player.baseInfo.id, attrs)
#    pushMessage(str(player.baseInfo.id), 'finish')
    player.baseInfo.setStatus(1)
    player.finance.setCoin(attrs['coin'])
    player.level.setExp(attrs['exp'])
    player.level.updateLevel()
    

def lobbyOperate(dynamicId,characterId,operaType,duration):
    '''
          大厅操作：修炼、卖艺
    @param operaType: 操作类型：1、训练   2、卖艺
    @param duration: 持续时间
        训练得到的经验=[(自身等级+1)*33]^1.15*训练小时数
        训练消耗的铜币=[(自身等级+1)*44]^1.15*训练小时数
    '''
    
    ret = CanDoServer(characterId)
    if not ret['result']:
        return ret

    player = PlayersManager().getPlayerByID(characterId)
    if player is None:
        return {'result':False,'message':Lg().g(18)}
    
    level = player.level.getLevel()
    exp = player.level.getExp()
    coin = player.finance.getCoin()
    startTime = datetime.datetime.now()
    finishTime = startTime + datetime.timedelta(hours = 1)
    status = 0
    getExp = 0
    costCoin = 0
    if operaType == 1:#训练
        status = 3
        getExp = int(math.pow((level + 1) * 33, 1.15) * duration)
        costCoin = int(math.pow(((level) + 1) * 44, 1.15) * duration)
        exp += getExp
        coin -= costCoin
        if coin < 0:
            return {'result':False, 'message':u'您的铜币不足'}
        dbaccess.updatePlayerInfo(characterId, {'status':status, 'coin':coin})
        bonusCount = getExp
    else:#卖艺
        status = 6
        pass
    dbaccess.updatePlayerLobbyRecord(characterId, {'startTime':str(startTime), 'finishTime':str(finishTime), 'isDoubleBonus':0})
    player.finance.setCoin(coin)
    player.baseInfo.setStatus(status)
    statusDesc = player.baseInfo.setStatus(1)
    durationTime = duration * 3600
    reactor.callLater(durationTime, doWhenLobbyOperateFinsihed, {'status':1, 'coin':coin, 'exp':exp}, player)
    
    startTime = int(time.mktime(startTime.timetuple()))
    finishTime = int(time.mktime(finishTime.timetuple()))
    
    return {'result':True, 'data':{'status':statusDesc, 'bonusCount':bonusCount, \
                                   'startTime':startTime, 'finishTime':finishTime, \
                                   'duration':duration}}

def terminateLobbyOperation(dynamicId,characterId,operaType):
    '''
          中断大厅操作
    @param operaType: 操作类型：1、训练   2、卖艺
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if player is None:
        return {'result':False,'message':Lg().g(18)}

    level = player.level.getLevel()
    lobbyRecord = dbaccess.getPlayerLobbyRecord(characterId)
    if lobbyRecord[2] == None or lobbyRecord[3] == None:
        return {'result':False, 'message':u'您的大厅操作记录不正确'}
    now = datetime.datetime.now()
    duration = int(((lobbyRecord[3] - now).seconds) / 3600)
    bonus = 0
    exp = player.level.getExp()
    if operaType == 1:
        if lobbyRecord[4] == 1:#双倍奖励
            bonus = int(math.pow((level + 1) * 33, 1.15) * duration * 2)
        else:
            bonus = int(math.pow((level + 1) * 33, 1.15) * duration)
            exp += bonus
        dbaccess.updatePlayerInfo(characterId, {'status':1, 'exp':exp})
        player.level.setExp(exp)
        player.level.updateLevel()
        player.baseInfo.setStatus(1)
    else:
        pass
    
    return {'result':True, 'data':{'bonus':bonus, 'level':player.level.getLevel()}}



    