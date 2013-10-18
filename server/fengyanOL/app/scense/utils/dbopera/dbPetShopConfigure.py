#coding:utf8
'''
Created on 2012-6-1
宠物商店最右侧 推荐宠物组合
@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
dbpool=dbaccess.dbpool
lists={}
def getAll():
    '''获取所有组合信息'''
    global lists
    sql="select * from tb_pet_shop_configure"
    cursor=dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    if result:
        for item in result:
            lists[item['typeid']]=item
    return lists
