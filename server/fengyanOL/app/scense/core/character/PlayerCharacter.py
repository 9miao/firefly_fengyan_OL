#coding:utf8
'''
Created on 2011-3-23

@author: sean_lan
'''

from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbCharacter
from app.scense.core.character.Character import Character
from app.scense.netInterface import pushObjectNetInterface

from app.scense.component.attribute.CharacterAttributeComponent import CharacterAttributeComponent
from app.scense.component.level.CharacterLevelComponent import CharacterLevelComponent
from app.scense.component.finance.CharacterFinanceComponent import CharacterFinanceComponent
from app.scense.component.profession.CharacterProfessionComponent import CharacterProfessionComponent
from app.scense.component.pack.CharacterPackComponent import CharacterPackageComponent
from app.scense.component.practice.CharacterPracticeComponent import CharacterPracticeComponent
from app.scense.component.friend.CharacterFriendComponent import CharacterFriendComponent
from app.scense.component.mail.CharacterMailListComponent import CharacterMailListComponent
from app.scense.component.dropping.CharacterDroppingComponent import CharacterDroppingComponent
from app.scense.component.shop.CharacterShopComponent import CharacterShopComponent
from app.scense.component.team.CharacterTeamComponent import CharacterTeamComponent
from app.scense.component.skill.CharacterSkillComponent_new import CharacterSkillComponent
from app.scense.component.guild.CharacterGuildComponent import CharacterGuildComponet
from app.scense.component.quest.CharacterQuestComponent_new import CharacterQuestComponent
from app.scense.component.effect.CharacterEffectComponent import CharacterEffectComponent
from app.scense.component.status.CharacterStatusComponent import CharacterStatusComponent
from app.scense.component.rank.CharacterRankComponent import CharacterRankComponent
from app.scense.component.pet.CharacterPetComponent import CharacterPetComponent
from app.scense.component.pet.PetWineshop import PetWineshop
from app.scense.component.messagebox.CharacterMSGComponent import CharacterMSGComponent
from app.scense.component.matrix.CharacterMatrixComponent import CharacterMatrixComponent
from app.scense.component.instance.InstanceColonize_com import InstanceColonizeComponent
from app.scense.component.icon.CharacterIconComponent import CharacterIconComponent
from app.scense.component.award.CharacterAwardComponent import CharacterAwardComponent
from app.scense.component.afk.CharacterAFKComponent import CharacterAFKComponent
from app.scense.component.raids.CharacterRaidsComponent import CharacterRaidsComponent
from app.scense.component.schedule.CharacterScheduleComponent import CharacterScheduleComponent
from app.scense.component.daily.CharacterDailyComponent import CharacterDailyComponent
from app.scense.component.nobility.CharacterNobility import CharacterNobility
from app.scense.component.godhead.CharacterGodheadComponent import CharacterGodheadComponent
from app.scense.component.strengthen.IconTime import IconTime
from app.scense.component.fate.CharacterFateComponent import CharacterFateComponent
from app.scense.component.arena.CharacterArenaComponent import CharacterAreanaComponent
from app.scense.component.tower.CharacterTowerComponent import CharacterTowerComponent
from app.scense.component.pvp.CharacterPVPComponent import CharacterPVPComponent
from app.scense.component.zhanyi.CharacterZhanYiComponent import CharacterZhanYiComponent
from app.scense.core.language.Language import Lg



MOVESPEEDX = 192 #X轴移动攻速
MOVESPEEDY = 192 #y轴移动攻速

class PlayerCharacter(Character):
    '''玩家角色类'''
    def __init__(self , cid , name = u'城管', dynamicId = -1,status = 1):
        '''构造方法
        @dynamicId （int） 角色登陆的动态ID socket连接产生的id
        '''
        Character.__init__(self, cid, name)
        self.setCharacterType(Character.PLAYERTYPE)#设置角色类型为玩家角色
        self.dynamicId = dynamicId    #角色登陆服务器时的动态id
        #--------角色的各个组件类------------
        self.level = CharacterLevelComponent(self)    #角色等级
        self.finance = CharacterFinanceComponent(self)    #角色资产
        self.profession = CharacterProfessionComponent(self) #角色职业
        self.pack = CharacterPackageComponent(self)    #角色包裹
        self.friend = CharacterFriendComponent(self)    #角色好友
        self.mail = CharacterMailListComponent(self)    #角色邮件列表
        self.shop = CharacterShopComponent(self)           #角色个人商店
        self.teamcom = CharacterTeamComponent(self)      #角色的队伍组件
        self.skill = CharacterSkillComponent(self)      #角色技能组件
        self.guild = CharacterGuildComponet(self)       #角色的行会
        self.practice = CharacterPracticeComponent(self) #角色修炼
        self.dropping = CharacterDroppingComponent(self)  #角色掉落
        self.quest = CharacterQuestComponent(self)   #角色任务
        self.rank = CharacterRankComponent(self)    #军衔
        self.effect = CharacterEffectComponent(self)
        self.status = CharacterStatusComponent(self)    #角色的状态
        self.attribute = CharacterAttributeComponent(self)  #角色属性
        self.pet = CharacterPetComponent(self) #角色的宠物
        self.matrix = CharacterMatrixComponent(self) #阵法摆放信息
        self.msgbox = CharacterMSGComponent(self)   #角色消息盒子
        self.instance = InstanceColonizeComponent(self) #角色殖民
        self.icon = CharacterIconComponent(self)    #角色图标
        self.award = CharacterAwardComponent(self)   #角色的奖励
        self.afk = CharacterAFKComponent(self)  #角色挂机
        self.raids = CharacterRaidsComponent(self) #角色扫荡
        self.schedule = CharacterScheduleComponent(self)#角色日程表
        self.nobility=CharacterNobility(self)#角色官爵
        self.daily = CharacterDailyComponent(self)#角色每日目标
        self.godhead = CharacterGodheadComponent(self)#角色神格
        self.qhtime=IconTime(self)#强化冷却时间
        self.petShop=PetWineshop(self)#宠物酒店
        self.fate = CharacterFateComponent(self)#符文
        self.arena = CharacterAreanaComponent(self)#竞技场
        self.tower = CharacterTowerComponent(self)#爬塔
        self.pvp = CharacterPVPComponent(self)#角色pvp信息
        self.zhanyi = CharacterZhanYiComponent(self)#角色的战役信息
        
        self.nodeId = 0               
        self.userId = 0     #角色的用户id
        self.CharacterType = 1     #角色的类型  1:玩家角色 2:怪物 3:宠物
        self.lastOnline = None
        self.outtime = None
        self.creatTime = None
        if status:
            self.initPlayerInfo() #初始化角色
        
    def initPlayerInfo(self):
        '''初始化角色信息'''
        data = dbaccess.getCharecterAllInfo(self.baseInfo.id)
        if not data:
            print "Inint_player _"+str(self.baseInfo.id)
        
        
        #------------初始化角色基础信息组件---------
        self.baseInfo.setType(data['viptype'])  #角色VIP类型
        self.baseInfo.setnickName(data['nickname']) #角色昵称
#        self.baseInfo.setPkStatus(data['pkStatus']) #角色PK状态
#        self.baseInfo.setStatus(data['status']) #角色状态
        self.baseInfo.setTown(data['town'])
        self.baseInfo.initPosition((data['position_x'],data['position_y']))
#        self.baseInfo.setLocation(data['location'])
        
        self.profession.setProfession(data['profession'])
        self.profession.setFigure(data['figure'])
        self.skill.initSkills()
        self.quest.initCharacterQuest()
        
        #-------------初始化爵位--------------------
        self.nobility.setLevel(data['NobilityLevel'])#爵位等级
        #-------------国相关信息------------------
        self.guild.setLeaveTime(data['leavetime'])
        
        #------------初始化角色经验等级组件-----------
        self.level.setLevel(data['level'])
        self.level.setExp(data['exp'])
        self.level.setVipExp(data['vipexp'])
        #------------初始化角色属性信息组件-----------
        self.attribute.setEnergy(data['energy'])
        #------------初始化buff信息----------
        self.effect.initEffect()
        
        #------------初始化角色资产信息组件-------------
        self.finance.setCoin(data['coin'])
        self.finance.reloadGold(data['gold'])
        self.finance.setMorale(data['morale'])#初始化角色斗气值
        self.finance.setPrestige(data['prestige'])#初始化角色威望值
#        #---------初始化角色的宠物信息---------
        self.pet.initCharacterPetInfo()
#        self.pet.setShow(data['petcarry'])
        #---------------初始化包裹---------------
        self.pack.initPack(packageSize=data['packageSize'])
        self.instance.pack.setSize(data['famPackSize'])
        #-----------初始化角色好友数量------------------
        self.attribute.setHp(data['hp'])
#        self.attribute.setMp(data['mp'])
        #-------------当前阵法-----------------
#        self.matrix.setNowMatrixId(data['nowmatrix'])
        self.lastOnline = data['LastonlineTime']
        self.outtime = data['outtime']
        self.creatTime = data['createtime']
        #-------------角色奖励相关-------------
        self.award.setAwardStep(data['novicestep'],state = 0)
        self.award.setDayAwardTime(data['dayawardtime'],state = 0)
        
        
    def setlastOnline(self,date):
        '''最好上线时间'''
        self.lastOnline = date
        dbCharacter.updatePlayerInfoByprops(self.baseInfo.id, {'isOnline':1,'LastonlineTime':str(date)})
            
    def getDynamicId(self):
        '''获取角色的动态Id'''
        return self.dynamicId
    
    def isHaveStrengthen(self):
        '''判断角色是否有殖民地'''
        from app.scense.core.instance.ColonizeManage import ColonizeManage
        pid=self.baseInfo.id#角色id
        flg=ColonizeManage().ishavestrengthen(pid)
        return flg
    
    def updateLocation(self,rate):
        '''更新角色的位置'''
        position = self.baseInfo.getPosition()
        destination = self.baseInfo.getDestination()
        
        if position== destination:
            self.pet.updatePetPosition(position,state = 0)
            return
        distanceX = rate*MOVESPEEDX#在这个时间段内能移动的距离
        distanceY = rate*MOVESPEEDY
        X = destination[0]
        Y = destination[1]
        if abs(destination[0]-position[0])>distanceX:
            if destination[0]>position[0]:
                X = position[0]+distanceX
            else:
                X = position[0]-distanceX
        if abs(destination[1]-position[1])>distanceY:
            if destination[1]>position[1]:
                Y = position[1]+distanceY
            else:
                Y = position[1]-distanceY
        self.baseInfo.setPosition((X,Y))
        self.pet.updatePetPosition(position)
        
    def updatePlayerInfo(self,statu=1):
        '''更新角色信息'''
        if statu:
            self.teamcom.pushTeamMemberInfo()
    
    def pushInfoChanged(self,statu=1):
        if statu:
            pushObjectNetInterface.pushUpdatePlayerInfo(self.dynamicId)
    
    def formatInfo(self):
        '''格式化角色基本信息'''
        if self.status.getLifeStatus()==1:
            self.effect.doEffectHot()
        attrinfo = self.attribute.getCharacterAttr()
        characterInfo = {}
        characterInfo['id'] = self.baseInfo.id#角色的ID
        characterInfo['nickname'] = self.baseInfo.getNickName()#角色的昵称
        characterInfo['roletype'] = self.baseInfo.getType()
        characterInfo['level'] = self.level.getLevel()
        characterInfo['profession'] = self.profession.getFigure()
        characterInfo['energy'] = self.attribute.getEnergy()
        characterInfo['rank'] = self.rank.getRankName()
        characterInfo['guildname'] = self.guild.getGuildInfo().get('name','')
        
        characterInfo['manualStr'] = attrinfo.get('Str',0)
        characterInfo['manualDex'] = attrinfo.get('Dex',0)
        characterInfo['manualVit'] = attrinfo.get('Vit',0)
        characterInfo['manualWis'] = attrinfo.get('Wis',0)
        characterInfo['maxHp'] = int(self.attribute.getMaxHp())
        characterInfo['hp'] = int(self.attribute.getHp())
        characterInfo['exp'] = int(self.level.getExp())
        characterInfo['maxExp'] = int(self.level.getMaxExp())
        
        characterInfo['physicalAttack'] = attrinfo.get('PhyAtt',0)
        characterInfo['magicAttack'] = attrinfo.get('MigAtt',0)
        characterInfo['physicalDefense'] = attrinfo.get('PhyDef',0)
        characterInfo['magicDefense'] = attrinfo.get('MigDef',0)
        characterInfo['speed'] = attrinfo.get('Speed',0)
        characterInfo['dodgeRate'] = attrinfo.get('Dodge',0)
        characterInfo['critRate'] = attrinfo.get('CriRate',0)
        characterInfo['block'] = attrinfo.get('Block',0)
        characterInfo['hitRate'] = attrinfo.get('HitRate',0)

        characterInfo['coin'] = self.finance.getCoin()
        characterInfo['gold'] = self.finance.getGold()

        characterInfo['deposit'] = 0
        characterInfo['appellation'] = {'idInDB':1001,'modID':1,'name':Lg().g(509)}
        characterInfo['appellationList'] = [{'idInDB':1001,'modID':1,'name':Lg().g(509)},{'idInDB':1001,'modID':1,'name':Lg().g(510)},
                                            {'idInDB':1001,'modID':1,'name':Lg().g(511)}]
        characterInfo['exULiliang'] = self.attribute.getGuildStr()
        characterInfo['exUMinjie'] = self.attribute.getGuildDex()
        characterInfo['exUZhili'] = self.attribute.getGuildWis()
        characterInfo['exUNaili'] = self.attribute.getGuildVit()
        characterInfo['exUWugong'] = int(self.attribute.getGuildPhyAtt())
        characterInfo['exUMonggong'] = int(self.attribute.getGuildMigAtt())
        characterInfo['unionType'] = self.guild.getUnionTypeStr()
        characterInfo['ranking'] = self.arena.ranking
        gname=self.guild.getGuildName()
        flg=True
        if not gname:
            gname=Lg().g(143)
            flg=False
        characterInfo['corpsInfo'] = {'joinCorpsFlag':flg,'corpsPosition':0,'corpsName':gname,'corpsLevel':0}
        if self.guild.getID():
            guildinfo = self.guild.getGuildInfo()
            characterInfo['corpsInfo']['joinCorpsFlag'] = flg
            characterInfo['corpsInfo']['corpsPosition'] = self.guild.getPost()#获取职务
            characterInfo['corpsInfo']['corpsName'] = guildinfo.get('name','')
            characterInfo['corpsInfo']['corpsLevel'] = guildinfo.get('level',0)
        return characterInfo
         
    def CheckClient(self,dynamicId):
        '''检测客户端id是否匹配'''
        if self.dynamicId ==dynamicId:
            return True
        return False
    
    def startAllTimer(self):
        '''启动角色身上所有的定时器
        '''
        self.effect.startAllEffectTimer()
        self.afk.startTrainTimer()
        self.afk.startMiningTimer()
        self.afk.startEnergyTimer()
    
    def stopAllTimer(self):
        '''停止 角色身上所有的定时器
        '''
        self.effect.stopAllEffectTimer()
        self.afk.stopTrainTimer()
        self.afk.stopMiningTimer()
        self.afk.stopGuaJiTimer()
        self.afk.stopEnergyTimer()
        
    def WritePlayerDBInfo(self):
        '''写入角色数据库信息
        '''
        dbCharacter.updatePlayerDB(self)
        self.zhanyi.updateCharacterZhangjie()
        
    def updatePlayerDBInfo(self):
        '''更新角色在数据库中的数据'''
        dbCharacter.updatePlayerDB(self)
        self.zhanyi.updateCharacterZhangjie()
        self.stopAllTimer()

    def getFightData(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取战斗数据'''
        attrinfo = self.attribute.getCharacterAttr(preDict = preDict)
        fightdata = {}
        fightdata['chaId'] = self.baseInfo.id               #角色的ID
        fightdata['chaName'] = self.baseInfo.getNickName()  #角色的昵称
        fightdata['chaLevel'] = self.level.getLevel()#角色的等级
        fightdata['characterType'] = self.CharacterType#角色的类型  1:玩家角色 2:怪物 3:宠物
        fightdata['figureType'] = self.profession.getFightFigure()#角色形象类型
        fightdata['chaBattleId'] = 0                        #角色在战场中的id
        fightdata['difficulty'] = 0#怪物难度
        fightdata['chaProfessionType'] = self.profession.getFightFigure()#角色的角色形象ID
        fightdata['chaIcon'] = self.profession.getProfession()
        fightdata['chatype'] = 0
        fightdata['chaDirection'] = 1#(角色在战斗中的归属阵营)1--(主动方)玩家朝向右，朝向右。2(被动方)--玩家朝向左
        fightdata['chaCurrentHp'] = self.attribute.getHp()#角色当前血量
        fightdata['chaCurrentPower'] = attrinfo.get('power',0)#角色的当前能量
        fightdata['chaTotalHp'] = self.attribute.getMaxHp(preDict=preDict)#角色的最大血量
        fightdata['chaTotalPower'] = Character.MAXPOWER#角色的最大能量
        fightdata['chaPos'] = (0,0)#角色的坐标
        fightdata['physicalAttack'] = attrinfo.get('PhyAtt',0)
        fightdata['magicAttack'] = attrinfo.get('MigAtt',0)#角色的魔法攻击
        fightdata['physicalDefense'] = attrinfo.get('PhyDef',0)#角色的物理防御
        fightdata['magicDefense'] = attrinfo.get('MigDef',0)#角色的魔法防御
        fightdata['speed'] = attrinfo.get('Speed',0)#角色的攻速
        fightdata['hitRate'] = attrinfo.get('HitRate',0)#角色的命中
        fightdata['critRate'] = attrinfo.get('CriRate',0)#角色的当前暴击率
        fightdata['block'] = attrinfo.get('Block',0)#角色的抗暴率
        fightdata['dodgeRate'] = attrinfo.get('Dodge',0)#角色的闪避几率
        fightdata['ActiveSkillList'] = self.skill.getActiveSkillList()#角色的主动攻击技能
        fightdata['ordSkill'] = self.profession.getOrdinarySkill()#角色的普通攻击技能
        fightdata['canDoMagicSkill'] = 1#可否释放魔法技能
        fightdata['canDoPhysicalSkill'] = 1#可否释放物理技能
        fightdata['canDoOrdSkill'] = 1#可否进行普通攻击
        fightdata['canBeTreat'] = 1#可否被治疗
        fightdata['canBeAttacked'] = 1#可否被攻击
        fightdata['canDied'] = 1#是否可死亡
        fightdata['skillIDByAttack'] = 0#被攻击的技能的ID 普通攻击为 0
        fightdata['expbound'] = 0#经验奖励
        return fightdata
        
        