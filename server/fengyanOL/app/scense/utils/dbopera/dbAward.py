#coding:utf8
'''
Created on 2012-4-7

@author: Administrator
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

ALL_NOVICE_AWARD = {}

def getAllAwardInfo():
    '''获取所有新手奖励的信息'''
    global ALL_NOVICE_AWARD
    sql = "SELECT * FROM tb_novice_award"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    for award in result:
        ALL_NOVICE_AWARD[award['step']] = award
    return ALL_NOVICE_AWARD



