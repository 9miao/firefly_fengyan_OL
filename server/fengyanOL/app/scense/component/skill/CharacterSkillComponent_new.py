#coding:utf8
'''
Created on 2009-12-2

@author: wudepeng
'''
from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbSkill
from app.scense.utils import dbaccess
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.netInterface.pushPrompted import pushPromptedMessage
from app.scense.core.language.Language import Lg


class CharacterSkillComponent(Component):
    '''
    skill component for character
    '''
    CATCHPETSKILLGROUP = 8108 #抓宠技能的技能组ID
    CATCHCONSUME = {1:20030066,2:20030067,3:20030068} #封印石的ID

    def __init__(self, owner):
        '''xx
        Constructor
        @param activeSkill: []skill object
        @param auxiliarySkills: []skill object
        @param passiveSkills: []skill object 
        '''
        Component.__init__(self, owner)
        self._skillPoint = 0
#        self._autoUnloaded = False#是否已经自动卸载了抓宠技能
        self._equipActiveSkill = {} #装备的技能列表
        self.learned_skillpool = {}   #已学技能//
        
    def initSkills(self):
        '''初始化技能'''
        characterId = self._owner.baseInfo.id 
        self.learned_skillpool = dbSkill.getCharacterLearnedSkills(characterId)
        self._equipActiveSkill = dbSkill.getCharacterSkillSetInfo(characterId)
        if not self._equipActiveSkill:
            dbSkill.insertCharacterSkillSet(characterId)
            self._equipActiveSkill = {'ActiveSkill_1':0,
                                      'ActiveSkill_2':-1,
                                      'ActiveSkill_3':-1}
            
    def getCatchPetLevel(self):
        '''获取抓宠技能的等级'''
        catchPetskill = self.learned_skillpool.get(self.CATCHPETSKILLGROUP)
        if not catchPetskill:
            return 0
        return catchPetskill.get('skillLevel')
    
    def checkHasEquipCatchSkill(self):
        '''检测是否装备了抓宠技能'''
        if self.CATCHPETSKILLGROUP in self._equipActiveSkill.values():
            return True
        return False
    
    def checkCanEquipCatchSkill(self):
        '''检测是否能装备抓宠技能'''
        level = self.getCatchPetLevel()
        itemTemplateID = self.CATCHCONSUME.get(level)
        if itemTemplateID and self._owner.pack.countItemTemplateId(itemTemplateID):
            return True
        return False
        
    def checkSkillLearnable(self,skillGroup):
        '''检测技能是否是可学技能
        @param skillGroup: int 技能的id
        '''
        if not dbSkill.SKILL_GROUP.has_key(skillGroup):
            return {'result':False,'message':Lg().g(471)}
        skillInfo = dbSkill.SKILL_GROUP[skillGroup].get(1)
        if not skillInfo:
            return {'result':False,'message':Lg().g(471)}
        if self.learned_skillpool.has_key(skillGroup):
            return {'result':False,'message':Lg().g(472)}#表示技能已学
        levelRequired = skillInfo.get('levelRequired')
        if self._owner.level.getLevel()<levelRequired:
            return {'result':False,'message':Lg().g(332)}#表示等级不足
        levelUpMoney = skillInfo.get('levelUpMoney')
        if self._owner.finance.getCoin()<levelUpMoney:
            return {'result':False,'message':Lg().g(88)}#表示资金不足
        profession = skillInfo.get('profession')
        if self._owner.profession.getProfession()!=profession and profession!=0:
            return {'result':False,'message':Lg().g(404)}#表示职业不符
        itemTemplateID = skillInfo.get('itemRequired')
        requiredCount = skillInfo.get('itemCountRequired')
        itemInfo = dbaccess.all_ItemTemplate.get(itemTemplateID)
        if itemInfo and requiredCount:
            if self._owner.pack.countItemTemplateId(itemTemplateID)<requiredCount:
                return {'result':False,'message':Lg().g(473)%itemInfo.get('name')}
        return {'result':True}
    
    def checkSkillLevelUp(self,skillGroup):
        '''检测技能是否是可升级
        @param skillGroup: int 技能的id
        '''
        if not self.learned_skillpool.has_key(skillGroup):
            return {'result':False,'message':Lg().g(474)}
        nowskillInfo = self.learned_skillpool.get(skillGroup)
        nowlevel = nowskillInfo.get('skillLevel',1)
        skillInfo = dbSkill.SKILL_GROUP[skillGroup].get(nowlevel+1)
        if not skillInfo:
            return {'result':False,'message':Lg().g(425)}
        levelRequired = skillInfo.get('levelRequired')
        if self._owner.level.getLevel()<levelRequired:
            return {'result':False,'message':Lg().g(332)}
        levelUpMoney = skillInfo.get('levelUpMoney')
        if self._owner.finance.getCoin()<levelUpMoney:
            return {'result':False,'message':Lg().g(88)}
        profession = skillInfo.get('profession')
        if self._owner.profession.getProfession()!=profession and profession!=0:
            return {'result':False,'message':Lg().g(404)}
        itemTemplateID = skillInfo.get('itemRequired')
        requiredCount = skillInfo.get('itemCountRequired')
        itemInfo = dbaccess.all_ItemTemplate.get(itemTemplateID)
        if itemInfo and requiredCount:
            if self._owner.pack.countItemTemplateId(itemTemplateID)<requiredCount:
                return {'result':False,'message':Lg().g(473)%itemInfo.get('name')}
        return {'result':True}
        
    def activationSkill(self,skillGroup):
        '''学习技能
        @skillGroup 技能组的ID
        '''
        characterId = self._owner.baseInfo.id
        reason = dbSkill.LearnSkill(characterId, skillGroup)
        if not reason:
            return False
        LearnedSkillInfo = {'skillId':skillGroup,'skillLevel':1}
        self.learned_skillpool[skillGroup] = LearnedSkillInfo
        skillInfo = dbSkill.SKILL_GROUP[skillGroup].get(1)
#        coinRequired = skillInfo.get('levelUpMoney')
#        itemTemplateID = skillInfo.get('itemRequired')
#        requiredCount = skillInfo.get('itemCountRequired')
#        itemInfo = dbaccess.all_ItemTemplate.get(itemTemplateID)
#        self._owner.finance.updateCoin(self._owner.finance.getCoin()-coinRequired)
#        if skillGroup ==self.CATCHPETSKILLGROUP:
#            self._owner.quest.specialTaskHandle(108)#特殊抓宠任务处理
##        else:
##            #特殊任务处理
#        if itemTemplateID and requiredCount:
#            self._owner.pack.delItemByTemplateId(itemTemplateID,requiredCount)
        self._owner.daily.noticeDaily(11,0,-1)
        msg = Lg().g(475)%skillInfo.get('skillName')
        pushOtherMessage(905, msg, [self._owner.getDynamicId()])
        return True
    
    def LevelUpSkill(self,skillGroup):
        '''技能升级
        @skillGroup 技能组的ID
        '''
        result = self.checkSkillLevelUp(skillGroup)
        if not result.get('result'):
            return result
        characterId = self._owner.baseInfo.id
        reason = dbSkill.LevelUpCharacterSkill(characterId, skillGroup)
        if not reason:
            return {'result':False,'message':Lg().g(476)}
        nowLevel = self.learned_skillpool[skillGroup]['skillLevel']+1
        self.learned_skillpool[skillGroup]['skillLevel']= nowLevel
        skillInfo = dbSkill.SKILL_GROUP[skillGroup].get(nowLevel)
        coinRequired = skillInfo.get('levelUpMoney')
        itemTemplateID = skillInfo.get('itemRequired')
        requiredCount = skillInfo.get('itemCountRequired')
        self._owner.finance.updateCoin(self._owner.finance.getCoin()-coinRequired)
        self._owner.quest.specialTaskHandle(104)#特殊任务处理
        if itemTemplateID and requiredCount:
            self._owner.pack.delItemByTemplateId(itemTemplateID,requiredCount)
        itemInfo = dbaccess.all_ItemTemplate.get(itemTemplateID)
        self._owner.daily.noticeDaily(12,0,-1)
        msg = Lg().g(477)%(skillInfo.get('skillName'),\
                    requiredCount,itemInfo.get('name'))
        return {'result':True,'message':msg}
    
    def getSkillSettingInfo(self):
        '''获取技能设置信息'''
        skillSettingInfo = []
        for skillIndex in range(1,4):
            info = {}
            info['skillInfo'] ={}
            equipSkillGroup = self._equipActiveSkill['ActiveSkill_%d'%skillIndex]
            if equipSkillGroup==-1:#未解锁
                info['skillStatus'] = 0
            elif equipSkillGroup==0:#未装备
                info['skillStatus'] = 1
            else:
                info['skillStatus'] = 2
                nowLevel = self.learned_skillpool[equipSkillGroup].get('skillLevel')
                info['skillInfo'] = dbSkill.SKILL_GROUP[equipSkillGroup][nowLevel]
                nextSkillInfo= dbSkill.SKILL_GROUP[equipSkillGroup].get(nowLevel+1)
                if nextSkillInfo:
                    info['skillInfo']['levelUpEffect'] = nextSkillInfo.get('skillDescript','')
                else:
                    info['skillInfo']['levelUpEffect'] = Lg().g(478)
            skillSettingInfo.append(info)
        return skillSettingInfo
    
    def getSkillTreeInfo(self):
        '''获取角色技能树信息'''
        skillTreeInfo = []
        profession = self._owner.profession.getProfession()
        allSkillGroup = dbSkill.PROFESSION_SKILLGROUP.get(profession,[])+\
                        dbSkill.PROFESSION_SKILLGROUP.get(0,[])
        for groupID in allSkillGroup:
            skillId = self.getSkillTreeNowSkill(groupID)
            info = {}
            info['skillInfo'] = dbSkill.ALL_SKILL_INFO[skillId]
            nowLevel = info['skillInfo'].get('level',1)
            nextSkillInfo= dbSkill.SKILL_GROUP[groupID].get(nowLevel+1,{})
            info['skillStatus'] = {True:1,False:0}.get(groupID not\
                                                        in self.learned_skillpool)
            itemTemplateID = nextSkillInfo.get('itemRequired')
            itemInfo = dbaccess.all_ItemTemplate.get(itemTemplateID,{})
            if nextSkillInfo:
                info['skillInfo']['levelUpEffect'] = nextSkillInfo.get('skillDescript','')
            else:
                info['skillInfo']['levelUpEffect'] = Lg().g(478)
            info['skillInfo']['itemNeed'] = itemInfo.get('name','')
            skillTreeInfo.append(info)
        return skillTreeInfo
    
    def getSkillTreeNowSkill(self,groupId):
        '''获取技能组当前该显示的技能的ID'''
        if groupId not in self.learned_skillpool:
            info = dbSkill.SKILL_GROUP[groupId].get(1)
            return info.get('skillId')
        nowLevel = self.learned_skillpool[groupId].get('skillLevel')
        info = dbSkill.SKILL_GROUP[groupId].get(nowLevel)
        return info.get('skillId')
    
    def getSkillNullSpace(self):
        '''获取技能空位'''
        self._equipActiveSkill = {'ActiveSkill_1':0,
                                      'ActiveSkill_2':-1,
                                      'ActiveSkill_3':-1}
        if self._equipActiveSkill.get('ActiveSkill_1')>=0:
            return 1
        elif self._equipActiveSkill.get('ActiveSkill_2')>=0:
            return 2
        elif self._equipActiveSkill.get('ActiveSkill_3')>=0:
            return 3
        return -1
        
        
    def updateSkillSetting(self,skillGroup,space):
        '''更新技能设置
        @param skillGroup:int 技能组的ID
        @param space: int 技能槽的位置  (1~5)主动技能槽的位置 (6~7)被动技能槽的位置
        '''
        if space<0:
            realySpace = self.getSkillNullSpace()
        else:
            realySpace = space+1
        if realySpace not in [1,2,3]:
            return {'result':False,'message':Lg().g(480)}
        if self._equipActiveSkill.get('ActiveSkill_%d'%realySpace,-1)==-1:
            return {'result':False,'message':Lg().g(481)}
        if self.checkSkillHasEquiped(skillGroup) and skillGroup:
            return {'result':False,'message':Lg().g(482)}
        if  not self.learned_skillpool.has_key(skillGroup) and skillGroup:
            return {'result':False,'message':Lg().g(474)}
        if skillGroup == self.CATCHPETSKILLGROUP and not self.checkCanEquipCatchSkill():
            level = self.getCatchPetLevel()
            return {'result':False,'message':Lg().g(483)%level}
        oldSkillGroup = self._equipActiveSkill['ActiveSkill_%d'%realySpace]
        self._equipActiveSkill['ActiveSkill_%d'%realySpace] = skillGroup
        fieldName = 'ActiveSkill_%d'%realySpace
        result = dbSkill.updateCharacterSkillSet(self._owner.baseInfo.id,\
                                                  fieldName, skillGroup)
        if result:
            if skillGroup:
                self._owner.quest.specialTaskHandle(103)
                level = self.learned_skillpool[skillGroup].get('skillLevel',0)
                nowskillInfo = dbSkill.SKILL_GROUP[skillGroup][level]
                skillname = nowskillInfo.get('skillName')
                msg = Lg().g(484)%(level,skillname)
            elif oldSkillGroup:
                oldlevel = self.learned_skillpool[oldSkillGroup].get('skillLevel',0)
                oldkillInfo = dbSkill.SKILL_GROUP[oldSkillGroup][oldlevel]
                oldskillname = oldkillInfo.get('skillName')
                msg = Lg().g(485)%(oldlevel,oldskillname)
            else:
                return {'result':False}
            return {'result':True,'message':msg}
        else:
            return {'result':False,'message':Lg().g(486)}
        
    def checkSkillHasEquiped(self,skillGroup):
        '''检测技能释放已装备
        @param skillGroup: int 技能的ID
        '''
        equipskillList = self._equipActiveSkill.values()
        if skillGroup in equipskillList:
            return True
        return False
        
    def OpenBattleSpace(self,spacePos):
        '''开启战斗技能位置'''
        if spacePos not in [0,1,2]:
            return {'result':False,'message':Lg().g(487)}
        fieldName = 'ActiveSkill_%d'%(spacePos+1)
        if self._equipActiveSkill[fieldName]!= -1:
            return {'result':False,'message':Lg().g(488)}
        result1 = self._owner.finance.addGold(-500)
        if not result1:
            msg = u'您的钻不足'
            return {'result':False,'message':msg}
        result = dbSkill.updateCharacterSkillSet(self._owner.baseInfo.id, fieldName, 0)

        if result:
            self._equipActiveSkill[fieldName] = 0
            return {'result':True,'message':Lg().g(489)}
        return {'result':False,'message':Lg().g(490)}
    
    def getActiveSkillList(self):
        '''获取角色技能列表'''
        activeSkillList = []
        for skillIndex in range(1,4):
            equipSkillGroup = self._equipActiveSkill['ActiveSkill_%d'%skillIndex]
            if equipSkillGroup>0:
                nowLevel = self.learned_skillpool[equipSkillGroup].get('skillLevel',1)
                skillInfo = dbSkill.SKILL_GROUP[equipSkillGroup].get(nowLevel)
                if skillInfo:
                    activeSkillList.append(skillInfo.get('skillId'))
        return activeSkillList
        
    def autoUnloadCatch(self):
        '''自动卸载战斗技能'''
        realySpace = ''
        for key ,value in self._equipActiveSkill.items():
            if value == self.CATCHPETSKILLGROUP:
                realySpace = key
                break
        if realySpace and not self.checkCanEquipCatchSkill():
            self._equipActiveSkill[realySpace] = 0
            dbSkill.updateCharacterSkillSet(self._owner.baseInfo.id,\
                                                  realySpace, 0)
            self.pushAutoUnloadCatch()
            
    def pushAutoUnloadCatch(self):
        '''推送自动卸载了抓宠技能的消息'''
        msg = u"<font color = '#FFFF00'>背包中缺少封印石，请及时补充</font>"
        pushPromptedMessage(msg, [self._owner.getDynamicId()])
        
        
        
