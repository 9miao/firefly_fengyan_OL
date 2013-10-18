#coding:utf8
'''
Created on 2011-11-18

@author: lan
'''
from app.scense.utils import dbaccess

All_ShieldWord = []

def getAll_ShieldWord():
    '''获取所有的屏蔽字'''
    sql = "SELECT sword FROM tb_shieldword;"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result