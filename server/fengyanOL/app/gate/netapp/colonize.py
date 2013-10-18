#coding:utf8
'''
Created on 2012-7-5

@author: Administrator
'''
from app.gate.serverconfig.localservice import localserviceHandle
from app.gate.core.VCharacterManager import VCharacterManager
from firefly.server.globalobject import GlobalObject

from app.gate.protoFile.instance import ColonizationBattle712_pb2

COLONIZE_POOL = []#正在被殖民的副本的列表

def bothhandle(resultdata,instanceId):
    '''延迟对象处理异常
    '''
    global COLONIZE_POOL
    COLONIZE_POOL.remove(instanceId)
    return resultdata

@localserviceHandle
def instanceColonizeBattle_712(key,dynamicId,request_proto):
    '''副本殖民的加锁处理，避免同时殖民同一个副本
    '''
    global COLONIZE_POOL
    argument = ColonizationBattle712_pb2.FightRequest()
    argument.ParseFromString(request_proto)
    response = ColonizationBattle712_pb2.FightResponse()
    
    dynamicId = dynamicId
    instanceid = argument.copyId #副本id（难度最小的那个）
    if instanceid in COLONIZE_POOL:
        response.result = False
        response.message = u'该副本正在进行殖民战斗'
        return response.SerializeToString()
    COLONIZE_POOL.append(instanceid)
    try:
        node = VCharacterManager().getNodeByClientId(dynamicId)
        d =  GlobalObject().root.callChild("scense_1000",key,dynamicId,request_proto)
        d.addBoth(bothhandle,instanceid)
        return d
    except :
        COLONIZE_POOL.remove(instanceid)
    
    