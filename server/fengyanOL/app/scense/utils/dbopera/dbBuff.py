#coding:utf8
'''
Created on 2011-9-9

@author: lan
'''

from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

ALL_BUFF_INFO = {}

def getAllBuffInfo():
    '''获取所有技能的信息'''
    sql = "SELECT * FROM tb_buff_info"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data = {}
    for buff in result:
        data[buff['buffId']] = buff
        effectInfo = getBuffEffect(buff['buffEffectID'])
        data[buff['buffId']]['buffEffects'] = effectInfo
    return data

def getBuffEffect(buffEffectID):
    '''获取buff效果'''
    sql = "SELECT * FROM tb_buff_effect where buffEffectID = %d"%buffEffectID
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result
    
    
    
    