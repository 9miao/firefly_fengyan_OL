#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import playerInfo
from twisted.python import log
from app.scense.serverconfig.node import nodeHandle

from app.scense.protoFile.playerInfo import GetPlayerInfo_pb2
from app.scense.protoFile.playerInfo import addPoint_pb2
from app.scense.protoFile.playerInfo import GetOtherRoleInfo221_pb2
from app.scense.protoFile.playerInfo import FriendChangeState309_pb2
from app.scense.protoFile.playerInfo import SceneLoadComplete2600_pb2
from app.scense.protoFile.playerInfo import AddHuoLi224_pb2
from app.scense.core.PlayersManager import PlayersManager

@nodeHandle
def getPlayerInfo_201(dynamicId, request_proto):
    '''获取角色信息'''
    argument = GetPlayerInfo_pb2.GetPlayerInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetPlayerInfo_pb2.GetPlayerInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    
    data = playerInfo.getPlayerInfo(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        infos = data.get('data')
        playerinfo = infos.get('playerInfo',{})
        hasBuyCount = infos.get('hasBuyCount',0)
        for info in playerinfo.items():
            if info[0]=='appellation':
                for item in info[1].items():
                    setattr(response.data.appellation,item[0],item[1])
                continue
            if info[0]=='appellationList':
                for appellation in info[1]:
                    appellationInfo =response.data.appellationList.add()
                    for item in appellation.items():
                        setattr(appellationInfo,item[0],item[1])
                continue
            if info[0] =='corpsInfo':
                for item in info[1].items():
                    setattr(response.data.corpsInfo,item[0],item[1])
                continue
            try:
                setattr(response.data,info[0],info[1])
            except Exception:
                log.err( info)
                raise "attr error",info
        response.buyCount = hasBuyCount
                
    return response.SerializeToString()

@nodeHandle
def addPoint_1101(dynamicId, request_proto):
    '''角色加点'''
    argument = addPoint_pb2.addPointRequest()
    argument.ParseFromString(request_proto)
    response = addPoint_pb2.addPointResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    manualStr = argument.manualStr
    manualVit = argument.manualVit
    manualDex = argument.manualDex
    
    data = playerInfo.addPoint(dynamicId, characterId, manualStr, manualVit, manualDex)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        result = data.get('data')
        response.data.sparePoint = result['sparePoint']
        response.data.manualStr = result['manualStr']
        response.data.manualVit = result['manualVit']
        response.data.manualDex = result['manualDex']
    return response.SerializeToString()

@nodeHandle
def GetOtherRoleInfo_221(dynamicId, request_proto):
    '''获取其他玩家的信息
    '''
    argument = GetOtherRoleInfo221_pb2.GetOtherRoleInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetOtherRoleInfo221_pb2.GetOtherRoleInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    roleId = argument.roleId
    data = playerInfo.GetOtherRoleInfo(dynamicId, characterId, roleId)
    dataInfo = data.get('data',{})
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if dataInfo.get('playerInfo',None):
        infos = dataInfo.get('playerInfo')
        for info in infos.items():
            if info[0]=='appellation':
                for item in info[1].items():
                    setattr(response.data.otherRoleInfo.appellation,item[0],item[1])
                continue
            if info[0]=='appellationList':
                for appellation in info[1]:
                    appellationInfo =response.data.otherRoleInfo.appellationList.add()
                    for item in appellation.items():
                        setattr(appellationInfo,item[0],item[1])
                continue
            if info[0]=='corpsInfo':
                for item in info[1].items():
                    setattr(response.data.otherRoleInfo.corpsInfo,item[0],item[1])
                continue
            try:
                setattr(response.data.otherRoleInfo,info[0],info[1])
            except Exception,e:
                raise str(e)

    if dataInfo.get('packageItemInfo',None):
        _packagedata = dataInfo.get('packageItemInfo')
        for _item in _packagedata:
            packageItemInfo = response.data.otherRoleItem.add()
            if not _item:
                continue
            packageItemInfo.position = _item['position']
            _item['itemComponent'].SerializationItemInfo(packageItemInfo.itemInfo)
    return response.SerializeToString()

@nodeHandle
def updatePlayerSpirit_309(dynamicId, request_proto):
    '''修改角色心情
    '''
    argument = FriendChangeState309_pb2.FriendChangeStateRequest()
    argument.ParseFromString(request_proto)
    response = FriendChangeState309_pb2.FriendChangeStateResponse()
    
    id = argument.id
    content = argument.content
    data=playerInfo.updateSpirit(id, content)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    response.content=content.decode('utf8')
    return response.SerializeToString()

@nodeHandle
def SceneLoadComplete_2600(dynamicId, request_proto):
    '''场景加载完成
    '''
    argument = SceneLoadComplete2600_pb2.SceneLoadCompleteRequest()
    argument.ParseFromString(request_proto)
    
    characterId = argument.id
    playerInfo.initplayerInfo(dynamicId, characterId)

@nodeHandle
def dropPlayerByid_999990(id):
    '''根据角色id删除角色'''
    PlayersManager().dropPlayerByID(id)
    
@nodeHandle
def getPlayerByid_999991(id):
    '''根据角色id删除角色'''
    import cPickle
    player=PlayersManager().getPlayerByID(id)
    return cPickle.dumps(player)

@nodeHandle
def AddHuoLi_224(dynamicId, request_proto):
    '''增加体力值'''
    argument = AddHuoLi224_pb2.AddHuoLiRequest()
    argument.ParseFromString(request_proto)
    response = AddHuoLi224_pb2.AddHuoLiResponse()
    
    pid=argument.id#角色id
    result = playerInfo.AddHuoLi(dynamicId,pid)

    response.result = result.get('result',False)
    response.message = result.get('message',u'')
    response.failType = result.get('failType',0)
    return response.SerializeToString()



