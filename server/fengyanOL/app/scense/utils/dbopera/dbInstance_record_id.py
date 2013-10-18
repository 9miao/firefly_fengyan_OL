#coding:utf8
'''
Created on 2012-4-23
激活码的处理
@author: Administrator
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
dbpool=dbaccess.dbpool

def insertInstanceRecord(characterid,instanceid):
    '''添加副本激活通关记录
    @param characterid: int 角色id
    @param instanceid: int副本id
    @param stateid: int 副本激活通关状态 1激活 2通关
    '''
    sql="insert  into `tb_instance_record_id`(`id`,`characterid`,`instanceid`) values (null,%d,%d)"%(characterid,instanceid)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getInstanceRecordInfo(characterid,instanceid):
    '''获取副本激活通关记录
    @param characterid: int 角色id
    @param instanceid: int副本id
    @param stateid: int 副本激活通关状态 1激活 2通关
    '''
    sql="select * from tb_instance_record_id where characterid=%d and instanceid=%d"%(characterid,instanceid)
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result
    return None

def getisInstanceRecord(characterid,instanceid):
    '''判断角色是否通关副本，返回通关分数 或者没有通关None
    @param characterid: int 角色id
    @param instanceid: int副本id
    '''
    sql="select score from tb_instance_record_id where characterid=%d and instanceid=%d"%(characterid,instanceid)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return None