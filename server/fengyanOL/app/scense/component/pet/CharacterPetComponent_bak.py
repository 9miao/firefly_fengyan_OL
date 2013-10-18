#coding:utf8
'''
Created on 2011-12-14
角色的宠物信息
@author: lan
'''
from app.scense.component.Component import Component
from app.scense.core.character.Pet import Pet
from app.scense.utils.dbopera import dbCharacterPet,dbVIP
from app.scense.utils import dbaccess
from app.scense.serverconfig import chatnode

from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
import random
from app.scense.core.language.Language import Lg

MAXPETCNT = 10 #拥有宠物的最大数量
CATCHPETTASKTYPE = 107


ERROR = {-5:Lg().g(159)}
PETTRAINCOINCONS = 250#宠物游戏币培养消耗的比例
PETTRAINGOLDCONS = {1:{'gold':30,'vip':1},
                2:{'gold':80,'vip':3},
                3:{'gold':200,'vip':5}}#宠物培养消耗
#技能消耗品的ID
SKILLCRYSTAL = {1:20030061,
                2:20030062,
                3:20030063,
                4:20030064,
                5:20030065}

RESURCUS = 10 #宠物复活消耗

CANCATCHPET = {1:1,2:2,3:4}


class CharacterPetComponent(Component):
    '''角色的宠物信息类'''
    
    def __init__(self,owner):
        '''init Object'''
        Component.__init__(self, owner)
        #角色的宠物列表
        self._pets = {}
        #角色的宠物信息是否已经初始化
        self._hasInit = 0
        #获取宠物消息的队列
        self._getPetMsg = []
        #宠物的移动频率
        self._moveTag = 0
        
    def initCharacterPetInfo(self):
        '''初始化角色宠物信息'''
        if self._hasInit:
            return
        petlist = dbCharacterPet.getCharacterAllPet(self._owner.baseInfo.id)
        for petid in petlist:
            petId = petid[0]
            pet = Pet(petId = petId)
            self._pets[petId] = pet
        self._hasInit = 1
        
    def getNowShowCnt(self):
        '''设置现在跟随的宠物的数量'''
        return len([pet for pet in self._pets.values() if pet.getFlowFlag()])
        
    def checkCanFlow(self):
        '''检查是否还能设置宠物设置'''
        catchPetLevel = self._owner.skill.getCatchPetLevel()
        canshowcnt = CANCATCHPET.get(catchPetLevel)
        nowcnt = self.getNowShowCnt()
        if nowcnt < canshowcnt:
            return True
        return False
    
    def updateShow(self,petId):
        '''设置展示的宠物的ID'''
        viplevel = self._owner.baseInfo._viptype
        if not dbVIP.vipCertification('petflow', viplevel):
            return {'result':False,'message':Lg().g(217)}
        pet = self.getPet(petId)
        FlowFlag = pet.getFlowFlag()
        if not FlowFlag:
            canFlow = self.checkCanFlow()
            if not canFlow:
                return {'result':False,'message':Lg().g(419)}
            pet.updateFlowFlag(True)
            return {'result':True,'message':Lg().g(420),'data':False}
        else:
            pet.updateFlowFlag(False)
            return {'result':True,'message':u'','data':True}
        
    def getPets(self):
        '''获取角色的宠物列表'''
        self.initCharacterPetInfo()
        return self._pets
        
    def formatCharacterPetListInfo(self):
        '''格式或角色的宠物信息'''
        pets = self.getPets()
        return pets.values()
    
    def getCharacterPetListInfo(self):
        '''获取角色宠物列表'''
        pets = self.getPets()
        PetListInfo = {}
        PetListInfo['curPetNum'] = len(pets)
        PetListInfo['maxPetNum'] = 10
        PetListInfo['petInfo'] = []
        for pet in pets.values():
            info = {}
            info['petId'] = pet.baseInfo.getId()
            info['resPetId'] = pet.templateInfo.get('resourceid')
            info['petName'] = pet.baseInfo.getName()
            info['petLevel'] = pet.level.getLevel()
            info['icon'] = pet.templateInfo.get('resourceid')
            info['type'] = pet.templateInfo.get('resourceid')
            PetListInfo['petInfo'].append(info)
        return PetListInfo
    
    def getPetNum(self):
        '''获取当前宠物的数量'''
        pets = self.getPets()
        return len(pets)
    
    def OpenPetEgg(self,level = 1):
        '''打开宠物蛋
        '''
        if level==1:
            petlist = [25085,25086,25087,25088,25089,25090,25091,25092,25093,25095,25096,25097,25098,25099,25100,25101,25102,25103,25104,25105,25106,25107,25108,25109,25110,35001,35002,35003,35004,35005,35006,25001,25002,25003,25004,25062,25063,25064,25065,25066,25067,25068,25069,25070,25071,25072,25073,35049,35050,35051]
        else:
            petlist = [25013,25014,25015,25016,25017,25018,25019,25020,25021,25022,25025,25026,25027,25029,25030,25031,25032,25033,25034,25035,25044,25045,25046,25048,25049,25050,25051,25052,25053,25054,25055,35080,35081,35082,35083,35084,35085,35086,25001,25002,25003,25004,25062,25063,25064,25065,25066,25067,25068,25069,25070,25071,25072,25073,35049,35050,35051]
        self._OpenPetEgg(petlist)
        
    def _OpenPetEgg(self,petlist):
        '''打开宠物蛋'''
        petId = random.choice(petlist)
        result = self.addPet(templateId = petId)
        if result not in [-1,-2]:
            self._owner.quest.specialTaskHandle(110)
        else:
            raise Exception(Lg().g(421))
        
    def OpenOrdEgg(self,templateId,quality = 1):
        '''打卡普通宠物蛋'''
        self.addPet(templateId,quality = 1)
        self._owner.quest.specialTaskHandle(110)
        
    def addPet(self,templateId,quality = 1,statu = 1):
        '''添加一个宠物'''
        self.initCharacterPetInfo()
        if self.getPetNum()>=MAXPETCNT:
            return -1#宠物数量达到上限
        pet = Pet(templateId = templateId,owner = self._owner.baseInfo.id)
        result = pet.InsertIntoDB()
        if result:
            msg = Lg().g(422)%pet.baseInfo.getName()
            if statu:
                pushOtherMessage(905, msg, [self._owner.getDynamicId()])
            else:
                self._owner.msgbox.putFightTMsg(msg)
            self._pets[pet.baseInfo.id] = pet
            return pet.baseInfo.getName()
        
    def DropPet(self,petId):
        '''丢弃宠物
        @param petId: int 宠物的id
        '''
        self.initCharacterPetInfo()
        if petId not in self._pets.keys():
            return -5#不存在该宠物
        pet = self._pets.get(petId)
        result = pet.destroyByDB()
        if result:
            del self._pets[petId]
            return 1
        return 0
        
    def activationPetSkill(self,petId):
        '''激活宠物的技能
        @param petId: int 宠物的id
        '''
        self.initCharacterPetInfo()
        if petId not in self._pets.keys():
            return -5#不存在该宠物
        itemtemplateID = SKILLCRYSTAL.get(1)
        count = self._owner.pack.countItemTemplateId(itemtemplateID)
        if count<1:
            msg = Lg().g(423)
            pushOtherMessage(905, msg, [self._owner.getDynamicId()])
            return -4
        pet = self._pets.get(petId)
        result,skillId = pet.learnSkill()
        if result==1:
            self._owner.pack.delItemByTemplateId(itemtemplateID,1)
            skillName = dbCharacterPet.PET_SKILL_POOL.get(skillId).get('name')
            msg = pet.getName()+Lg().g(424)+skillName
            pushOtherMessage(905, msg, [self._owner.getDynamicId()])
        return result
    
    def LevelUpPetSkill(self,petId,skillpos):
        '''升级宠物技能'''
        self.initCharacterPetInfo()
        if petId not in self._pets.keys():
            return -5#不存在该宠物
        pet = self._pets.get(petId)
        skillId = pet.getPetSkillId(skillpos)
        if not skillId:
            return -4#技能信息不存在
        skillInfo = dbCharacterPet.PET_SKILL_POOL.get(skillId)
        skillgroup = skillInfo.get('skillGroup')
        nowskillLevel = skillInfo.get('level')+1
        nowskillinfo = dbCharacterPet.PET_SKILLGROUP[skillgroup].get(nowskillLevel)
        if not nowskillinfo:
            msg = Lg().g(425)
            pushOtherMessage(905, msg, [self._owner.getDynamicId()])
            return -3
        itemtemplateID = SKILLCRYSTAL.get(nowskillLevel)
        count = self._owner.pack.countItemTemplateId(itemtemplateID)
        if count<1:
            msg = Lg().g(426)%nowskillLevel
            pushOtherMessage(905, msg, [self._owner.getDynamicId()])
            return -2
        result = pet.levelUpSkill(skillpos)
        if result==1:
            self._owner.pack.delItemByTemplateId(itemtemplateID,1)
            skillName = nowskillinfo.get('name')
            msg = pet.getName()+Lg().g(424)+skillName
            pushOtherMessage(905, msg, [self._owner.getDynamicId()])
        return result
        
    def Training(self,petId,trainingLevel,position):
        '''宠物培养
        @param petId: int 宠物的id
        @param trainingLevel: int 培养的层次
        '''
        item = self._owner.pack._package._PropsPagePack.getItemByPosition(position)
        if not item:
            return {'result':False,'message':Lg().g(189)}
        templateId = item.baseInfo.getItemTemplateId()
        itemdict = {20030069:1,20030070:2,20030071:3}
        trainingLevel = itemdict.get(templateId,0)
        if not trainingLevel:
            return {'result':False,'message':Lg().g(427)}
        self.initCharacterPetInfo()
        if petId not in self._pets.keys():
            return {'result':False,'message':Lg().g(159)}#
        pet = self._pets.get(petId)
        result = pet.Training(trainingLevel)
        self._owner.pack.dropItem(position,3,1)
        if result:
            return {'result':True}
        return {'result':False}
        
    def getPet(self,petId):
        '''获取指定的宠物'''
        self.initCharacterPetInfo()
        return self._pets.get(petId)
        
    def updateName(self,petId,petName):
        '''修改宠物名称'''
        self.initCharacterPetInfo()
        pet = self.getPet(petId)
        result = pet.updateName(petName)
        return result
        
    def modifySlogan(self,petId,slogan):
        '''修改战斗宣言
        @param petId: int 宠物的id
        @param slogan: string 战斗宣言
        '''
        self.initCharacterPetInfo()
        pet = self.getPet(petId)
        result = pet.modifySlogan(slogan)
        return result
        
    def ResurPet(self,petId):
        '''复活宠物'''
        if self._owner.finance.getGold()<RESURCUS:
            return {'result':False,'message':Lg().g(190),'data':{'failType':1}}
        self.initCharacterPetInfo()
        pet = self.getPet(petId)
        result = pet.resurPet()
        if result.get('result'):
            self._owner.finance.addGold(-RESURCUS)
            self._owner.pushInfoChanged()
        return result
        
    def updatePetPosition(self,position,state = 1):
        '''更新所有展示的宠物的位置
        @param position: int 宠物的位置
        '''
        if not state:
            self._moveTag +=1
            if self._moveTag !=10:
                return
            else:
                self._moveTag =0
        for petId in self._pets.keys():
            pet = self.getPet(petId)
            if pet.getFlowFlag():
                pet.updatePosition(position)
        
    def restorationPetHP(self,Surplus):
        '''恢复所有宠物的血'''
        for petId in self._pets.keys():
            Surplus = self._pets[petId].restorationHp(Surplus)
            if Surplus ==0:
                return 0
        return Surplus
        
        
        
        
        
