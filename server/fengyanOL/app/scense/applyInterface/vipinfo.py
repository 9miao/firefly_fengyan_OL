#coding:utf8
'''
Created on 2012-7-3
VIP功能信息
@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.language.Language import Lg

def GetVipInfo_3800(dynamicId,characterId):
    '''获取角色包裹信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.level.getVIPInfo()
    return result
