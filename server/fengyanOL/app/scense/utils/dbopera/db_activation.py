#coding:utf8
'''
Created on 2012-4-23
激活码的处理
@author: Administrator
'''
from app.scense.utils import dbaccess

def checkActivation(activation,characterId):
    '''检测激活码是否可用
    @param characterId: int 角色的id
    @param activation: str 激活码
    @return: int 1可用 2激活码已经被使用 3无效的激活码 4角色已使用过该类型的激活码
    '''
    
    
    sql = "SELECT * from tb_active where active_no = '%s'"%(activation)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    if not result:
        return 3,0
    if result[5]:
        return 2,0
    key_type = result[2]
    used = checkuserUsed(key_type,characterId)
    if used:
        return 4,key_type
    return 1,key_type

def checkuserUsed(key_type,characterId):
    '''判断角色是否使用过该种类型的礼包
    @param characterId: int 角色的id
    @param key_type: int 激活码的类型
    '''
    sql = "SELECT * from tb_active where character_id = %d\
     and key_type = %d"%(characterId,key_type)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    if result:
        return True
    return False

def useActivation(activation,key_type,characterId):
    '''使用激活码
    @param characterId: int 角色的id
    @param activation: str 激活码
    @param key_type: int 激活码的类型
    '''
    sql = "update tb_active set character_id = %d,used = %d\
     where active_no = '%s' and key_type = %d"%(characterId,1,activation,key_type)
    cursor = dbaccess.dbpool.cursor()
    count=cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>0:
        return True
    return False
    
def insertActivation(activation,key_type,characterId,used):
    '''插入激活码记录
    @param activation: str 激活码
    @param key_type: int 类型
    @param characterId: int 角色的ID
    @param used: int 是否被已经使用 
    '''
    sql = "INSERT INTO tb_active(active_no,key_type,character_id,used)\
     VALUES('%s',%d,%d,%d)"%(activation,key_type,characterId,used)
    cursor = dbaccess.dbpool.cursor()
    count=cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>0:
        return True
    return False
    
def getUsernameByCharacterId(characterId):
    '''根据角色ID获取用户名
    '''
    sql = "SELECT username FROM tb_register WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    if result:
        return result[0].lower()
    return ''
    
    
    
