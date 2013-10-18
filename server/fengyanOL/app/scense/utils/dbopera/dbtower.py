#coding:utf8
'''
Created on 2012-7-17

@author: Administrator
'''
from app.scense.utils import dbaccess,util
from MySQLdb.cursors import DictCursor
import datetime
from twisted.python import log

ALL_TOWER_INFO = {}#克洛塔的所有层数的信息

def initAllTowerInfo():
    '''初始化所有塔层的信息
    '''
    global ALL_TOWER_INFO
    sql = "select * from tb_tower_info"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    for towerinfo in result:
        ALL_TOWER_INFO[towerinfo['id']] = towerinfo
        try:
            rule = eval(towerinfo['rule'])
        except:
            log.err("----------------%d"%towerinfo['id'])
        ALL_TOWER_INFO[towerinfo['id']]['rule'] = rule
 
def getCharacterTowerInfo(characterId):
    '''获取角色的爬塔记录
    '''
    sql = "SELECT * from tb_tower_record where characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchone()
    if not result:
        nowdate = datetime.date.today()
        sql2 = "insert into tb_tower_record(characterId,recordDate)\
         values(%d,'%s')"%(characterId,str(nowdate))
        cursor.execute(sql2)
        dbaccess.dbpool.commit()
        result = {'characterId':characterId,'climbtimes':0,'nowLayers':1,
                  'recordDate':nowdate,'high':0}
    cursor.close()
    return result
    
def updateCharacterTowerRecord(characterId,props):
    '''更新角色的爬塔记录
    '''
    sql = "update `tb_tower_record` set"
    sql = util.forEachUpdateProps(sql, props)
    sql += " where characterId = %d" % characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    
    
    
    