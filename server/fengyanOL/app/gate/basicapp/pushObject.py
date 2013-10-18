#coding:utf8
'''
Created on 2012-2-27

@author: sean_lan
'''

from app.gate.protoFile import EnterMessage_1321_pb2
from app.gate.protoFile import ContinueMessage_905_pb2
from firefly.server.globalobject import GlobalObject
from app.gate.core.VCharacterManager import VCharacterManager

def pushObject(topicID,msg,sendList):
    '''根据客户端的ID推送信息'''
    GlobalObject().root.callChild('net',"pushData",topicID,msg,sendList)
#    root.callChildByName('netserver',0,topicID,msg,sendList)
    
def pushObjectByCharacterId(topicID,msg,sendList):
    '''根据角色的ID推送信息'''
    _sendList = [VCharacterManager().getClientIdByCharacterId(cid) for cid in sendList]
    GlobalObject().root.callChild('net',"pushData",topicID,msg,sendList)
#    root.callChildByName('netserver',0,topicID,msg,sendList)
    
def pushEnterMessage(msg ,sendList,wtype = 0):
    '''推送确认提示框
    @param wtype: int//弹窗类型 [0:包含一个确定按钮]
    '''
    request = EnterMessage_1321_pb2.EnterMessage()
    try:
        request.type = wtype
        request.msg = msg
    except Exception:
        request.msg = unicode(msg,'gbk')
    data = request.SerializeToString()
    pushObject(1321,data,sendList)
    
def pushOtherMessage(msg ,sendList):
    '''推送3秒提示信息'''
    response = ContinueMessage_905_pb2.OtherMessage()
    try:
        response.msg = msg
    except Exception:
        response.msg = unicode(msg,'gbk')
    data = response.SerializeToString()
    pushObject(905,data,sendList)
    
    