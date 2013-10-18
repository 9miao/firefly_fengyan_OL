#coding:utf8
'''
Created on 2013-1-8

@author: lan
'''

from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.language.Language import Lg

def getZhanYiInfo(dynamicId,characterId ,index):
    '''获取角色的战役信息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    zhanyiinfo = player.zhanyi.getZhanYiInfo(index)
    return {'result':True,'data':zhanyiinfo}

def zhangjieFight(dynamicId,characterId,zhangjieid):
    '''章节战斗
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    fightresult = player.zhanyi.doZhangJie(zhangjieid)
    return fightresult




