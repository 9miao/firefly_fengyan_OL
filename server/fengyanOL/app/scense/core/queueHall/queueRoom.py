#coding:utf8
'''
Created on 2011-8-17
排队房间
@author: lan
'''
from twisted.internet import reactor
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.team.TeamManager import TeamManager
from app.scense.netInterface.pushObjectNetInterface import pushRoomRoleInfo,\
    pushRoomMatrixInfo,pushEnterPlace,pushQuitHallMessage,pushRoomInfo
from app.scense.core.matrix.matrix import Matrix
from app.scense.applyInterface.instance_app import enterInstance1


reactor = reactor

class QueueRoom:
    '''在排队大厅中的房间'''
    
    def __init__(self,roomowner,groupName,minLevel,copySceneId,groupPwd):
        '''初始化房间
        @param id: int 房间的id
        @param roomowner: int 房主的id
        @param members: list [int] 房间成员列表
        @param formation: int 队形编号
        @param password: str 房间的密码
        @param copySceneId: int 选择副本的ID
        @param roomName: str 房间的名称 
        @param minLevel: int 进入房间满足的最低等级限制
        @param matrix: Matrix object 房间阵法信息
        '''
        self.id = 0
        self.roomowner = roomowner
        self.members = {}
        self.formation = 0
        self.password = groupPwd
        self.copySceneId = 5010
        self.copyLevel = 1
        self.roomName = groupName
        self.minLevel = minLevel
        self.matrix = None
        self.initQueueRoomInfo()
        
    def initQueueRoomInfo(self):
        '''初始化房间信息'''
        self.initMembers()
        self.initMatrix()
    
    def initMembers(self):
        '''初始化房间成员信息'''
        self.members[1] = {'id':self.roomowner,'status':0}
        self.members[2] = None
        self.members[3] = None
        self.members[4] = None
        self.members[5] = None
        self.pushRoomRoleInfo()
        
    def initMatrix(self):
        '''初始化房间阵法'''
        self.matrix = Matrix(100001)
        self.matrix.addMember(self.roomowner)
        
    def setId(self,id):
        '''设置房间的ID'''
        self.id = id
        
    def getId(self):
        '''获取房间的ID'''
        return self.id
    
    def setRoomOwner(self,characterId):
        '''房主的ID'''
        self.roomowner = characterId
    
    def getMinLevel(self):
        '''获取最低等级'''
        return self.minLevel
    
    def setMinLevel(self,minLevel):
        '''设置最低等级'''
        self.minLevel = minLevel
        
    def getCopySceneId(self):
        '''获取房间选择的副本'''
        return self.copySceneId
    
    def setCopySceneId(self,copySceneId):
        '''设置房间的副本'''
        self.copySceneId = copySceneId
        
    def getPassword(self):
        '''获取房间密码'''
        return self.password
    
    def setPassword(self,password):
        '''设置房间密码'''
        self.password = password
    
    def getmembers(self):
        '''获取成员列表'''
        return self.members
    
    def findSpace(self):
        '''寻找房间空余座位'''
        for key in self.members.keys():
            if not self.members[key]:
                return key
        return 0
    
    def findNewOwner(self):
        '''寻找新的房主'''
        for key in self.members.keys():
            if self.members[key]:
                return self.members[key]['ID']
        return 0
    
    def areAllReady(self):
        '''判断是否所有的玩家都已经准备好了'''
        for key in self.members.keys():
            if self.members[key] and (not self.members[key]['status'] and self.members[key]['id'] !=self.roomowner):
                return False
        return True
    
    def findMemberSpace(self,characterId):
        '''查找成员在房间中的位置'''
        for key in self.members.keys():
            if self.members[key] and self.members[key]['id']==characterId:
                return key
        return 0
    
    def addmember(self,playerId,password,tag = 0):
        '''添加房间成员'''
        player = PlayersManager().getPlayerByID(playerId)
        result = self.checkCanJoin(player, password=password,tag = tag)
        if not result['result']:
            return result
        space = self.findSpace()
        self.members[space] = {'id':player.baseInfo.id,'status':0}
        self.pushRoomRoleInfo()
        if self.matrix:
            self.matrix.addMember(playerId)
            self.pushRoomMatrixInfo()
        return {'result':True}
        
    def dropmember(self,characterId):
        '''开除房间成员'''
        try:
            space = self.findMemberSpace(characterId)
            if not space:
                return 0
            self.members[space] = None
            if characterId == self.roomowner:
                newowner = self.findNewOwner()
                if not newowner:
                    return -1
                self.setRoomOwner(newowner)
            if self.matrix:
                self.matrix.dropMember(characterId)
                self.pushRoomMatrixInfo()
            self.pushRoomRoleInfo()
            return 1
        except Exception as e:
            #print e
            return 0
    
    def formatRoomInfo(self,roomNum=0):
        '''格式化房间信息'''
        info = {}
        info['id'] = self.id
        info['roomNum'] = roomNum
        info['locked'] = len(self.password)!=0
        info['groupName'] = self.roomName
        info['curRoleNum'] = len([m for m in self.members.values() if m])
        info['copySceneLevel'] = 0
        info['copySceneId'] = self.copySceneId
        return info
        
    def checkCanJoin(self,player,password = "",tag=0):
        '''检测角色是否可以加入'''
        if not tag:
            if password != self.getPassword():
                return {'result':False,'message':u'密码不正确'}
        if player.level.getLevel()< self.getMinLevel():
            return {'result':False,'message':u'不符合房间需求等级'}
        if self.members.has_key(player.baseInfo.id):
            return {'result':False,'message':u'你已经在房间中'}
        if not self.findSpace():
            return {'result':False,'message':u'房间已满'}
        return {'result':True,'message':u'可以加入'}
    
    def pushRoomRoleInfo(self):
        '''推送房间中角色的信息'''
        sendList = []
        playerListInfo = []
        for key in self.members.keys():
            member = self.members[key]
            if not member:
                playerListInfo.append(None)
                continue
            player = PlayersManager().getPlayerByID(member['id'])
            if not player:
                self.dropmember(member['id'])
                continue
            sendList.append(player.getDynamicId())
            info = {}
            info['roleId']= member['id']
            info['roleLevel'] = player.level.getLevel()
            info['roleName'] = player.baseInfo.getNickName()
            info['roleWork'] = player.profession.getFigure()
            info['isRoomOwner'] = member['id']==self.roomowner
            info['isReady'] = bool(member['status'])
            info['roleSkillInfo'] = []
            playerListInfo.append(info)
        reactor.callLater(0,pushRoomRoleInfo,sendList,playerListInfo)
        
    def setMatrix(self,roleId,matrixId,matrixListInfo):
        '''设置阵法'''
        if roleId!=self.roomowner:
            return {'result':False,'message':u'只有房主能'}
        self.matrix = Matrix(matrixId)
        for eye in matrixListInfo:
            self.matrix.setFrontEye(eye.pos,eye.roleId)
        self.pushRoomMatrixInfo()
        
    def pushRoomMatrixInfo(self):
        '''推送房间阵法的信息'''
        matrixInfo = self.matrix.fromatMatrixInfo()
        sendList = []
        for key in self.members.keys():
            member = self.members[key]
            if not member:
                continue
            player = PlayersManager().getPlayerByID(member['id'])
            if player:
                sendList.append(player.getDynamicId())
        pushRoomMatrixInfo(sendList, matrixInfo)
        
    def updateReadyStatu(self,characterId,readyStatu):
        '''更新角色准备状态
        @param chracterId: int 角色的ID
        @param readyStatu: int 准备状态  1准备 0 取消
        '''
        for key in self.members.keys():
            if self.members[key]['id'] == characterId:
                self.members[key]['status'] = readyStatu
                self.pushRoomRoleInfo()
                return True
        return False
    
    def startCopyScene(self,characterId,vipMatrix):
        '''开始副本
        @param chracterId: 角色的ID
        '''
        if characterId != self.roomowner:
            return {'result':False,'message':u'只有房主有权限'}
        if not self.areAllReady():
            return {'result':False,'message':u'还有玩家没有准备好'}
        player = PlayersManager().getPlayerByID(characterId)
        
        if vipMatrix ==1:
            if player.finance.getCoin()>=5000:
                self.matrix.setNowEffect(vipMatrix)
                player.finance.updateCoin(player.finance.getCoin() -5000)
        elif vipMatrix ==2:
            if player.finance.getGold()>=10:
                self.matrix.setNowEffect(vipMatrix)
                player.finance.updateGold(player.finance.getGold() -10)
        elif vipMatrix ==3 :
            if player.finance.getGold()>=50:
                self.matrix.setNowEffect(vipMatrix)
                player.finance.updateGold(player.finance.getGold() -50)
        
        sendList = []
        if len([member for member in self.members.values() if member])>1:
            team = TeamManager().creatTeam(characterId)
            team.setMatrix(self.matrix)
            for member in self.members.values():
                if member:
                    pp = PlayersManager().getPlayerByID(member['id'])
                    if pp:
                        sendList.append(pp.getDynamicId())
                    team.addMember(member['id'])
        data = enterInstance1(0, characterId, self.copySceneId)
        if data['result']:
            player = PlayersManager().getPlayerByID(characterId)
            dynamicId = player.getDynamicId()
            pushQuitHallMessage(sendList)
            pushEnterPlace(data['data'].get('placeId'), [dynamicId])
        return data
        
    def getRoomInfo(self):
        '''获取房间信息'''
        data = {}
        data['roomId'] = self.id
        data['groupName'] = self.roomName
        data['groupPassword'] = self.password
        data['copySceneId'] = self.copySceneId
        data['copyLevel'] = self.copyLevel
        return data
    
    def ModifyRoomInfo(self,characterId,groupName,groupPassword,copySceneId,copyLevel):
        '''修改房间信息'''
        if characterId != self.roomowner:
            return {'result':False,'message':u'只有房主有权限'}
        self.roomName = groupName
        self.password = groupPassword
        self.copySceneId = copySceneId
        self.copyLevel = copyLevel
        roomInfo = self.getRoomInfo()
        sendList = []
        for key in self.members.keys():
            member = self.members[key]
            if not member:
                continue
            player = PlayersManager().getPlayerByID(member['id'])
            if player:
                sendList.append(player.getDynamicId())
        pushRoomInfo(sendList, roomInfo)
        return {'result':True}
        
    def updateMatrixEffect(self,characterId,matrixEffect):
        '''更新阵法的效果
        @param matrixEffect: 阵法的效果
        '''
        if characterId != self.roomowner:
            return {'result':False,'message':u'只有房主有权限'}
        player = PlayersManager().getPlayerByID(characterId)
        if matrixEffect ==1 and player.finance.getCoin()>=5000:
            return {'result':True}
        elif matrixEffect ==2 and player.finance.getGold()>=10:
            return {'result':True}
        elif matrixEffect ==3 and player.finance.getGold()>=50:
            return {'result':True}
        else:
            return {'result':False,'message':u'资金不足'}
            
            
            
    
    
    
    
    
        