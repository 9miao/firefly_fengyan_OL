#coding:utf8
'''
Created on 2012-6-29

@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.applyInterface import arena
from app.scense.protoFile.arena import GetJingJiInfo3700_pb2
from app.scense.protoFile.arena import AddJingJiCount3703_pb2
from app.scense.protoFile.arena import ArenaBattle_3704_pb2
from app.scense.protoFile.arena import JingJiCleanCD_2705_pb2
from app.scense.protoFile.fight import battle_new703_pb2
from app.scense.netInterface.pushObjectNetInterface import pushApplyMessage

@nodeHandle
def GetJingJiInfo_3700(dynamicId, request_proto):
    '''获取竞技场信息
    '''
    argument = GetJingJiInfo3700_pb2.GetJingJiRequest()
    argument.ParseFromString(request_proto)
    response = GetJingJiInfo3700_pb2.GetJingJiResponse()
    
    characterId = argument.id
    data = arena.GetJingJiInfo3700(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        info = data.get('data')
        response.jingjiInfo.rankInfo = info.get('jiangli',0)
        response.jingjiInfo.jifen = info.get('jifen',0)
        response.jingjiInfo.weiwang = info.get('weiwang',0)
        response.jingjiInfo.rank = info.get('paiming',0)
        response.jingjiInfo.liansheng = info.get('liansheng',0)
        response.jingjiInfo.tzCount = info.get('surplustimes',0)
        response.jingjiInfo.addCount = info.get('addCount',0)
        response.jingjiInfo.reqCoin = info.get('reqCoin',0)
        response.jingjiInfo.obtainTime = info.get('obtainTime',0)
        battleInfoList = response.jingjiInfo.battleInfoList
        for _battleinfo in info.get('battleInfoList',[]):
            battleinfo = battleInfoList.add()
            battleinfo.battleStr = _battleinfo
        duishoulist = response.jingjiInfo.drList
        for duishou in info.get('drList',[]):
            duishouinfo = duishoulist.add()
            duishouinfo.bId = duishou['characterId']
            duishouinfo.bName = duishou['nickname']
            duishouinfo.bLevel = duishou['level']
            duishouinfo.profession = duishou['profession']
            duishouinfo.bRank = duishou['ranking']
    return response.SerializeToString()
    

@nodeHandle
def AddJingJiCount_3703(dynamicId, request_proto):
    '''添加竞技场次数
    '''
    argument = AddJingJiCount3703_pb2.AddJingJiCountRequest()
    argument.ParseFromString(request_proto)
    response = AddJingJiCount3703_pb2.AddJingJiCountResponse()
    
    characterId = argument.id
    data = arena.AddJingJiCount3703(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        info = data.get('data',0)
        response.bCount = info.get('bCount',0)
        response.addCount = info.get('addCount',0)
        response.reqCoin = info.get('reqCoin',0)
    return response.SerializeToString()
    
@nodeHandle
def ArenaBattle_3704(dynamicId, request_proto):
    '''竞技场战斗
    '''
    argument = ArenaBattle_3704_pb2.ArenaBattleRequest()
    argument.ParseFromString(request_proto)
    response = ArenaBattle_3704_pb2.FightResponse()
    fightResponse = battle_new703_pb2.FightResponse()
    
    characterId = argument.id
    tocharacterId = argument.tiID
    data = arena.ArenaBattle_3704(dynamicId, characterId, tocharacterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        from twisted.internet import reactor
        responsedata = data.get('data')
        battle = responsedata.get('fight')
        bounds = data.get('bound')
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
        setData = fightResponse.data.setData.add()
        setData.id = characterId
        setData.coinBonus = bounds.get('coin',0)
        setData.popularity = bounds.get('popularity',0)
        setData.name = bounds.get('name',u'')
        battlemsg = fightResponse.SerializeToString()
        reactor.callLater(1,pushApplyMessage,711,battlemsg,[dynamicId])
    return response.SerializeToString()
    
@nodeHandle
def JingJiCleanCD_3705(dynamicId, request_proto):
    '''
    '''
    argument = JingJiCleanCD_2705_pb2.JingjiCleanCDRequest()
    argument.ParseFromString(request_proto)
    response = JingJiCleanCD_2705_pb2.JingjiCleanCDResponse()
    
    characterId = argument.id
    data = arena.JingJiCleanCD_2705(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()
    
    