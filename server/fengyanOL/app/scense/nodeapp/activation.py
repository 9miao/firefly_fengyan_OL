#coding:utf8
'''
Created on 2012-4-23

@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.applyInterface import activation
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.protoFile.activation import activation_pb2

@nodeHandle
def active_3000(dynamicId, request_proto):
    '''激活激活码'''    
    argument = activation_pb2.ActivationRequest()
    argument.ParseFromString(request_proto)
    response = activation_pb2.ActivationResponse()
    
    characterId = argument.id
    activationId = argument.activation
    data = activation.active(characterId, activationId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('message'):
        msg = data.get('message')
        pushOtherMessage(905, msg, [dynamicId])
    return response.SerializeToString()
    
    
    
