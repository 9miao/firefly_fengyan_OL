#coding:utf8
'''
Created on 2012-7-18

@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.applyInterface import tower
from app.scense.protoFile.tower import GetCurLevelInfo4200_pb2
from app.scense.protoFile.tower import RefreshInfo4201_pb2
from app.scense.protoFile.tower import AutoPaTa4202_pb2
from app.scense.protoFile.tower import TowerBattle_4203_pb2
from app.scense.protoFile.fight import battle_new703_pb2
from app.scense.netInterface.pushObjectNetInterface import pushApplyMessage

@nodeHandle
def GetCurLevelInfo_4200(dynamicId, request_proto):
    '''获取当前塔层信息
    '''
    argument = GetCurLevelInfo4200_pb2.GetCurLevelInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetCurLevelInfo4200_pb2.GetCurLevelInfoResponse()
    
    characterId = argument.id
    data = tower.GetCurLevelInfo4200(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        info = data.get('data')
        response.panPaInfo.curLev = info.get('layer',0)
        try:
            response.panPaInfo.curMonster = info.get('monsterinfo','')
            response.panPaInfo.obtainItem = info.get('boundInfo','')
        except:
            response.panPaInfo.curMonster = info.get('monsterinfo','').decode('utf8')
            response.panPaInfo.obtainItem = info.get('boundInfo','').decode('utf8')
        response.panPaInfo.reCount = info.get('surplus',0)
        response.panPaInfo.reZuan = info.get('gold',0)
    return response.SerializeToString()

@nodeHandle
def RefreshInfo_4201(dynamicId, request_proto):
    '''刷新塔层信息
    '''
    argument = RefreshInfo4201_pb2.RefreshInfoRequest()
    argument.ParseFromString(request_proto)
    response = RefreshInfo4201_pb2.RefreshInfoResponse()
    
    characterId = argument.id
    data = tower.RefreshInfo4201(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def AutoPaTa_4202(dynamicId, request_proto):
    '''自动爬塔
    '''
    argument = AutoPaTa4202_pb2.AutoPaTaRequest()
    argument.ParseFromString(request_proto)
    response = AutoPaTa4202_pb2.AutoPaTaResponse()
    
    characterId = argument.id
    data = tower.AutoPaTa4202(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        info = data.get('data',[])
        for _boundinfo in info:
            bound = response.paTaInfoList.add()
            bound.itemStr = _boundinfo
    return response.SerializeToString()

@nodeHandle
def TowerBattle_4203(dynamicId, request_proto):
    '''爬塔战斗
    '''
    argument = TowerBattle_4203_pb2.TowerBattleRequest()
    argument.ParseFromString(request_proto)
    response = TowerBattle_4203_pb2.TowerBattleResponse()
    fightResponse = battle_new703_pb2.FightResponse()
    characterId = argument.id
    data = tower.TowerBattle_4203(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    battlemsg = None
    if data.get('data',None):
        from twisted.internet import reactor
        responsedata = data.get('data')
        battle = responsedata.get('fight')
        bounds = responsedata.get('bound')
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


