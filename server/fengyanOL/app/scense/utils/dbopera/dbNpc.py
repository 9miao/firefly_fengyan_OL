#coding:utf8
'''
Created on 2011-10-24
npc 表的操作
@author: lan
'''

from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

dbaccess = dbaccess

ALL_NPCS = {}#所有的npc信息

def getAllNpcInfo():
    '''获取所有npc的信息'''
    global ALL_NPCS
    sql = "SELECT * FROM tb_npc"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for npcInfo in result:
        ALL_NPCS[npcInfo['id']] = npcInfo
    

