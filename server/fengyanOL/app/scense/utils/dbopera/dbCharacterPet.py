#coding:utf8
'''
Created on 2011-12-14

@author: lan
'''

from app.scense.utils import dbaccess,util
from MySQLdb.cursors import DictCursor

PET_SKILL_POOL = {}
PET_SKILLGROUP = {}
PET_TRAIN_CONFIG = {}
PET_TEMPLATE = {}#宠物模板表
PET_TYPE = {}
PET_EXP = {}
PET_GROWTH = {}
PET_ITEM = {}#宠物与需要收集的道具的关系

#shopAll1=[]#灵兽商店50以下所有宠物
shopAll={1:[],2:[],3:[]}#    1高级宠物  2中级宠物  3低级宠物 根据宠物颜色来
shopXy=[]#50以幸运领取的宠物

##shopAll2=[]#幻兽商店50-70
#shopAll2={1:[],2:[],3:[]}#幻兽商店50-70   1高级宠物  2中级宠物  3低级宠物
#shopXy2=[]#50-70 幸运领取的宠物
#
##shopAll3=[]#圣兽商店70以上
#shopAll3={1:[],2:[],3:[]}#圣兽商店70以上      1高级宠物  2中级宠物  3低级宠物
#shopXy3=[]#70以上 幸运领取的宠物

def getPetExp():
    '''获取宠物的经验表'''
    global PET_EXP
    sql = "SELECT * FROM tb_pet_experience"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for exp in result:
        PET_EXP[exp['level']] = exp['ExpRequired']
        
def getAllPetGrowthConfig():
    '''获取宠物成长配置
    '''
    global PET_GROWTH
    sql = "SELECT * FROM tb_pet_growth"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for growthconfig in result:
        attrType = growthconfig['pettype']
        quality = growthconfig['quality']
        if not PET_GROWTH.has_key(attrType):
            PET_GROWTH[attrType] = {}
        PET_GROWTH[attrType][quality] = growthconfig

def getAllPetTemplate():
    '''获取宠物的模板信息'''
    from app.scense.applyInterface import configure
    global PET_TEMPLATE,shopAll,shopXy,PET_TYPE
    sql = "SELECT * FROM tb_pet_template ORDER BY `level` , `id`;"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for pet in result:
        attrType = pet['attrType']
        if not PET_TYPE.has_key(attrType):
            PET_TYPE[attrType] = []
        PET_TYPE[attrType].append(pet['id'])
        PET_TEMPLATE[pet['id']] = pet

        if pet['coin']>0:
            zi=configure.getzizhidengji(pet['baseQuality'])
            if zi>0: 
                shopAll[zi].append(pet)
        if pet['xy']>0:
            shopXy.append(pet)
        
    initPETITEM()
                
def initPETITEM():
    """初始化宠物与需要收集的道具的关系
    """
    global PET_ITEM
    for pet in PET_TEMPLATE.values():
        soulrequired = pet['soulrequired']
        if soulrequired:
            PET_ITEM[soulrequired] = pet['id']
            
def sortPetType():
    '''排序宠物的各个分类'''
            

def getAllPetSkill():
    '''获取所有的宠物技能'''
    global  PET_SKILL_POOL,PET_SKILLGROUP
    sql = "SELECT * FROM tb_pet_skill"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for skill in result:
        PET_SKILL_POOL[skill['skillID']] = skill
        if not PET_SKILLGROUP.has_key(skill['skillGroup']):
            PET_SKILLGROUP[skill['skillGroup']] = {}
        PET_SKILLGROUP[skill['skillGroup']][skill['level']] = skill

def getPetTrainConfig():
    '''获取宠物培养配置信息'''
    global PET_TRAIN_CONFIG
    sql = "SELECT * FROM tb_pet_training "
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for train in result:
        PET_TRAIN_CONFIG[train['quality']] = train
    return result

def getPetInfoById(petId):
    '''更具宠物的ID获取宠物的信息'''
    sql = "SELECT * FROM tb_pet WHERE id = %d"%petId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def getCharacterAllPet(chacterId):
    '''获取角色的所有的宠物信息
    @param chacterId: int 角色的id
    '''
    sql = "SELECT id FROM tb_pet WHERE ownerID = %d"%chacterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def updatePetInfo(petId,prop):
    '''更新宠物的信息'''
    sql = 'update `tb_pet` set'
    sql = util.forEachUpdateProps(sql, prop)
    sql += " where id = %d" % petId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def InsertPetInfoInDB(characterId,template,hp,quality):
    '''插入宠物数据信息'''
    sql = "INSERT INTO tb_pet(ownerID,templateID,hp,quality) VALUES (%d,%d,%d,%d)"\
    %(characterId,template,hp,quality)
    sql2 = "SELECT @@IDENTITY"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.execute(sql2)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return 0

def InsertPetInfoInDB_new(characterId,template,hp,StrGrowth,WisGrowth,
                          VitGrowth,DexGrowth,level):
    '''插入宠物数据信息'''
    sql = "INSERT INTO tb_pet(ownerID,templateID,hp,StrGrowth,\
    WisGrowth,VitGrowth,DexGrowth,level) VALUES (%d,%d,%d,%d,%d,%d,%d,%d)"\
    %(characterId,template,hp,StrGrowth,WisGrowth,VitGrowth,DexGrowth,level)
    sql2 = "SELECT @@IDENTITY"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.execute(sql2)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return 0

def DelPetInfo(petId):
    '''删除宠物的信息'''
    sql = "DELETE FROM tb_pet WHERE id = %d"%petId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False
    
def getCharacterCollect(characterId):
    '''获取角色已经收集到的的宠物信息'''
    sql = "SELECT collect FROM tb_character_collect WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return None
    
def insertCharacterCollect(characterId):
    '''加入角色收集信息'''
    sql = "INSERT INTO tb_character_collect(characterId) values('%d')"%characterId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def updateCharacterCollect(characterId,collectList):
    ''''''
    collectstr = str(collectList)[1:-1]
    sql = "UPDATE tb_character_collect set collect = '%s' WHERE characterId = '%d'"\
    %(collectstr,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False




    