#coding:utf8
'''
Created on 2012-12-6

@author: lan
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

dbaccess = dbaccess


ALL_MAP_INFO = {}#所有的公共地图信息
ALL_DOOR_INFO = {}#所有传送门的信息
ALL_MAP_MONSTER = {}#所有的场景怪物配置


def getAllMapInfo():
    '''获取公共场景信息'''
    global ALL_MAP_INFO
    sql="SELECT * FROM tb_map"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for scene in result:
        ALL_MAP_INFO[scene['id']] = scene
    
def getAllDoorInfo():
    '''获取所有传送门的信息'''
    global ALL_DOOR_INFO
    sql = "SELECT * FROM tb_door"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for portalInfo in result:
        ALL_DOOR_INFO[portalInfo['id']] = portalInfo
        
def getAllMonsterConfig():
    '''获取所有场景的怪物配置信息'''
    global ALL_MAP_MONSTER
    sql = "SELECT * FROM tb_map_monster"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for config in result:
        config['rule'] = eval(config['rule'])
        ALL_MAP_MONSTER[config['id']] = config
        
        
        

        
        