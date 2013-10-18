#coding:utf8
'''
Created on 2012-4-12

@author: Administrator
'''
from app.scense.utils import dbaccess,util

def getCharacterTrainData(characterId):
    '''获取所有新手奖励的信息'''
    sql = "SELECT * FROM tb_training where characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result

def getCharacterMining(characterId):
    '''获取角色挖矿信息'''
    sql = "SELECT * FROM tb_mining where characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result

def getCharacterTurnRecord(characterId):
    '''获取角色换取记录'''
    sql = "SELECT * FROM tb_turnrecord where characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result

def InsertCharacterTurnRecord(characterId):
    '''插入角色换取经验'''
    sql = "insert into tb_turnrecord(characterId) values(%d)"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    
def InsertCharacterMining(characterId,miningtype,dtime):
    '''记录角色的挖矿'''
    starttime = str(dtime)
    sql = "insert into tb_mining(characterId,miningType,starttime)\
     values(%d,%d,'%s')"%(characterId,miningtype,starttime)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    
def InsertCharacterTrain(characterId,memberId,traintype,dtime):
    '''记录角色的挖矿'''
    starttime = str(dtime)
    sql = "insert into tb_training(characterId,memberId,traintype,starttime)\
     values(%d,%d,%d,'%s')"%(characterId,memberId,traintype,starttime)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    
    
def delCharacterMining(characterId):
    '''删除角色的挖矿记录'''
    sql = "DELETE FROM tb_mining where characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    
def delCharacterTrain(characterId):
    '''删除角色的挖矿记录'''
    sql = "DELETE FROM tb_training where characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()

def updateCharacterMining(characterId,props):
    '''更新角色的挖掘记录'''
    sql = "update `tb_mining` set"
    sql = util.forEachUpdateProps(sql, props)
    sql += " where characterId = %d" % characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    
def updateCharacterTrain(characterId,props):
    '''更新角色的挖掘记录'''
    sql = "update `tb_training` set"
    sql = util.forEachUpdateProps(sql, props)
    sql += " where characterId = %d" % characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    
def updateCharacterTurnRecord(characterId,props):
    '''更新角色点石成金和加急训练信息'''
    sql = "update `tb_turnrecord` set"
    sql = util.forEachUpdateProps(sql, props)
    sql += " where characterId = %d" % characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    


    
    
