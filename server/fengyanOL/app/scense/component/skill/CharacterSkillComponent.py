#coding:utf8
'''
Created on 2009-12-2

@author: wudepeng
'''
from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbSkill

SKILLITEM = {1:20030061,2:20030062,3:20030063,4:20030064,5:20030065}

class CharacterSkillComponent(Component):
    '''
    skill component for character
    '''

    def __init__(self, owner):
        '''xx
        Constructor
        @param activeSkill: []skill object
        @param auxiliarySkills: []skill object
        @param passiveSkills: []skill object 
        '''
        Component.__init__(self, owner)
        self._equipActiveSkill = [] #装备的技能列表
        self._allSkillGroup = []    #角色的技能分组
        self.learned_skillpool = []   #已学技能
#        self.initSkills()
        
    def initSkills(self):
        '''初始化技能'''
        characterId = self._owner.baseInfo.id 
        learnedSkills = dbSkill.getCharacterLearnedSkill(characterId)
        for skill in learnedSkills:
            self.learned_skillpool.append(skill['skillId'])
        equipSkills = dbSkill.getCharacterSkillSetInfo(characterId)
        if not equipSkills:#如果没有技能设置的信息则重新创建
            dbSkill.insertCharacterSkillSet(characterId)
            equipSkills = dbSkill.getCharacterSkillSetInfo(characterId)
        for i in range(1,4):
            try:
                self._equipActiveSkill[i-1] = equipSkills['ActiveSkill_%d'%i]
            except Exception:
                self._equipActiveSkill.append(equipSkills['ActiveSkill_%d'%i])
#        self.setSkillPoint(equipSkills['skillPoint'])
        self.initAllSkillGroup()
        
    def getDBCharacterLearnedSkill(self,characterId):
        '''获取角色技能设置信息'''
        data = dbSkill.getCharacterSkillSetInfo(characterId)
        if not data:
            result = dbSkill.insertCharacterSkillSet(characterId)
            if not result:
                raise "数据库写入出错"
        data = dbSkill.getCharacterSkillSetInfo(characterId)
        return data
        
    def checkSkillLearnable(self,skillId):
        '''检测技能是否是可学技能
        @param skillId: int 技能的id
        '''
        if skillId in self.learned_skillpool:
            return -1#表示技能已学
        if self.resolveSkillLevel(skillId)!=1 and skillId-1 not in self.learned_skillpool:
            return -2#表示技能的上一等级没有学
        requiredProfession = self.resolveSkillProfession(skillId)
        profession = self._owner.profession.getProfession()
        if requiredProfession != profession and requiredProfession!=8:
            return -3#表示职业不符
        if not dbSkill.ALL_SKILL_INFO.get(skillId,None):
            return -4#表示技能不存在
        if dbSkill.ALL_SKILL_INFO[skillId]['levelRequired']>self._owner.level.getLevel():
            return -5#表示角色等级不足
        return 1 #表示技能是可学的
    
    def getCanntLearnReason(self,reasonId):
        '''获取不能学习的原因'''
        reason = {-1:u'您已经掌握了这个技能，不能重复学习',-2:u'技能的上一等级没有学',\
                  -3:u'职业不符，无法学习该技能',-4:u'技能已到顶级',-5:u"角色等级与技能要求不符，不能学习该技能"}
        return reason.get(reasonId)
        
    def getProfessionAllSkills(self):
        '''获取所有职业技能'''
        skills = dbSkill.getSkillByProfession(self._owner.profession.getProfession())
        return list(skills)
    
    def initAllSkillGroup(self):
        '''初始化所有的技能组'''
        skills = dbSkill.getSkillByProfession(self._owner.profession.getProfession())
        self._allSkillGroup = self.skillFilter(skills)
            
    def skillFilter(self,skills):
        '''技能过滤器，过滤掉同种技能选择最高等级的技能
        @param skills: list[int] 技能的id列表
        '''
        return list(set([skill/100 for skill in skills]))
            
    def resolveSkillGroupId(self,skillId):
        '''根据技能解析出技能的技能组ID
        @param skillId: int 技能的ID
        '''
        groupId = skillId/100
        return groupId
    
    def resolveSkillLevel(self,skillId):
        '''解析技能的等级
        @param skillId: int 技能的ID
        '''
        level = skillId%100
        return level
        
    def resolveSkillProfession(self,skillId):
        '''解析技能的职业归属
        @param skillId: int 技能的ID
        '''
        profession = skillId/100000
        return profession
    
    def resolveSkillReleaseType(self,skillId):
        '''解析出技能的释放类型  1主动 2被动
        @param skillId: int 技能的ID
        '''
        releaseType = (skillId%100000)/10000
        return releaseType
    
    def getAllSkills(self):
        '''获取所有的技能'''
        return [groupId*100+1 for groupId in self._allSkillGroup]
    
    def getCanLearnningSkills(self):
        '''获取可学的技能列表'''
        
    def activationSkill(self,skillId):
        '''激活技能'''
        requiredCount = 1
        skillitem = SKILLITEM.get(1)
        count = self._owner.pack.countItemTemplateId(skillitem)
        if count<requiredCount:
            return {'result':False,'message':u'缺少[技能水晶Lv1]'}
        result = self.learnSkill(skillId)
#        if result.get('result',False):
#            self._owner.quest.specialTaskHandle(111)#特殊任务处理
##            self._owner.quest.specialTaskHandle(103)#特殊任务处理
        return result
    
    def LevelUpSkill(self,skillId):
        '''技能升级'''
        result = self.learnSkill(skillId+1)
        if result.get('result',False):
            self._owner.quest.specialTaskHandle(104)#特殊任务处理
        return result
        
    def learnSkill(self,skillId):
        '''学习技能'''
        level = skillId%100
        itemTemplateID = SKILLITEM.get(level)
        requiredCount = 1
        count = self._owner.pack.countItemTemplateId(itemTemplateID)
#        skillInfo = 
        coinRequired = 0#dbSkill.ALL_SKILL_INFO.get(skillId).get('levelUpMoney',0)
        if self._owner.finance.getCoin() < coinRequired:
            return {'result':False,'message':u'资金不足'}
        if count < requiredCount:
            return {'result':False,'message':u'缺少[技能水晶Lv%d]'%level}
        result = self.checkSkillLearnable(skillId)
        if result!=1:
            return {'result':False,'message':self.getCanntLearnReason(result)}
        characterId = self._owner.baseInfo.id
        reason = dbSkill.LearnSkill(characterId, skillId)
        if not reason:
            return {'result':False,'message':u'学习技能失败'}
#        self.updateSkillPoint(skillPoint)
        self.learned_skillpool.append(skillId)
        if reason:
            self._owner.finance.updateCoin(self._owner.finance.getCoin()-coinRequired)
            self._owner.pack.delItemByTemplateId(itemTemplateID,requiredCount)
        return {'result':True,'message':u'学习技能成功'}
        
    def oblivionSkill(self,skillId):
        '''遗忘技能'''
        characterId = self._owner.baseInfo.id
        reason = dbSkill.OblivionSkill(characterId, skillId)
        if not reason:
            return {'result':False,'message':u'遗忘技能失败'}
        skillPoint = self.getSkillPoint() + 10
        self.updateSkillPoint(skillPoint)
        self.learned_skillpool.remove(skillId)
        return {'result':True,'message':u'遗忘技能成功'}
    
    def getSkillSettingInfo(self):
        '''获取技能设置信息'''
        skillSettingInfo = []
        for skillId in self._equipActiveSkill:
            info = {}
            info['skillInfo'] ={}
            if skillId==-1:#未解锁
                info['skillStatus'] = 0
            elif skillId==0:#未装备
                info['skillStatus'] = 1
            else:
                info['skillStatus'] = 2
                info['skillInfo'] = dbSkill.ALL_SKILL_INFO[skillId]
                nextSkillInfo= dbSkill.ALL_SKILL_INFO.get(skillId+1)
                if nextSkillInfo:
                    info['skillInfo']['levelUpEffect'] = nextSkillInfo.get('skillDescript','')
                else:
                    info['skillInfo']['levelUpEffect'] = u'最高等级'
            skillSettingInfo.append(info)
        return skillSettingInfo
    
    def getSkillTreeInfo(self):
        '''获取角色技能树信息'''
        skillTreeInfo = []
        for groupID in self._allSkillGroup:
            skillId = self.getSkillTreeNowSkill(groupID)
            info = {}
            info['skillInfo'] = dbSkill.ALL_SKILL_INFO[skillId]
            nextSkillInfo= dbSkill.ALL_SKILL_INFO.get(skillId+1)
            if nextSkillInfo:
                info['skillInfo']['levelUpEffect'] = nextSkillInfo.get('skillDescript','')
            else:
                info['skillInfo']['levelUpEffect'] = u'最高等级'
            info['skillStatus'] = {True:1,False:0}.get(skillId not in self.learned_skillpool)
            skillTreeInfo.append(info)
        return skillTreeInfo
    
    def getSkillTreeNowSkill(self,groupId):
        '''获取技能组当前该显示的技能的ID'''
        groupSkills = [skillID for skillID in self.learned_skillpool if skillID/100==groupId]
        if not groupSkills:
            return groupId*100+1
        groupSkills.sort()
        return groupSkills[-1]
        
    def updateSkillSetting(self,skillId,space):
        '''更新技能设置
        @param skillId:int 技能的ID
        @param space: int 技能槽的位置  (1~5)主动技能槽的位置 (6~7)被动技能槽的位置
        '''
        if self._equipActiveSkill[space]==-1:
            return {'result':False,'message':u'技能槽尚未激活'}
        if skillId not in self.learned_skillpool and skillId !=0:
            return {'result':False,'message':u'技能尚未学习'}
        try:
            self._equipActiveSkill[space] = skillId
        except Exception:
            return {'result':False,'message':u'技能设置失败'}
        fieldName = 'ActiveSkill_%d'%(space+1)
        result = dbSkill.updateCharacterSkillSet(self._owner.baseInfo.id, fieldName, skillId)
        if result:
            return {'result':True}
        else:
            return {'result':False,'message':u'技能设置失败'}
        
    def OpenBattleSpace(self,spacePos):
        '''开启战斗技能位置'''
        if spacePos not in [0,1,2]:
            return {'result':False,'message':u'技能槽位置不符'}
        if self._equipActiveSkill[spacePos]!= -1:
            return {'result':False,'message':u'技能槽位置已经激活'}
        self._equipActiveSkill[spacePos] = -1
        fieldName = 'ActiveSkill_%d'%(spacePos+1)
        result = dbSkill.updateCharacterSkillSet(self._owner.baseInfo.id, fieldName, 0)
        if result:
            return {'result':True}
        return {'result':False,'message':u'激活失败'}
        
        
    def getCatchPetSkill(self):
        '''获得抓宠技能'''
        if dbSkill.ALL_SKILL_INFO.get(810801):
            self._equipActiveSkill[1] = 810801
            
    def getActiveSkillList(self):
        '''获取角色技能列表'''
        return [skillId for skillId in self._equipActiveSkill if skillId>0]
        
