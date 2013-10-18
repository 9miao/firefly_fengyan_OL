#coding:utf8
'''
Created on 2011-11-16
私聊
@author: SIOP_09
'''
from app.scense.core.ChaterLogManager import ChaterLogManager
from app.scense.core.PlayersManager import PlayersManager
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.chat import SendChatMessage1013_pb2
from app.scense.protoFile.chat import GetOneObjectChatInfo1011_pb2
from app.scense.protoFile.chat import CloseChatWindow1014_pb2
import time
from app.scense.core.language.Language import Lg

@nodeHandle
def SendChatMessageRequest_1013(dynamicId, request_proto):
    '''当前角色发送私聊信息'''
    argument = SendChatMessage1013_pb2.SendChatMessageRequest()
    argument.ParseFromString(request_proto)
    response = SendChatMessage1013_pb2.SendChatMessageResponse()
    id = argument.id
    tid = argument.chatId
    context = argument.chatMessage
#    print str(id)+" ############ "+str(tid)
    player=PlayersManager().getPlayerByID(id)
    timet=str(time.strftime('%Y-%m-%d %X'))
    title="<font color='#ffffff'>"
    title+=player.baseInfo.getNickName()
    title+=" : &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+timet+"</font><br/>"
    title+="<font color='#ffffff'>"+str(context)+"</font><br/>"
    
    ChaterLogManager().addLog(id, tid, title,timet)
    response.result =True
    response.message =u''
    return response.SerializeToString()
@nodeHandle
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
        response.chatMessage=val.get('result','')
        response.level=val.get('level',0)
        response.perfession=val.get('perfession',Lg().g(143))
        response.chatObjectPos=val.get('chatObjectPos','')
        response.name=val.get('name','')
        
    else:
        response.result =True
        response.message =u''
        response.chatMessage=val.get('result','')
        response.level=val.get('level',0)
        response.perfession=val.get('perfession',Lg().g(143))
        response.chatObjectPos=val.get('chatObjectPos','')
        response.name=val.get('name','')
    return response.SerializeToString()
@nodeHandle
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