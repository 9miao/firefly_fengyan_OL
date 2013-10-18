#coding:utf8
'''
Created on 2011-12-14
宠物类
@author: lan
'''
from app.scense.core.character.Character import Character
from app.scense.utils.dbopera import dbCharacterPet
import random
from app.scense.core.language.Language import Lg

MAXSKILLCNT = 6#宠物的最大技能个数
RANDOM_BASE = 100000#随机基数

def getRandomPetSkill():
    '''随机获取宠物的技能'''
    skillGroup = random.choice(dbCharacterPet.PET_SKILLGROUP.keys())
    skillId = dbCharacterPet.PET_SKILLGROUP[skillGroup][1].get('skillID')
    return skillId


def PetTrain(trainLevel):
    '''高级培养
    @param attrNum: int 属性的个数
    '''
    attrprop = {}
    config = list(dbCharacterPet.PET_TRAIN_CONFIG)
    for i in range(trainLevel+1):
        attr = random.choice(config)
        attrname = attr.get('attrname')
        if trainLevel ==1:
            down = attr.get('ord_down')
            up = attr.get('ord_up')
        elif trainLevel ==2:
            down = attr.get('adv_down')
            up = attr.get('adv_up')
        elif trainLevel ==3:
            down = attr.get('ext_down')
            up = attr.get('ext_up')
        else:
            down = attr.get('god_down')
            up = attr.get('god_up')
        values = random.randint(down,up)
        attrprop[attrname] = values
        config.remove(attr)
    return attrprop
    

class Pet(Character):
    '''宠物类'''
    
    
    def __init__(self,petId = 0,name = '',templateId = 0,owner = 0,quality = 1):
        '''初始化宠物的信息'''
        #角色类型
        Character.__init__(self, petId, name)
        self.setCharacterType(self.PETTYPE)
        #宠物的拥有者的ID
        self._owner = owner
        #宠物是否跟随
        self.flowFlag = False
        #宠物的当前血量
        self.hp = 0
        #宠物的当前生存状态
        self.lifestate = 1
        #宠物的等级
        self.level = 1
        #宠物的经验
        self.exp = 0
        #宠物的品质
        self.quality = quality
        #宠物的模板ID
        self._templateId = templateId
        #宠物的基础信息
        self._baseInfo = {}
        #宠物的附加属性信息
        self._extAttribute = {}
        #宠物的技能信息
        self._skillInfo = []
        #宠物的坐标信息
        self.position = (300,400)
        #初始化宠物的信息
        self.initData()
        
    def initData(self):
        '''初始或宠物的'''
        if not self.baseInfo.id:
            self.__initData_0()
        else:
            self.__initData_1()
        
    def __initData_0(self):
        '''不存在实例时的初始化方式'''
        self._baseInfo = dbCharacterPet.PET_TEMPLATE.get(self._templateId)
        self.baseInfo.setName(self._baseInfo.get('name',''))
        
    def __initData_1(self):
        '''存在数据库实例时的初始化方式'''
        petInstanceData = dbCharacterPet.getPetInfoById(self.baseInfo.id)
        self._templateId = petInstanceData.get('templateID')
        self._baseInfo = dbCharacterPet.PET_TEMPLATE.get(self._templateId)
        self.flowFlag = bool(petInstanceData.get('showed'))
        self._extAttribute = petInstanceData
        self.setHp(petInstanceData.get('hp',0))
        self.setLevel(petInstanceData.get('level',0))
        self.setExp(petInstanceData.get('exp',0))
        self.setQuality(petInstanceData.get('quality',0))
        self.setLifeState(petInstanceData.get('lifestate',0))
        if petInstanceData.get('name',''):
            self.baseInfo.setName(petInstanceData.get('name',''))
        else:
            self.baseInfo.setName(self._baseInfo.get('nickname'))
        self._owner = petInstanceData.get('ownerID',0)
        #初始化宠物的技能
        for i in range(1,MAXSKILLCNT+1):
            skillId = petInstanceData.get('skill_%d'%i,0)
            if skillId:
                self._skillInfo.append(skillId)
                
    def setFlowFlag(self,flowFlag):
        '''设置跟随状态'''
        self.flowFlag = flowFlag
        
    def getFlowFlag(self):
        '''获取跟随状态'''
        return self.flowFlag
    
    def updateFlowFlag(self,flowFlag):
        '''更新跟随状态'''
        self.flowFlag = flowFlag
        dbCharacterPet.updatePetInfo(self.baseInfo.id, {'showed':flowFlag})
        
    def updatePosition(self,position):
        '''更新宠物的坐标'''
        offsertX = random.randint(-40,40)
        offsertY = random.randint(-100,100)
        self.position = (position[0]+offsertX,position[1]+offsertY)
        
    def getPosition(self):
        '''获取宠物的位置'''
        return self.position
                
    def getHp(self):
        '''获取当前血量'''
        return self.hp
    
    def setHp(self,hp):
        '''设置当前血量'''
        maxhp =self.getMaxHp()
        if hp > maxhp:
            self.hp = maxhp
        else:
            self.hp = hp
        
    def updateHp(self,hp):
        '''更新当前血量'''
        self.setHp(hp)
        dbCharacterPet.updatePetInfo(self.baseInfo.id, {'hp':self.hp})
        
    def addHp(self,hp):
        '''添加血量'''
        nowhp = self.hp+hp
        self.updateHp(nowhp)
        
    def setQuality(self,quality):
        '''设置宠物的品质'''
        self.quality = quality
    
    def getMaxHp(self):
        '''获取最大血量'''
        level = self.getLevel()
        hppercent = (1+int(level/10)*0.05)*level
        maxhp = int((self._baseInfo['hp']+self.quality)*hppercent)
        return maxhp
    
    def getMaxExp(self):
        '''获取当前等级的最大经验'''
        requiredExp = dbCharacterPet.PET_EXP.get(self.level,{}).get('ExpRequired',2)
        return requiredExp
    
    def getExp(self):
        '''获取当前血量'''
        return self.exp
    
    def setExp(self,exp):
        '''设置当前血量'''
        self.exp = exp
        
    def addExp(self,exp):
        '''添加宠物经验'''
        exp = self.exp + exp
        self.updateExp(exp)
        
    def updateExp(self,exp):
        '''更新当前血量'''
        state = 0
        while exp>=self.getMaxExp():
            print self.getMaxExp()
            exp = exp - self.getMaxExp()
            self.level += 1
            state = 1
        self.exp = exp
        if state:
            self.updateLevel(self.level)
        dbCharacterPet.updatePetInfo(self.baseInfo.id, {'exp':self.exp})
    
    def getLifeState(self):
        '''获取生存状态'''
        return self.lifestate
    
    def setLifeState(self,lifestate):
        '''设置生存状态'''
        self.lifestate = lifestate
        
    def updateLifeState(self,lifestate):
        '''设置生存状态'''
        self.lifestate = lifestate
        dbCharacterPet.updatePetInfo(self.baseInfo.id, {'lifestate':lifestate})
        
    def getLevel(self):
        '''获取宠物的等级'''
        return self.level
    
    def setLevel(self,level):
        '''设置等级'''
        self.level = level
    
    def updateLevel(self,level):
        '''更新宠物的等级'''
        self.level = level
        dbCharacterPet.updatePetInfo(self.baseInfo.id, {'level':level})
                
    def getName(self):
        '''获取宠物的名称'''
        return self._baseInfo.get('nickname','')
                
    def getResourceId(self):
        '''获取资源ID'''
        return self._baseInfo.get('resourceid')
    
    def getIcon(self):
        '''获取图标'''
        return self._baseInfo.get('icon')
    
    def getType(self):
        '''获取图标类型'''
        return self._baseInfo.get('type')
    
    def getCharacterType(self):
        '''获取角色类型'''
        return self.CharacterType
                
    def destroyByDB(self):
        '''删除宠物在数据库中的数据'''
        result = dbCharacterPet.DelPetInfo(self.baseInfo.id)
        return result
    
    def InsertIntoDB(self):
        '''将不存在的实例写入数据库，生成数据库中的实例'''
        characterId = self._owner
        hp = self.getMaxHp()
        petId = dbCharacterPet.InsertPetInfoInDB(characterId, self._templateId,hp,self.quality)
        if id:
            self.baseInfo.setId(petId)
            self.__initData_1()
            return True
        return False
    
    def updateName(self,petName):
        '''更新宠物名称'''
        prop = {'name':petName}
        result = dbCharacterPet.updatePetInfo(self.baseInfo.id, prop)
        if result:
            self.baseInfo.setName(petName)
            return 1
        return 0
        
    def foundSkillSpace(self):
        '''获取技能空位'''
        nowskillCnt = len(self._skillInfo)
        if nowskillCnt >= MAXSKILLCNT:
            return None
        return 'skill_%d'%(nowskillCnt+1)
    
    def getPetSkillId(self,skillSpace):
        '''获取宠物的技能ID
        @param skillSpace: int 技能的位置
        '''
        if  0 > skillSpace or len(self._skillInfo) <= skillSpace:
            return 0#超过位置范围
        skillId = self._skillInfo[skillSpace]
        return skillId
        
    def learnSkill(self):
        '''宠物学习(激活)技能'''
        skillSpace = self.foundSkillSpace()
        if not skillSpace:
            return -1#技能槽已满
        newskill = getRandomPetSkill()
        self._skillInfo.append(newskill)
        prop = {skillSpace:newskill}
        result = dbCharacterPet.updatePetInfo(self.baseInfo.id, prop)
        if result:
            return 1,newskill
        return 0,newskill
        
    def levelUpSkill(self,skillSpace):
        '''升级宠物技能
        @param skillSpace: int 技能的位置
        '''
        if  0 > skillSpace or len(self._skillInfo) <= skillSpace:
            return -2#超过位置范围
        skillId = self._skillInfo[skillSpace]
        skillInfo = dbCharacterPet.PET_SKILL_POOL.get(skillId)
        if not skillInfo:
            return -1#技能信息不存在
        groupId = skillInfo.get('skillGroup')#技能组ID
        level = skillInfo.get('level')#技能等级
        newskillInfo = dbCharacterPet.PET_SKILLGROUP[groupId].get(level+1)
        if newskillInfo:
            propname = 'skill_%d'%(skillSpace+1)
            newSkillId = newskillInfo.get('skillID')
            prop = {propname:newSkillId}
            result = dbCharacterPet.updatePetInfo(self.baseInfo.id, prop)
            if result:
                self._skillInfo[skillSpace] = newSkillId
                return 1#成功
            else:
                return -3#数据库写入出错
        return 0#技能达到最高等级
    
    def Training(self,trainingLevel):
        '''培养
        @param trainingLevel: int 培养的级别
        '''
        prop = PetTrain(trainingLevel+1)
        result = dbCharacterPet.updatePetInfo(self.baseInfo.id, prop)
        if result:
            for item in prop.items():
                self._extAttribute[item[0]] = item[1]
        return 1
    
    def modifySlogan(self,slogan):
        '''更新战斗宣言
        @param slogan: string 战斗宣言
        '''
        prop = {'slogan':str(slogan)}
        result = dbCharacterPet.updatePetInfo(self.baseInfo.id, prop)
        if result:
            self._extAttribute['slogan'] = slogan
            return 1
        return 0
    
    def restorationHp(self,Surplus):
        '''宠物回血'''
        cons = self.getMaxHp()-self.hp#消耗
        if cons< 0:
            return Surplus
        su = Surplus -cons
        if su>0:
            self.addHp(su)
            return su
        else:
            self.addHp(Surplus)
            return 0
        
        
    def resurPet(self):
        '''复活宠物'''
        if self.lifestate:
            return {'result':False,'message':Lg().g(506)}
        self.updateLifeState(1)
        self.updateHp(self.getMaxHp())
        return {'result':True,'message':Lg().g(507)}
        
    def formatPetInfo(self):
        '''格式化宠物的信息'''
        bearer = {}
#        INT(宠物1级物防(魔防)*(1+INT(宠物当前等级/10)*0.07)*宠物当前等级)

#        percent = (1+1.0*self.getLevel()**2/20)
        bearer['petId'] = self.baseInfo.id
        bearer['resPetId'] = self._baseInfo.get('resourceid')
        bearer['petName'] = self.baseInfo.getName()
        bearer['petLevel'] = self.getLevel()
        bearer['inMatrixFlag'] = 0#是否在阵法中
        bearer['petDes'] = self._baseInfo.get('descript')#宠物描述
        bearer['baseHp'] = self.getHp()
        bearer['manualHp'] = 0#self.getMaxHp()
        level = self.getLevel()
        attackpercent = 0.051*(1+int(level/10)*0.05)*level
        bearer['basePhyAttack'] = int((self._baseInfo.get('PhysicalAttack')+self.quality)*attackpercent)
        bearer['manualPhyAttack'] = self._extAttribute.get('extPhysicalAttack')+\
                                int(self.passiveSkillAddition.get('physicalAttack',0))
        bearer['baseMagicAttack'] = int((self._baseInfo.get('MagicAttack')+self.quality)*attackpercent)
        bearer['manualMagicAttack'] = self._extAttribute.get('extMagicAttack')+\
                                int(self.passiveSkillAddition.get('magicAttack',0))
        defensepercent = (1+int(level/10)*0.07)*level
        bearer['basePhyDefense'] = int((self._baseInfo.get('PhysicalDefense')+self.quality)*defensepercent)
        bearer['manualPhyDefense'] = self._extAttribute.get('extPhysicalDefense')+\
                                int(self.passiveSkillAddition.get('physicalDefense',0))
        bearer['baseMagicDefense'] = int((self._baseInfo.get('MagicDefense')+self.quality)*defensepercent)
        bearer['manualMagicDefense'] = self._extAttribute.get('extMagicDefense')+\
                                int(self.passiveSkillAddition.get('magicDefense',0))
        bearer['baseHitRate'] = int(self._baseInfo.get('Hit')+self.quality)
        bearer['manualHitRate'] = self._extAttribute.get('extHitRate')+\
                                int(self.passiveSkillAddition.get('hitRate',0))
        bearer['baseDodgeRate'] = int(self._baseInfo.get('Dodge')+self.quality)
        bearer['manualDodgeRate'] = self._extAttribute.get('extDodge')+\
                                int(self.passiveSkillAddition.get('dodgeRate',0))
        bearer['baseSpeed'] = int(self._baseInfo.get('Speed')+self.quality)
        bearer['manualSpeed'] = self._extAttribute.get('extSpeed')+\
                                int(self.passiveSkillAddition.get('speed',0))
        bearer['baseCritRate'] = (self._baseInfo.get('Force')+self.quality)
        bearer['manualCritRate'] = self._extAttribute.get('extCriRate')+\
                                int(self.passiveSkillAddition.get('criRate',0))
        bearer['icon'] = self._baseInfo.get('icon',0)
        bearer['type'] = self._baseInfo.get('type',0)
        bearer['slogan'] = self._extAttribute.get('slogan','')
        return bearer

    @property
    def passiveSkillAddition(self):
        '''获取技能加成'''
        actor = {}
        for skillId in self._skillInfo:
            skillInfo = dbCharacterPet.PET_SKILL_POOL[skillId]
            if skillInfo['skillType']==2:
                try:
                    exec(skillInfo['effectScript'])
                except Exception:
                    print "坑爹呢，宠物被动技能配置错误"
        return actor
        
    def SerializationPetInfo(self,bearer):
        '''序列化宠物的信息
        @param bearer: message 载体
        '''
        info = self.formatPetInfo()
        bearer.petId = self.baseInfo.id
        bearer.resPetId = self._baseInfo.get('resourceid')
        bearer.petName = self.baseInfo.getName()
        bearer.petLevel = self.getLevel()
        bearer.inMatrixFlag = 0#是否在阵法中
        bearer.petDes = self._baseInfo.get('descript')#宠物描述
        bearer.baseHp = self.getHp()
        bearer.manualHp = info.get('manualHp',0)
        bearer.basePhyAttack = info.get('basePhyAttack',0)
        bearer.manualPhyAttack = info.get('manualPhyAttack',0)
        bearer.baseMagicAttack = info.get('baseMagicAttack',0)
        bearer.manualMagicAttack = info.get('manualMagicAttack',0)
        bearer.basePhyDefense = info.get('basePhyDefense',0)
        bearer.manualPhyDefense = info.get('manualPhyDefense',0)
        bearer.baseMagicDefense = info.get('baseMagicDefense',0)
        bearer.manualMagicDefense = info.get('manualMagicDefense',0)
        bearer.baseHitRate = info.get('baseHitRate',0)
        bearer.manualHitRate = info.get('manualHitRate',0)
        bearer.baseDodgeRate = info.get('baseDodgeRate',0)
        bearer.manualDodgeRate = info.get('manualDodgeRate',0)
        bearer.baseSpeed = info.get('baseSpeed',0)
        bearer.manualSpeed = info.get('manualSpeed',0)
        bearer.baseCritRate = info.get('baseCritRate',0)
        bearer.manualCritRate = info.get('manualCritRate',0)
        bearer.icon = self._baseInfo.get('icon',0)
        bearer.type = self._baseInfo.get('type',0)
        bearer.flowFlag = self.flowFlag
        for skillId in self._skillInfo:
            skillInfo = dbCharacterPet.PET_SKILL_POOL.get(skillId)
            if not skillInfo:
                print "skill error %d"%skillId
                continue
            skill = bearer.petSkillInfo.add()
            skill.hasActivationFlag = True
            skill.petSkillId = skillInfo.get('skillID')
            skill.icon = skillInfo.get('icon')
            skill.type = skillInfo.get('type')
            skill.petSkillName = skillInfo.get('name')
            skill.petSkillLevel = skillInfo.get('level')
            skill.petSkillDes = skillInfo.get('descript')
            skill.petSkillMaxLevel   = skillInfo.get('maxlevel')
            
    def getFightData(self):
        '''获取怪物战斗数据'''
        info = self.formatPetInfo()
        fightdata = {}
        fightdata['chaId'] = self.baseInfo.id           #角色的ID
        fightdata['chaName'] = self.baseInfo.getName()  #角色的昵称
        fightdata['chaLevel'] = self.getLevel()#角色的等级
        fightdata['characterType'] = self.getCharacterType()#角色的类型  1:玩家角色 2:怪物 3:宠物
        fightdata['figureType'] = self._baseInfo['resourceid']
        fightdata['chaBattleId'] = 0                        #角色在战场中的id
        fightdata['difficulty'] = 0#怪物难度
        fightdata['chaProfessionType'] = self._baseInfo['resourceid']#角色的角色形象ID
        fightdata['chaDirection'] = 1#(角色在战斗中的归属阵营)1--(主动方)玩家朝向右，朝向右。2(被动方)--玩家朝向左
        fightdata['chaCurrentHp'] = self.getHp()#角色当前血量
        fightdata['chaCurrentPower'] = 0#角色的当前能量
        fightdata['chaTotalHp'] = self.getMaxHp()#角色的最大血量s
        fightdata['chaTotalPower'] = Character.MAXPOWER#角色的最大能量
        fightdata['chaPos'] = (0,0)#角色的坐标
        fightdata['physicalAttack'] = info['basePhyAttack']+info['manualPhyAttack']#角色的物理攻击
        fightdata['magicAttack'] = info['baseMagicAttack']+info['manualMagicAttack']#角色的魔法攻击
        fightdata['physicalDefense'] = info['basePhyDefense']+info['manualPhyDefense']#角色的物理防御
        fightdata['magicDefense'] = info['baseMagicDefense']+info['manualMagicDefense']#角色的魔法防御
        fightdata['speed'] = info['baseSpeed']+info['manualSpeed']#角色的攻速
#        fightdata['squelch'] = 0#角色的反击
#        fightdata['ignore'] = 0#角色的破甲
        fightdata['hitRate'] = info['baseHitRate']+info['manualHitRate']#角色的命中
        fightdata['critRate'] = info['baseCritRate']+info['manualCritRate']#角色的当前暴击率
        fightdata['block'] = 0
        fightdata['dodgeRate'] = info['baseDodgeRate']+info['manualDodgeRate']#角色的闪避几率
        fightdata['ActiveSkillList'] = []#self.skill#角色的主动攻击技能
        fightdata['ordSkill'] = self._baseInfo['ordSkill']#角色的普通攻击技能
#        fightdata['rebound'] = 0 #反弹
        fightdata['canDoMagicSkill'] = 1#可否释放魔法技能
        fightdata['canDoPhysicalSkill'] = 1#可否释放物理技能
        fightdata['canDoOrdSkill'] = 1#可否进行普通攻击
        fightdata['canBeTreat'] = 1#可否被治疗
        fightdata['canBeAttacked'] = 1#可否被攻击
        fightdata['canDied'] = 1#是否可死亡
        fightdata['skillIDByAttack'] = 0#被攻击的技能的ID 普通攻击为 0
        fightdata['expbound'] = 0#经验奖励
        return fightdata
        
        