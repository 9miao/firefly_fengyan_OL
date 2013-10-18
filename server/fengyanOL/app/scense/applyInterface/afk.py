#coding:utf8
'''
Created on 2012-4-12

@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessageByCharacterId
from app.scense.core.language.Language import Lg

def GetWaJueInfo(characterId):
    '''获取加急信息'''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        info = player.afk.getWaJueInfo()
        return {'result':True,'data':info}
    return {'result':False,'message':Lg().g(18)}
    
def StartWaJue(characterId,miningtype):
    '''开始挖掘'''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        data = player.afk.doMining(miningtype)
        if not data.get('result'):
            pushOtherMessageByCharacterId(data.get('message',u''), [characterId])
        return data
    return {'result':False,'message':Lg().g(18)}
    

def DianShiChengJin(characterId):
    '''点石成金'''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        data = player.afk.dianshichengjin()
        if not data.get('result'):
            pushOtherMessageByCharacterId(data.get('message',u''), [characterId])
        else:
            msg = Lg().g(19)%(data.get('data',0))
            pushOtherMessageByCharacterId(msg, [characterId])
        return data
    return {'result':False,'message':Lg().g(18)}
    
def LevelUpSpeedWaJue(characterId,mtype):
    '''加强挖掘'''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        data = player.afk.updateMiningMode(mtype)
        if not data.get('result'):
            pushOtherMessageByCharacterId(data.get('message',u''), [characterId])
        return data
    return {'result':False,'message':Lg().g(18)}

def NowSuccWaJue(characterId):
    '''立即完成挖掘'''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        data = player.afk.FinishedMining()
        msg = data.get('message',u'')
        if msg:
            pushOtherMessageByCharacterId(msg, [characterId])
        return data 
    return {'result':False,'message':Lg().g(18)}

def GetAramListInfo(characterId):
    '''获取训练列表'''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        info = player.afk.getAramListInfo()
        return {'result':True,'data':info}
    return {'result':False,'message':Lg().g(18)}

def AramStartXunLian(characterId,ttype,funType,funId):
    '''开始训练'''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        data = player.afk.doTrain(ttype,funType,funId)
        if not data.get('result'):
            pushOtherMessageByCharacterId(data.get('message',u''), [characterId])
        return data 
    return {'result':False,'message':Lg().g(18)}

def AramJiaJiXunLian(characterId,ptype,funId):
    '''加急训练'''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        data = player.afk.JiaJiXunLian(ptype,funId)
        if not data.get('result'):
            pushOtherMessageByCharacterId(data.get('message',u''), [characterId])
        else:
            msg = u"获得%d经验"%(data.get('data',0))
            pushOtherMessageByCharacterId(msg, [characterId])
        return data
    return {'result':False,'message':Lg().g(18)}

def AramLevelUpSpeedXunLian(characterId,tmode,funType,funId):
    '''加速训练'''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        info = player.afk.updateTrainMode(tmode)
        return {'result':True,'data':info}
    return {'result':False,'message':Lg().g(18)}

def AramNowSuccXunLian(characterId,ptype,funId):
    '''立即完成训练'''
    player = PlayersManager().getPlayerByID(characterId)
    if player:
        info = player.afk.FinishedTrain()
        msg = info.get('message',u'')
        if msg:
            pushOtherMessageByCharacterId(msg, [characterId])
        return info
    return {'result':False,'message':Lg().g(18)}

def Saodang(characterId,fubenId,sdType,sdRound):
    '''扫荡
    @param characterId: int 角色的ID
    @param fubenId: int 副本的ID
    @param sdType: int 扫荡类型
    @param sdRound: int 扫荡回合数
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'messge':Lg().g(18)}
    if sdType == 0:
        rounds = 0
    else:
        rounds = sdRound
    result = player.raids.doRaids(rounds,fubenId)
    msg = result.get('message',u'')
    if msg:
        pushOtherMessageByCharacterId(msg, [characterId])
    return result

    
    

