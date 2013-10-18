#coding:utf8
'''
Created on 2012-2-27

@author: sean_lan
'''
from app.gate.serverconfig.localservice import localserviceHandle
from app.gate.app import login
from app.gate.utils.dbopera import dbnamepool
from app.gate.utils.dbopera.db_language_login import getLanguageStr

from app.gate.protoFile.login import loginToServer101_pb2
from app.gate.protoFile.login import activeNewPlayer102_pb2
from app.gate.protoFile.login import roleLogin_pb2
from app.gate.protoFile.login import deleteRole_pb2
from app.gate.protoFile.login import getRandomName_pb2
from app.gate.protoFile.login import enterPlace_pb2
from app.gate.protoFile.instance import enterInstance_pb2
from app.gate.protoFile.instance import  escInstance_pb2

PROFESSIONID = {1:u'战士',
                2:u'法师',
                3:u'游侠',
                4:u'牧师'
                }

@localserviceHandle
def loginToServer_101(key,dynamicId,request_proto):
    argument = loginToServer101_pb2.loginToServerRequest()
    argument.ParseFromString(request_proto)
    response = loginToServer101_pb2.loginToServerResponse()
    
    dynamicId = dynamicId
    username = argument.user
    password = argument.password
    if not password:
        data = login.loginToServer_new(dynamicId, username)
    else:
        data = login.loginToServer(dynamicId, username, password)
    response.result = data.get('result',False)
    msgtag = data.get('message','')
    response.message = getLanguageStr(msgtag)
    if data.get('data',None):
        data = data.get('data')
        response.data.userId = data.get('userId',0)
        response.data.hasRole = data.get('hasRole',False)
        response.data.defaultId = data.get('defaultId',0)
    return response.SerializeToString()

@localserviceHandle
def activeNewPlayer_102(key,dynamicId,request_proto):
    '''创建角色
    '''
    argument = activeNewPlayer102_pb2.activeNewPlayerRequest()
    argument.ParseFromString(request_proto)
    response = activeNewPlayer102_pb2.activeNewPlayerResponse()
    
    dynamicId = dynamicId
    userId = argument.userId
    nickName = argument.nickName
    profession = argument.profession
    data = login.activeNewPlayer(dynamicId, userId, nickName, profession)
    response.result = data.get('result',False)
    msgtag = data.get('message','')
    response.message = getLanguageStr(msgtag)
    if data.get('data',None):
        data = data.get('data')
        response.data.userId = data.get('userId',0)
        response.data.newCharacterId = data.get('newCharacterId',0)
    return response.SerializeToString()

@localserviceHandle
def roleLogin_103(key,dynamicId, request_proto):
    '''角色登陆'''
    argument = roleLogin_pb2.roleLoginRequest()
    argument.ParseFromString(request_proto)
    response = roleLogin_pb2.roleLoginResponse()
    
    userId = argument.userId
    characterId = argument.id
    data = login.roleLogin(dynamicId, userId, characterId)
    response.result = data.get('result',False)
    msgtag = data.get('message','')
    response.message = getLanguageStr(msgtag)
    if data.get('data',None):
        response.data.placeId = data['data'].get('placeId',1000)
    return response.SerializeToString()

@localserviceHandle
def deleteRole_104(key,dynamicId, request_proto):
    '''删除角色'''
    argument = deleteRole_pb2.deleteRoleRequest()
    argument.ParseFromString(request_proto)
    response = deleteRole_pb2.deleteRoleResponse()
    
    userId = argument.userId
    characterId = argument.id
    password = argument.password
    data = login.deleteRole(dynamicId, userId, characterId,password)
    
    response.result = data.get('result',False)
    msgtag = data.get('message','')
    response.message = getLanguageStr(msgtag)
    if data.get('data',None):
        response.data.len = len(data.get('data',[]))
        for character in data['data'].get('UserCharacterListInfo',[]):
            characterInfo = response.data.character.add()
            characterInfo.id = character.get('id',0)
            characterInfo.nicName = character.get('nickname',u'')
            characterInfo.level = character.get('level',1)
            professionId = character.get('profession',1)
            professionName = PROFESSIONID.get(professionId,u'新手')
            characterInfo.profession = professionName
            characterInfo.roletype = character.get('viptype',1)
    return response.SerializeToString()


@localserviceHandle
def getRandomName_1606(key,dynamicId,request_proto):
    response = getRandomName_pb2.getRandomNameResponse()
    data = dbnamepool.getRandomName()
    response.result = True
    response.message = ''
    response.name = data
    return response.SerializeToString()


def SerializePartialEnterScene(result,response):
    '''序列化进入场景的返回消息
    '''
    response.result = result.get('result',False)
    response.message = result.get('message','')
    data = result.get('data',None)
    if data:
        response.data.placeId = data.get('placeId')
    return response.SerializeToString()

@localserviceHandle
def enterScene_601(key,dynamicId,request_proto):
    '''进入公共场景'''
    argument = enterPlace_pb2.enterPlaceRequest()
    argument.ParseFromString(request_proto)
    response = enterPlace_pb2.enterPlaceResponse()
    characterId = argument.id
    placeId = argument.placeId
    force = argument.force
    dd = login.enterScene(dynamicId, characterId, placeId, force)
    if not dd:
        return
    dd.addCallback(SerializePartialEnterScene,response)
    return dd
    
def SerializePartialEnterFam(result,response):
    '''序列化进入场景的返回消息'''
    response.result = result.get('result',False)
    response.message = result.get('message','')
    data = result.get('data',None)
    if data:
        response.data.placeId = data.get('placeId',-1)
    return response.SerializeToString()

@localserviceHandle
def enterInstance_1501(key,dynamicId,request_proto):
    '''进入副本'''
    argument = enterInstance_pb2.enterInstanceRequest()
    argument.ParseFromString(request_proto)
    response = enterPlace_pb2.enterPlaceResponse()
    characterId=argument.id #用户角色Id
    instanceId=argument.InstanceId #副本Id
    dd=login.enterInstance1(dynamicId, characterId, instanceId) #进入副本
    if not dd:
        return
    dd.addCallback(SerializePartialEnterFam,response)
    return dd

#@localserviceHandle
#def closeInstance_1502(key,dynamicId,request_proto):
#    '''退出副本'''
#    argument= escInstance_pb2.escInstanceRequest()
#    response = escInstance_pb2.escInstanceResponse()
#    argument.ParseFromString(request_proto)
#    characterId=argument.id #用户角色Id
#    dd=login.closeInstance(dynamicId,characterId)
#    if dd:
#        dd.addCallback(SerializePartialEnterScene,response)
#    return dd

