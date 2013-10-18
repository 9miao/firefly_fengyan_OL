#coding:utf8
'''
Created on 2011-8-29

@author: lan
'''

from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

ALL_SKILL_INFO = {}
SKILL_GROUP = {}
PROFESSION_SKILLGROUP = {}

#buff和buff直接的效果配置
BUFF_BUFF = {}
#buff对技能加成配置表
BUFF_SKILL = {}

def getBuffOffsetInfo():
    '''获取所有buff之间效果的信息配置
    '''
    global BUFF_BUFF
    sql = "SELECT * FROM tb_buff_buff"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    for offset in result:
        if not BUFF_BUFF.has_key(offset['buffId']):
            BUFF_BUFF[offset['buffId']] = {}
        BUFF_BUFF[offset['buffId']][offset['tbuffId']] = offset
    
def getBuffAddition():
    '''获取buff对技能的加成
    '''
    global BUFF_SKILL
    sql = "SELECT * FROM tb_buff_skill"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    for addition in result:
        if not BUFF_SKILL.has_key(addition['buffId']):
            BUFF_SKILL[addition['buffId']] = {}
        BUFF_SKILL[addition['buffId']][addition['skillId']] = addition['addition']

def getAllSkillInfo():
    '''获取所有技能的信息'''
    sql = "SELECT * FROM tb_skill_info"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    data = {}
    for skill in result:
        data[skill['skillId']] = skill
        effectInfo = getSkillEffectByID(skill['effect'])
        data[skill['skillId']]['effect'] = effectInfo
    return data

def getSkillEffectByID(skillEffectID):
    '''获取技能效果ID'''
    sql = "SELECT * FROM tb_skill_effect where effectId=%d"%skillEffectID
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchone()
    return result

def getAllSkill():
    '''初始化技能信息
    #职业技能组
    #技能池
    #技能组
    '''
    global  ALL_SKILL_INFO,SKILL_GROUP,PROFESSION_SKILLGROUP
    sql = "SELECT * FROM tb_skill_info"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for skill in result:
        effectInfo = getSkillEffectByID(skill['effect'])
        skill['effect'] = effectInfo
        ALL_SKILL_INFO[skill['skillId']] = skill
        if not SKILL_GROUP.has_key(skill['skillGroup']):
            SKILL_GROUP[skill['skillGroup']] = {}
        SKILL_GROUP[skill['skillGroup']][skill['level']] = skill
    #初始化职业技能组ID
    for groupID in SKILL_GROUP:
        skillInfo = SKILL_GROUP[groupID].get(1)
        profession = skillInfo.get('profession',0)
        if not PROFESSION_SKILLGROUP.has_key(profession):
            PROFESSION_SKILLGROUP[profession] = []
        PROFESSION_SKILLGROUP[profession].append(groupID)
    
def insertSkillSetting(characterId):
    '''插入技能设置记录
    @param characterId: int 角色的id
    '''
    sql = "INSERT INTO tb_character_skillsetting(characterId) VALUES (%d)"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count<1:
        return False
    return True


def getSkillInfoById(skillId):
    '''根据技能的ID获取技能的信息
    @param skillId: int 技能的ID
    '''
    sql = "SELECT * FROM tb_skill_info WHERE skillId = %d"%skillId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchone()
    return result

def LearnSkill(characterId,skillId):
    '''学习技能
    @param characterId: int 角色的ID
    @param skillId: int 技能的ID
    '''
    sql = "INSERT INTO tb_character_skill(characterId,skillId) VALUES (%d,%d)"%(characterId,skillId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count<1:
        return False
    return True
    
def OblivionSkill(characterId,skillId):
    '''遗忘技能
    @param characterId: int 角色的ID
    @param skillId: int 技能的ID
    '''
    sql = "DELETE FROM tb_character_skill WHERE characterId = %d AND skillId = %d"%(characterId,skillId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count<1:
        return False
    return True

def getCharacterSkillSetInfo(characterId):
    '''获取角色技能设置信息
    @param characterId: int 角色的ID
    '''
    sql = "SELECT ActiveSkill_1,ActiveSkill_2,ActiveSkill_3\
     FROM tb_character_skillsetting WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchone()
    return result

def insertCharacterSkillSet(characterId):
    '''插入角色的技能设置记录
    @param characterId: int 角色的ID
    '''
    sql = "INSERT INTO tb_character_skillsetting (characterId) VALUES (%d)"%characterId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count<1:
        return False
    return True

def updateCharacterSkillSet(characterId,fieldName,skillID):
    '''更新角色技能设置
    @param characterId: int 角色的ID
    @param fieldName: str 字段名
    @param skillID: int 技能id
    '''
    sql = "UPDATE tb_character_skillsetting SET %s = %d WHERE characterId = %d"%(fieldName,skillID,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count<1:
        return False
    return True

def getCharacterLearnedSkill(characterId):
    '''获取角色所有已学技能
    @param characterId: int 角色的ID
    '''
    sql = "SELECT * FROM tb_character_skill WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    return result

def getCharacterSkillPoint(characterId):
    '''获取角色的技能点
    @param characterId: int 角色的ID
    '''
    sql = "SELECT skillPoint FROM tb_character_skillsetting\
     WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    if result:
        return result[0]
    return 0

def updateCharacterSkillPoint(characterId,skillPoint):
    '''更新角色的技能点
    @param characterId: int 角色的ID
    @param skillPoint: int 技能点
    '''
    sql = "UPDATE tb_character_skillsetting SET skillPoint = %d\
     WHERE characterId = %d"%(skillPoint,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count<1:
        return False
    return True
    
def getLearnedSkills(characterId):
    '''获取角色已学技能
    @param characterId: int 角色的id
    '''
    sql = "SELECT a.*,b.releaseType FROM tb_character_skill a,tb_skill_info b\
     WHERE characterId = 1000009 AND a.skillId = b.skillId"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    return result
    
def getSkillByProfession(profession):
    '''获取相关职业的所有技能信息
    @param profession: int 职业的编号
    '''
    sql = "SELECT skillId FROM tb_skill_info WHERE\
     CAST(skillId/100000 AS SIGNED INTEGER )=%d OR\
      CAST(skillId/100000 AS SIGNED INTEGER )=8"%profession
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    data = []
    for skill in result:
        data.append(skill[0])
    return data

##################################################################

def getCharacterLearnedSkills(characterId):
    '''获取角色所有学习过的技能
    @param characterId: int 角色的ID
    '''
    sql = "SELECT skillId,skillLevel FROM tb_character_skill\
     WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    learnedPool = {}
    for learnedskill in result:
        learnedPool[learnedskill['skillId']] = learnedskill
    return learnedPool

def LevelUpCharacterSkill(characterId,skillId):
    '''升级角色技能等级'''
    sql = "UPDATE tb_character_skill SET skillLevel = skillLevel+1 WHERE\
     characterId = %d AND skillId = %d"%(characterId,skillId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count<1:
        return False
    return True

def ActivationSkill(characterId,skillId):
    '''激活技能
    @param characterId: int 角色的ID
    @param skillId: int 技能的ID
    '''
    sql = "INSERT INTO tb_character_skill(characterId,skillId)\
     VALUES (%d,%d)"%(characterId,skillId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count<1:
        return False
    return True

