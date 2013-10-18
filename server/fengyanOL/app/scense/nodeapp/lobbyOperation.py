#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import lobbyOperation
from app.scense.serverconfig.node import nodeHandle

@nodeHandle
def lobbyOperate_401(dynamicId,request_proto):
    '''
          大厅操作：修炼、卖艺
    @param type: 操作类型：1、训练   2、卖艺
    @param duration: 持续时间
        训练得到的经验=[(自身等级+1)*33]^1.15*训练小时数
        训练消耗的铜币=[(自身等级+1)*44]^1.15*训练小时数
    '''
    from app.scense.protoFile.lobby import lobbyOperate_pb2
    arguments = lobbyOperate_pb2.lobbyOperateRequest()
    arguments.ParseFromString(request_proto)
    response = lobbyOperate_pb2.lobbyOperateResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id
    operaType = arguments.type
    duration = arguments.duration
    data = lobbyOperation.lobbyOperate(dynamicId, characterId, operaType, duration)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        result = data.get('data')
        response.data.status = result['status']
        response.data.bonusCount = result['bonusCount']
        response.data.startTime = result['startTime']
        response.data.finishTime = result['finishTime']
        response.data.duration = result['duration']
    return response.SerializeToString()

def terminateLobbyOperation(dynamicId,request_proto):########没有
    '''
          中断大厅操作
    @param type: 操作类型：1、训练   2、卖艺
    '''
    from app.scense.protoFile.lobby import terminateLobbyOperation_pb2
    arguments = terminateLobbyOperation_pb2.terminateLobbyOperationRequest()
    arguments.ParseFromString(request_proto)
    response = terminateLobbyOperation_pb2.terminateLobbyOperationResponse()
    
    
    characterId=arguments.id
    operaType= arguments.type
    data = lobbyOperation.terminateLobbyOperation(dynamicId, characterId, operaType)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        result = data.get('data')
        response.data.bonus = result['bonus']
        response.data.level = result['level']    
    return response.SerializeToString()
