#coding:utf8
'''
Created on 2012-5-21

@author: Administrator
'''
from app.scense.applyInterface import compound
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.item import GetAllHeChengInfos2114_pb2
from app.scense.protoFile.item import GetOneItemHeChengInfo2115_pb2
from app.scense.protoFile.item import Hecheng2116_pb2

@nodeHandle
def GetAllHeChengInfos_2114(dynamicId,request_proto):
    '''获取所有的合成信息
    '''
    argument = GetAllHeChengInfos2114_pb2.GetAllHechengInfosRequest()
    argument.ParseFromString(request_proto)
    response = GetAllHeChengInfos2114_pb2.GetAllHechengInfosResponse()
    characterId = argument.id
    
    result = compound.GetAllHeChengInfos2114(dynamicId, characterId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        data = result.get('data')
        equiplist = data.get('equiplist')
        gemlist = data.get('gemlist')
        for equip in equiplist:
            equipresponse = response.data.equiplist.add()
            equipresponse.itemId = equip['itemId']
            equipresponse.itemname = equip['itemname'].decode('utf8')
            equipresponse.level = equip['level']
        for gem in gemlist:
            gemresponse = response.data.gemlist.add()
            gemresponse.itemId = gem['itemId']
            gemresponse.itemname = gem['itemname'].decode('utf8')
            gemresponse.level = gem['level']
    return response.SerializeToString()
    
@nodeHandle
def GetOneItemHeChengInfo_2115(dynamicId,request_proto):
    '''获取某个物品的合成信息
    '''
    argument = GetOneItemHeChengInfo2115_pb2.GetOneItemHechengRequest()
    argument.ParseFromString(request_proto)
    response = GetOneItemHeChengInfo2115_pb2.GetOneItemHechengResponse()
    characterId = argument.id
    itemId = argument.itemId
    result = compound.GetOneItemHeChengInfo2115(dynamicId, characterId, itemId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        data = result.get('data')
        response.data.coinrequired = data.get('coinrequired',0)
        response.data.itemA = data.get('itemA',0)
        response.data.itemAcnt = data.get('itemAcnt',0)
        response.data.itemAGoal = data.get('itemAGoal',0)
        response.data.itemB = data.get('itemB',0)
        response.data.itemBcnt = data.get('itemBcnt',0)
        response.data.itemBGoal = data.get('itemBGoal',0)
        response.data.itemBound = data.get('itemBound',0)
    return response.SerializeToString()

@nodeHandle
def Hecheng_2116(dynamicId,request_proto):
    '''物品合成
    '''
    argument = Hecheng2116_pb2.HeChengRequest()
    argument.ParseFromString(request_proto)
    response = Hecheng2116_pb2.HeChengResponse()
    characterId = argument.id
    itemId = argument.itemId
    result = compound.Hecheng2116(dynamicId, characterId, itemId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    return response.SerializeToString()
    
    