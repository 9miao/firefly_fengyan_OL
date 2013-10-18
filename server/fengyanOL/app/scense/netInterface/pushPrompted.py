#coding:utf8
'''
Created on 2011-11-22
提示信息推送
@author: lan
'''
from app.scense.netInterface.pushObjectNetInterface import pushApplyMessage,pushObjectByCharacterId

def pushPromptedMessage(msg ,sendList):
    '''推送其他提示信息'''
    from app.scense.protoFile import PromptedMessage_pb2
    response = PromptedMessage_pb2.PromptedMessage()
    try:
        response.prompted = msg
    except Exception:
        response.prompted = unicode(msg,'gbk')
    data = response.SerializeToString()
    pushApplyMessage(2200,data,sendList)
    
def pushPromptedMessageByCharacter(msg ,sendList):
    '''推送其他提示信息'''
    from app.scense.protoFile import PromptedMessage_pb2
    response = PromptedMessage_pb2.PromptedMessage()
    try:
        response.prompted = msg
    except Exception:
        response.prompted = unicode(msg,'gbk')
    data = response.SerializeToString()
    pushObjectByCharacterId(2200,data,sendList)
    
    
