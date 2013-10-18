#coding:utf8
'''
Created on 2011-3-19

@author: sean_lan
'''


from app.chatServer.protoFile.chat import chatMessage1002_pb2
from app.chatServer.protoFile.chat import ChatToObjectListInfo1010_pb2
from app.chatServer.protoFile.chat import ServerSendChatInfo1012_pb2
from app.chatServer.protoFile import pushOtherMessage_pb2
from app.chatServer.core.language.Language import Lg
from firefly.server.globalobject import GlobalObject

def pushSystemToInfo2700(str,sendList):
    '''推送跑马灯'''
    from app.chatServer.protoFile.chat import SystemToInfo2700_pb2
    response=SystemToInfo2700_pb2.SystemToInfoResponse()
    response.s_info=str
    data = response.SerializeToString()
    pushApplyMessage(2700 , data, sendList)

def pushApplyMessage(topic,msg,sendList):
    '''推送消息'''
    GlobalObject().netfactory.pushObject(topic , msg, sendList)
    

def pushChatMessage(topic,characterId,fromName,profession,content,linkData,sendList):
    '''推送聊天消息
    @param topic: int 聊天通道id    1世界 2当前 3国 4GM 5系统通告 6国通告 7错误提示   
    @param characterId: int 角色的id （系统 -1）
    @param fromName: str 发送者得名称 （例如 系统时 为系统）
    @param profession: int 职业（主要 ）
    @param content: str聊天的文字内容
    @param sendList: list [int] 发送的客户端id列表
    '''
    response = chatMessage1002_pb2.chatMessageResponse()
    
    #content=u"[%%]"
    
    response.topic = topic
    response.id = characterId 
    response.fromName = fromName
    response.profession = profession
    for _item in linkData:
        item = response.linkData.add()
        item.chatEquipType = _item['chatEquipType']
        item.id = _item['id']
        item.name = _item['name']
        if _item.has_key('itemInfo'):
            _item['itemInfo'].SerializationItemInfo(item.itemInfo)
    try:
        response.content = content
    except Exception:
        response.content = content.decode('gbk')
    
    data = response.SerializeToString()
    GlobalObject().netfactory.pushObject(1002 , data, sendList)


def pushChatToObjectList(id,tid):
    '''推送私聊角色列表'''
    from app.chatServer.core.ChaterManager import ChaterManager
    from app.chatServer.core.ChaterLogManager import ChaterLogManager
    response=ChatToObjectListInfo1010_pb2.ChatToObjectListResponse()
    clog=ChaterLogManager().addChatLog(id) #获取聊天类
    listid=clog.getFriends()#获取角色私聊对象id列表
    if len(listid)<0:
        return
    player=ChaterManager().getChaterByCharacterId(id)
#    player=PlayersManager().getPlayerByID(id)
    if not player:
        #print "推送私聊角色列表时没有角色"+str(id)
        return 
    #print "角色私聊角色列表发送给"+player.baseInfo.getNickName()
    playerid=player.getDynamicId()
    for cid in listid:
        player1=ChaterManager().getChaterByCharacterId(cid)
        info=response.chatObjectInfo.add()
        info.chatObjectId=cid
        info.name=player1.getCharacterName()
        #print "私聊信息角色列表："+player1.baseInfo.getNickName()
        info.level=str(player1.level)
        info.perfession=player1.getProfessionName()
        if player1.island:
                info.chatObjectPos=player1.scenename
        else:
            info.chatObjectPos=Lg().g(106)
        info.readFlag=ChaterLogManager().getFriendReaderState(id, cid)
    #print "------------------------------------------------------------------"
    msg = response.SerializeToString()
    pushApplyMessage(1010,msg,[playerid])

def pushServerSendChatInfo(id,message,tid):
    '''推送的私聊信息
    @param id: int 私聊对象角色id
    @param tid: int 私聊角色id
    @param message: str 聊天内容
    '''
    from app.chatServer.core.ChaterManager import ChaterManager
    response=ServerSendChatInfo1012_pb2.ServerSendChatInfoResponse()
    response.id=tid
    response.chatMessage=message
    msg=response.SerializeToString()
    chater=ChaterManager().getChaterByCharacterId(id)#推送给这个人的角色
    dyid=chater.dynamicId
    pushApplyMessage(1012,msg,[dyid])
    
def pushOtherMessage(orderId ,msg ,sendList):
    '''推送其他提示信息'''
    request = pushOtherMessage_pb2.OtherMessage()
    try:
        request.msg = msg
    except Exception:
        request.msg = unicode(msg,'gbk')
    data = request.SerializeToString()
    pushApplyMessage(905,data,sendList)
    