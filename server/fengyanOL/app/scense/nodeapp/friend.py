#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import firend, playerInfo
from app.scense.utils.dbopera import dbCharacter
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.friend import addPlayerFriend301_pb2
from app.scense.protoFile.friend import getPlayerFrinds302_pb2
from app.scense.protoFile.friend import removePlayerFriend_pb2
from app.scense.protoFile.friend import searchCharacterByName_pb2
from app.scense.protoFile.friend import addReport_pb2
from app.scense.protoFile.friend import FriendsLoadGameShowMessage307_pb2
from app.scense.protoFile.friend import SearchChatObjectFromFriends1004_pb2
from app.scense.protoFile.friend import FriendLevelUpReplyRequest311_pb2
from app.scense.core.language.Language import Lg

@nodeHandle
def addPlayerFriend_301(dynamicId, request_proto):
    '''添加好友'''
    argument = addPlayerFriend301_pb2.addPlayerFriendRequest()
    argument.ParseFromString(request_proto)
    response = addPlayerFriend301_pb2.addPlayerFriendResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    friendName = argument.playerName
    friendType = argument.type
    isSheildedMail=0
    if friendType==1:
        isSheildedMail=0
    elif friendType==2:
        isSheildedMail=1
    data = firend.addPlayerFriend(dynamicId, characterId, friendName, friendType, isSheildedMail=isSheildedMail)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def getPlayerFrinds_302(dynamicId, request_proto):
    '''获取好友信息'''
    argument = getPlayerFrinds302_pb2.getPlayerFrindsRequest()
    argument.ParseFromString(request_proto)
    response = getPlayerFrinds302_pb2.getPlayerFrindsResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = firend.getPlayerFrinds(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('friends',None):
        friendsInfo = data.get('friends')
        for friendInfo in friendsInfo:
            friends = response.data.friends.add()
            friends.roleId = friendInfo['id'] #角色id
            friends.roleName = friendInfo['nickname'] #角色名称
            friends.roleProfession = friendInfo['profession'] #角色职业
            friends.level = friendInfo['level'] #角色等级
            friends.comp = friendInfo['name'] #行会名称
            friends.zx=friendInfo['zx'] #是否在线
            friends.scenename=friendInfo['scenename']#角色所在场景名称
            friends.spirit=friendInfo['spirit'] #角色心情
    else:
        response.data.friends.extend([])
    return response.SerializeToString()

@nodeHandle
def getPlayerEnemys_300(dynamicId, request_proto):
    argument = getPlayerFrinds302_pb2.getPlayerFrindsRequest()
    argument.ParseFromString(request_proto)
    response = getPlayerFrinds302_pb2.getPlayerFrindsResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = firend.getPlayerFrinds(dynamicId, characterId,friendType=2)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('friends',None):
        friendsInfo = data.get('friends')
        for friendInfo in friendsInfo:
            friends = response.data.friends.add()
            friends.roleId = friendInfo['id'] #角色id
            friends.roleName = friendInfo['nickname'] #角色名称
            friends.roleProfession = friendInfo['profession'] #角色职业
            friends.level = friendInfo['level'] #角色等级
            friends.comp = friendInfo['name'] #行会名称
            friends.zx=friendInfo['zx'] #是否在线
            friends.scenename=friendInfo['scenename']#角色所在场景名称
            friends.spirit=friendInfo['spirit'] #角色心情
    else:
        response.data.friends.extend([])
    return response.SerializeToString()
@nodeHandle
def removePlayerFriend_303(dynamicId, request_proto):
    '''移除好友'''
    argument = removePlayerFriend_pb2.removePlayerFriendRequest()
    argument.ParseFromString(request_proto)
    response = removePlayerFriend_pb2.removePlayerFriendResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    friendId = argument.friendId
    data = firend.removePlayerFriend(dynamicId, characterId, friendId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        response.result=False
        response.message=Lg().g(325)
    return response.SerializeToString()
    

@nodeHandle
def searchCharacterByName_305(dynamicId, request_proto):
    '''根据昵称获取角色信息'''
    argument = searchCharacterByName_pb2.searchCharacterByNameRequest()
    argument.ParseFromString(request_proto)
    response = searchCharacterByName_pb2.searchCharacterByNameResponse()
    
    name=argument.nickName
    ziduan=argument.ziduan #按那个字段排序 1按角色名称,0角色等级，2行会名称  3最近登录时间
    guize=argument.guize #排序规则 1正序   0倒序
    data = firend.selectFriends(name, ziduan, guize)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('friends',None):
        friendsInfo = data.get('friends')
        for friendInfo in friendsInfo:
            friends = response.data.friends.add()
            friends.roleId = friendInfo['id'] #角色id
            friends.roleName = friendInfo['nickname']
            friends.roleProfession = friendInfo['profession']
            friends.level = friendInfo['level']
            friends.comp = friendInfo['name']
            friends.zx=friendInfo['zx']
            friends.lastLoadTime=str(friendInfo['LastonlineTime'])
    else:
        friends = response.data.friends.add()
    return response.SerializeToString()
@nodeHandle
def AddReport_306(dynamicId, request_proto):
    '''添加举报信息'''
    argument = addReport_pb2.getReportRequest()
    argument.ParseFromString(request_proto)
    response = addReport_pb2.getReportResponse()
    cid=argument.cid
    tocid=argument.tocid
    context=argument.context
    
    data=firend.AddReport(cid, tocid, context)
    if data:
        response.result=data
        response.message=Lg().g(69)
        response.data=0
    else:
        response.result=data
        response.message=Lg().g(70)
        response.data=0
    return response.SerializeToString()
@nodeHandle
def setShowMesFlag_307(dynamicId, request_proto):
    '''设置好友上线提示'''
    argument = FriendsLoadGameShowMessage307_pb2.friendsLoadGameShowMessageRequest()
    argument.ParseFromString(request_proto)
    response = FriendsLoadGameShowMessage307_pb2.friendsLoadGameShowMessageResponse()
    
    id=argument.id #当前角色id
    friendId=argument.friendId #好友id
    showMesFlag=argument.showMesFlag #好友上线是否提示
    data=firend.setShowMesFlag(id, friendId, showMesFlag)
    if not data:
        response.result=False
        response.message=Lg().g(608)
    else:
        response.result=True
        response.message=Lg().g(609)
    return response.SerializeToString()
@nodeHandle
def getFriendByLikeNames_1004(dynamicId, request_proto):
    argument=SearchChatObjectFromFriends1004_pb2.SearchChatObjectFromFriendsRequest()
    argument.ParseFromString(request_proto)
    response=SearchChatObjectFromFriends1004_pb2.SearchChatObjectFromFriendsResponse()
    
    characterid=argument.id
    nickname=argument.nameStr
    
    result=dbCharacter.getFriendByLikeNames(characterid, nickname)

    if not result or len(result)<1:
        response.result=False
        response.message=Lg().g(75)
        response.chatObjectData.extend([])
        return response.SerializeToString()
    response.result=True
    response.message=Lg().g(166)
    for item in result:
        val=response.chatObjectData.add()
        val.roleId=item.get('id')
        val.roleName=item.get('nickname')
    return response.SerializeToString()
@nodeHandle
def FriendLevelupReplyRequest_311(dynamicId, request_proto):
    '''好友祝福后增加经验'''
    argument=FriendLevelUpReplyRequest311_pb2.FriendLevelupReplyRequest()
    argument.ParseFromString(request_proto)
    response=FriendLevelUpReplyRequest311_pb2.FriendLevelupReplyResponse()
    
    id=argument.id #反馈好友角色id
    friend_id=argument.friend_id #升级角色id
    handle_type=argument.handle_type #反馈信息 0:错误 1:恭喜 2:鄙视
    data=playerInfo.celebrateAddExp(id,friend_id,handle_type) #增加祝福经验
    response.result=data.get('result',False)
    response.message=data.get('message',u'')
    response.friend_id=friend_id
    name = data.get('name',u'')
    response.friend_name= name if isinstance(name, unicode) else name.decode('gbk')
    response.handle_type=handle_type
    return response.SerializeToString()
