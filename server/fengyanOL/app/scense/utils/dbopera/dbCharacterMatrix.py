#coding:utf8
'''
Created on 2011-12-19
角色阵法设置信息
@author: lan
'''
from app.scense.utils import dbaccess,util
from MySQLdb.cursors import DictCursor

def getAllCharacterMatrix(characterId):
    '''获取角色的所有的阵法设置信息'''
    sql = "SELECT eyes_1,eyes_2,eyes_3,eyes_4,eyes_5,eyes_6,eyes_7,eyes_8,\
    eyes_9 FROM tb_character_matrix WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result


def getCharacterMatrixInfo(characterId,matrixId):
    '''获取角色阵法信息'''
    sql = "SELECT * FROM tb_character_matrix WHERE\
     characterId = %d and matrixId = %d"%(characterId,matrixId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    

def InsertCharacterMatrixInfo(characterId,props):
    '''插入角色的阵法设置信息'''
    sql = "INSERT INTO tb_character_matrix "
    sql = util.forEachInsertByProps(sql, props)
    #print sql
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def updateCharacterMatrixInfo(characterId,props):
    '''更新角色的阵法设置信息
    @param characterId: int 角色的id
    @param matrixId: int 阵法的id
    @param props: dict 更新的属性
    '''
    sql = "UPDATE tb_character_matrix set "
    sql = util.forEachUpdateProps(sql, props)
    sql += " where characterId = %d" %( characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False



