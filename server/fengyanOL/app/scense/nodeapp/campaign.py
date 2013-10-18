#coding:utf8
'''
Created on 2012-9-11

@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.applyInterface import campaign
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.protoFile.campaign import GetCityListInfo4402_pb2,GetGroupLingDiInfo4400_pb2,\
ObtainJiangLi4401_pb2,GroupPK4403_pb2,GetXuYuanInfo4404_pb2,UseXingYun4405_pb2,\
GetBattleInfo4406_pb2,JoinBattle4407_pb2,CancelBattle4409_pb2,AutoJoinBattle4408_pb2

@nodeHandle
def GetGroupLingDiInfo_4400(dynamicId, request_proto):
    '''获取国领地信息
    '''
    argument = GetGroupLingDiInfo4400_pb2.GetGroupLingDiInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetGroupLingDiInfo4400_pb2.GetGroupLingDiInfoResponse()
    characterId = argument.id
    data = campaign.GetGroupLingDiInfo4400(dynamicId, characterId)
    
    response.result = data.get('result',False)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    response.message = msg
    if data.get('data',None):
        LingdiInfo = data.get('data')
        response.groupInfo.ldType = LingdiInfo['ldType']
        response.groupInfo.groupName = LingdiInfo['groupName']
        response.groupInfo.groupLevel = LingdiInfo['groupLevel']
        response.groupInfo.groupLeader = LingdiInfo['groupLeader']
        response.groupInfo.obtainJL = LingdiInfo['obtainJL']
        response.groupInfo.icon = LingdiInfo['icon']
        response.groupInfo.battleInfo.extend(LingdiInfo['battleInfo'])
        response.groupInfo.battleTime = LingdiInfo['battleTime']
    return response.SerializeToString()

@nodeHandle
def ObtainJiangLi_4401(dynamicId, request_proto):
    '''获取国领地奖励
    '''
    argument = ObtainJiangLi4401_pb2.ObtainJiangLiRequest()
    argument.ParseFromString(request_proto)
    response = ObtainJiangLi4401_pb2.ObtainJiangLiResponse()
    characterId = argument.id
    data = campaign.GetCityListInfo4402(dynamicId, characterId)
    
    response.result = data.get('result',False)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    response.message = msg
    return response.SerializeToString()


@nodeHandle
def GetCityListInfo_4402(dynamicId, request_proto):
    '''获取城镇征战列表
    '''
    argument = GetCityListInfo4402_pb2.GetCityListInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetCityListInfo4402_pb2.GetCityListInfoResponse()
    characterId = argument.id
    data = campaign.GetCityListInfo4402(dynamicId, characterId)
    
    response.result = data.get('result',False)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    response.message = msg
    if data.get('data',None):
        cityinfos = data.get('data')
        for city in cityinfos:
            cityinof = response.cityInfo.add()
            cityinof.lzName = city.get('kimoriname')
            cityinof.lzIcon = city.get('kimoriemblem')
            cityinof.tzName = city.get('siegename')
            cityinof.tzIcon = city.get('siegeemblem')
            cityinof.btnState = city.get('fortressstatus')
    return response.SerializeToString()
    

@nodeHandle
def GroupPK_4403(dynamicId, request_proto):
    '''国战申请
    '''
    argument = GroupPK4403_pb2.GroupPKRequest()
    argument.ParseFromString(request_proto)
    response = GroupPK4403_pb2.GroupPKResponse()
    characterId = argument.id
    pkId = argument.pkId
    data = campaign.GroupPK4403(dynamicId, characterId, pkId)
    
    response.result = data.get('result',False)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    response.message = msg
    return response.SerializeToString()

@nodeHandle
def GetXuYuanInfo_4404(dynamicId, request_proto):
    '''获取许愿信息
    '''
    argument = GetXuYuanInfo4404_pb2.GetXuYuanInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetXuYuanInfo4404_pb2.GetXuYuanInfoResponse()
    characterId = argument.id
    data = campaign.GetXuYuanInfo4404(dynamicId, characterId)
    
    response.result = data.get('result',False)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    response.message = msg
    if data.get('data',None):
        xuyuanInfos = data.get('data')
        response.xuYuanInfo.xyValue = xuyuanInfos.get('xyValue',0)
        usedInfo = response.xuYuanInfo.usedInfo
        for xuyuan in xuyuanInfos.get('cliffordLog',{}):
            xuyuanResponse = usedInfo.add()
            xuyuanResponse.name = xuyuan.get('name','')
            xuyuanResponse.type = xuyuan.get('type','')
    return response.SerializeToString()

@nodeHandle
def UseXingYun_4405(dynamicId, request_proto):
    '''使用幸运许愿
    '''
    argument = UseXingYun4405_pb2.UseXingYunRequest()
    argument.ParseFromString(request_proto)
    response = UseXingYun4405_pb2.UseXingYunResponse()
    characterId = argument.id
    usetype = argument.type
    data = campaign.UseXingYun4405(dynamicId, characterId, usetype)
    
    response.result = data.get('result',False)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    response.message = msg
    return response.SerializeToString()

@nodeHandle
def GetBattleInfo_4406(dynamicId, request_proto):
    '''获取国战的信息
    '''
    argument = GetBattleInfo4406_pb2.GetBattleInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetBattleInfo4406_pb2.GetBattleInfoResponse()
    characterId = argument.id
    data = campaign.GetBattleInfo4406(dynamicId, characterId)
    
    response.result = data.get('result',False)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    response.message = msg
    if data.get('data',None):
        BattleInfos = data.get('data')
        dataResponse = response.groupBattleInfo
        dataResponse.roundCount = BattleInfos.get('roundCount')
        dataResponse.remainTime = BattleInfos.get('remainTime')
        dataResponse.jishaCount = BattleInfos.get('jishaCount')
        dataResponse.failCount = BattleInfos.get('failCount')
        dataResponse.obtainCoin = BattleInfos.get('obtainCoin')
        dataResponse.obtainSw   = BattleInfos.get('obtainSw')
        
        battleListResponse = dataResponse.battleInfoList
        for battleInfo in BattleInfos['battleInfoList']:
            battleResponse = battleListResponse.add()
            battleResponse.roleId1 = battleInfo.get('roleId1')
            battleResponse.roleName1 = battleInfo.get('roleName1')
            battleResponse.roleId2 = battleInfo.get('roleId2')
            battleResponse.roleName2 = battleInfo.get('roleName2')
            battleResponse.sucObCoin = battleInfo.get('sucObCoin')
            
        guild1Info = BattleInfos['group1Info']
        group1InfoResponse = dataResponse.group1Info
        group1InfoResponse.groupName = guild1Info.get('groupName',u'')
        group1InfoResponse.groupCount = guild1Info.get('groupCount',0)
        group1InfoResponse.icon = guild1Info.get('icon',0)
        group1MemberListResponse = group1InfoResponse.groupMember
        for role in guild1Info.get('groupMember',[]):
            roleResponse = group1MemberListResponse.add()
            roleResponse.memberId = role['memberId']
            roleResponse.memberName = role['memberName']
            
        guild2Info = BattleInfos['group2Info']
        group2InfoResponse = dataResponse.group2Info
        group2InfoResponse.groupName = guild2Info.get('groupName',u'')
        group2InfoResponse.groupCount = guild2Info.get('groupCount',0)
        group2InfoResponse.icon = guild2Info.get('icon',0)
        group2MemberListResponse = group2InfoResponse.groupMember
        for role in guild2Info.get('groupMember',[]):
            roleResponse = group2MemberListResponse.add()
            roleResponse.memberId = role['memberId']
            roleResponse.memberName = role['memberName']
            
    return response.SerializeToString()

@nodeHandle
def Participate_4407(dynamicId, request_proto):
    '''角色参战
    '''
    argument = JoinBattle4407_pb2.JoinBattleRequest()
    argument.ParseFromString(request_proto)
    response = JoinBattle4407_pb2.JoinBattleResponse()
    characterId = argument.id
    data = campaign.Participate4407(dynamicId, characterId)
    
    response.result = data.get('result',False)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    response.message = msg
    return response.SerializeToString()

@nodeHandle
def AutoJoinBattle_4408(dynamicId, request_proto):
    '''自动参战或取消自动参战
    '''
    argument = AutoJoinBattle4408_pb2.AutoJoinBattleRequest()
    argument.ParseFromString(request_proto)
    response = AutoJoinBattle4408_pb2.AutoJoinBattleResponse()
    characterId = argument.id
    autoJoinFlag = argument.autoJoinFlag
    data = campaign.AutoJoinBattle4408(dynamicId, characterId, autoJoinFlag)
    
    response.result = data.get('result',False)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    response.message = msg
    return response.SerializeToString()

@nodeHandle
def CancelBattle_4409(dynamicId, request_proto):
    '''角色参战
    '''
    argument = CancelBattle4409_pb2.CancelBattleRequest()
    argument.ParseFromString(request_proto)
    response = CancelBattle4409_pb2.CancelBattleResponse()
    characterId = argument.id
    data = campaign.CancelParticipate4409(dynamicId, characterId)
    
    response.result = data.get('result',False)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    response.message = msg
    return response.SerializeToString()




    
    