#coding:utf8
'''
Created on 2011-3-17
这个正在用
@author: sean_lan
'''
from app.chatServer.app import chat
from app.chatServer.core.Item import Item
from app.chatServer.core.Lt import Lt
from app.chatServer.protoFile.chat import loginToChatServer_pb2
from app.chatServer.protoFile.chat import sendMessage1003_pb2
from app.chatServer.core.language.Language import Lg
from firefly.server.globalobject import netserviceHandle

@netserviceHandle
def loginToChatServer_1001(_conn, request_proto):
    '''登陆聊天服务器'''
    argument = loginToChatServer_pb2.loginToChatServerRequest()
    argument.ParseFromString(request_proto)
    response = loginToChatServer_pb2.loginToChatServerResponse()
    
    dynamicId = _conn.transport.sessionno
    characterId = argument.id
    roomId = argument.placeId
    data = chat.loginToChatServer(dynamicId, characterId,roomId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@netserviceHandle
def sendMessage_1003(_conn, request_proto):
    '''发送聊天消息'''
    from app.chatServer.core.ChaterManager import ChaterManager
#    from core.Item import Item
    argument = sendMessage1003_pb2.chatConectingRequest()
    argument.ParseFromString(request_proto)
    response = sendMessage1003_pb2.chatConectingResponse()
    
    dynamicId = _conn.transport.sessionno
    characterId = argument.id #当前角色id
    topic = argument.topic #频道号  
    tonickname=argument.chatOjbect #角色昵称
    content = argument.content #内容
    
    chater=ChaterManager().getChaterByCharacterId(characterId)
    if chater.donttalk==0:#不禁言
        linkData = [] #聊天连接信息
        for _item in argument.linkData:
            item = {}
            item['chatEquipType'] = _item.chatEquipType #0物品 1角色 2怪物
            item['id'] = _item.id
            item['name'] = _item.name
            
            if _item.chatEquipType==0:
                item1=Item(id=_item.id)
                item['itemInfo']=item1
#            elif _item.chatEquipType==1:
#                linkData.append(item)
#                continue
            
            linkData.append(item)
        Lt().add(characterId, tonickname, content)
        data = chat.sendMessage(dynamicId, characterId, topic, content,linkData,tonickname)
        response.result = data.get('result',False)
        response.message = data.get('message',u'')
    else:#禁言
        response.result = False
        response.message =Lg().g(644) 
    return response.SerializeToString()


