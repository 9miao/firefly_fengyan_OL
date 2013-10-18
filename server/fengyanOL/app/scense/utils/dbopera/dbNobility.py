#coding:utf8
'''
Created on 2012-5-16

@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
all={}
def getAll():
    '''获取所有爵位信息'''
    global all
    sql = "SELECT * FROM tb_nobility"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    if result:
        for item in result:
            all[item['levels']]=item
    return None
