#coding:utf8
'''
Created on 2012-8-9

@author: Administrator
'''
from app.gate.serverconfig.localservice import localserviceHandle
from app.gate.app import playerinfo
from app.gate.protoFile.playerInfo import GetOtherRoleInfo221_pb2

@localserviceHandle
def GetOtherPlayerInfo_221(key,dynamicId,request_proto):
    '''获取其他角色的信息
    '''
    
    argument = GetOtherRoleInfo221_pb2.GetOtherRoleInfoRequest()
    argument.ParseFromString(request_proto)
    pid = argument.id
    tid = argument.roleId
    dd =  playerinfo.getOtherPlayerInfo(dynamicId, pid, tid, request_proto)
    return dd