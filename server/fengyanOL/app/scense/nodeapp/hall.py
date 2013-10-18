#coding:utf8
'''
Created on 2011-8-18
排队大厅外部接口
@author: lan
'''
from app.scense.applyInterface import hall
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.hall import GetGroupInfo_pb2
from app.scense.protoFile.hall import CreateGroup_pb2
from app.scense.protoFile.hall import JoinGroup_pb2
from app.scense.protoFile.hall import FastEnterGroup_pb2
from app.scense.protoFile.hall import GetUserOrFriendsListInfo_pb2
from app.scense.protoFile.hall import LeaveRoom_pb2
from app.scense.protoFile.hall import InviteJoinGroup_pb2
from app.scense.protoFile.hall import InviteJoinGroupAccept_pb2
from app.scense.protoFile.hall import InviteJoinGroupRefuse_pb2
from app.scense.protoFile.hall import getMatrixsInfo_pb2
from app.scense.protoFile.hall import OpeningMatrix_pb2
from app.scense.protoFile.hall import ReadyForQueueRoom_pb2
from app.scense.protoFile.hall import StartCopyScene_pb2
from app.scense.protoFile.hall import KickRoomMember_pb2
from app.scense.protoFile.hall import leaveHall_pb2
from app.scense.protoFile.hall import GetRoomInfo1821_pb2
from app.scense.protoFile.hall import ModifyRoomInfo1822_pb2
from app.scense.protoFile.hall import CheckMatrixCanUse1823_pb2

@nodeHandle
def GetGroupInfo_1801(dynamicId, request_proto):
    argument = GetGroupInfo_pb2.GetGroupInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetGroupInfo_pb2.GetGroupInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    curPage = argument.curPage
    data = hall.getHallInfo(dynamicId, characterId, curPage)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        data = data.get('data')
        response.data.maxPage = data['maxPage']
        response.data.curPage = data['curPage']
        for room in data['roomList']:
            roomInfo = response.data.everyGroupInfo.add()
            roomInfo.groupHallId = room['id']
            roomInfo.groupHallNumber = room['roomNum']
            roomInfo.groupHallClock = room['locked']
            roomInfo.copySceneLevel = room['copySceneLevel']
            roomInfo.groupName = room['groupName']
            roomInfo.curRoleNum = room['curRoleNum']
            roomInfo.copySceneId = room['copySceneId']
    return response.SerializeToString()        

@nodeHandle
def CreateGroup_1802(dynamicId, request_proto):
    '''创建房间'''
    argument = CreateGroup_pb2.CreateGroupRequest()
    argument.ParseFromString(request_proto)
    response = CreateGroup_pb2.CreateGroupResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    groupName = argument.groupName
    minLevel = argument.minLevel
    copyScenceId = argument.copySceneId
    groupPwd = argument.groupPwd
    data = hall.CreateGroup(dynamicId, characterId, groupName, minLevel, copyScenceId, groupPwd)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle     
def JoinGroup_1803(dynamicId, request_proto):
    '''加入排队房间'''
    argument = JoinGroup_pb2.JoinGroupRequest()
    argument.ParseFromString(request_proto)
    response = JoinGroup_pb2.JoinGroupResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    groupId = argument.groupId
    password = argument.password
    data = hall.JoinGroup(dynamicId, characterId, groupId, password)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def FastEnterGroup_1804(dynamicId, request_proto):
    '''快速加入房间'''
    argument = FastEnterGroup_pb2.FastEnterGroupRequest()
    argument.ParseFromString(request_proto)
    response = FastEnterGroup_pb2.FastEnterGroupResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = hall.FastEnterGroup(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def GetUserOrFriendsListInfo_1807(dynamicId, request_proto):
    '''获取可邀请玩家列表'''
    argument = GetUserOrFriendsListInfo_pb2.GetUserOrFriendsListInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetUserOrFriendsListInfo_pb2.GetUserOrFriendsListInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    curPage = argument.curPage
    dataType = argument.dataType
    data = hall.GetUserOrFriendsListInfo(dynamicId, characterId, curPage, dataType)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        data = data.get('data')
        response.data.maxPage = data['maxPage']
        response.data.curPage = data['curPage']
        roleInfoList = data['userOrFriendInfo']
        for role in roleInfoList:
            roleInfo = response.data.userOrFriendInfo.add()
            roleInfo.roleId = role['roleId']
            roleInfo.roleLevel = role['roleLevel']
            roleInfo.roleName = role['roleName']
            roleInfo.roleProfession = role['roleProfession']
    return response.SerializeToString()

@nodeHandle    
def LeaveRoom_1809(dynamicId, request_proto):
    '''离开房间'''
    argument = LeaveRoom_pb2.LeaveRoomRequest()
    argument.ParseFromString(request_proto)
    response = LeaveRoom_pb2.LeaveRoomResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = hall.LeaveRoom(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def InviteJoinGroup_1808(dynamicId, request_proto):
    '''邀请加入房间'''
    argument = InviteJoinGroup_pb2.InviteJoinGroupRequest()
    argument.ParseFromString(request_proto)
    response = InviteJoinGroup_pb2.InviteJoinGroupResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    roleId = argument.roleId
    data = hall.InviteJoinGroup(dynamicId, characterId, roleId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def InviteJoinGroupAccept_1811(dynamicId, request_proto):
    '''接受邀请'''
    argument = InviteJoinGroupAccept_pb2.InviteJoinGroupAcceptRequest()
    argument.ParseFromString(request_proto)
    response = InviteJoinGroupAccept_pb2.InviteJoinGroupAcceptResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    inviteId = argument.inviteId
    areaId = argument.areaId
    roomId = argument.roomId
    data = hall.InviteJoinGroupAccept(dynamicId, characterId, inviteId, areaId, roomId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def InviteJoinGroupRefuse_1812(dynamicId, request_proto):
    '''拒绝邀请'''
    argument = InviteJoinGroupRefuse_pb2.InviteJoinGroupRefuseRequest()
    argument.ParseFromString(request_proto)
    response = InviteJoinGroupRefuse_pb2.InviteJoinGroupRefuseResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    inviteId = argument.inviteId
    data = hall.InviteJoinGroupRefuse(dynamicId, characterId, inviteId)
    if data:
        response.result = data.get('result',False)
        response.message = data.get('message','')
        return response.SerializeToString()

@nodeHandle
def getMatrixsInfo_1813(dynamicId, request_proto):
    '''获取所有的阵法信息'''
    argument = getMatrixsInfo_pb2.getMatrixsInfoRequest()
    argument.ParseFromString(request_proto)
    response = getMatrixsInfo_pb2.getMatrixsInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = hall.getMatrixsInfo(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        data = data.get('data')
        for _mat in data:
            mat = response.data.matrixList.add()
            mat.matrixId = _mat['matrixId']
            mat.matrixname = _mat['matrixname']
            mat.description = _mat['description']
            mat.noweffect = _mat['noweffect']
            eyeList = _mat['frontEyeList']
            for _eye in eyeList:
                frontEye = mat.frontEyeList.add()
                frontEye.pos = _eye['pos']
                frontEye.isOpened = _eye['isOpened']
                frontEye.effectPercen = _eye['effectPercen']
                frontEye.isHaveRole = _eye['isHaveRole']
                roleInfo = _eye['roleInfo']
                if roleInfo:
                    frontEye.roleInfo.roleId = roleInfo['roleId']
                    frontEye.roleInfo.profession = roleInfo['profession']
                    frontEye.roleInfo.rolename = roleInfo['rolename']
                    frontEye.roleInfo.rolelevel = roleInfo['rolelevel']
    return response.SerializeToString()

@nodeHandle
def OpeningMatrix_1814(dynamicId, request_proto):
    '''获取所有的阵法信息'''
    argument = OpeningMatrix_pb2.OpeningMatrixRequest()
    argument.ParseFromString(request_proto)
    response = OpeningMatrix_pb2.OpeningMatrixResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    matrixId = argument.matrixId
    matrixListInfo = argument.matrixListInfo
    data = hall.OpeningMatrix(dynamicId, characterId, matrixId, matrixListInfo)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def ReadyForQueueRoom_1816(dynamicId, request_proto):
    '''房间准备与取消'''
    argument = ReadyForQueueRoom_pb2.ForQueueRoomReques()
    argument.ParseFromString(request_proto)
    response = ReadyForQueueRoom_pb2.ForQueueRoomResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    readyStatu = argument.readyStatu
    data = hall.ReadyForQueueRoom(dynamicId, characterId, readyStatu)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def StartCopyScene_1817(dynamicId, request_proto):
    '''开始房间副本'''
    argument = StartCopyScene_pb2.startCopySceneRequest()
    argument.ParseFromString(request_proto)
    response = StartCopyScene_pb2.startCopySceneResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    vipMatrix = argument.vipMatrix
    
    data = hall.StartCopyScene(dynamicId, characterId,vipMatrix)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def KickRoomMember_1818(dynamicId, request_proto):
    '''踢出房间成员'''
    argument = KickRoomMember_pb2.KickRoomMemberRequest()
    argument.ParseFromString(request_proto)
    response = KickRoomMember_pb2.KickRoomMemberResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    tocharacterId = argument.tid
    data = hall.KickRoomMember(dynamicId, characterId, tocharacterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    msg = response.SerializeToString()
    return msg

@nodeHandle
def leaveHall_1819(dynamicId, request_proto):
    '''离开大厅'''
    argument = leaveHall_pb2.leaveHallRequest()
    argument.ParseFromString(request_proto)
    response = leaveHall_pb2.leaveHallResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = hall.leaveHall(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def GetRoomInfo_1821(dynamicId, request_proto):
    '''获取房间信息'''
    argument = GetRoomInfo1821_pb2.GetRoomInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetRoomInfo1821_pb2.GetRoomInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = hall.GetRoomInfo(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        data = data.get('data')
        response.data.roomId = data['roomId']
        response.data.groupName = data['groupName']
        response.data.groupPassword = data['groupPassword']
        response.data.copySceneId = data['copySceneId']
        response.data.copyLevel = data['copyLevel']
        
    return response.SerializeToString()

@nodeHandle
def ModifyRoomInfo_1822(dynamicId, request_proto):
    '''修改房间信息'''
    argument = ModifyRoomInfo1822_pb2.ModifyRoomInfoRequest()
    argument.ParseFromString(request_proto)
    response = ModifyRoomInfo1822_pb2.ModifyRoomInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    groupName = argument.groupName
    groupPassword = argument.groupPassword
    copySceneId = argument.copySceneId
    copyLevel = argument.copyLevel
    data = hall.ModifyRoomInfo(dynamicId, characterId, groupName, groupPassword, copySceneId, copyLevel)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def CheckMatrixCanUse_1823(dynamicId, request_proto):
    '''验证阵法效果是否能启用'''
    argument = CheckMatrixCanUse1823_pb2.CheckMatrixCanUseRequest()
    argument.ParseFromString(request_proto)
    response = CheckMatrixCanUse1823_pb2.CheckMatrixCanUseResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    vipMatrix = argument.vipMatrix
    data = hall.CheckMatrixCanUse(dynamicId, characterId, vipMatrix)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

    
    
