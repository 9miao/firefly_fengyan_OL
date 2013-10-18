#coding:utf8
'''
Created on 2011-9-17
角色表
@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

from twisted.python import log


all=[]

def updateAll():
    '''获取所有殖民头衔获得条件信息'''
    sql="SELECT * FROM tb_instance_colonize_title"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    if not result:
        return all
    elif result:
        for item in result:
            all.append(item)
            
def getname(count):
    '''根据连胜次数获取称号'''
    for item in all:
        if item['min']<count and item['max']>count:
            return item['nickname'] #连胜头衔
    return False
        