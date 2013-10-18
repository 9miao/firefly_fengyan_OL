#coding:utf8
'''
Created on 2012-5-15
角色神格相关
@author: Administrator
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor


ALL_GODHEAD = {}#所有的神格信息
ALL_HEADTYPE = {}#所有的神格类型

def getAllGodhead():
    '''获取所有的神格信息'''
    global ALL_GODHEAD
    sql = "SELECT * from tb_godhead;"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    for godhead in result:
        ALL_GODHEAD[godhead['id']] = godhead
        
def getAllHeadtype():
    '''获取所有的神格类型信息
    '''
    global ALL_HEADTYPE
    sql = "SELECT * from tb_godhead_type;"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    for headtype in result:
        ALL_HEADTYPE[headtype['headtype']] = headtype


def activeGodhead(characterId,godheadId):
    '''激活神格
    @param characterId: int 角色的ID
    @param godheadId: int 神格的ID
    '''
    sql = "INSERT INTO tb_character_godhead (characterId,godheadId)\
     values(%d,%d)"%(characterId,godheadId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count<1:
        return False
    return True
    
def getCharacterAllGodhead(characterId):
    '''获取角色所有已激活的神格信息
    '''
    sql = "SELECT godheadId FROM tb_character_godhead WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    godheadlist = []
    for godheadid in result:
        godheadlist.append(godheadid[0])
    return godheadlist
        
        
        
