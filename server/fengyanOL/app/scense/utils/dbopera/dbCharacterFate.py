#coding:utf8
'''
Created on 2012-6-7

@author: Administrator
'''
from app.scense.utils import dbaccess,util
from MySQLdb.cursors import DictCursor

FATE_TEMPLATE = {}
FATE_GROUP = {0:[],1:[]}

def getAllFateTemplate():
    '''获取命格的模板信息'''
    global FATE_TEMPLATE,FATE_GROUP
    sql = "SELECT * FROM tb_fate_template"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for fate in result:
        FATE_TEMPLATE[fate['id']] = fate
        if not FATE_GROUP.has_key(fate['quality']):
            FATE_GROUP[fate['quality']] = []
        FATE_GROUP[fate['quality']].append(fate['id'])
        
def getCharacterFate(characterId):
    '''获取角色的所有命格信息
    @param characterId: int 角色的ID
    '''
    sql = "SELECT * FROM tb_fate WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getCharacterFateSetting(characterId):
    '''获取角色占星设置的信息
    @param characterId: int 角色的ID
    '''
    sql = "SELECT * FROM tb_character_fate WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def insertCharacterFateSetting(characterId):
    sql = "INSERT INTO tb_character_fate(characterId) values(%d)"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    

def insertFateInfo(templateId,characterId,equip,position):
    '''插入命格信息
    '''
    sql = "INSERT INTO tb_fate(tempalteId,characterId,equip,position) values(%d,%d,%d,%d)"%\
    (templateId,characterId,equip,position)
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

def updateCharacterFateSetting(characterId,prop):
    '''更新角色命格设置
    '''
    sql = 'update `tb_character_fate` set'
    sql = util.forEachUpdateProps(sql, prop)
    sql += " where characterId = %d" % characterId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False


def DelFateInfo(fateId):
    '''删除命格信息
    @param fateId: int 命格的ID
    '''
    sql = "DELETE FROM tb_fate WHERE id = %d"%fateId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False
    
def updateFateInfo(fateId,prop):
    '''更新宠物的信息'''
    sql = 'update `tb_fate` set'
    sql = util.forEachUpdateProps(sql, prop)
    sql += " where id = %d" % fateId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False
    
    
    
    
    
        
        