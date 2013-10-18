#coding:utf8
'''
Created on 2011-5-16

@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.language.Language import Lg

def getMonsterPracticeExp(dynamicId,characterId,monsterId):
    '''获取单个怪物修炼所得经验
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param monsterId: int 怪物的模板id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.practice.getMonsterPracticeExp(monsterId)
    return data

def pratice(dynamicId,characterId,monsterId,singleExpBonus,monsterCount,monsterLevel):
    '''进行修炼
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param monsterId: int 怪物的模板id
    @param singleExpBonus: int 单个怪物修炼获取的经验
    @param monsterCount: int 修炼的数量
    @param monsterLevel: 怪物的等级
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.practice.pratice(monsterId, singleExpBonus, monsterCount, monsterLevel)
    return data

def terminatePractice(dynamicId,characterId):
    '''终止修炼
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.practice.terminatePractice()
    return data

def immediateFinishPractice(dynamicId,characterId,payType,payNum):
    '''立即完成修炼
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param payType: int 支付类型
    @param payNum: int  支付的数量
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.practice.immediateFinishPractice(payType, payNum)
    return data
    
    
    
    