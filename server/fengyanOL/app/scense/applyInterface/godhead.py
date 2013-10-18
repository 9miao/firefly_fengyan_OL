#coding:utf8
'''
Created on 2012-5-15
角色神格相关
@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

def getGodheadInfo(dynamicId,characterId,headtype):
    '''获取指定神格类型的神格信息列表
    @param characterId: int 角色的ID
    @param headtype: int 神格的类型
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data  = player.godhead.getGodheadInfo(headtype)
    return data

def ActiveGodhead(dynamicId,characterId,godheadid):
    '''激活神格'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data  = player.godhead.ActiveGodhead(godheadid)
    pushOtherMessage(905, data.get('message',u''), [dynamicId])
    return data
    
    
