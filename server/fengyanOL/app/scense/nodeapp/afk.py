#coding:utf8
'''
Created on 2012-4-12

@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.applyInterface import afk
from app.scense.protoFile.afk import GetWaJueInfo2800_pb2
from app.scense.protoFile.afk import StartWaJue2801_pb2
from app.scense.protoFile.afk import NowSuccWaJue2804_pb2
from app.scense.protoFile.afk import DianShiChengJi2802_pb2
from app.scense.protoFile.afk import LevelUpSpeedWaJue2803_pb2
from app.scense.protoFile.afk import GetAramListInfo2805_pb2
from app.scense.protoFile.afk import AramStartXunLian2806_pb2
from app.scense.protoFile.afk import SaoDang3205_pb2
from app.scense.protoFile.afk import AramNowSuccWaJue2809_pb2
from app.scense.protoFile.afk import AramJiaJiXunLian2807_pb2
from app.scense.protoFile.afk import AramLevelUpSpeedWaJue2808_pb2

@nodeHandle
def GetWaJueInfo_2800(dynamicId, request_proto):
    argument = GetWaJueInfo2800_pb2.GetWaJueInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetWaJueInfo2800_pb2.GetWaJueInfoResponse()
    
    characterId = argument.id
    data = afk.GetWaJueInfo(characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        info = data.get('data')
        response.remainTime = info.get('remainTime',0)
        response.runningTask = info.get('runningTask',False)
        response.sptimes = info.get('sptimes',0)
        response.coinbound = info.get('coinbound',0)
        response.goldreq = info.get('goldreq',0)
    return response.SerializeToString()

@nodeHandle
def StartWaJue_2801(dynamicId, request_proto):
    argument = StartWaJue2801_pb2.StartWaJueRequest()
    argument.ParseFromString(request_proto)
    response = StartWaJue2801_pb2.StartWaJueResponse()
    
    characterId = argument.id
    miningtype = argument.type
    data = afk.StartWaJue(characterId, miningtype)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def DianShiChengJin_2802(dynamicId, request_proto):
    argument = DianShiChengJi2802_pb2.DianShiChengJiRequest()
    argument.ParseFromString(request_proto)
    response = DianShiChengJi2802_pb2.DianShiChengJiResponse()
    
    characterId = argument.id
    data = afk.DianShiChengJin(characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def LevelUpSpeedWaJue_2803(dynamicId, request_proto):
    argument = LevelUpSpeedWaJue2803_pb2.LevelUpSpeedWaJueRequest()
    argument.ParseFromString(request_proto)
    response = LevelUpSpeedWaJue2803_pb2.LevelUpSpeedWaJueResponse()
    
    characterId = argument.id
    mtype = argument.type
    data = afk.LevelUpSpeedWaJue(characterId, mtype)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def NowSuccWaJue_2804(dynamicId, request_proto):
    argument = NowSuccWaJue2804_pb2.NowSuccWaJueRequest()
    argument.ParseFromString(request_proto)
    response = NowSuccWaJue2804_pb2.NowSuccWaJueResponse()
    
    characterId = argument.id
    data = afk.NowSuccWaJue(characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def GetAramListInfo_2805(dynamicId, request_proto):
    argument = GetAramListInfo2805_pb2.GetAramListInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetAramListInfo2805_pb2.GetAramListInfoResponse()
    
    characterId = argument.id
    data = afk.GetAramListInfo(characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        info = data.get('data')
        response.roleRunningFlag = info.get('roleRunningFlag',False)
        response.roleRunTime = info.get('roleRunTime',0)
        response.sptimes = info.get('sptimes',0)
        response.expbound = info.get('expbound',0)
        response.goldreq = info.get('goldreq',0)
        petAramInfo = response.petAramInfo
        for pet in info.get('petAramInfo',[]):
            petInfo = petAramInfo.add()
            petInfo.petId = pet.get('petId')
            petInfo.resPetId = pet.get('resPetId')
            petInfo.petName = pet.get('petName')
            petInfo.petLevel = pet.get('petLevel')
            petInfo.icon = pet.get('icon')
            petInfo.type = pet.get('type')
            petInfo.runningFlag = pet.get('runningFlag')
            petInfo.remainTime = pet.get('remainTime')
    return response.SerializeToString()

@nodeHandle
def AramStartXunLian_2806(dynamicId, request_proto):
    argument = AramStartXunLian2806_pb2.AramStartXunLianRequest()
    argument.ParseFromString(request_proto)
    response = AramStartXunLian2806_pb2.AramStartXunLianResponse()
    
    characterId = argument.id
    ttype = argument.type
    funType = argument.funType
    funId = argument.funId
    data = afk.AramStartXunLian(characterId, ttype, funType, funId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def AramJiaJiXunLian_2807(dynamicId, request_proto):
    argument = AramJiaJiXunLian2807_pb2.JiaJiXunLianRequest()
    argument.ParseFromString(request_proto)
    response = AramJiaJiXunLian2807_pb2.JiaJiXunLianResponse()
    
    characterId = argument.id
    ptype = argument.type
    funId = argument.funId
    data = afk.AramJiaJiXunLian(characterId, ptype, funId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()
    

@nodeHandle
def AramStartXunLian_2808(dynamicId, request_proto):
    argument = AramLevelUpSpeedWaJue2808_pb2.AramLevelUpSpeedWaJueRequest()
    argument.ParseFromString(request_proto)
    response = AramLevelUpSpeedWaJue2808_pb2.AramLevelUpSpeedWaJueResponse()
    
    characterId = argument.id
    tmode = argument.type
    funType = argument.funType
    funId = argument.funId
    data = afk.AramLevelUpSpeedXunLian(characterId, tmode, funType, funId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def AramNowSuccXunLian_2809(dynamicId, request_proto):
    argument = AramNowSuccWaJue2809_pb2.AramNowSuccWaJueRequest()
    argument.ParseFromString(request_proto)
    response = AramNowSuccWaJue2809_pb2.AramNowSuccWaJueResponse()
    
    characterId = argument.id
    ptype = argument.type
    funId = argument.funId
    data = afk.AramNowSuccXunLian(characterId, ptype, funId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def SaoDang_3205(dynamicId, request_proto):
    '''扫荡
    '''
    argument = SaoDang3205_pb2.SaoDangRequest()
    argument.ParseFromString(request_proto)
    response = SaoDang3205_pb2.SaoDangResponse()
    characterId = argument.id
    fubenId = argument.fubenId
    sdType = argument.sdType
    sdRound = argument.sdRound
    data = afk.Saodang(characterId, fubenId, sdType, sdRound)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        msglist = data.get('data')
        for msg in msglist:
            baInfo = response.baInfoList.add()
            baInfo.baDesStr = msg
    return response.SerializeToString()
    


