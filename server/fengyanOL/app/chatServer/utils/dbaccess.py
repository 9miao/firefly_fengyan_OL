#coding:utf8
'''
Created on 2011-3-31

@author: sean_lan
'''
from app.chatServer.utils.dbpool import DBPool
from MySQLdb.cursors import DictCursor
database = ''
dbpool = DBPool()
all_ItemTemplate = {}


def getAll_ItemTemplate():
    sql="select * from `tb_item_template`"
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data = {}
    for _item in result:
        data[_item['id']] = _item
    return data



