#coding:utf8
'''
Created on 2011-9-24

@author: lan
'''
import random
from app.scense.core.language.Language import Lg

GAPX = 100#随机差距
GAPY = 30

from twisted.python import log
from app.scense.utils.dbopera import dbNpc,dbPortals,dbfightfail
from app.scense.core.character.Monster import Monster
from app.scense.netInterface.pushObjectNetInterface import pushRemovePlayerInMap,\
    pushApplyMessage,pushEnterPlace_new
from app.scense.netInterface.pushPrompted import pushPromptedMessage
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.fight.battleSide import BattleSide
from app.scense.applyInterface import dropout

from app.scense.protoFile.scene import pushSceneMessage_pb2
from app.scense.core.instance.ColonizeManage import ColonizeManage


DISTANCE = 200 #怪物的视力范围
MOVERATE = 10  #怪物的移动频率
MOVESPEED = 224 #场景中移动的攻速
MOVESPEEDX = 350 #X轴移动攻速
MOVESPEEDY = 250 #y轴移动攻速
HEIGHT = 325



def getRealCenter(now_x,width):
    '''获取战斗的中心点位置'''
    if now_x <550:
        now_x = 550
    elif now_x > (width - 550):
        now_x = width - 550
    return int(now_x)
    

class BaseScene(object):
    '''基础场景类'''
    
    def __init__(self,id,type = 1,group = 0):
        '''
        @param id: int 公共场景的id
        '''
        self._id = id   #场景的id
        self._name = '' #场景的名称
        self._type = type  #场景的类型
        self._levelRequired = 1 #场景的等级需求
        self._memberRequired = 500 #场景可容纳人数
        self._height = 500 #场景的高度
        self._width = 2000 #场景的宽度
        self._init_X = 200 #场景进入的初始化x坐标
        self._init_Y = 400 #场景进入的初始化Y坐标
        self._resourceid = 1000 #场景的资源IDER
        self._npclist = [] #场景的npc资源    
        self._portals = [] #传送门列表
        self._playerlist = [] #角色列表
        self._canRec = set([]) #能够接受场景消息的角色的ID的列表
        self._monsters = {} #怪物列表
        self._identitytag = 1001    #怪物动态身份标识
        self._movetag = 0           #怪物移动标识控制怪物移动的频率
        self._group = group
        self.initSceneInfo()
        
    def initSceneInfo(self):
        '''初始化场景信息'''
        pass
        
    def getID(self):
        '''获取场景的ID'''
        return self._id
    
    def getNPC(self):
        '''获取场景中的NPC列表'''
        return self._npclist
    
    def getInitPosition(self):
        '''获取进入场景的初始坐标'''
        return (self._init_X,self._init_Y)
    
    def formatSceneInfo(self):
        '''格式化场景信息'''
        sceneInfo = {}
        sceneInfo['id'] = self._id  #场景的ID
        sceneInfo['resourceId'] = self._resourceid #场景的资源类型
        sceneInfo['sceneType'] = self._type #场景的类型
        sceneInfo['scenename'] = self._name  #场景的名称
        sceneInfo['npclist'] = [dbNpc.ALL_NPCS.get(npcID) for\
                                 npcID in self._npclist] #场景的npc信息
        sceneInfo['portals'] = [dbPortals.ALL_PORTALS.get(portalId) for\
                                 portalId in self._portals] #场景中传送门的信息
        if self._type ==1:#公共场景时
            colonizeInfo = ColonizeManage().getCityByCityid(self._id)
            if colonizeInfo:
                sceneInfo['corpsName'] = colonizeInfo.get('gname')
                sceneInfo['rewardCorpsName'] = colonizeInfo.get('pname')
        elif self._type ==2:#副本场景时
            colonizeInfo = ColonizeManage().getInstanceInfoByid(self._group)
            if colonizeInfo:
                sceneInfo['corpsName'] = colonizeInfo.get('gname')
                sceneInfo['rewardCorpsName'] = colonizeInfo.get('pname')
            
        return sceneInfo
        
    def addPlayer(self,playerId):
        '''添加一个角色到当前场景
        @param playerId: int 角色的id
        '''
        if playerId in self._playerlist:
            self.dropPlayer(playerId)
        self._playerlist.append(playerId)
        player=PlayersManager().getPlayerByID(playerId) #根据角色id获取角色实例
        if player:
            player.quest.setNpcList(self.getNPC())
            dyid=player.getDynamicId()
            sendList = [dyid]
            initx = self._init_X+random.randint(-GAPX,GAPX)
            inity = self._init_Y+random.randint(-GAPY,GAPY)
            player.baseInfo.initPosition((initx,inity))
            self.pushEnterPlace(sendList)
            
    def pushEnterPlace(self,sendList):
        '''推送进入场景的信息'''
        sceneInfo = self.formatSceneInfo()
        pushEnterPlace_new(sceneInfo, sendList)
        
    def dropPlayer(self,playerId,sendList = []):
        '''清除场景中的角色
        @param playerId: int 角色的id
        '''
        try:
            if playerId in self._playerlist:
                self._playerlist.remove(playerId)
                log.msg("scene drop player playerId")
                self._canRec.remove(playerId)
                log.msg("scene canRec drop player playerId")
        except Exception,e:
            log.msg(e)
        if not sendList:
            sendList = self.getSendList()
        pushRemovePlayerInMap(playerId,sendList)
        
    def addPortals(self,portalId):
        '''添加一个传送门
        @param portalId: int 传送门的id 
        '''
        self._portals.append(portalId)
        
    def dropPortals(self,portalId,sendList = []):
        '''删除一个传送门
        @param portalId: int 传送门的id
        '''
        self._portals.remove(portalId)
        if not sendList:
            sendList = self.getSendList()
        pushRemovePlayerInMap(portalId,sendList)
        
    def addNPC(self,npcId):
        '''添加一个npc'''
        self._npclist.append(npcId)
    
    def dropNPC(self,npcId,sendList = []):
        '''移除一个npc'''
        self._npclist.remove(npcId)
        if not sendList:
            sendList = self.getSendList()
        pushRemovePlayerInMap(npcId,sendList)
        
    def getMonsterById(self,id):
        '''根据怪物在场景中的id获取怪物'''
        if self._monsters.has_key(id):
            return self._monsters[id]
        return None
        
    def addMonster(self,monster):
        '''添加一个怪物
        @param monster: Monster instance 怪物的实例
        '''
        if self._monsters.has_key(monster.baseInfo.id):
            raise Exception("系统记录冲突")
        self._monsters[monster.baseInfo.id] = monster
        self._identitytag +=1
        
    def createMonster(self,temlateId):
        '''随机生成一个怪物'''
        self._identitytag +=1
        monster = Monster(id = self._identitytag,templateId = temlateId)
        return monster
    
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
        sendList = self.getSendList()
        pushRemovePlayerInMap(monsterId,sendList)
    
    def produceMonster(self,templateId,positionX = 600,positionY =400,\
                       matrixId=100009,rule = []):
        '''产生一个怪物'''
        monster = self.createMonster(templateId)
        monster.baseInfo.setStaticPosition((positionX,positionY))
        monster.setMatrixId(matrixId)
        monster.setRule(rule)
        self.addMonster(monster)
    
    def pushSceneInfo(self,rate):
        '''给每一个在场景中的玩家推送场景信息
        @param rate: int 移动的频率
        '''
        if not self._playerlist:
            return
        self.updateAllPlayerLocation(rate)
        if self._monsters:
            self.updateAllMonsterLocation()
        sendlist = self.getSendList()
        sceneInfo = pushSceneMessage_pb2.pushSceneMessage()
        for playerId in self._playerlist:
            player = PlayersManager().getPlayerByID(playerId)
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
                PetPosition.currentHP = pet.attribute.getHp()
                PetPosition.MaxHP = pet.attribute.getMaxHp()
                
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
        sceneInfo.sceneId = self._id
        msg = sceneInfo.SerializeToString()
        pushApplyMessage(602,msg, sendlist)
    
    def cleanMonster(self):
        '''清除场景中的怪物'''
        for monsterId in self._monsters.keys():
            self.dropMonster(monsterId)
            
    def updateAllPlayerLocation(self,rate):
        '''更新场景中所有角色的坐标
        @param rate: int 移动的频率
        '''
        playerList = list(self._playerlist)
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
            for playerId in self._playerlist:
                pposition = PlayersManager().getPlayerByID(playerId).baseInfo.getPosition()
                if abs(mposition[0]-pposition[0])<DISTANCE:
                    hasMove = 1
                    monster.baseInfo.setPosition(pposition)
                    continue
                if not hasMove and self._movetag==MOVERATE:
                    tag = 1
                    monster.updateLocation()
        if tag:
            self._movetag=0
        
    def FightInScene(self,monsterId,now_X,playerId):
        '''副本战斗
        @param monsterId: int 怪物的id
        @param now_X: int 碰撞点的x坐标
        '''
        from app.scense.core.fight.fight_new import Fight
        if not self._monsters:
            return {'result':False,'message':u'不存在怪物实例'}
        fightInfo = {}
        fightType = 1
        sendList = self.getSendList()
        players = [PlayersManager().getPlayerByID(playerId) for playerId in self._playerlist]
        monster = self._monsters.get(monsterId,None)
        deffen = []
        if not monster:
            return {'result':False,'message':u'不存在怪物实例'}
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
        matrixId = monster.getMatrixId()
        ruleInfo = monster.getRule()
        if not ruleInfo:
            deffen.append(monster)
            defenders = BattleSide(deffen)
        else:
            temlist,rule = ruleInfo
            for tem in temlist:
                _monser = self.createMonster(tem)
                deffen.append(_monser)
            defenders = BattleSide(deffen,state = 0)
            defenders.setMatrixPositionBatch(rule)
        #获取战场中心位置
        realcenter = self._width/2
        data = Fight( challengers, defenders, realcenter)
        data.DoFight()
        
        #战后处理
        if data.battleResult == 1:
            self.dropMonster(monsterId)
        elif data.battleResult == 3:
            fightType = 3
            monster = self._monsters[monsterId]
            for player in self._playerlist:
                pl = PlayersManager().getPlayerByID(player)
                pl.baseInfo.initPosition(self.getInitPosition())
            monster.baseInfo.initPosition(monster.baseInfo.getStaticPosition())
        elif data.battleResult == 2:
            fightType = 2
            monster = self._monsters[monsterId]
            for player in self._playerlist:
                pl = PlayersManager().getPlayerByID(player)
                pl.baseInfo.initPosition(self.getInitPosition())
                self.pushFightFailHelp(pl)
            monster.baseInfo.initPosition(monster.baseInfo.getStaticPosition())
        if not self._monsters and self._type ==2:
            fightType = 4
            #print '通关副本'
        settlementData = []
        dropoutid = monster.formatInfo['dropoutid']
        for player in data.fighters.values():
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
        
        return {'result':True,'data':fightInfo}
    
    def pushNowScenePosition(self,sendId,playerID):
        '''推送在场景中当前的所有角色和怪物的坐标
        @param sendId: int 推送的目标ID
        '''
        self._canRec.add(playerID)
        sceneInfo = pushSceneMessage_pb2.pushSceneMessage()
        for playerId in self._playerlist:
            player = PlayersManager().getPlayerByID(playerId)
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
                PetPosition.headicon = figure
                PetPosition.figure = figure
                PetPosition.x = int(position[0])
                PetPosition.y = int(position[1])
                PetPosition.masterId = playerId
                PetPosition.currentHP = pet.attribute.getHp()
                PetPosition.MaxHP = pet.attribute.getMaxHp()
        
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
        sceneInfo.sceneId = self._id
        msg = sceneInfo.SerializeToString()
        pushApplyMessage(602,msg, [sendId])
        
    def getSendList(self):
        '''获取可发送的客户端列表'''
        sendList = []
        for pId in self._playerlist:
            pl = PlayersManager().getPlayerByID(pId)
            if pl and (pId in self._canRec) and pl.baseInfo.getStatus()!=4:
                sendList.append(pl.getDynamicId())
        return sendList
        
    def pushFightFailHelp(self,pl):
        '''获取战败后的帮助
        @param pl: PlayerCharacter Object 接受帮助信息的角色的实例
        '''
        failinfo = dbfightfail.ALLFIGHTFAILOPE.get(self._id)
        if not failinfo:
            return
        sysOpeType = failinfo.get('failtype')
        tishiStr = failinfo.get('tishiStr')
        contentStr = failinfo.get('contentStr')
        caozuoStr = failinfo.get('caozuoStr')
        recCharacterId = pl.baseInfo.id
        args = (recCharacterId,sysOpeType,tishiStr,contentStr,caozuoStr)
        pl.msgbox.putFightfailmsg(args)
#        pushCorpsApplication(recCharacterId,sysOpeType,tishiStr,contentStr,caozuoStr)
    
    
    
    