#coding:utf8
'''
Created on 2012-8-9
多人副本信息
@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

teamInstanceAll={} #所有多人副本数据 key:副本类型

def getAll():
    global teamInstanceAll
    sql="select * from tb_teaminstance"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    if result:
        for item in result:
            item['dropid']=eval(item['dropid'])
            item['mosters']=eval(item['mosters'])
            teamInstanceAll[item['tpid']]=item
    return None