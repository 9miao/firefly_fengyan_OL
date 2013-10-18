#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import lodge
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.lodeg import getRestRoomInfo_pb2
from app.scense.protoFile.lodeg import restOperate_pb2

@nodeHandle
def getRestRoomInfo_406(dynamicId,request_proto):
    '''获取宿屋信息'''
    argument = getRestRoomInfo_pb2.getRestRoomInfoRequest()
    argument.ParseFromString(request_proto)
    response = getRestRoomInfo_pb2.getRestRoomInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    placeId = argument.placeId 
    data = lodge.getRestRoomInfo(dynamicId, characterId, placeId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        response.data.countList.nap = data.get('data')['nap']
        response.data.countList.lightSleep = data.get('data')['lightSleep']
        response.data.countList.peacefulSleep = data.get('data')['peacefulSleep']
        response.data.countList.spoor = data.get('data')['spoor']
        
    return response.SerializeToString()

@nodeHandle
def restOperate_407(dynamicId,request_proto):
    '''宿屋操作'''
    argument = restOperate_pb2.restOperateRequest()
    argument.ParseFromString(request_proto)
    response = restOperate_pb2.restOperateResponse()
    
    
    characterId = argument.id
    restType = argument.type
    payType = argument.payType
    payNum = argument.payNum
    data = lodge.restOperate(dynamicId, characterId, restType, payType, payNum)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        result = data.get('data')
        response.data.hp = result['hp']
        response.data.mp = result['mp']
        response.data.energy = result['energy']
        response.data.gold = result['gold']
        response.data.coupon = result['coupon']
        response.data.coin = result['coin']
        response.data.type = result['type']
        response.data.count = result['count']
    return response.SerializeToString() 
    