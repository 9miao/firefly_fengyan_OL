#coding:utf8
'''
Created on 2011-5-16

@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.language.Language import Lg

def getRestRoomInfo(dynamicId,characterId,placeId):
    '''获取宿屋信息
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param placeId: int 场景的id 
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    restNum = player.attribute.getRestNum()
    return {'result':True,'data':restNum}

def restOperate(dynamicId,characterId,restType,payType,payNum):
    '''宿屋各种休息操作
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param type: str 休息的类型 ['meal','nap','lightSleep','peacefulSleep','spoor']
    @param payType: str 支付币的类型 'coin','gold','coupon'
    @param payNum: int 支付的数量
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
#    restTypeList = ['meal','nap','lightSleep','peacefulSleep','spoor']
#    restType = restTypeList[type-1]
    restNum = player.attribute.getRestNum()
    if type<>u'meal' and restNum[restType] == 0:
        return {'result':False,'message':u'今天操作次数已满'}
    data = player.attribute.doRest(restType, payType, payNum)
    return data
    
    
        
        