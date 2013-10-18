#coding:utf8
'''
Created on 2012-12-6

@author: lan
'''
from app.scense.utils.dbopera import dbNpc,dbMap
from twisted.python import log
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.character.Monster import Monster
from app.scense.netInterface.pushObjectNetInterface import pushRemovePlayerInMap,\
    pushApplyMessage
from app.scense.protoFile.scene import pushSceneMessage_pb2,EnterSceneMessage_605_pb2
from app.scense.netInterface.pushPrompted import pushPromptedMessage
from app.scense.core.fight.battleSide import BattleSide
from app.scense.core.language.Language import Lg
from app.scense.serverconfig.chatnode import pushSystemInfo
#from serverconfig.chatnode import chatnoderemote 
from app.scense.applyInterface import dropout
import random


GAPX = 100#随机差距
GAPY = 30
HEIGHT = 325
DISTANCE = 0 #怪物的视力范围
MOVERATE = 2  #怪物的移动频率
HEIGHT = 325


class BaseMap(object):
    '''基础地图类'''
    
    def __init__(self,mid):
        '''
        @param id: int 地图的ID
        '''
        self._id = mid#场景的ID
        self._name = ''#场景的名称
        self._country = 1#场景所属的国家
        self._level = 0#场景进入的等级限制
        self._member_cnt = 500#场景的最大人数限制
        self._height = 2000#场景的高度
        self._width = 2000#场景的宽度
        self._resourceid = 1000#场景的资源ID
        self._npclist = [] #场景的npc资源
        self._portals = [] #传送门列表
        self._playerlist = set([]) #角色列表
        self._canRec = set([]) #能够接受场景消息的角色的ID的列表
        self._monsters = {} #场景中的怪物列表
        self._tag = 1000 #怪物的起始ID
        self._movetag = 1 #控制怪物的移动频率
        self._killed = [] #记录被杀死的怪物，一遍下次定时刷怪
        self.initMap()
        
    def initMap(self):
        '''初始化地图的信息
        '''
        sceneInfo = dbMap.ALL_MAP_INFO.get(self._id)
        if not sceneInfo:
            log.err('map %d does not exist'%self._id)
            return
        self._name = sceneInfo['name']
        self._level = sceneInfo['level']
        self._member_cnt = sceneInfo['member_cnt']
        self._height = sceneInfo['height']
        self._width = sceneInfo['width']
        self._resourceid = sceneInfo['resourceid']
        self._npclist = [npc['id'] for npc in dbNpc.ALL_NPCS.values() \
                                if npc['sceneId']==self._id]
        self._portals = [door['id'] for door in dbMap.ALL_DOOR_INFO.values() \
                                if door['mapid']==self._id]
        self._killed = [(mconfig['id'],0) for mconfig in dbMap.ALL_MAP_MONSTER.values() \
                            if mconfig['map_id'] ==self._id]
        self._mProducers = self.produceMonster()
        self._mProducers.next()
        
    def getID(self):
        '''获取场景的ID'''
        return self._id
    
    def getSceneName(self):
        '''获取场景的名称'''
        return self._name
    
    def getCamp(self):
        '''获取场景所属阵营
        '''
        from app.scense.core.campaign.FortressManager import FortressManager
        f = FortressManager().getFortressBySceneId(self._id)
        if not f:
            return 0
        if not f.isOccupied:
            return 0
        if not f.kimori:
            return 0
        guildId =f.kimori
        return guildId
    
    def getSceneGuildName(self):
        '''获取城镇占领国的名称
        '''
        from app.scense.core.campaign.FortressManager import FortressManager
        from app.scense.core.guild.GuildManager import GuildManager
        f = FortressManager().getFortressBySceneId(self._id)
        if not f:
            return ''
        if not f.isOccupied:
            return ''
        if not f.kimori:
            return ''
        guildId = f.kimori
        guild = GuildManager().getGuildById(guildId)
        return guild.name
    
    def getNPCInfoList(self):
        '''获取NPC信息列表
        '''
        guildname = self.getSceneGuildName()
        if not guildname:
            return [npc for npc in dbNpc.ALL_NPCS.values() \
                                if npc['sceneId']==self._id]
        npclist = []
        for npcid in self._npclist:
            npcinfo = dbNpc.ALL_NPCS.get(npcid)
            _npcinfo = dict(npcinfo)
            _npcinfo['name'] = u'【%s】%s'%(guildname,npcinfo['name'])
            npclist.append(_npcinfo)
        return npclist
    
    def formatSceneInfo(self):
        '''格式化场景信息'''
        sceneInfo = {}
        sceneInfo['id'] = self._id  #场景的ID
        sceneInfo['resourceId'] = self._resourceid #场景的资源类型
        sceneInfo['sceneType'] = 1 #场景的类型
        sceneInfo['scenename'] = self._name  #场景的名称
        sceneInfo['npclist'] = self.getNPCInfoList() #场景的npc信息
        sceneInfo['portals'] = [dbMap.ALL_DOOR_INFO.get(portalId) for\
                                 portalId in self._portals] #场景中传送门的信息
        return sceneInfo
    
    def getSendList(self):
        '''获取可发送的客户端列表'''
        sendList = []
        for pId in self._playerlist:
            pl = PlayersManager().getPlayerByID(pId)
            if pl and (pId in self._canRec) and pl.baseInfo.getStatus()!=4:
                sendList.append(pl.getDynamicId())
        return sendList
    
    def KilledMonster(self,mconfigId,monstertag):
        '''记录被杀死的怪物
        @param mconfigId: int 被杀死的怪物的配置ID
        '''
        if monstertag < 10:
            self._killed.append((mconfigId,300))
        else:
            self._killed.append((mconfigId,10))
        self.dropMonster(monstertag)
        
    def addMonster(self,monster):
        '''添加一个怪物
        @param monster: Monster instance 怪物的实例
        '''
        if self._monsters.has_key(monster.baseInfo.id):
            raise Exception("系统记录冲突")
        self._monsters[monster.baseInfo.id] = monster
        self._tag +=1
        
    
    def produceMonster(self):
        '''产生怪物
        '''
        while True:
            mconfigId = yield
            configinfo = dbMap.ALL_MAP_MONSTER.get(mconfigId)
            templateId = configinfo.get('monster')
            position = (configinfo.get('position_x'),configinfo.get('position_y'))
            rule = configinfo.get('rule',[])
            monster = Monster(id = self._tag,templateId = templateId)
            monster.baseInfo.setStaticPosition(position)
            monster.setRule(rule)
            monster.setMconfig(mconfigId)
            self.addMonster(monster)
            
    def produce(self):
        '''定时生成怪物
        '''
        _killed = []
        for mconfigid,delta in self._killed:
            if delta==0:
                self._mProducers.send(mconfigid)
            else:
                delta -= 1
                _killed.append((mconfigid,delta))
        self._killed = _killed
        
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
        
    def addPlayer(self,playerId):
        '''添加一个角色到当前场景
        @param playerId: int 角色的id
        '''
        self._playerlist.add(playerId)
        self.checkPlayerCamp(playerId)
        
    def checkPlayerCamp(self,playerId):
        '''检测角色的阵营是否属于本场景，不是发出警告
        '''
        player = PlayersManager().getPlayerByID(playerId)
        camp = player.guild.getID()
        mapCamp = self.getCamp()
        if camp!=0 and camp!=mapCamp and mapCamp!=0:#发出警告
            guildname = player.guild.getGuildName()
            nickname = player.baseInfo.getName()
            pushSystemInfo(u'%s国的【%s】进入%s境内'%(guildname,nickname,self._name))
        
    def dropPlayer(self,playerId,sendList = []):
        '''清除场景中的角色
        @param playerId: int 角色的id
        '''
        try:
            if playerId in self._playerlist:
                self._playerlist.remove(playerId)
                self._canRec.remove(playerId)
        except Exception,e:
            log.msg(e)
        if not sendList:
            sendList = self.getSendList()
        pushRemovePlayerInMap(playerId,sendList)
        
    def dropPet(self,petId):
        '''移除一个宠物'''
        sendList = self.getSendList()
        pushRemovePlayerInMap(petId, sendList)
        
    def dropMonster(self,monsterId):
        '''移除场景中的一个怪物
        '''
        try:
            del self._monsters[monsterId]
            pushRemovePlayerInMap(monsterId,\
                [PlayersManager().getPlayerByID(player).getDynamicId()\
                  for player in self._playerlist])
        except Exception,e:
            log.msg('delete monster %d error! %s'%(monsterId,e))
            return
        
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
            
    def updateAllMonsterLocation(self):
        '''更新场景中所有怪物的坐标
        '''
        self._movetag +=1
        tag = 0
        for player in self._playerlist:#如果副本中有人在战斗，所有怪物停止移动
            pl = PlayersManager().getPlayerByID(player)
            if pl.baseInfo.getStatus()==4:
                return
        for monster in self._monsters.values():
            hasMove = 0
            if not monster.getMoveable():#判断怪物在场景能否移动
                continue
            mposition = monster.baseInfo.getStaticPosition()
            _nmposition = monster.baseInfo.getPosition()
            for playerId in self._playerlist:
                pposition = PlayersManager().getPlayerByID(playerId).baseInfo.getPosition()
                if abs(mposition[0]-pposition[0])<DISTANCE and abs(mposition[1]-pposition[1])<DISTANCE:
                    hasMove = 1
                    monster.baseInfo.setPosition(pposition)
                    continue
                if not hasMove and self._movetag>=MOVERATE:
                    tag = 1
                    if random.randint(-1,2)>0:
                        monster.updateLocation()
        if tag:
            self._movetag=0
        
    def pushSceneInfo(self,rate):
        '''给每一个在场景中的玩家推送场景信息
        @param rate: int 移动的频率
        '''
        if not self._playerlist:
            return
        self.updateAllPlayerLocation(rate)
        if self._monsters:
            self.updateAllMonsterLocation()
        from app.scense.core.campaign.FortressManager import FortressManager
        fortress = FortressManager().getFortressBySceneId(self.getID())
        if fortress:
            sceneCamp = fortress.kimori
        else:
            sceneCamp = 0
        sendlist = self.getSendList()
        sceneInfo = pushSceneMessage_pb2.pushSceneMessage()
        for playerId in self._playerlist:
            player = PlayersManager().getPlayerByID(playerId)
            camp = player.guild.getID()
            if not player:
                self.dropPlayer(playerId)
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
            position = player.baseInfo.getDestination()
            PlayerPosition.x = int(position[0])
            PlayerPosition.y = int(position[1])
            PlayerPosition.level = player.level.getLevel()
            PlayerPosition.viptype = player.baseInfo.getType()
            PlayerPosition.gemlevel = player.pack._equipmentSlot.getGemLevel()
            PlayerPosition.currentHP = player.attribute.getHp()
            PlayerPosition.MaxHP = player.attribute.getMaxHp()
            PlayerPosition.camp = camp
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
                PetPosition.name = player.baseInfo.getNickName()+u'·'+pet.baseInfo.getName()
                PetPosition.profession = pet.baseInfo.getName()
                PetPosition.headicon = figure
                PetPosition.figure = figure
                PetPosition.x = int(position[0])
                PetPosition.y = int(position[1])
                PetPosition.masterId = playerId
                PetPosition.currentHP = pet.attribute.getHp()
                PetPosition.MaxHP = pet.attribute.getMaxHp()
                PetPosition.camp = camp
                
        for monster in self._monsters.values():
            MonsterPosition = sceneInfo.MonsterPosition.add()
            MonsterPosition.id = monster.baseInfo.id
            MonsterPosition.profession = monster.formatInfo['name']
            MonsterPosition.figure  = monster.formatInfo['resourceid']
            MonsterPosition.name = monster.formatInfo['name']
            MonsterPosition.x = int(monster.baseInfo.getPosition()[0])
            MonsterPosition.y = int(monster.baseInfo.getPosition()[1])
            MonsterPosition.currentHP = monster.formatInfo['maxHp']
            MonsterPosition.MaxHP = monster.formatInfo['maxHp']
            MonsterPosition.camp = sceneCamp if sceneCamp and monster.baseInfo.id<10 else -1
        sceneInfo.sceneId = self._id
        msg = sceneInfo.SerializeToString()
        pushApplyMessage(602,msg, sendlist)
        
    def pushNowScenePosition(self,sendId,playerID):
        '''推送在场景中当前的所有角色和怪物的坐标
        @param sendId: int 推送的目标ID
        '''
        from app.scense.core.campaign.FortressManager import FortressManager
        fortress = FortressManager().getFortressBySceneId(self.getID())
        if fortress:
            sceneCamp = fortress.kimori
        else:
            sceneCamp = 0
        self._canRec.add(playerID)
        sceneInfo = pushSceneMessage_pb2.pushSceneMessage()
        for playerId in self._playerlist:
            player = PlayersManager().getPlayerByID(playerId)
            camp = player.guild.getID()
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
            PlayerPosition.currentHP = player.attribute.getHp()
            PlayerPosition.MaxHP = player.attribute.getMaxHp()
            PlayerPosition.camp = camp
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
                PetPosition.name = player.baseInfo.getNickName()+u'·'+pet.baseInfo.getName()
                PetPosition.profession = pet.baseInfo.getName()
                PetPosition.headicon = figure
                PetPosition.figure = figure
                PetPosition.x = int(position[0])
                PetPosition.y = int(position[1])
                PetPosition.masterId = playerId
                PetPosition.currentHP = pet.attribute.getHp()
                PetPosition.MaxHP = pet.attribute.getMaxHp()
                PetPosition.camp = camp
        
        for monster in self._monsters.values():
            MonsterPosition = sceneInfo.MonsterPosition.add()
            MonsterPosition.id = monster.baseInfo.id
            MonsterPosition.profession = monster.formatInfo['name']
            MonsterPosition.figure  = monster.formatInfo['resourceid']
            MonsterPosition.name = monster.formatInfo['name']
            MonsterPosition.x = int(monster.baseInfo.getPosition()[0])
            MonsterPosition.y = int(monster.baseInfo.getPosition()[1])
            MonsterPosition.currentHP = monster.formatInfo['maxHp']
            MonsterPosition.MaxHP = monster.formatInfo['maxHp']
            MonsterPosition.camp = sceneCamp if sceneCamp and monster.baseInfo.id<10 else -1
        sceneInfo.sceneId = self._id
        msg = sceneInfo.SerializeToString()
        pushApplyMessage(602,msg, [sendId])
        
    def checkCanFight(self,monsterId,playerId):
        '''检测是否能进行战斗
        '''
        if monsterId > 10:
            return True
        player = PlayersManager().getPlayerByID(playerId)
        camp = player.guild.getID()
        if camp==0:
            return False
        from app.scense.core.campaign.FortressManager import FortressManager
        f = FortressManager().getFortressBySceneId(self._id)
        if not f.isOccupied:
            mapcamp = 0#fortressInfo.get('kimori')
        else:
            mapcamp = f.kimori
        if mapcamp == camp:
            return False#不能攻击同国家的旗帜
        if monsterId == 1:
            if set([2,3,4,5])&(set(self._monsters.keys())):
                return False#副旗没砍掉之前不能攻击主旗
        return True
        
    def FightInScene(self,monsterId,now_X,playerId):
        '''副本战斗
        @param monsterId: int 怪物的id
        @param now_X: int 碰撞点的x坐标
        '''
        from app.scense.core.fight.fight_new import Fight
        if not self._monsters:
            return {'result':False,'message':u'不存在怪物实例'}
#        if not self.checkCanFight(monsterId, playerId):
#            return {'result':False,'message':u'无法进行攻击'}
        fightInfo = {}
        fightType = 1
        sendList = self.getSendList()
        players = [PlayersManager().getPlayerByID(playerId)]
        monster = self._monsters.get(monsterId,None)
        deffen = []
        guildname = players[0].guild.getGuildName()
        if not monster:
            return {'result':False,'message':u'不存在怪物实例'}
        if monsterId <10:
            pushSystemInfo(u'%s正在遭受%s国攻击'%(self._name,guildname))
        msgsendList = []
        for pp in players:#如果有抓宠技能则消耗相应的道具
            pp.skill.autoUnloadCatch()
            if pp.skill.checkHasEquipCatchSkill():
                level = pp.skill.getCatchPetLevel()
                itemTemplateID = pp.skill.CATCHCONSUME.get(level,0)
                msgsendList.append(pp.getDynamicId())
                if itemTemplateID:
                    pp.pack.delItemByTemplateId(itemTemplateID,1)
        
        if monster.formatInfo['difficulty']==5 and msgsendList:
            msg = Lg().g(574)
            pushPromptedMessage(msg, msgsendList)
        challengers = BattleSide(players)
        ruleInfo = monster.getRule()
        if not ruleInfo:
            deffen.append(monster)
            defenders = BattleSide(deffen)
        else:
            temlist,rule = ruleInfo[0],ruleInfo[1]
            i = 100
            for tem in temlist:
                i+=1
                _monser = Monster(id = i,templateId = tem)
                deffen.append(_monser)
            defenders = BattleSide(deffen,state = 0)
            defenders.setMatrixPositionBatch(rule)
        #获取战场中心位置
        realcenter = self._width/2
        data = Fight( challengers, defenders, realcenter)
        data.DoFight()
        
        #战后处理
        if data.battleResult == 1:
            mconfigId = monster.getMconfig()
            self.KilledMonster(mconfigId, monsterId)
        elif data.battleResult == 3:
            fightType = 3
            monster = self._monsters[monsterId]
            for player in self._playerlist:
                pl = PlayersManager().getPlayerByID(player)
                pl.baseInfo.initPosition((300,300))
            monster.baseInfo.initPosition(monster.baseInfo.getStaticPosition())
        elif data.battleResult == 2:
            fightType = 2
            monster = self._monsters[monsterId]
            for player in self._playerlist:
                pl = PlayersManager().getPlayerByID(player)
#                pl.baseInfo.initPosition((300,300))
            monster.baseInfo.initPosition(monster.baseInfo.getStaticPosition())
            
        settlementData = []
        dropoutid = monster.formatInfo['dropoutid']
        for player in data.fighters.values():
            if player['characterType']==2:#怪物
                currentHp = player['chaCurrentHp']
            if player['characterType']==3:#宠物
                pet = PlayersManager().getPlayerByID(playerId).pet._pets.get(player['chaId'])
                pet.attribute.updateHp(int(player['chaCurrentHp']))#更新宠物的血量
                if data.battleResult == 1:
                    exp = monster.formatInfo.get('expbound',100)*len(deffen)
                    pet.level.addExp(exp)
                continue
            if player['characterType']==1:
                pp = PlayersManager().getPlayerByID(player['chaId'])
                if data.battleResult == 1:
                    dropoutIitem = dropout.getDropByid(dropoutid)
                    info = {}
                    info['id'] = player['chaId']
                    info['name'] = player['chaName']
                    info['profession'] = player['figureType']
                    info['expBonus'] = monster.formatInfo.get('expbound',100)*len(deffen)
                    info['coinBonus'] = 0
                    info['goldBonus'] = 0
                    info['itemsBonus'] = dropoutIitem#None#getDropByid(1)
                    info['popularity'] = 0
                    info['attackGoal'] = 0
                    info['defenseGoal'] = 0
                    info['slayGoal'] = 0
                    settlementData.append(info)
                    expEff = pp.attribute.getExpEff()#经验加成
                    pp.level.updateExp(pp.level.getExp()+info['expBonus']*expEff,state = 0)
                    pp.finance.updateCoin(pp.finance.getCoin()+info['coinBonus'],state = 0)
                    pp.finance.updateGold(pp.finance.getGold()+info['goldBonus'],state = 0)
                    if info['itemsBonus']:
                        pp.pack.putNewItemInPackage(info['itemsBonus'],state=0)
                    for monster in deffen:
                        pp.quest.killMonster(monster.templateId)
                pp.attribute.updateHp(int(player['chaCurrentHp']),state = 0)
                pp.effect.doEffectHot()#执行效果战后处理
            
        fightInfo['fightType'] = fightType
        fightInfo['battle'] = data
        fightInfo['sendList'] = sendList
        fightInfo['centerX'] = realcenter
        fightInfo['setData'] = settlementData
        fightInfo['centerY'] = HEIGHT
        self.afterFight(monsterId, playerId, currentHp)
        return {'result':True,'data':fightInfo}
    
    def afterFight(self,monsterId,playerId,currentHp):
        '''场景中的战后处理
        @monsterId 怪物的ID
        @param playerId: int 攻击的角色的ID
        @currentHp: int 怪物的当前血量 
        '''
        if monsterId>10:
            return
        monster = self._monsters.get(monsterId)
        if not monster:
            if monsterId == 1:#主帅旗被砍掉
                from app.scense.core.guild.GuildManager import GuildManager
                from app.scense.core.campaign.FortressManager import FortressManager
                from app.scense.utils.dbopera import dbfortress
                player = PlayersManager().getPlayerByID(playerId)
                guildId = player.guild.getID()
                fortress = FortressManager().getFortressBySceneId(self._id)
                info = {}
                info['kimoriScore'] = 0
                info['siegeScore'] = 0
                info['siege'] = 0
                info['isOccupied'] = 1
                info['kimori'] = guildId
                info['siege'] = 0
                guild1 = GuildManager().getGuildById(guildId)
                if guild1:
                    guild1.addExp(3500)
                    msg = u"%s国成功征战%s，成为其国领地！"%(guild1.name,self._name)
                    pushSystemInfo(msg)
                    dbfortress.updateFortressInfo(fortress.id, {'kimori':info['kimori'],
                                                'isOccupied':1,'siege':0})
                return
            else:
                return
        monster.updateHp(currentHp)
        
        
        