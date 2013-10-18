#coding:utf8
'''
Created on 2012-2-15
城镇场景
@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
Allinfo={}
def getAllInfo():
    '''获取所有城镇的信息'''
    global Allinfo
    sql='SELECT * FROM tb_publicscene'
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    if data:
        for item in data:
            Allinfo[item['id']]=item
    return data