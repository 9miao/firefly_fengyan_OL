#coding:utf8
'''
Created on 2012-8-9

@author: Administrator
'''
from app.gate.serverconfig.localservice import localserviceHandle
from firefly.server.globalobject import GlobalObject
from app.gate.app import zuidui
from app.gate.protoFile.zuidui import CreateZuDui4301_pb2,JoinDuiWu4303_pb2

@localserviceHandle
def CreateZuDui_4301(key,dynamicId,request_proto):
    '''创建队伍
    '''
    argument = CreateZuDui4301_pb2.CreateZuDuiRequest()
    argument.ParseFromString(request_proto)
#    response = CreateZuDui4301_pb2.CreateZuDuiResponse()
    
    dynamicId = dynamicId
    pid = argument.id
    pos = argument.pos
    gkType = argument.gkType
    dd=zuidui.CreateZuDui(dynamicId, pid, pos, gkType)
    if not dd:
        return
    return dd


@localserviceHandle
def JoinDuiWu_4303(key,dynamicId,request_proto):
    '''加入队伍
    '''
    argument = JoinDuiWu4303_pb2.JoinDuiWuRequest()
    argument.ParseFromString(request_proto)
#    response = CreateZuDui4301_pb2.CreateZuDuiResponse()
    
    dynamicId = dynamicId
    pid = argument.id
    pos = argument.pos
    dwId = argument.dwId
    dd=zuidui.JoinDuiWu(dynamicId, pid, pos, dwId)
    if not dd:
        return
    return dd
    

@localserviceHandle
def a_4300(key,dynamicId,request_proto):
    return GlobalObject().root.callChild(9999,key,dynamicId,request_proto)

@localserviceHandle
def a_4302(key,dynamicId,request_proto):
    return GlobalObject().root.callChild(9999,key,dynamicId,request_proto)

@localserviceHandle
def a_4304(key,dynamicId,request_proto):
    return GlobalObject().root.callChild(9999,key,dynamicId,request_proto)

@localserviceHandle
def a_4305(key,dynamicId,request_proto):
    return GlobalObject().root.callChild(9999,key,dynamicId,request_proto)

@localserviceHandle
def a_4306(key,dynamicId,request_proto):
    return GlobalObject().root.callChild(9999,key,dynamicId,request_proto)

@localserviceHandle
def a_4308(key,dynamicId,request_proto):
    return GlobalObject().root.callChild(9999,key,dynamicId,request_proto)


