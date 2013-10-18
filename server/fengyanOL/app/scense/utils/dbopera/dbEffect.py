#coding:utf8
'''
Created on 2011-11-6

@author: lan
'''

from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
import datetime

ALL_EFFECT_INFO = {}

def getAllEffectInfo():
    '''获取所有的效果信息'''
    sql = "SELECT * FROM tb_effect"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data = {}
    for effect in result:
        data[effect['id']] = effect
    return data

def getCharacterEffect(characterId):
    '''获取角色的效果'''
    sql = "SELECT * FROM tb_character_effect WHERE characterID =%d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    return result
    
    
def delCharacterEffect(characterId,effectId):
    '''删除角色身上的效果'''
    sql = "DELETE FROM tb_character_effect WHERE\
     characterId = %d and effectID = %d"%(characterId,effectId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count<1:
        return False
    return True

def addNewItemEffct(characterId,effect):
    '''给角色添加一个物品使用效果'''
    nowtime = str(datetime.datetime.now())
    sql = "INSERT INTO tb_character_effect(characterID,\
    effectID,startTime,surplus) VALUES (%d,%d,'%s',%d)"\
    %(characterId,effect['id'],nowtime,effect['surplus'])
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

def updateEffectInfo(characterId,effectId,surplus):
    '''更新效果信息'''
    sql = "UPDATE tb_character_effect SET surplus = %d WHERE\
     characterId = %d and effectID = %d"%(surplus,characterId,effectId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count<1:
        return False
    return True
    
    
    
    

