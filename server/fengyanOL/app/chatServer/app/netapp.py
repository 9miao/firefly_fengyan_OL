#coding:utf8
'''
Created on 2012-2-25

@author: sean_lan
'''
from app.chatServer.app import chat
from firefly.server.globalobject import GlobalObject,netserviceHandle
from app.chatServer.protoFile.chat import sendMessage1003_pb2

@netserviceHandle
def loginToChatServer_1001(_conn, request_proto):
    '''登陆聊天服务器'''
    GlobalObject
    from app.chatServer.protoFile.chat import loginToChatServer_pb2
    argument = loginToChatServer_pb2.loginToChatServerRequest()
    argument.ParseFromString(request_proto)
    response = loginToChatServer_pb2.loginToChatServerResponse()
    
    dynamicId = _conn.transport.sessionno
    characterId = argument.id
    data = chat.loginToChatServer(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@netserviceHandle
def sendMessage_1003(_conn, request_proto):
    '''发送聊天消息'''
#    from protoFile.chat import sendMessage1003_pb2
#    from core.Item import Item
    argument = sendMessage1003_pb2.chatConectingRequest()
    argument.ParseFromString(request_proto)
    response = sendMessage1003_pb2.chatConectingResponse()
    
    dynamicId = _conn.transport.sessionno
    characterId = argument.id #当前角色id
    topic = argument.topic #频道号  
    tonickname=argument.chatOjbect #角色昵称
    content = argument.content #内容
    linkData = [] #聊天连接信息
    for _item in argument.linkData:
        item = {}
        item['chatEquipType'] = _item.chatEquipType
        item['id'] = _item.id
        item['name'] = _item.name
#        try:
#            item1=Item(id=_item.id)
#        except Exception:
#            linkData.append(item)
#            continue
#        item['itemInfo']=item1
#        linkData.append(item)
#        del item1
        
    
    data = chat.sendMessage(dynamicId, characterId, topic, content,linkData,tonickname)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

