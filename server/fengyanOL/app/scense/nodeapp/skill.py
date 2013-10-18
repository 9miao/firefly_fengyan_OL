#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import skill
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.skill import GetSkillInfo_pb2
from app.scense.protoFile.skill import ActivationSkill_pb2
from app.scense.protoFile.skill import LevelUpSkill_pb2
from app.scense.protoFile.skill import LoadSkill_pb2
from app.scense.protoFile.skill import UnLoadSkill_pb2
from app.scense.protoFile.skill import OpenBattleSpace807_pb2
from app.scense.protoFile.skill import getAllSkills_pb2
from app.scense.protoFile.skill import getLearnableSkills_pb2
from app.scense.protoFile.skill import getLearnedSkills_pb2
from app.scense.protoFile.skill import equipSkill_pb2
from app.scense.core.language.Language import Lg

@nodeHandle
def getSkillTreeInfo_801(dynamicId,request_proto):
    '''获取技能数信息'''
    argument = GetSkillInfo_pb2.GetSkillInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetSkillInfo_pb2.GetSkillInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = skill.getSkillTreeInfo(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        skillInfoList = data.get('data')
        for sinfo in skillInfoList:
            info = sinfo['skillInfo']
            skillinfo = response.data.skillInfoList.add()
            skillinfo.skillId = info['skillGroup']
            skillinfo.skillName = info['skillName']
            skillinfo.skillLevel = info['level']
            skillinfo.remainRoleLevel = info['levelRequired']
            skillinfo.skillDes = info['skillDescript']
            skillinfo.releasePreEnergy = info['expendPower']
            skillinfo.levelUpEffect = info['levelUpEffect']
            skillinfo.levelUpProps = info['itemNeed']
            skillinfo.levelUpMoney = info['levelUpMoney']
            skillinfo.levelUpRoleLevel = info['levelRequired']+10
            skillinfo.skillStatus = sinfo['skillStatus']
            skillinfo.icon = info['icon']
            skillinfo.type = info['type']
            skillinfo.skillType = info['skillType']
    return response.SerializeToString()

@nodeHandle
def getSkillSettingInfo_804(dynamicId,request_proto):
    '''获取技能设置信息'''
    argument = GetSkillInfo_pb2.GetSkillInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetSkillInfo_pb2.GetSkillInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = skill.getSkillSettingInfo(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        skillInfoList = data.get('data')
        for sinfo in skillInfoList:
            info = sinfo['skillInfo']
            skillinfo = response.data.skillInfoList.add()
            skillinfo.skillType = 3
            skillinfo.skillStatus = sinfo['skillStatus']
            if sinfo['skillStatus'] == 0 or sinfo['skillStatus']==1:#0未解锁1未装备2已装备
                continue
            skillinfo.skillId = info['skillGroup']
            skillinfo.skillName = info['skillName']
            skillinfo.skillLevel = info['level']
            skillinfo.remainRoleLevel = info['levelRequired']
            skillinfo.skillDes = info['skillDescript']
            skillinfo.releasePreEnergy = info['expendPower']
            skillinfo.levelUpEffect = info['levelUpEffect']
            skillinfo.levelUpProps = Lg().g(619)%(info['skillId']%100)
            skillinfo.levelUpMoney = info['levelUpMoney']
            skillinfo.levelUpRoleLevel = info['levelRequired']+10
            skillinfo.icon = info['icon']
            skillinfo.type = info['type']
            
    return response.SerializeToString()

@nodeHandle
def activationSkill_803(dynamicId,request_proto):
    '''激活技能'''
    argument = ActivationSkill_pb2.ActivationSkillRequest()
    argument.ParseFromString(request_proto)
    response = ActivationSkill_pb2.ActivationSkillResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    skillId = argument.skillId
    data = skill.activationSkill(dynamicId, characterId, skillId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def skillLevelUp_802(dynamicId,request_proto):
    '''技能升级'''
    argument = LevelUpSkill_pb2.LevelUpSkillRequest()
    argument.ParseFromString(request_proto)
    response = LevelUpSkill_pb2.LevelUpSkillResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    skillId = argument.skillId
    data = skill.skillLevelUp(dynamicId, characterId, skillId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def LoadSkill_805(dynamicId,request_proto):
    '''装备技能'''
    argument = LoadSkill_pb2.LoadSkillRequest()
    argument.ParseFromString(request_proto)
    response = LoadSkill_pb2.LoadSkillResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    skillId = argument.skillId
    skillPos = argument.skillPos
    data = skill.equipSkill(dynamicId, characterId, skillId, skillPos)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def UnLoadSkill_806(dynamicId,request_proto):
    '''卸下技能'''
    argument = UnLoadSkill_pb2.UnLoadSkillRequest()
    argument.ParseFromString(request_proto)
    response = UnLoadSkill_pb2.UnLoadSkillResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    skillId = argument.skillId
    skillPos = argument.skillPos
    data = skill.equipSkill(dynamicId, characterId, 0, skillPos)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def OpenBattleSpace_807(dynamicId,request_proto):
    '''激活技能槽'''
    argument = OpenBattleSpace807_pb2.OpenBattleSpaceRequest()
    argument.ParseFromString(request_proto)
    response = OpenBattleSpace807_pb2.OpenBattleSpaceResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    spacePos = argument.spacePos
    data = skill.OpenBattleSpace(dynamicId, characterId, spacePos)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()
    
#========================过期的接口=====================

def getAllSkills(dynamicId,request_proto):######没有
    '''获取所有的技能'''
    argument = getAllSkills_pb2.getAllSkillsRequest()
    argument.ParseFromString(request_proto)
    response = getAllSkills_pb2.getAllSkillsResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = skill.getAllSkills(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        skillsInfo = data.get('data')
        for info in skillsInfo:
            skillInfo = response.data.add()
            skillInfo.skillLevel = info['level']
            for _item in info.items():
                setattr(skillInfo.skillInfo, _item[0], _item[1]) 
            
    return response.SerializeToString()

def getLearnableSkills(dynamicId,request_proto):
    '''获取可学技能信息'''
    argument = getLearnableSkills_pb2.getLearnableSkillsRequest()
    argument.ParseFromString(request_proto)
    response = getLearnableSkills_pb2.getLearnableSkillsResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = skill.getLearnableSkills(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        skillsInfo = data.get('data')
        for info in skillsInfo:
            skillInfo = response.data.add()
            skillInfo.skillLevel = info['level']
            for _item in info.items():
                setattr(skillInfo.skillInfo, _item[0], _item[1]) 
            
    return response.SerializeToString()

def getLearnedSkills(dynamicId,request_proto):
    '''获取已学技能信息'''
    argument = getLearnedSkills_pb2.getLearnedSkillsRequest()
    argument.ParseFromString(request_proto)
    response = getLearnedSkills_pb2.getLearnedSkillsresponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    data = skill.getLearnedSkills(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        skillsInfo = data.get('data')
        for info in skillsInfo:
            skillInfo = response.data.add()
            skillInfo.skillLevel = info['level']
            for _item in info.items():
                setattr(skillInfo.skillInfo, _item[0], _item[1]) 
            
    return response.SerializeToString()
    
def equipSkill(dynamicId,request_proto):
    '''装备技能'''
    argument = equipSkill_pb2.equipSkillRequest()
    argument.ParseFromString(request_proto)
    response = equipSkill_pb2.equipSkillResponse()
    
    
    characterId = argument.id
    skillInstanceId = argument.skillInstanceId 
    skillPosition = argument.skillPosition
    
    data = skill.equipSkill(dynamicId, characterId, skillInstanceId, skillPosition)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()
    