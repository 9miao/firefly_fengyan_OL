#coding:utf8
'''
Created on 2011-5-26
@author: sean_lan
'''

from app.scense.applyInterface import fight
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.fight import battle_new703_pb2
from app.scense.protoFile.fight import quitFight_pb2
from app.scense.protoFile.fight import getAllCardInfo705_pb2
from app.scense.protoFile.fight import TurnCard_pb2
from app.scense.protoFile.fight import FightWithPlayer720_pb2
from app.scense.netInterface.pushObjectNetInterface import pushApplyMessage,pushOtherMessage

@nodeHandle
def FightInScene_703(dynamicId, request_proto):
    '''副本场景战斗'''
    argument = battle_new703_pb2.FightRequest()
    argument.ParseFromString(request_proto)
    response = battle_new703_pb2.FightResponse()
    
    characterId = argument.id
    monsterId = argument.tid
    result = fight.FightInScene(dynamicId, characterId, monsterId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        data = result['data']
        response.data.fightType = data.get('fightType',1) 
        response.data.centerX = int(data['centerX'])
        response.data.centerY = data['centerY']
        battle = data['battle']
        response.data.battleResult = battle.battleResult
        rResArr = response.data.rResArr
        startData = response.data.startData
        setpdata = response.data.stepData
        battle.SerializationResource(rResArr)
        battle.SerializationInitBattleData(startData)
        battle.SerializationStepData(setpdata)
        for _item in data['setData']:
            setData = response.data.setData.add()
            for attr in _item.items():
                if attr[0]=='itemsBonus':
                    if attr[1]:
                        items1=setData.itemsBonus
                        items1.itemId = attr[1].baseInfo.itemTemplateId
                        items1.stack = attr[1].pack.getStack()
                    continue
                setattr(setData,attr[0],attr[1])                        
    msg = response.SerializeToString()
    return msg
    
    
@nodeHandle
def quitFight_704(dynamicId,request_proto):
    '''退出战斗'''
    argument = quitFight_pb2.quitFightRequest()
    argument.ParseFromString(request_proto)
    response = quitFight_pb2.quitFightResponse()
    
    characterId = argument.id
    data = fight.quitFight(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        response.data.placeId = data['data'].get('placeId',1000)
    return response.SerializeToString() 

@nodeHandle
def getAllCardInfo_705(dynamicId,request_proto):
    '''获取所有卡片的信息
    '''
    argument = getAllCardInfo705_pb2.getAllCardInfoRequest()
    argument.ParseFromString(request_proto)
    response = getAllCardInfo705_pb2.getAllCardInfoResponse()
    
    characterId = argument.id
    data = fight.getAllCardInfo(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        cardsInfo = data.get('data')
        for cardInfo in cardsInfo:
            card = response.data.card.add()
            card.cardId = cardInfo['cardId']
            card.coinBounds = cardInfo['coinBounds']
            if cardInfo['itemBound']:
                card.itemBound.itemId = cardInfo['itemBound'].baseInfo.itemTemplateId
                card.itemBound.stack = cardInfo['itemBound'].pack.getStack()
    return response.SerializeToString()

@nodeHandle
def TurnCard_707(dynamicId,request_proto):
    '''翻转卡片'''
    argument = TurnCard_pb2.TurnCardRequest()
    argument.ParseFromString(request_proto)
    response = TurnCard_pb2.TurnCardResponse()
    
    characterId = argument.characterId
    cardId = argument.cardId
    
    data = fight.TurnCard(dynamicId, characterId, cardId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()


@nodeHandle
def FightWithPlayer_720(dynamicId,request_proto):
    '''场景中玩家战斗
    '''
    argument = FightWithPlayer720_pb2.FightPkRequest()
    argument.ParseFromString(request_proto)
    response = FightWithPlayer720_pb2.FightPkResponse()
    fightResponse = battle_new703_pb2.FightResponse()
    
    characterId = argument.id
    tid = argument.tid
    data = fight.FightWithPlayer(dynamicId, characterId, tid)
    msg = data.get('message','')
    response.result = data.get('result',False)
    response.message = msg
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    if data.get('data',None):
        from twisted.internet import reactor
        battle = data.get('data',None)
        sendlist = data.get('sendlist',[])
        fightResponse.data.battleResult = battle.battleResult
        fightResponse.data.centerX = 550
        fightResponse.data.centerY = 550
        fightResponse.data.fightType = 1
        
        rResArr = fightResponse.data.rResArr
        startData = fightResponse.data.startData
        setpdata = fightResponse.data.stepData
        fightResponse.result = True
        fightResponse.message = u''
        
        battle.SerializationResource(rResArr)
        battle.SerializationInitBattleData(startData)
        battle.SerializationStepData(setpdata)
        battlemsg = fightResponse.SerializeToString()
        setData1 = fightResponse.data.setData.add()
        setData1.id = characterId
        setData1.coinBonus = 10
        setData2 = fightResponse.data.setData.add()
        setData2.id = tid
        setData2.coinBonus = 10
        reactor.callLater(1,pushApplyMessage,711,battlemsg,sendlist)
    return response.SerializeToString()
    
    