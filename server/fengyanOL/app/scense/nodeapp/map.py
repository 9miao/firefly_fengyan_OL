#coding:utf8
'''
Created on 2012-2-17

@author: lan
'''
from app.scense.applyInterface import map
from app.scense.core.guild.GuildManager import GuildManager
from app.scense.serverconfig.node import nodeHandle

from app.scense.protoFile.map import MapMessage_pb2

DEFAULTCOLOR = int("0xCCCC99",16)

@nodeHandle
def SceneMapInfos_2501(dynamicId, request_proto):
    '''获取大地图信息'''
    argument = MapMessage_pb2.SceneMapInfosRequest()
    argument.ParseFromString(request_proto)
    response = MapMessage_pb2.SceneMapInfosResponse()
    
    characterId = argument.id
    result = map.SceneMapInfos(dynamicId, characterId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    response.self_color = result.get('self_color',0)
    infos = result.get('infos',[])
    for _info in infos:
        mapinfo = response.infos.add()
        mapinfo.id = _info.get('cityid',0)
        mapinfo.tax = 0
        mapinfo.income = _info.get('reward',0)
        mapinfo.scene_name = _info.get('cityname','')
        mapinfo.union_name = _info.get('gname','')
        mapinfo.color = _info.get('color',0)
    return response.SerializeToString()

@nodeHandle
def InstanceMapInfos_2502(dynamicId, request_proto):
    '''获取副本组信息'''
    argument = MapMessage_pb2.InstanceMapInfosRequest()
    argument.ParseFromString(request_proto)
    response = MapMessage_pb2.InstanceMapInfosResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    result = map.InstanceMapInfos(dynamicId, characterId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    response.self_color = result.get('self_color',0)
    infos = result.get('infos',{})
    for key,_info in infos.items():
        mapinfo = response.infos.add()
        mapinfo.id = key
        mapinfo.once = _info.get('reward',0)
        mapinfo.income = _info.get('rewardAll',0)
        mapinfo.instance_name = _info.get('instancename','')
        mapinfo.union_name = _info.get('pname','')+"(%s)"%_info.get('gname','')
        guildId = _info.get('gid',0)
        color = 0
        if not guildId:
            if not _info.get('pid',0):
                color = 0
            else:
                color = DEFAULTCOLOR
        else:
            guild = GuildManager().getGuildById(guildId)
            if guild:
                color = guild.guildinfo.get('color',0)
            
        mapinfo.color = color
    return response.SerializeToString()
    
    