#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import practice
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.practice import getMonsterPracticeExp_pb2
from app.scense.protoFile.practice import pratice_pb2
from app.scense.protoFile.practice import terminatePractice_pb2
from app.scense.core.language.Language import Lg

def getMonsterPracticeExp(dynamicId,request_proto):#####没有
    '''获取单个怪物修炼获取的经验'''
    argument = getMonsterPracticeExp_pb2.getMonsterPracticeExpRequest()
    argument.ParseFromString(request_proto)
    response = getMonsterPracticeExp_pb2.getMonsterPracticeExpResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    monsterId = argument.monsterId
    data = practice.getMonsterPracticeExp(dynamicId, characterId, monsterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        result = data.get('data')
        response.data.expBonus = result['expBonus']
        response.data.monsterLevel = result['monsterLevel']
    return response.SerializeToString()

@nodeHandle
def pratice_403(dynamicId,request_proto):
    '''怪物修炼'''
    argument = pratice_pb2.praticeRequest()
    argument.ParseFromString(request_proto)
    response = pratice_pb2.praticeResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    monsterId = argument.monsterId 
    singleExpBonus = argument.singleExpBonus
    monsterCount = argument.monsterCount 
    monsterLevel = argument.monsterLevel
    data = practice.pratice(dynamicId, characterId, monsterId, singleExpBonus, monsterCount, monsterLevel)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        statuses = {1:Lg().g(616),2:Lg().g(174),3:Lg().g(617),4:Lg().g(172),5:Lg().g(171),6:Lg().g(618)}
        response.data.status = statuses.get(data.get('data')['status'],u'')
    return response.SerializeToString()

@nodeHandle
def terminatePractice_405(dynamicId,request_proto):
    '''立即结束修炼'''
    argument = terminatePractice_pb2.terminatePracticeRequest()
    argument.ParseFromString(request_proto)
    response = terminatePractice_pb2.terminatePracticeResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = practice.terminatePractice(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        response.data.monsterName  = data.get('data')['monsterName']
        response.data.currentExp = data.get('data')['currentExp']
        response.data.currentCountHit = data.get('data')['currentCountHit']
        statuses = {1:Lg().g(616),2:Lg().g(174),3:Lg().g(617),4:Lg().g(172),5:Lg().g(171),6:Lg().g(618)}
        response.data.status = statuses.get(data.get('data')['status'],u'')
        response.data.level = data.get('data')['level']
    return response.SerializeToString()

@nodeHandle
def immediateFinishPractice_404(dynamicId,request_proto):
    '''立即完成修炼'''
