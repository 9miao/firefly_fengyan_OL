#coding:utf8
'''
Created on 2012-3-14
商城数据库处理
@author: lan
'''

from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

def getAllMallInfo():
    '''获取所有商城物品信息'''
    sql = "SELECT * FROM tb_mall_item"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    return result
