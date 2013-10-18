#coding:utf8
'''
Created on 2011-11-20
传送门表的操作
@author: lan
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

dbaccess = dbaccess

ALL_PORTALS = {}#所有传送门的信息
all=[] #所有传送门信息

def getAllPortalsInfo():
    '''获取所有传送门的信息'''
    global ALL_PORTALS
    sql = "SELECT * FROM tb_portals"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for portalInfo in result:
        ALL_PORTALS[portalInfo['id']] = portalInfo
        all.append(portalInfo)
        

