#coding:utf8
'''
Created on 2012-3-19
场景类
@author: Administrator
'''
from app.scense.utils.dbopera import dbScene,dbNpc,dbPortals
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushApplyMessage

from firefly.utils.singleton import Singleton
from twisted.python import log
import random

from app.scense.protoFile.scene import pushSceneMessage_pb2,\
    EnterSceneMessage_605_pb2,removePlayerInMap_pb2
from app.scense.core.language.Language import Lg
from app.scense.applyInterface import configure
from app.scense.core.campaign import fortress
    
UP = 20

class Scene(object):
    '''基础场景类'''
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''
        @param id: int 公共场景的id
        @param rooms: int 场景数据房间
        '''
        self.rooms = []
        self._name = Lg().g(272)
    
    def initPublicSceneData(self,sid):
        '''初始化公共场景数据
        '''
        sceneInfo = dbScene.ALL_PUBLICSCENE_INFO.get(sid,{})
        if not sceneInfo:
            log.err('public scene %d does not exist'%sid)
            return
        self._id = sid
        self._name = sceneInfo['name']
        self._levelrequired = sceneInfo['levelRequired']
        self._type = sceneInfo['type']
        self._height = sceneInfo['height']#场景的高度
        self._width = sceneInfo['width']#场景的宽度
        self._init_X = sceneInfo['init_X']#场景进入的初始化x坐标
        self._init_Y = sceneInfo['init_Y']#场景进入的初始化x坐标
        self._resourceid = sceneInfo['resourceid']#场景的资源ID
        self._monsters = {} #怪物列表
#        self._playerlist = []#场景角色列表
        self._canRec = set([])#场景能够接受场景消息角色列表
        self._portals = eval('['+sceneInfo['portals']+']')
        self._npclist = eval('['+sceneInfo['npclist']+']')
        self._npclistInfo = [dbNpc.ALL_NPCS.get(npcID) for\
                                 npcID in self._npclist]
        self._portalsInfo = [dbPortals.ALL_PORTALS.get(portalId) for\
                                 portalId in self._portals]
        
    def getSceneGuildName(self):
        '''获取城镇占领国的名称
        '''
        from app.scense.core.campaign.FortressManager import FortressManager
        from app.scense.core.guild.GuildManager import GuildManager
        f = FortressManager().getFortressBySceneId(self._id)
        if not f.isOccupied:
            return ''
        if not f.kimori:
            return ''
        guildId = f.kimori
        guild = GuildManager().getGuildById(guildId)
        return guild.get('name')
    
    def getSceneName(self):
        '''获取场景的名称'''
        return self._name
    
    def getNPCInfoList(self):
        '''获取NPC信息列表
        '''
        guildname = self.getSceneGuildName()
        if not guildname:
            return self._npclistInfo
        npclist = []
        for npcinfo in self._npclistInfo:
            npc = dict(npcinfo)
            npc['name'] = u'【%s】%s'%(guildname,npcinfo['name'])
            npclist.append(npc)
        return npclist
        
        
    def addPlayer(self,playerId):
        '''添加一个角色到当前场景
        @param playerId: int 角色的id
        '''
        if not self.rooms:
            self.rooms.append([])
        tag = 0
        for room in self.rooms:
            if len(room)<UP:
                room.append(playerId)
                return
        if not tag:
            self.rooms.append([])
            self.rooms[-1].append(playerId)
        
    def dropPlayer(self,playerId):
        '''清除场景中的角色
        @param playerId: int 角色的id
        '''
        for room in self.rooms:
            if playerId in room:
                room.remove(playerId)
                sendList = self.getSendList(room)
                self.pushRemovePlayerInMap(playerId, sendList)
                break
        try:
            self._canRec.remove(playerId)
        except Exception:
            pass
        
    def dropPet(self,petId):
        '''移除一个宠物'''
        sendList = self.getAllSendList()
        self.pushRemovePlayerInMap(petId, sendList)
        
    def getInitPosition(self):
        '''获取角色进入的初始坐标'''
        offsetx = random.randint(-400,400)
        offsety = random.randint(-60,60)
        return self._init_X + offsetx,self._init_Y + offsety
        
    def updateAllPlayerLocation(self,rate):
        '''更新场景中所有角色的坐标
        @param rate: int 移动的频率
        '''
        playerList = list(self._canRec)
        for playerId in playerList:
            player = PlayersManager().getPlayerByID(playerId)
            if not player:
                self.dropPlayer(playerId)
                continue
            player.updateLocation(rate)#更新角色的位置
            
    def formatSceneInfo(self):
        '''格式化场景信息'''
        sceneInfo = {}
        sceneInfo['id'] = self._id  #场景的ID
        sceneInfo['resourceId'] = self._resourceid #场景的资源类型
        sceneInfo['sceneType'] = self._type #场景的类型
        sceneInfo['scenename'] = self._name  #场景的名称
        sceneInfo['npclist'] = self.getNPCInfoList() #场景的npc信息
        sceneInfo['portals'] = self._portalsInfo#场景中传送门的信息
        if self._type ==1:#公共场景时
            sceneInfo['corpsName'] = Lg().g(143)
            sceneInfo['rewardCorpsName'] = Lg().g(143)
        elif self._type ==2:#副本场景时
            sceneInfo['corpsName'] = Lg().g(143)
            sceneInfo['rewardCorpsName'] = Lg().g(143)
        return sceneInfo
            
    def pushNowScenePosition(self,sendId,playerID):
        '''推送在场景中当前的所有角色和怪物的坐标
        @param sendId: int 推送的目标ID
        '''
        self._canRec.add(playerID)
        for room in self.rooms:
            if playerID not in room:
                continue
            sceneInfo = pushSceneMessage_pb2.pushSceneMessage()
            for playerId in room:
                player = PlayersManager().getPlayerByID(playerId)
                if not player:
                    continue
                PlayerPosition = sceneInfo.PlayerPosition.add()
                PlayerPosition.id = player.baseInfo.id
                PlayerPosition.name = player.baseInfo.getNickName()
                PlayerPosition.profession = player.profession.getProfessionName()
                PlayerPosition.headicon = player.profession.getFigure()
                GuildInfo = player.guild.getGuildInfo()
                if GuildInfo:
                    PlayerPosition.guildname = GuildInfo.get('name','')
                PlayerPosition.figure = player.profession.getSceneFigure()
                position = player.baseInfo.getPosition()
                PlayerPosition.x = int(position[0])
                PlayerPosition.y = int(position[1])
                PlayerPosition.level = player.level.getLevel()
                PlayerPosition.viptype = player.baseInfo.getType()
                PlayerPosition.gemlevel = player.pack._equipmentSlot.getGemLevel()
                ###############角色展示宠物的处理################
                player.pet.updatePetPosition(position)
                for petId in player.matrix._matrixSetting.values():
                    if petId<=0:
                        continue
                    pet = player.pet.getPet(petId)
                    figure = pet.templateInfo['resourceid']
                    position = pet.getPosition()
                    PetPosition = sceneInfo.petInfo.add()
                    PetPosition.id = petId
                    PetPosition.name = pet.baseInfo.getName()
                    PetPosition.profession = pet.baseInfo.getName()
                    PlayerPosition.headicon = figure
                    PetPosition.figure = figure
                    PetPosition.x = int(position[0])
                    PetPosition.y = int(position[1])
                    PetPosition.masterId = playerId
#                for petId in player.pet._pets.keys():
#                    pet = player.pet.getPet(petId)
#                    flowFlag = pet.getFlowFlag()
#                    if not flowFlag:
#                        continue
#                    figure = pet._baseInfo['resourceid']
#                    position = pet.getPosition()
#                    PetPosition = sceneInfo.petInfo.add()
#                    PetPosition.id = petId
#                    PetPosition.name = pet.getName()
#                    PetPosition.profession = pet.getName()
#                    PetPosition.figure = figure
#                    PetPosition.x = int(position[0])
#                    PetPosition.y = int(position[1])
            sceneInfo.sceneId = self._id
            msg = sceneInfo.SerializeToString()
            pushApplyMessage(602,msg, [sendId])
            return
        
    def pushSceneInfo(self,rate):
        '''给每一个在场景中的玩家推送场景信息
        @param rate: int 移动的频率
        '''
        if not self._canRec:
            return
        self.updateAllPlayerLocation(rate)
        if self._monsters:
            self.updateAllMonsterLocation()
        
        groupState = configure.isteamInstanceTime(20)#组队副本时间判断
        guildFightState = fortress.IsWarTime()#国战时间判断
        
        for room in self.rooms:
            sendlist = []
            sceneInfo = pushSceneMessage_pb2.pushSceneMessage()
            for playerId in room:
                player = PlayersManager().getPlayerByID(playerId)
                if not player:
                    continue
                player.icon.groupIconManager(groupState)#组队战图标管理
                player.icon.guildFightManager(guildFightState)#国战图标管理
                PlayerPosition = sceneInfo.PlayerPosition.add()
                PlayerPosition.id = player.baseInfo.id
                PlayerPosition.name = player.baseInfo.getNickName()
                PlayerPosition.profession = player.profession.getProfessionName()
                PlayerPosition.headicon = player.profession.getFigure()
                GuildInfo = player.guild.getGuildInfo()
                if GuildInfo:
                    PlayerPosition.guildname = GuildInfo.get('name','')
                PlayerPosition.figure = player.profession.getSceneFigure()
                position = player.baseInfo.getDestination()
                PlayerPosition.x = int(position[0])
                PlayerPosition.y = int(position[1])
                PlayerPosition.level = player.level.getLevel()
                PlayerPosition.viptype = player.baseInfo.getType()
                PlayerPosition.gemlevel = player.pack._equipmentSlot.getGemLevel()
                sendlist.append(player.getDynamicId())
                ###############角色展示宠物的处理################
                petremove = player.pet.popLastRemove()
                for petId in petremove:
                    self.dropPet(petId)
                for petId in player.matrix._matrixSetting.values():
                    if petId<=0:
                        continue
                    pet = player.pet.getPet(petId)
                    figure = pet.templateInfo['resourceid']
                    position = pet.getPosition()
                    PetPosition = sceneInfo.petInfo.add()
                    PetPosition.id = petId
                    PetPosition.name = pet.baseInfo.getName()
                    PetPosition.profession = pet.baseInfo.getName()
                    PetPosition.headicon = figure
                    PetPosition.figure = figure
                    PetPosition.x = int(position[0])
                    PetPosition.y = int(position[1])
                    PetPosition.masterId = playerId
            sceneInfo.sceneId = self._id
            msg = sceneInfo.SerializeToString()
            pushApplyMessage(602,msg, sendlist)
        

    def pushEnterPlace(self,sendList):
        '''推送进入场景的信息
        '''
        sceneInfo = self.formatSceneInfo()
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
        
    def pushRemovePlayerInMap(self,playerId,sendList):
        '''通知场景移除玩家'''
        request = removePlayerInMap_pb2.removePlayerInMap()
        request.id = playerId
        msg = request.SerializeToString()
        pushApplyMessage(604,msg,sendList)
        
    def getSendList(self,room):
        '''获取接受场景消息的角色的客户端ID'''
        sendlist = []
        for playerId in room:
            player = PlayersManager().getPlayerByID(playerId)
            if playerId in self._canRec and player and player.baseInfo.getStatus()!=4:
                sendlist.append(player.getDynamicId())
        return sendlist
    
    def getAllSendList(self):
        '''获取接受场景消息的角色的客户端ID'''
        sendlist = []
        for playerId in self._canRec:
            player = PlayersManager().getPlayerByID(playerId)
            if player and player.baseInfo.getStatus()!=4:
                sendlist.append(player.getDynamicId())
        return sendlist
        
        
        