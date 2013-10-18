#coding:utf8
'''
Created on 2012-4-16
战后失败的处理
@author: Administrator
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor


ALLFIGHTFAILOPE = {}#所有的失败消息

def getAllFightFail():
    '''获取所有新手奖励的信息'''
    global ALL_NOVICE_AWARD
    sql = "SELECT * FROM tb_fightfail"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    for fial in result:
        ALLFIGHTFAILOPE[fial['sceneId']] = fial



