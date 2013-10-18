#coding:utf8
'''
Created on 2012-2-15
城镇场景
@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

def getDefence_scene_bonus(sid):
    '''根据城市id,获得城市奖励金额'''
    sql='SELECT  * FROM tb_defence_scene_bonus WHERE  sid='+str(sid)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    if not data:
        return 0
    return data['bonus']