#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import team
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.team import invitedGroup_pb2
from app.scense.protoFile.team import agreeGroup_pb2
from app.scense.protoFile.team import rejectGroup_pb2

@nodeHandle
def invitedGroup_902(dynamicId,request_proto):
    '''邀请组队'''
    argument = invitedGroup_pb2.invitedGroupRequest()
    argument.ParseFromString(request_proto)
    response = invitedGroup_pb2.invitedGroupResponse()
    
    dynamicId = dynamicId
    id = argument.id
    tid = argument.tid
    
    data = team.invitedGroup(dynamicId, id, tid)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        pass
    return response.SerializeToString()

@nodeHandle
def agreeGroup_903(dynamicId,request_proto):
    '''同意组队'''
    argument = agreeGroup_pb2.agreeGroupRequest()
    argument.ParseFromString(request_proto)
    response = agreeGroup_pb2.agreeGroupResponse()
    
    dynamicId = dynamicId
    id = argument.id
    tid = argument.tid
    
    data = team.agreeGroup(dynamicId, id, tid)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        pass
    return response.SerializeToString()

@nodeHandle
def rejectGroup_904(dynamicId,request_proto):
    '''拒绝组队'''
    argument = rejectGroup_pb2.rejectGroupRequest()
    argument.ParseFromString(request_proto)
    response = rejectGroup_pb2.rejectGroupResponse()
    
    
    id,tid = (argument.id ,argument.toid)
    data = team.rejectGroup(dynamicId, id, tid)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        pass
    return response.SerializeToString()
    