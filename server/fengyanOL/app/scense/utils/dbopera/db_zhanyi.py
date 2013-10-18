#coding:utf8
'''
Created on 2013-1-8
战役相关数据库操作
@author: lan
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor


ALL_ZHANYI_INFO = {}#所有的战役的信息
ALL_ZHANGJIE_INFO = {}#所有章节的信息
ALL_ZHANGJIE_GROP = {}#战役与章节关系

def getAllZhanYiInfo():
    '''获取所有战役的信息
    '''
    global ALL_ZHANYI_INFO
    sql = "SELECT * FROM tb_zhanyi"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for zhanyi in result:
        ALL_ZHANYI_INFO[zhanyi['id']] = zhanyi
        
        
def getAllZhangJieInfo():
    '''获取章节的信息
    '''
    global ALL_ZHANGJIE_INFO,ALL_ZHANGJIE_GROP
    sql = "SELECT * FROM tb_zhangjie"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for zhangjie in result:
        ALL_ZHANGJIE_INFO[zhangjie['id']] = zhangjie
        if not ALL_ZHANGJIE_GROP.get(zhangjie['yid']):
            ALL_ZHANGJIE_GROP[zhangjie['yid']] = []
        ALL_ZHANGJIE_GROP[zhangjie['yid']].append(zhangjie['id'])
            
def getCharacterZhangJieInfo(characterId):
    '''获取角色的章节信息
    '''
    sql = "SELECT * FROM tb_zhanyi_record where characterId=%d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if not result:
        insertZhangJieInfo(characterId)
        result = {'characterId':characterId,'zhanyi':1000,'zhangjie':1000}
    return result
    
def insertZhangJieInfo(characterId):
    '''插入角色章节记录
    '''
    sql = "INSERT INTO `tb_zhanyi_record`(characterId) values(%d)"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
    
def updateCharacterZhangjie(characterId,zj,zy):
    sql = "UPDATE tb_zhanyi_record SET zhanyi=%d,zhangjie=%d WHERE \
    characterId= %d;"%(zy,zj,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
    
            

        
        