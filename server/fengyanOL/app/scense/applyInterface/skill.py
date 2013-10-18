#coding:utf8
'''
Created on 2011-4-21

@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

def getSkillTreeInfo(dynamicId,characterId):
    '''获取角色技能数信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    skillTree = player.skill.getSkillTreeInfo()
    return {'result':True,'data':skillTree}

def getSkillSettingInfo(dynamicId,characterId):
    '''获取角色的技能设置信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    skillSettingInfo = player.skill.getSkillSettingInfo()
    return {'result':True,'data':skillSettingInfo}

def activationSkill(dynamicId,characterId,skillId):
    '''激活技能
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param skillId: int 技能id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.skill.activationSkill(skillId)
    pushOtherMessage(905,result.get('message',''), [dynamicId])
    return result

def skillLevelUp(dynamicId,characterId,skillId):
    '''技能升级'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.skill.LevelUpSkill(skillId)
    pushOtherMessage(905,result.get('message',''), [dynamicId])
    return result

def OpenBattleSpace(dynamicId,characterId,spacePos):
    '''激活技能槽'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.skill.OpenBattleSpace(spacePos)
    pushOtherMessage(905,result.get('message',''), [dynamicId])
    return result

#====================================过期的接口=====================

def getAllSkills(dynamicId,characterId):
    '''获取所有的技能
    @param dynamicId: int 动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    allSkills = player.skill.getProfessionAllSkills()
    return {'result':True,'data':allSkills}

def getLearnedSkills(dynamicId,characterId):
    '''获取已学技能的信息
    @param dynamicId: int 动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    skillsInfo = player.skill.getLearnedSkillsInfo()
    return {'result':True,'data':skillsInfo}

def getLearnableSkills(dynamicId,characterId):
    '''获取能学技能的信息
    @param dynamicId: int 动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(id)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    skillsInfo = player.skill.getLearnableSkills()
    return {'result':True,'data':skillsInfo}

def equipSkill(dynamicId,characterId,skillInstanceId,skillPosition):
    '''装备技能
    @param dynamicId: int 动态id
    @param characterId: int 角色的id
    @param skillTeamplateId: int 已学技能的实例id
    @param skillPosition: int 技能的位置 1:第一技能  2:第二技能  3:第三技能
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.skill.updateSkillSetting(skillInstanceId,skillPosition)
    pushOtherMessage(905,result.get('message',''), [dynamicId])
    return result


