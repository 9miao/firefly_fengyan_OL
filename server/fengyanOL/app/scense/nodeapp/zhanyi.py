#coding:utf8
'''
Created on 2013-1-8

@author: lan
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.zhanyi import GetNowZhanYiInfo4500_pb2,ZhangJieFight4501_pb2
from app.scense.protoFile.fight import battle_new703_pb2
from app.scense.netInterface.pushObjectNetInterface import pushApplyMessage

from app.scense.applyInterface import zhanyi

@nodeHandle
def GetNowZhanYiInfo_4500(dynamicId, request_proto):
    argument = GetNowZhanYiInfo4500_pb2.GetNowZhanYiInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetNowZhanYiInfo4500_pb2.GetNowZhanYiInfoResponse()
    
    characterId = argument.id
    index = argument.index
    data = zhanyi.getZhanYiInfo(dynamicId, characterId, index)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        info = data.get('data')
        response.data.index = info.get('index')
        response.data.maxpage = info.get('maxpage')
        zhanyiInfo = info.get('zyinfo')
        response.data.name = zhanyiInfo.get('name')
        response.data.desc = zhanyiInfo.get('desc')
        response.data.state = zhanyiInfo.get('state')
        zymonsterResponse = response.data.monster
        zymonster = zhanyiInfo.get('monster')
        zymonsterResponse.id = zymonster.get('id')
        zymonsterResponse.name = zymonster.get('nickname')
        zymonsterResponse.resource = zymonster.get('resourceid')
        zhangjielistInfo = zhanyiInfo.get('zhangjielist')
        for _zhanjie in zhangjielistInfo:
            zhanjieResponse = response.data.zhangjielist.add()
            zhanjieResponse.zhangjieid = _zhanjie.get('zhangjieid')
            zhanjieResponse.name = _zhanjie.get('name')
            zhanjieResponse.desc = _zhanjie.get('desc')
            zhanjieResponse.state = _zhanjie.get('state')
            zhanjiemonster = _zhanjie.get('monster')
            zhanjieResponse.monster.id = zhanjiemonster.get('id')
            zhanjieResponse.monster.name = zhanjiemonster.get('nickname')
            zhanjieResponse.monster.resource = zhanjiemonster.get('resourceid')
    return response.SerializeToString()

@nodeHandle
def ZhangJieFight_4501(dynamicId, request_proto):
    '''爬塔战斗
    '''
    argument = ZhangJieFight4501_pb2.ZhangJieFightRequest()
    argument.ParseFromString(request_proto)
    response = ZhangJieFight4501_pb2.ZhangJieFightResponse()
    fightResponse = battle_new703_pb2.FightResponse()
    characterId = argument.id
    zhangjieid = argument.zhangjieid
    data = zhanyi.zhangjieFight(dynamicId, characterId, zhangjieid)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    battlemsg = None
    if data.get('data',None):
        from twisted.internet import reactor
        responsedata = data.get('data')
        battle = responsedata.get('fight')
        bounds = responsedata.get('bound',{})
        fightResponse.data.fightType = data.get('fightType',1) 
        fightResponse.data.centerX = 550
        fightResponse.data.centerY = 350#data['centerY']
        fightResponse.data.battleResult = battle.battleResult
        rResArr = fightResponse.data.rResArr
        startData = fightResponse.data.startData
        setpdata = fightResponse.data.stepData
        fightResponse.result = True
        fightResponse.message = u''
        battle.SerializationResource(rResArr)
        battle.SerializationInitBattleData(startData)
        battle.SerializationStepData(setpdata)
        setData = fightResponse.data.setData.add()
        setData.id = characterId
        setData.expBonus = bounds.get('exp',0)
        setData.name = bounds.get('name',u'')
        itembound = bounds.get('item')
        if itembound:
            itemsBoundResponse=setData.itemsBonus
            itemsBoundResponse.itemId = itembound.baseInfo.itemTemplateId
            itemsBoundResponse.stack = itembound.pack.getStack()
        battlemsg = fightResponse.SerializeToString()
        reactor.callLater(1,pushApplyMessage,711,battlemsg,[dynamicId])
    return response.SerializeToString()





