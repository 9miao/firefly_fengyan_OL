#coding:utf8
'''
Created on 2012-3-5

@author: sean_lan
'''

from app.scense.serverconfig.node import pushObject,pushObjectByCharacterId,pushObjectToAll
from app.scense.core.PlayersManager import PlayersManager
#from utils.dbopera import dbFriend

from app.scense.protoFile import pushOtherMessage_pb2
from app.scense.protoFile.playerInfo import updatePlayerInfo_pb2
from app.scense.protoFile.guild import CorpsInvitePlayerNotify_pb2
from app.scense.protoFile.hall import GetRoleOfRoomInfo_pb2,GetRoomInfo1821_pb2
from app.scense.protoFile.hall import quitHallMessage_pb2,pushRoomMatrixInfo_pb2
from app.scense.protoFile.guild import SysOpeCorps2900_pb2
from app.scense.protoFile.strengthen import StrengthenTime2120_pb2

import random
from app.scense.core.language.Language import Lg



pushApplyMessage = pushObject
pushObjectToAll = pushObjectToAll

def getzudui_4308(data1,plist,msg,zy):
    '''多人副本战斗
    @param data1: obj 战斗信息 
    @param plist: [角色id] 托送的角色id列表
    @param msg: str 战斗结束后的消息
    @param zy: int 场景资源id
    '''
    from app.scense.protoFile.zudui import GroupBattle4308_pb2
    response=GroupBattle4308_pb2.FightResponse()
    
    response.result = True
    response.data.battleResult = data1.battleResult
    response.data.centerX = data1.center
    response.data.centerY = 325
    response.data.fightmsg=msg
    response.data.zyid=zy
    rResArr = response.data.rResArr
    startData = response.data.startData
    setpdata = response.data.stepData
    data1.SerializationResource(rResArr)
    data1.SerializationInitBattleData(startData)
    data1.SerializationStepData(setpdata)
    
    data=response.SerializeToString()
    pushObjectByCharacterId(4308,data,plist)

def team4304(dwid,plist):
    '''队伍详细信息
    @param dwid: int 队伍id
    @param plist: [] 队伍中角色的id列表[1,2,3]
    '''
    from app.scense.protoFile.zudui import GetGroupInfo4304_pb2
    from app.scense.core.teamfight.TeamFight import TeamFight
    
    response=GetGroupInfo4304_pb2.GetGroupInfoResponse()
    response.message=u''
    response.result=True
    if TeamFight().ishaveteam(dwid):#如果有队伍
        result=TeamFight().getTeamInfoByPlayerId1(dwid)
        if len(result)>0:
            for item in result:
                info=response.dwMemberInfo.add()
                info.roleId=item.get('roleId')
                info.pos=item.get('pos')
                info.level=item.get('level')
                info.roleName=item.get('roleName')
                info.proType=item.get('roleType')
    else:#如果没有队伍
        response.dwMemberInfo.extend([])
    data=response.SerializeToString()
    pushObjectByCharacterId(4304,data,plist)
    
def teamClean4304(dwid,plist):
    '''队伍详细信息
    @param dwid: int 队伍id
    @param plist: [] 队伍中角色的id列表[1,2,3]
    '''
    from app.scense.protoFile.zudui import GetGroupInfo4304_pb2
    
    response=GetGroupInfo4304_pb2.GetGroupInfoResponse()
    response.message=u''
    response.result=True
    response.dwMemberInfo.extend([])
    data=response.SerializeToString()
    pushObjectByCharacterId(4304,data,plist)

def StrengthenTime2120(pid,sstime):
    '''推送强化剩余时间
    @param pid: int 角色id
    @param sstime: int 剩余秒数    
    '''
    r = StrengthenTime2120_pb2.StrengthenTimeResponse()
    r.message=u''
    r.result=True
    r.reTime=sstime
    data = r.SerializeToString()
    pushObjectByCharacterId(2120,data,[pid])

def pushOtherMessage(orderId ,msg ,sendList):
    '''推送其他提示信息'''
    request = pushOtherMessage_pb2.OtherMessage()
    try:
        request.msg = msg
    except Exception:
        request.msg = unicode(msg,'gbk')
    data = request.SerializeToString()
    pushApplyMessage(905,data,sendList)
    
def pushOtherMessageByCharacterId(msg ,sendList):
    '''推送其他提示信息'''
    request = pushOtherMessage_pb2.OtherMessage()
    try:
        request.msg = msg
    except Exception:
        request.msg = unicode(msg,'gbk')
    data = request.SerializeToString()
    pushObjectByCharacterId(905,data,sendList)
    
def pushUpdatePlayerInfo(dynamicId,topicID=209):
    '''推送更新角色信息的消息'''
    response = updatePlayerInfo_pb2.updatePlayerInfo()
    response.signal = 1
    msg = response.SerializeToString()
    pushApplyMessage(topicID,msg,[dynamicId])
    
def pushCharacterLevelMessage(sendList,name,level):
    '''推送角色升级消息'''
    from app.scense.protoFile.playerInfo import pushCharacterLevelMessage_pb2
    response = pushCharacterLevelMessage_pb2.pushCharacterLevelMessage()
    response.Signal = 1
    msg = response.SerializeToString()
    pushObjectByCharacterId(218,msg,sendList)
    #-------发送给所有在线好友升级提示
#    player=PlayersManager().getPlayerBydynamicId(sendList[0])
#    id=player.baseInfo.getId()
#    name=player.baseInfo.getNickName()
#    level=player.level.getLevel()
    #print"推送升级消息"+name+str(level)
    pushzhFriend(sendList[0],name,level)
    
def pushzhFriend(id,name,level):
    '''当角色升级后推送当前角色的等级信息到该角色的所有在线好友，用以祝贺只用
    @param id: int 角色id
    @param name: str 角色名称
    @param level: int 角色的等级
    '''
    
    from app.scense.protoFile.friend import FriendLevelUpNotify310_pb2
    response=FriendLevelUpNotify310_pb2.FriendLevelUpNotify()
    player=PlayersManager().getPlayerByID(id)
    if player:
        cityid=player.baseInfo.getTown()#角色所在城市
        list=[] #存储好友动态id
        val=player.friend.getFriends()
        if not val or len(val)<1:#如果该角色没有好友
            return
        for itid in val: 
            playert=PlayersManager().getPlayerByID(itid)
            if playert and playert.baseInfo.getTown()==cityid:#如果角色在线并且和升级角色在同一个城市
                list.append(playert.baseInfo.getId())
        if len(list)<1: #如果该角色好友都没有在线
            return
       
        response.id=id
        response.name=name
        response.level=level
        msg = response.SerializeToString()
        pushObjectByCharacterId(310,msg,list)
    
def pushaddPlayerFriendto(id,name,sendList):
    '''推送反加好友界面
    @param id: 预备好友角色id
    @param name: 预备好友角色名称
    '''
    from app.scense.protoFile.friend import addPlayerFriendto308_pb2
    response=addPlayerFriendto308_pb2.addPlayerFriendtoRequest()
    response.id=id
    response.playerName=name
    msg = response.SerializeToString()
    pushApplyMessage(308,msg,sendList)
    
def pushEnterMessage(msg ,sendList,type = 0):
    '''推送确认提示框'''
    from app.scense.protoFile.guild import CorpsInviteCallBackNotify1321_pb2
    request = CorpsInviteCallBackNotify1321_pb2.UnionInvitePlayerBackNotify()
    try:
        request.type = type
        request.msg = msg
    except Exception:
        request.msg = unicode(msg,'gbk')
    data = request.SerializeToString()
    pushApplyMessage(1321,data,sendList)
    
def pushInviteOtherJoinGuild(playerid,unionid,playername,unionname,sendList):
    '''推送加入行会的信息'''
    response = CorpsInvitePlayerNotify_pb2.UnionInvitePlayerNotify()
    response.playerid = playerid
    response.unionid = unionid
    response.playername = playername
    response.unionname= unionname
    msg = response.SerializeToString()
    pushApplyMessage(1319,msg,sendList)
    
def pushInviteJoinGroupMsg(sendList,argumnts):
    '''推送邀请加入房间的消息'''
    
    from app.scense.protoFile.hall import InviteJoinGroupMsg_pb2
    response = InviteJoinGroupMsg_pb2.InviteJoinGroupMsg()
    for item in argumnts.items():
        setattr(response,item[0],item[1])
    msg = response.SerializeToString()
    pushApplyMessage(1810, msg, sendList)
    
    
def pushGameTopTitle2400(sendList,typelist):
    '''推送奖励图标
    @param sendList: 角色id列表
    @param typeid: int 奖励类型 1为殖民  2殖民管理
    '''
    from app.scense.protoFile.defence import GameTopTitle2400_pb2
    response=GameTopTitle2400_pb2.GameTopTitleResponse()
    if len(typelist)<1:
        response.anouInfo.extend([])
    else:
        for typeid in typelist:
            an=response.anouInfo.add()
            an.anouType=typeid
    data = response.SerializeToString()
    pushObjectByCharacterId(2400 , data, sendList)
#    pushApplyMessage(2400 , data, sendList)
    
    
def pushGameTopTitle2400Clear(sendList):
    '''推送清空奖励图标
    @param typeid: int 奖励类型 1为殖民
    '''
    from app.scense.protoFile.defence import GameTopTitle2400_pb2
    response=GameTopTitle2400_pb2.GameTopTitleResponse()
    response.anouInfo.extend([]) 
    data = response.SerializeToString()
    pushApplyMessage(2400 , data, sendList)
    
def pushLeaderInstance(sendList,leaderid):
    '''向队伍角色推送是否进入副本提示框'''
    from app.scense.protoFile.revive import insTeamPlace_pb2
    response = insTeamPlace_pb2.instanceTeamResponse()
    response.leaderid=leaderid
    msg = response.SerializeToString()
    pushApplyMessage(1503, msg, sendList)
    
def pushEnterPlace(placeId,sendList):
    '''推送进入场景
    @param placeId: int 场景的Id
    @param isboos: int 是否是boss
    @param copySceneId: 副本的Id
    @param sceneType: 场景类型
    '''
    from app.scense.protoFile.scene import enterPlace_pb2
    response = enterPlace_pb2.enterPlaceResponse()
    response.result = True
    response.data.placeId = placeId
    msg = response.SerializeToString()
    pushApplyMessage(605,msg,[sendList])
    
def pushEnterPlace_new(sceneInfo,sendList):
    '''推送进入场景
    @param placeId: int 场景的Id
    @param isboos: int 是否是boss
    @param copySceneId: 副本的Id
    @param sceneType: 场景类型
    '''
    from app.scense.protoFile.scene import EnterSceneMessage_605_pb2
    response = EnterSceneMessage_605_pb2.EnterSceneMessage()
    response.sceneId = sceneInfo.get('id',0)
    response.resourceId = sceneInfo.get('resourceId',0)
    response.sceneType = sceneInfo.get('sceneType',0)
    response.scenename = sceneInfo.get('scenename',u'')
    response.corpsName = sceneInfo.get('corpsName',Lg().g(601))
    response.rewardCorpsName = sceneInfo.get('rewardCorpsName',Lg().g(601))
    npclist = response.npclist
    for npc in sceneInfo.get('npclist',[]):
        if not npc:
            continue
        npcInfo = npclist.add()
        npcInfo.npcId = npc['id']
        npcInfo.npcName = npc['name']
        npcInfo.resourceId = npc['resourceid']
        npcInfo.funcType = npc['featureType']
        npcInfo.positionX = npc['position_X']
        npcInfo.positionY = npc['position_Y']
    portals = response.portals
    for portal in sceneInfo['portals']:
        if not portal:
            continue
        portalInfo = portals.add()
        portalInfo.portalId = portal['id']
        portalInfo.portalName = portal['name']
        portalInfo.funcType = portal['functionType']
        portalInfo.positionX = portal['position_x']
        portalInfo.positionY = portal['position_y']
        portalInfo.resourceId = portal['resourceId']
    msg = response.SerializeToString()
    pushApplyMessage(605,msg,sendList)
    
def pushInvitedGroup(id ,msg ,sendList):
    '''像对方发送邀请组队消息'''
    from app.scense.protoFile.team import pushInvitedGroup_pb2
    request = pushInvitedGroup_pb2.pushInvitedGroupRequest()
    request.inviterId = id
    request.msg = msg
    data = request.SerializeToString()
    pushApplyMessage(901,data,sendList)
    
def pushRemovePlayerInMap(playerId,sendList):
    '''通知场景移除玩家'''
    from app.scense.protoFile.scene import removePlayerInMap_pb2
    request = removePlayerInMap_pb2.removePlayerInMap()
    request.id = playerId
    msg = request.SerializeToString()
    pushApplyMessage(604,msg,sendList)
    
def pushScene(placeId,players,monsters):
    '''推送场景信息'''
    if not players:
        return
    from app.scense.protoFile.scene import pushSceneMessage_pb2
    sceneInfo = pushSceneMessage_pb2.pushSceneMessage()
    sendList = []
    for player in players:
        PlayerPosition = sceneInfo.PlayerPosition.add()
        PlayerPosition.id = player.baseInfo.id
        PlayerPosition.name = player.baseInfo.getNickName()
        PlayerPosition.profession = player.profession.getProfessionName()
        GuildInfo = player.guild.getGuildInfo()
        if GuildInfo:
            PlayerPosition.guildname = GuildInfo.get('name','')
        PlayerPosition.figure = player.profession.getSceneFigure()
        if player.baseInfo.id<10000 and random.randint(1,10)==10:
            player.baseInfo.setPosition((random.randint(300,2000),random.randint(450,560)))
        PlayerPosition.x = int(player.baseInfo.getDestination()[0])
        PlayerPosition.y = int(player.baseInfo.getDestination()[1])
        sendList.append(player.dynamicId)
    if not sendList:
        return
    for monster in monsters.values():
        MonsterPosition = sceneInfo.MonsterPosition.add()
        MonsterPosition.id = monster.baseInfo.id
        MonsterPosition.profession = monster.formatInfo['name']
        MonsterPosition.figure  = monster.formatInfo['resourceid']
        MonsterPosition.name = monster.formatInfo['name']
        MonsterPosition.x = int(monster.baseInfo.getPosition()[0])
        MonsterPosition.y = int(monster.baseInfo.getPosition()[1])
    sceneInfo.sceneId = placeId
    msg = sceneInfo.SerializeToString()
    pushApplyMessage(602,msg, sendList)
    
def pushFightMessage(data,sendList):
    '''推送战斗消息'''
    pushApplyMessage(711,data,sendList)
    
    
def pushRoomRoleInfo(sendList,playerInfoList):
    '''推送房间角色信息'''
    response = GetRoleOfRoomInfo_pb2.GetRoleOfRoomInfoResponse()
    for playerInfo in playerInfoList:
        role = response.roleOfRoomInfo.add()
        if not playerInfo:
            continue
        role.roleId = playerInfo['roleId']
        role.roleLevel = playerInfo['roleLevel']
        role.roleName = playerInfo['roleName']
        role.roleWork = playerInfo['roleWork']
        role.isRoomOwner = playerInfo['isRoomOwner']
        role.isReady = playerInfo['isReady']
    msg = response.SerializeToString()
    pushApplyMessage(1806, msg, sendList)
    
def pushRoomMatrixInfo(sendList,matrixInfo):
    '''推送房间的阵法信息'''
    response = pushRoomMatrixInfo_pb2.RoomMatrixInfo()
    
    response.matrixId = matrixInfo['matrixId']
    response.matrixname = matrixInfo['matrixname']
    response.description = matrixInfo['description']
    response.noweffect = matrixInfo['noweffect']
    eyeList = matrixInfo['frontEyeList']
    for _eye in eyeList:
        frontEye = response.frontEyeList.add()
        frontEye.pos = _eye['pos']
        frontEye.isOpened = _eye['isOpened']
        frontEye.effectPercen = _eye['effectPercen']
        frontEye.isHaveRole = _eye['isHaveRole']
        roleInfo = _eye['roleInfo']
        if roleInfo:
            frontEye.roleInfo.roleId = roleInfo['roleId']
    msg = response.SerializeToString()
    pushApplyMessage(1815, msg, sendList)
    
def pushQuitHallMessage(sendList):
    '''推送离开大厅的消息'''
    response = quitHallMessage_pb2.QuitHallMessage()
    response.signal = 1
    msg = response.SerializeToString()
    pushApplyMessage(1820, msg, sendList)
    
def pushRoomInfo(sendList,roomInfo):
    '''推送房间信息'''
    response = GetRoomInfo1821_pb2.GetRoomInfoResponse()
    response.result = True
    response.data.roomId = roomInfo['roomId']
    response.data.groupName = roomInfo['groupName']
    response.data.groupPassword = roomInfo['groupPassword']
    response.data.copySceneId = roomInfo['copySceneId']
    response.data.copyLevel = roomInfo['copyLevel']
    msg = response.SerializeToString()
    pushApplyMessage(1821, msg, sendList)


def pushChatToObjectList(id,tid):
    '''推送私聊角色列表'''
    from app.scense.protoFile.chat import ChatToObjectListInfo1010_pb2
    from app.scense.core.ChaterLogManager import ChaterLogManager
    from app.scense.core.character.PlayerCharacter import PlayerCharacter
    response=ChatToObjectListInfo1010_pb2.ChatToObjectListResponse()
    clog=ChaterLogManager().addChatLog(id) #获取聊天类
    listid=clog.getFriends()#获取角色私聊对象id列表
    if len(listid)<0:
        return
    player=PlayersManager().getPlayerByID(id)
    if not player:
        #print "推送私聊角色列表时没有角色"+str(id)
        return 
    #print "角色私聊角色列表发送给"+player.baseInfo.getNickName()
    playerid=player.getDynamicId()
    for cid in listid:
        players=PlayersManager().getPlayerByID(cid)
        player1=PlayerCharacter(cid)#角色实例
        info=response.chatObjectInfo.add()
        info.chatObjectId=cid
        info.name=player1.baseInfo.getNickName()
        #print "私聊信息角色列表："+player1.baseInfo.getNickName()
        info.level=str(player1.level._level)
        info.perfession=player1.profession.getProfessionName()
        del player1
        if players:
            if players.baseInfo.getState()>0:
                info.chatObjectPos=Lg().g(316)
            info.chatObjectPos=players.baseInfo.getSceneName().decode('utf8')
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
    from app.scense.protoFile.chat import ServerSendChatInfo1012_pb2
    response=ServerSendChatInfo1012_pb2.ServerSendChatInfoResponse()
    response.id=tid
    response.chatMessage=message
    msg=response.SerializeToString()
    playerto=PlayersManager().getPlayerByID(id) #推送给这个人的角色
    if not playerto:
        return
    dyid=playerto.getDynamicId()
    pushApplyMessage(1012,msg,[dyid])
    
    
def pushCorpsApplication(recCharacterId,sysOpeType,tishiStr,contentStr,caozuoStr,
                         roleId = 0,roleName = u'',icon =0,
                         type = 0,pos=0,curPage = 0,toposition = 0,guaJiInfo={}):
    '''推送角色国申请
    @param roleId: int 申请者的ID
    @param roleName: str 角色的名称
    @param recCharacterId: int 接受消息的角色的ID
    '''
    response = SysOpeCorps2900_pb2.SysOpeCorpsResponse()
    response.roleId = roleId
    response.roleName = roleName
    response.sysOpeType = sysOpeType
    response.icon = icon
    response.type = type
    response.pos = pos
    response.curPage = curPage
    try:
        response.tishiStr = tishiStr
    except Exception:
        response.tishiStr = tishiStr.decode('utf8')
    try:
        response.contentStr = contentStr
    except Exception:
        response.contentStr = contentStr.decode('utf8')
    try:
        response.caozuoStr = caozuoStr
    except Exception:
        response.caozuoStr = caozuoStr.decode('utf8')
    response.toposition = toposition
    if guaJiInfo:
        response.guaJiInfo.exp = guaJiInfo.get('exp',0)
        response.guaJiInfo.time = guaJiInfo.get('time',0)
    msg = response.SerializeToString()
    pushObjectByCharacterId(2900, msg, [recCharacterId])
    
    
    
    