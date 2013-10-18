#coding:utf8
'''
Created on 2012-3-31

@author: Administrator
'''
from app.chatServer.core.ChaterManager import ChaterManager
from app.chatServer.core.ChatRoomManager import ChatRoomManager
from app.chatServer.net.pushObjectNetInterface import pushChatMessage

from app.chatServer.protoFile.chat import SystemToInfo2700_pb2
from app.chatServer.core.Lt import Lt
from app.chatServer.core.GuildManager import GuildManager
from app.chatServer.core.language.Language import Lg
from firefly.server.globalobject import GlobalObject,rootserviceHandle

@rootserviceHandle
def JoinRoom(characterId,roomId,scenename):
    '''
    @param characterId: int character id
    @param roomId: int room id
    '''
    chater = ChaterManager().addChaterByid(characterId)
    if not chater:
        return
    clientId = chater.getDynamicId()
    oldroomId = chater.getRoomId()
    chater.setSceneName(scenename)
    if not oldroomId or clientId < 0:
        return
    if oldroomId :
        ChatRoomManager().leaveRoom(clientId, oldroomId)
    chater.setRoomId(roomId)
    ChatRoomManager().joinRoom(clientId, roomId)
    
@rootserviceHandle
def leaveRoom(characterId):
    '''
    @param characterId: int character id
    @param roomId: int room id
    '''
    chater = ChaterManager().getChaterByCharacterId(characterId)
    if not chater:
        return
    clientId = chater.getDynamicId()
    oldroomId = chater.getRoomId()
    if not oldroomId or clientId < 0:
        return
    if oldroomId :
        ChatRoomManager().leaveRoom(clientId, oldroomId)

@rootserviceHandle
def addBacklist(id,tid):
    '''
    @param id: int nowplayerid
    @param tid: int back id
    '''
    chater=ChaterManager().addChaterByid(id)
    if tid in chater.blacklist:
        return
    elif tid in chater.whitelist:
        chater.whitelist.remove(tid)
        chater.blacklist.add(tid)
        return
    else:
        chater.blacklist.add(tid)
    
       
@rootserviceHandle
def dropfriend(id,tid):
    chater=ChaterManager().addChaterByid(id)
    if tid in chater.whitelist:
        chater.whitelist.remove(tid)
    if tid in chater.blacklist:
        chater.blacklist.remove(tid)
        
@rootserviceHandle
def addWhitelist(id,tid):
    '''
    @param id: int nowplayerid
    @param tid: int player id
    '''
    chater=ChaterManager().addChaterByid(id)
    
    if tid in chater.whitelist:
        return
    elif tid in chater.blacklist:
        chater.blacklist.remove(tid)
        chater.whitelist.add(tid)
    else:
        chater.whitelist.add(tid)
        
        
@rootserviceHandle
def updateCharteLevel(characterid,level):
    '''角色等级同步
    @param characterid: int 角色id
    @param level: int 等级
    '''
    chater=ChaterManager().addChaterByid(characterid)
    chater.level=level
    
    


@rootserviceHandle
def updateGuild(characterid,guild,tag):
    '''角色行会同步
    @param characterid: int 角色id
    @param guild: int 行会id
    @param tag: int 1加入国  0退出国
    '''
    chater=ChaterManager().addChaterByid(characterid)
    if tag==1:
        GuildManager().add(chater.dynamicId, guild)
        chater.guildid=guild
    if tag==0:
        GuildManager().delete(chater.dynamicId, guild)
        chater.guildid=0

@rootserviceHandle
def pushSystemToInfo(strInfo):
    '''推送系统消息'''
    response=SystemToInfo2700_pb2.SystemToInfoResponse()
    try:
        response.s_info=strInfo
    except Exception:
        response.s_info=strInfo.decode('utf8')
    sendList = [charter.getDynamicId() for charter in ChaterManager()._chaters.values()]
    data = response.SerializeToString()
    GlobalObject().netfactory.pushObject(2700 , data, sendList)
    
@rootserviceHandle
def pushSystemchat(strInfo):
    '''推送聊天框系统消息系统
    @param strInfo: str 系统消息内容
    '''
    sendList = [charter.getDynamicId() for charter in ChaterManager()._chaters.values()]
    pushChatMessage(5, -1, Lg().g(128), 0, strInfo,[], sendList)
    
@rootserviceHandle
def updateDontTalk(characterid,flg):
    '''更爱角色禁言状态
    @param characterid: int 角色id
    @param flg: int 0:不禁言   1禁言
    return 是否成功 True or False
    '''
    return ChaterManager().donttalk(characterid, flg)

@rootserviceHandle
def getTalkLog():
    '''获取聊天记录'''
    return Lt().get()
