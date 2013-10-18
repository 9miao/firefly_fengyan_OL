#coding:utf8
'''
Created on 2012-5-2

@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.applyInterface import meditation

@nodeHandle
def StartUpGuaJi_3200(dynamicId, request_proto):
    '''开始挂机'''
    from app.scense.protoFile.meditation import StartUpGuaJi3200_pb2
    argument = StartUpGuaJi3200_pb2.StartUpGuaJiRequest()
    argument.ParseFromString(request_proto)
    response = StartUpGuaJi3200_pb2.StartUpGuaJiResponse()
    
    characterId = argument.id
    data = meditation.StartUpGuaJi(dynamicId,characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def GetGuaJiInfo_3201(dynamicId,request_proto):
    '''获取挂机信息'''
    from app.scense.protoFile.meditation import GetGuaJiInfo3201_pb2
    argument = GetGuaJiInfo3201_pb2.GetGuaJiInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetGuaJiInfo3201_pb2.GetGuaJiInfoResponse()
    
    characterId = argument.id
    data = meditation.GetGuaJiInfo(characterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    response.expStr = data.get('expStr',u'0')
    response.zhanliStr = data.get('zhanliStr',u'0')
    response.gujiTime = data.get('gujiTime',0)
    return response.SerializeToString()

@nodeHandle
def CancelGuaJi_3202(dynamicId, request_proto):
    '''取消挂机'''
    from app.scense.protoFile.meditation import CancelGuaJi3202_pb2
    argument = CancelGuaJi3202_pb2.CancelGuajiRequest()
    argument.ParseFromString(request_proto)
    response = CancelGuaJi3202_pb2.CancelGuajiResponse()
    
    characterId = argument.id
    data = meditation.CancelGuaJi(characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()


