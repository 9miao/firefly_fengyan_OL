#coding:utf8
'''
Created on 2012-9-20
记录角色的消费行为
@author: Administrator
'''

from app.scense.utils import dbaccess


def InsertRecords(valuesStr):
    '''批量记录角色的消费行为记录
    '''
    sql = "INSERT INTO `tb_bill`(`characterId`,`spendType`,`spendGold`,`spendDetails`,`recordDate`,`itemId`)\
        values"+valuesStr
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
