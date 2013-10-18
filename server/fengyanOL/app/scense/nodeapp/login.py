#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.utils.DataLoader import loader
from app.scense.applyInterface import login
from app.scense.serverconfig.node import nodeHandle

@nodeHandle
def loginToServer_101(dynamicId, request_proto):
    '''登陆服务器
    '''
    from app.scense.protoFile.login import loginToServer_pb2
    argument = loginToServer_pb2.loginToServerRequest()
    argument.ParseFromString(request_proto)
    response = loginToServer_pb2.loginToServerResponse()
    
    dynamicId = dynamicId
    username = argument.user
    password = argument.password
    data = login.loginToServer(dynamicId, username, password)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        response.data.len = data['data'].get('len',0)
        response.data.userId = data['data'].get('userId',0)
        response.data.defaultId = data['data'].get('defaultId',-1)
        for character in data['data'].get('UserCharacterList',[]):
            characterInfo = response.data.character.add()
            characterInfo.id = character.get('id',0)
            characterInfo.nickname = character.get('nickname',u'')
            characterInfo.level = character.get('level',1)
            professionId = character.get('profession',1)
            professionName = loader.getById('profession',professionId,['name']).get('name',u'新手')
            characterInfo.profession = professionName
            characterInfo.viptype = character.get('viptype',1)
    return response.SerializeToString()

@nodeHandle
def activeNewPlayer_102(dynamicId, request_proto):
    '''创建角色
    '''
    from app.scense.protoFile.login import activeNewPlayer_pb2
    argument = activeNewPlayer_pb2.activeNewPlayerRequest()
    argument.ParseFromString(request_proto)
    response = activeNewPlayer_pb2.activeNewPlayerResponse()
    
    dynamicId = dynamicId
    userId = argument.userId
    nickName = argument.nickName
    profession = argument.profession
    data = login.activeNewPlayer(dynamicId, userId, nickName, profession)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        response.data.len = data['data'].get('len',0)
        response.data.userId = userId
        response.data.newCharacterId = data['data'].get('newCharacterId',0)
        for character in data['data'].get('UserCharacterList',[]):
            characterInfo = response.data.character.add()
            characterInfo.id = character.get('id',0)
            characterInfo.nicName = character.get('nickname',u'')
            characterInfo.level = character.get('level',1)
            professionId = character.get('profession',1)
            professionName = loader.getById('profession',professionId,['name']).get('name',u'新手')
            characterInfo.profession = professionName
            characterInfo.roletype = character.get('viptype',1)
            
    return response.SerializeToString()

@nodeHandle
def roleLogin_103(dynamicId, request_proto):
    '''角色登陆'''
    from app.scense.protoFile.login import roleLogin_pb2
    argument = roleLogin_pb2.roleLoginRequest()
    argument.ParseFromString(request_proto)
    response = roleLogin_pb2.roleLoginResponse()
    
    dynamicId = dynamicId
    userId = argument.userId
    characterId = argument.id
    data = login.roleLogin(dynamicId, userId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        response.data.placeId = data['data'].get('placeId',1000)
    return response.SerializeToString()

@nodeHandle
def deleteRole_104(dynamicId, request_proto):
    '''删除角色'''
    from app.scense.protoFile.login import deleteRole_pb2
    argument = deleteRole_pb2.deleteRoleRequest()
    argument.ParseFromString(request_proto)
    response = deleteRole_pb2.deleteRoleResponse()
    
    
    userId = argument.userId
    characterId = argument.id
    password = argument.password
    data = login.deleteRole(dynamicId, userId, characterId,password)
    
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        response.data.len = len(data.get('data',[]))
        for character in data['data'].get('UserCharacterListInfo',[]):
            characterInfo = response.data.character.add()
            characterInfo.id = character.get('id',0)
            characterInfo.nicName = character.get('nickname',u'')
            characterInfo.level = character.get('level',1)
            professionId = character.get('profession',1)
            professionName = loader.getById('profession',professionId,['name']).get('name',u'新手')
            characterInfo.profession = professionName
            characterInfo.roletype = character.get('viptype',1)
    return response.SerializeToString()
    
