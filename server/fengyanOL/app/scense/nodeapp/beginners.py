#coding:utf8
'''
Created on 2011-6-21

@author: lan
'''

from app.scense.applyInterface import beginners
from app.scense.serverconfig.node import nodeHandle
#from app.scense.app.scense.protoFile.beginners import beginnersLogin_pb2
from app.scense.protoFile.beginners import getRandomName_pb2
from app.scense.protoFile.beginners import RecordStepID_pb2
from app.scense.protoFile.beginners import beginnersRegist_pb2
from app.scense.protoFile.beginners import FinalRegist_pb2
from app.scense.protoFile.beginners import GMInfo4000_pb2
from app.scense.core.language.Language import Lg

#@nodeHandle
#def beginnersLogin_1603(dynamicId,request_proto):
#    '''新手登陆'''
#    response = beginnersLogin_pb2.beginnersLoginReponse()
#    data = beginners.beginnersLogin()
#    response.result = data.get('result',False)
#    response.message = data.get('message',u'')
#    if data.get('data',0):
#        response.data = data.get('data')
#    return response.SerializeToString()

@nodeHandle
def getRandomName_1606(dynamicId,request_proto):
    '''获取随机名称'''
    response = getRandomName_pb2.getRandomNameResponse()
    data = beginners.getRandomName(dynamicId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',Lg().g(602)):
        response.name = data.get('data')
    return response.SerializeToString()
@nodeHandle
def RecordStepID_1604(dynamicId,request_proto):
    '''更新新手操作步骤'''
    arguments = RecordStepID_pb2.RecordStepIDRequest()
    arguments.ParseFromString(request_proto)
    beginnerId = arguments.beginnerId
    recordId = arguments.recordId
    beginners.RecordStepID(dynamicId, beginnerId, recordId)
@nodeHandle
def beginnersRegist_1601(dynamicId,request_proto):
    '''新手注册'''
    arguments = beginnersRegist_pb2.beginnersRegistRequest()
    arguments.ParseFromString(request_proto)
    response = beginnersRegist_pb2.beginnersRegistResponse()
    beginnerId = arguments.beginnerId
    nickname  = arguments.nickname 
    data = beginners.beginnersRegist(dynamicId,beginnerId,nickname)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',0):
        response.data = data.get('data')
    return response.SerializeToString()
@nodeHandle
def FinalRegist_1602(dynamicId,request_proto):
    '''新手引导结束后最终注册'''
    arguments = FinalRegist_pb2.FinalRegistRequest()
    arguments.ParseFromString(request_proto)
    response = FinalRegist_pb2.FinalRegistResponse()
    username = arguments.username
    password = arguments.password
    nickname = arguments.nickname
    profession = arguments.profession
    data = beginners.FinalRegist(dynamicId, username, password, nickname, profession)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',0):
        response.data.userId = data.get('data').get('userId',0)
        response.data.characterId = data.get('data').get('characterId',0)
        response.data.placeId = data.get('data').get('placeId',1001)
    return response.SerializeToString()

@nodeHandle
def GMInfo_4000(dynamicId,request_proto):
    '''GM消息反馈
    '''
    arguments = GMInfo4000_pb2.GMInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GMInfo4000_pb2.GMInfoResponse()
    characterId = arguments.id
    gmMsg = arguments.gmMsg
    data = beginners.GMInfo4000(dynamicId, characterId, gmMsg)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()
    
    
    
    
    
