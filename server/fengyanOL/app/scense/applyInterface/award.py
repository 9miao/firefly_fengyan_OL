#coding:utf8
'''
Created on 2012-4-8

@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.language.Language import Lg

def getAwardInfo(dynamicId,characterId,awardtype):
    '''获取奖励信息
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param awardtype: int 奖励的类型
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if  not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    awardInfo = player.award.getAwardInfo(awardtype)
    return {'result':True,'message':u'','rewardInfo':awardInfo}

def receiveAward(dynamicId,characterId,awardtype):
    '''领取奖励
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param awardtype: int 奖励的类型
    '''
    player = PlayersManager().getPlayerByID(characterId)
    
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.award.receiveAward(awardtype)
    return {'result':result,'message':u''}
    
    