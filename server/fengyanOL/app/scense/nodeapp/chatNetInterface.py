#coding:utf8
'''
Created on 2011-3-17

@author: sean_lan
'''
from app.scense.applyInterface import chat
from app.scense.utils.dbopera import dbChat
from app.scense.core.language.Language import Lg

def loginToChatServer(_conn, request_proto):
    '''登陆聊天服务器'''
    from app.scense.protoFile.chat import loginToChatServer_pb2
    argument = loginToChatServer_pb2.loginToChatServerRequest()
    argument.ParseFromString(request_proto)
    response = loginToChatServer_pb2.loginToChatServerResponse()
    
    dynamicId = _conn.transport.sessionno
    characterId = argument.id
    data = chat.loginToChatServer(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

def sendMessage(_conn, request_proto):
    '''发送聊天消息'''
    from app.scense.protoFile.chat import sendMessage1003_pb2
    from app.scense.core.Item import Item
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
        try:
            item1=Item(id=_item.id)
        except Exception:
            linkData.append(item)
            continue
        item['itemInfo']=item1
        linkData.append(item)
        del item1
        
    
    data = chat.sendMessage(dynamicId, characterId, topic, content,linkData,tonickname)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()
    
def GetChatSettingInfo(_conn, request_proto):
    '''获取角色聊天设置信息'''
    from app.scense.protoFile.chat import GetChatSettingInfo1007_pb2
    argument = GetChatSettingInfo1007_pb2.GetChatSettingInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetChatSettingInfo1007_pb2.GetChatSettingInfoResponse()
    
    characterid=argument.id #角色id
    data=dbChat.getBycharacter(characterid)
    if not data:
        response.result=False
        response.message=u""
#        response.data.rankingInfo.extend([])
        return response.SerializeToString()
    response.result=True
    response.message=Lg().g(166)
    response.data.systemCK=bool(data.get('xt',0))
    response.data.showCK=bool(data.get('ts',0))
    response.data.commonCK=bool(data.get('alls',0))
    response.data.groupCK=bool(data.get('team',0))
    response.data.corpsCK=bool(data.get('jt',0))
    response.data.selfCK=bool(data.get('sl',0))
    return response.SerializeToString()

def ModifyChatSetting(_conn, request_proto):
    '''修改聊天你设置信息'''
    from app.scense.protoFile.chat import ModifyChatSetting1006_pb2
    argument = ModifyChatSetting1006_pb2.ModifyChatSettingRequest()
    argument.ParseFromString(request_proto)
    response = ModifyChatSetting1006_pb2.ModifyChatSettingResponse()
    
    characterid=argument.id
    xt=argument.systemCK
    ts=argument.showCK
    all=argument.commonCK
    team=argument.groupCK
    jt=argument.corpsCK
    sl=argument.selfCK
    if dbChat.CharByCharacter(characterid, xt, ts, all, team, jt, sl):
        response.result=True
        response.message=Lg().g(166)
    else:
        response.result=False
        response.message=u"操作失败"
    return response.SerializeToString()
#def chatUseItemHorn(_conn, request_proto):
#    '''使用大喇叭或者小喇叭'''
#    from protoFile.chat import UseItemHorn1005_pb2
#    argument = UseItemHorn1005_pb2.UseItemHornRequest()
#    argument.ParseFromString(request_proto)
#    response = UseItemHorn1005_pb2.UseItemHornResponse()
#    
#    id=argument.id
#    itemid=argument.itemId
#    hh=argument.hornContent
#    itemTemplateId=argument.itemTemplateId
#    data = chat.sendMessages(id, hh,itemid,itemTemplateId)
#    if not data:
#        response.result=False
#        response.message=u"失败"
#    response.result=True
#    response.message=Lg().g(166)
#    return response.SerializeToString()