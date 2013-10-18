#coding:utf8
'''
Created on 2011-8-18
区域大厅
@author: lan
'''
from app.scense.core.queueHall.queueRoom import QueueRoom
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.language.Language import Lg

class AreaHall:
    '''区域大厅'''
    
    def __init__(self,id):
        '''
        @param id: int 区域的ID
        @param copySenceList: int 区域副本列表
        '''
        self.id = id
        self.copySenceList = []
        self.waitPlayers = []
        self.queueRooms = {}
        self.tag = 1000
        
    def addPlayer(self,characterId):
        '''添加玩家到区域大厅'''
        if self.waitPlayers.count(characterId):
            return False
        self.waitPlayers.append(characterId)
        return True
        
    def dropPlayer(self,characterId):
        '''清除区域大厅中的玩家'''
        if not self.waitPlayers.count(characterId):
            return False
        self.waitPlayers.remove(characterId)
        return True
        
    def addQueueRoom(self,queueroom):
        '''填加一个房间到房间列表'''
        self.tag += 1
        queueroom.setId(self.tag)
        self.queueRooms[self.tag] = queueroom
        
    def dropQueueRoomById(self,roomId):
        '''关闭一个房间'''
        try:
            del self.queueRooms[roomId]
        except Exception as e:
            pass
        
        
    def getQueueRoomById(self,roomId):
        '''根据Id获取'''
        return self.queueRooms.get(roomId,None)
        
    def creatQueueRoom(self,characterId,roomName,minLevel,copySceneId,password):
        '''创建区域房间
        @param characterId: int 创建者的Id
        @param roomName: str 房间的名称
        @param minlevel: int 房间的等级下线
        @param password: str 房间的密码
        ''' 
        room = QueueRoom( characterId, roomName, minLevel,copySceneId ,password)
        self.addQueueRoom(room)
        room.pushRoomMatrixInfo()
        return room.getId()
    
    def getQueueRoomList(self,curPage,limit = 10):
        '''获取排队房间列表'''
        resultInfo = {}
        roomlistInfo = []
        allroomList = self.queueRooms.values()
        roomList = allroomList[(curPage-1)*limit:curPage*limit]
        for i in range(len(roomList)):
            room = roomList[i]
            info = room.formatRoomInfo(roomNum=i+1+(curPage-1)*limit)
            roomlistInfo.append(info)
        resultInfo['roomList'] = roomlistInfo
        resultInfo['maxPage'] = len(allroomList)/limit + 1
        resultInfo['curPage'] = curPage
        return resultInfo
        
    def FastEnterGroup(self,player):
        '''快速加入'''
        for room in self.queueRooms.values():
            result = room.checkCanJoin(player)
            if result['result']:
                self.dropPlayer(player.baseInfo.id)
                return {'result':True,'message':Lg().g(572)}
        roomId = self.creatQueueRoom(player.baseInfo.id, u'', 1,281000, "")
        newroom = self.getQueueRoomById(roomId)
        newroom.pushRoomMatrixInfo()
        player.baseInfo.setQueueRoom(roomId)
        self.dropPlayer(player.baseInfo.id)
        return {'result':True,'message':Lg().g(573)}
    
    def getwaitPlayerList(self,curPage,limit=10):
        '''获取大厅等待玩家列表'''
#        import random
        data = {}
        data['maxPage']= len(self.waitPlayers)/limit+1
        data['curPage'] = curPage
        data['userOrFriendInfo'] = []
        roleIdList = self.waitPlayers[(curPage-1)*limit:curPage*limit]
        for role in roleIdList:
            player = PlayersManager().getPlayerByID(role)
            if not player:
                self.dropPlayer(role)
                continue
            info = {}
            info['roleId'] = role
            info['roleLevel'] = player.level.getLevel()
            info['roleName'] = player.baseInfo.getNickName()
            info['roleProfession'] = player.profession.getFigure()
            data['userOrFriendInfo'].append(info)
        return data
    
    
