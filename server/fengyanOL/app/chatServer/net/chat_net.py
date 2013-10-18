#coding:utf8
'''
Created on 2011-11-16
私聊
@author: SIOP_09
'''
from app.chatServer.core.ChaterLogManager import ChaterLogManager

from app.chatServer.protoFile.chat import SendChatMessage1013_pb2
from app.chatServer.protoFile.chat import GetOneObjectChatInfo1011_pb2
from app.chatServer.protoFile.chat import CloseChatWindow1014_pb2
from app.chatServer.core.language.Language import Lg
from firefly.server.globalobject import netserviceHandle

@netserviceHandle
def SendChatMessageRequest_1013(dynamicId, request_proto):
    '''当前角色发送私聊信息'''
    import time
    from app.chatServer.core.ChaterManager import ChaterManager
    argument = SendChatMessage1013_pb2.SendChatMessageRequest()
    argument.ParseFromString(request_proto)
    response = SendChatMessage1013_pb2.SendChatMessageResponse()
    id = argument.id
    tid = argument.chatId
    context = argument.chatMessage
    
    chater=ChaterManager().getChaterByCharacterId(id)
    if chater.donttalk==0:#不禁言
        timet=str(time.strftime('%Y-%m-%d %X'))
        title="<font color='#ffffff'>"
        title+=chater.getCharacterName()
        title+=":</font><br/>"
        title+=u"<font color='#ffffff'>&nbsp;&nbsp;%s</font><br/>"%context
        ChaterLogManager().addLog(id, tid, title,timet)
        response.result =True
        response.message =u''
    else:#禁言
        response.result =True
        response.message =Lg().g(644)
    return response.SerializeToString()
@netserviceHandle
def GetChatInfoRequest_1011(dynamicId, request_proto):
    '''获取私聊信息'''
    argument=GetOneObjectChatInfo1011_pb2.GetOneObjectChatInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetOneObjectChatInfo1011_pb2.GetOneObjectChatInfoResponse()
    
    id=argument.id
    tid=argument.chatObjectId
    val=ChaterLogManager().getLog(id, tid)
    if val.get('result',None):
        response.result =True
        response.message =u''
        response.chatMessage=val.get('result',u'')
        response.level=val.get('level',0)
        response.perfession=val.get('perfession',Lg().g(143))
        response.chatObjectPos=val.get('chatObjectPos',u'')
        response.name=val.get('name',u'')
        
    else:
        response.result =True
        response.message =u''
        response.chatMessage=val.get('result',u'')
        response.level=val.get('level',0)
        response.perfession=val.get('perfession',Lg().g(143))
        response.chatObjectPos=val.get('chatObjectPos',u'')
        response.name=val.get('name',u'')
    return response.SerializeToString()
@netserviceHandle
def CloseChatWindowRequest_1014(dynamicId, request_proto):
    '''关闭私聊窗口'''
    argument=CloseChatWindow1014_pb2.CloseChatWindowRequest()
    argument.ParseFromString(request_proto)
    response=CloseChatWindow1014_pb2.CloseChatWindowResponse()
    
    id=argument.id #当前角色id
    ChaterLogManager().closeChat(id)
    response.result=True
    response.message=u''
    return response.SerializeToString()