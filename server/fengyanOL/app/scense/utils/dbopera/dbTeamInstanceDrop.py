#coding:utf8
'''
Created on 2012-8-9
组队副本掉落信息
@author: jt
'''

from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

teamInstanceDropAll={} #所有多人副本掉落数据 key:多人副本掉落表主键id
#[物品id,物品数量,1,2],[物品id,物品数量,3,10]
def getAll():
    global teamInstanceDropAll
    sql="select * from tb_teaminstance_drop"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    if result:
        for item in result:
            item['ditem']=eval(item['ditem'])
            teamInstanceDropAll[item['id']]=item
    return None
    