#coding:utf8
'''
Created on 2011-8-18
排队大厅相关接口
@author: lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.matrix.matrixManager import MatrixManager
from app.scense.core.queueHall.Hall import Hall
from app.scense.netInterface.pushObjectNetInterface import pushInviteJoinGroupMsg,pushOtherMessage
from app.scense.core.language.Language import Lg


def enterHall(dynamicId,characterId):
    '''进入排队大厅
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    areahall.getQueueRoomList()
    result = areahall.addPlayer(characterId)
    if result:
        return {'result':True,'message':Lg().g(101)}
    
def getHallInfo(dynamicId,characterId,curPage):
    '''获取大厅信息'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    areahall.addPlayer(characterId)
    data = areahall.getQueueRoomList(curPage)
    player.baseInfo.setStatus(2)
    return {'result':True,'message':Lg().g(101),'data':data}

def CreateGroup(dynamicId,characterId,groupName,minLevel,copySceneId,groupPwd):
    '''创建房间'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if player.baseInfo.getQueueRoom():
        return {'result':False,'message':Lg().g(102)}
    areahall = Hall().getAreaHallById(1)
    areahall.dropPlayer(characterId)
    roomId = areahall.creatQueueRoom(characterId,groupName,minLevel,copySceneId,groupPwd)
    player.baseInfo.setQueueRoom(roomId)
    return {'result':True,'message':Lg().g(103)}
    
def JoinGroup(dynamicId,characterId,groupId,password):
    '''加入房间
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if player.baseInfo.getQueueRoom():
        return {'result':False,'message':Lg().g(102)}
    areahall = Hall().getAreaHallById(1)
    queueroom = areahall.getQueueRoomById(groupId)
    result = queueroom.addmember(characterId,password)
    if result['result']:
        areahall.dropPlayer(characterId)
        player.baseInfo.setQueueRoom(groupId)
    return result

def FastEnterGroup(dynamicId,characterId):
    '''快速加入房间'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if player.baseInfo.getQueueRoom():
        return {'result':False,'message':Lg().g(102)}
    areahall = Hall().getAreaHallById(1)
    result = areahall.FastEnterGroup(player)
    return result

def getRoomMemberInfo(dynamicId,characterId,queueroomId):
    '''获取房间成员信息
    @param dynamicId: int 客户端的动态ID
    @param characterId: int 角色的id号
    @param queueroomId: int 房间号
    '''
    

def getHallWaitPlayerList(dynamicId,characterId,curPage):
    '''获取房间等待玩家列表
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    @param curPage: int 当前页数
    '''
    
    
def quitQueueRoom(dynamicId,characterId,queueroomId):
    '''退出房间
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    @param queueroomId: int 角色所在房间号
    '''
    
def GetUserOrFriendsListInfo(dynamicId,characterId,curPage,dataType):
    '''获取可邀请的玩家列表
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    @param curPage: int 当前的页数
    @param dataType: int 数据类型 0为大厅用户数据1好友
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if dataType==0:
        areahall = Hall().getAreaHallById(1)
        data = areahall.getwaitPlayerList(curPage)
    else:
        areahall = Hall().getAreaHallById(1)
        data = areahall.getwaitPlayerList(curPage)
    return {'result':True,'data':data}
    
    
def LeaveRoom(dynamicId,characterId):
    '''离开房间
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    roomId = player.baseInfo.getQueueRoom()
    if not roomId:
        return {'result':False,'message':Lg().g(104)}
    room = areahall.getQueueRoomById(roomId)
    if not room:
        return {'result':False,'message':Lg().g(104)}
    result = room.dropmember(characterId)
    if result ==-1:
        areahall.dropQueueRoomById(roomId)
    elif result ==1:
        areahall.addPlayer(characterId)
    player.baseInfo.setQueueRoom(0)
    areahall.addPlayer(characterId)
    return {'result':True,'message':Lg().g(105)}
    
def InviteJoinGroup(dynamicId,characterId,roleId):
    '''邀请加入房间
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 邀请者的ID
    @param roleId: int 被邀请者的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    toplayer = PlayersManager().getPlayerByID(roleId)
    if not toplayer:
        return {'result':False,'message':Lg().g(106)}
    if toplayer.baseInfo.getQueueRoom():
        return {'result':False,'message':Lg().g(107)}
    sendList = []
    sendList.append(toplayer.getDynamicId())
    argument = {}
    argument['inviteID']= characterId
    argument['areaID'] = 1
    argument['roomId'] = player.baseInfo.getQueueRoom()
    argument['message'] = Lg().g(108)%player.baseInfo.getNickName()
    pushInviteJoinGroupMsg(sendList,argument)
    return {'result':True,'message':Lg().g(109)}

def InviteJoinGroupAccept(dynamicId,characterId,inviteId,areaId,roomId):
    '''接受邀请
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    @param inviteId: int 邀请者的ID
    @param areaId: int 区域的ID
    @param roomId: int 房间的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    room = areahall.getQueueRoomById(roomId)
    player.baseInfo.setQueueRoom(roomId)
    data = room.addmember(characterId,password='',tag=1)
    if data['result']:
        areahall.dropPlayer(characterId)
    return data

def InviteJoinGroupRefuse(dynamicId,characterId,inviteId):
    '''拒绝邀请
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    @param inviteId: int 邀请者的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    toplayer = PlayersManager().getPlayerByID(inviteId)
    if not toplayer:
        return {'result':False,'message':Lg().g(106)}
    msg = u'玩家%s拒绝了你的邀请'%player.baseInfo.getNickName()
    sendList = []
    sendList.append(toplayer.getDynamicId())
    pushOtherMessage(905, msg, sendList)
    return {'result':True,'message':u''}

def getMatrixsInfo(dynamicId,characterId):
    '''获取阵法列表信息
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = MatrixManager().getMatrixsInfo()
    return {'result':True,'message':'','data':data}

def OpeningMatrix(dynamicId,characterId,matrixId,matrixListInfo):
    '''开启阵法
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    @param matrixId: int 阵法的ID
    @param matrixListInfo: list[(roleID,pos)] 阵法的设置信息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    roomId = player.baseInfo.getQueueRoom()
    if not roomId:
        return {'result':False,'message':Lg().g(104)}
    room = areahall.getQueueRoomById(roomId)
    room.setMatrix(characterId,matrixId,matrixListInfo)
    return {'result':True,'message':Lg().g(247)}

def ReadyForQueueRoom(dynamicId,characterId,readyStatu):
    '''房间准备与取消
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    @param readyStatu: int 要更新的准备状态 0 取消准备 1准备
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    roomId = player.baseInfo.getQueueRoom()
    if not roomId:
        return {'result':False,'message':Lg().g(104)}
    room = areahall.getQueueRoomById(roomId)
    result = room.updateReadyStatu(characterId,readyStatu)
    if not result:
        return {'result':False,'message':u''}
    return {'result':True,'message':u''}

def KickRoomMember(dynamicId,characterId,tocharacterId):
    '''踢出房间成员
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的id
    @param tocharacterId: int 房间成衣店的ID 
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if characterId==tocharacterId:
        return {'result':False,'message':Lg().g(110)}
    areahall = Hall().getAreaHallById(1)
    roomId = player.baseInfo.getQueueRoom()
    if not roomId:
        return {'result':False,'message':Lg().g(104)}
    room = areahall.getQueueRoomById(roomId)
    result = room.dropmember(tocharacterId)
    if result==0:
        return {'result':False,'message':Lg().g(111)}
    return {'result':True,'message':Lg().g(112)}

def StartCopyScene(dynamicId,characterId,vipMatrix):
    '''开始房间副本
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    roomId = player.baseInfo.getQueueRoom()
    if not roomId:
        return {'result':False,'message':Lg().g(104)}
    room = areahall.getQueueRoomById(roomId)
    data = room.startCopyScene(characterId,vipMatrix)
    if data['result']:
        areahall.dropQueueRoomById(roomId)
        player.baseInfo.setStatus(1)
    return data
    
def leaveHall(dynamicId,characterId):
    '''离开大厅
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    roomId = player.baseInfo.getQueueRoom()
    room = areahall.getQueueRoomById(roomId)
    if room:
        room.dropmember(characterId)
    else:
        areahall.dropPlayer(characterId)
    player.baseInfo.setStatus(1)
    return {'result':True}
    
def GetRoomInfo(dynamicId,characterId):
    '''获取房间信息'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    roomId = player.baseInfo.getQueueRoom()
    if not roomId:
        return {'result':False,'message':Lg().g(104)}
    room = areahall.getQueueRoomById(roomId)
    data = room.getRoomInfo()
    return {'result':True,'data':data}

def ModifyRoomInfo(dynamicId,characterId,groupName,groupPassword,copySceneId,copyLevel):
    '''修改房间信息
    @param groupName: str 房间名称
    @param groupPassword: str 房间密码
    @param copySceneId: int 房间的副本
    @param copyLevel: int 副本等级 
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    roomId = player.baseInfo.getQueueRoom()
    if not roomId:
        return {'result':False,'message':Lg().g(104)}
    room = areahall.getQueueRoomById(roomId)
    data = room.ModifyRoomInfo(characterId,groupName,groupPassword,copySceneId,copyLevel)
    return data
    
def CheckMatrixCanUse(dynamicId,characterId,vipMatrix):
    '''验证是否能启用阵法高级效果
    @param dynamicId: int 客户端的动态Id
    @param characterId: int 角色的ID
    @param vipMatrix: int 阵法的效果1(高级阵法)2（白金阵法）3（至尊阵法）
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    areahall = Hall().getAreaHallById(1)
    roomId = player.baseInfo.getQueueRoom()
    if not roomId:
        return {'result':False,'message':Lg().g(104)}
    room = areahall.getQueueRoomById(roomId)
    data = room.updateMatrixEffect(characterId,vipMatrix)
    return data
    
