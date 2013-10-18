#coding:utf8
'''
Created on 2011-9-26
行会战数据
@author: lan
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

def getGuildBattleChecklist():
    '''获取行会战清单'''
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    sql = "SELECT * FROM tb_guild_battle WHERE \
    DATE_SUB(CURDATE(), INTERVAL 0 DAY) <= DATE(confirmdTime) AND result = 0"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def creatGuildBattlefield(recordId,battleFieldId):
    '''创建行会战战场'''
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    sql = "UPDATE tb_guild_battle SET \
    battlefieldArea = %d AND result = 1 WHERE id = %d"%(battleFieldId,recordId)
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>0:
        return True
    return False

def getGuildBattlefieldId(guildId):
    '''获取行会战id'''
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    sql = ""
    
    