#coding:utf8
'''
Created on 2012-4-8

@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.applyInterface import award
from app.scense.protoFile.award import GetRewardInfo2410_pb2
from app.scense.protoFile.award import ObtainTodayAndEveryDayReward2411_pb2

@nodeHandle
def GetRewardInfo_2410(dynamicId, request_proto):
    '''获取奖励信息'''
    argument = GetRewardInfo2410_pb2.GetRewardInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetRewardInfo2410_pb2.GetRewardInfoResponse()
    
    characterId = argument.id
    awardtype = argument.r_type
    data = award.getAwardInfo(dynamicId, characterId, awardtype)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('rewardInfo',None):
        data = data.get('rewardInfo')
        try:
            response.rewardInfo.rewardDes = data.get('rewardDes',u'')
        except Exception:
            response.rewardInfo.rewardDes = data.get('rewardDes',u'').decode('utf8')
        response.rewardInfo.gold = data.get('gold',0)
        response.rewardInfo.zuan = data.get('zuan',0)
        response.rewardInfo.tili = data.get('tili',0)
        itemInfo = response.rewardInfo.itemInfo
        for _item in data.get('itemInfo',[]):
            itemresponse = itemInfo.add()
            _item.SerializationItemInfo(itemresponse)
    return response.SerializeToString()

@nodeHandle
def ReceiveAward_2411(dynamicId, request_proto):
    '''领取奖励'''
    argument = ObtainTodayAndEveryDayReward2411_pb2.ObtainTodayAndEveryDayRewardRequest()
    argument.ParseFromString(request_proto)
    response = ObtainTodayAndEveryDayReward2411_pb2.ObtainTodayAndEveryDayRewardResponse()
    
    characterId = argument.id
    awardtype = argument.type
    data = award.receiveAward(dynamicId, characterId, awardtype)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

