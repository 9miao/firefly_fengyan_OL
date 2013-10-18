#coding:utf8
'''
Created on 2011-6-21

@author: lan
'''
from app.scense.utils import dbaccess

def getBeginnerByNickName(nickname):
    '''根据昵称获取角色的id
    @param nickname: string 角色的昵称
    '''
    sql = "select id from `tb_beginner` where nickname ='%s'"%nickname
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def getLastInsertBeginnerId():
    sql = "select id from `tb_beginner` where id=LAST_INSERT_ID()"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def creatBeginner():
    sql = "INSERT INTO tb_beginner() VALUES()"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    data = getLastInsertBeginnerId()
    if data:
        return data[0]
    return 0

def updateBeginnerNickname(beginnerId,nickname):
    '''新手引导写入数据库'''
    sql = "UPDATE tb_beginner SET nickname = '%s' where id= %d"%(nickname,beginnerId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count<0:
        return False
    return True

def updateRecordId(beginnerId,recordId):
    '''更新记录记录'''
    sql = "UPDATE tb_beginner SET stepID = %d WHERE id = %d"%(recordId,beginnerId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count<0:
        return False
    return True

def getRandomName():
    '''获取随机名称'''
    sql = "SELECT * FROM tb_namepool ORDER BY RAND() LIMIT 0,1"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def insertGMmsg(characterName,msg):
    '''插入GM消息记录
    '''
    sql = "INSERT INTO tb_gmbug(characterName,`desc`) VALUES('%s','%s')"%(characterName,msg)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count<0:
        return False
    return True



    
    