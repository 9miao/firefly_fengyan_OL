#coding:utf8
'''
Created on 2011-8-12

@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

All_MonsterInfo = {}

def getAllMonsterInfo():
    '''获取所有怪物的信息'''
    global All_MonsterInfo
    sql = "SELECT * FROM tb_monster"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    allmonsterInfo = {}
    for monster in result:
        All_MonsterInfo[monster['id']] = monster
    return allmonsterInfo

def getById(id):
    '''根据怪物id获取怪物信息'''
    sql="select * from tb_monster where id=%d"%id
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result
