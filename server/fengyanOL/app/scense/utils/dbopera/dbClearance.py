#coding:utf8
'''
Created on 2012-6-20
通关副本的记录
@author: Administrator
'''

from app.scense.utils import dbaccess


def getClearanceRecord(characterId):
    '''获取角色所有的通关副本的ID
    @param characterId: int 角色的id
    '''
    sql = "select instanceid from `tb_instance_record_id` where characterId=%d"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    recordlist = []
    for record in result:
        recordlist.append(record[0])
    return recordlist

def getGroupRecord(characterId):
    '''获取角色副本组通关记录
    '''
    sql = "select instanceid from `tb_instance_record` where characterId=%d"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    recordlist = []
    for record in result:
        recordlist.append(record[0])
    return recordlist



