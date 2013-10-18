#coding:utf8
'''
Created on 2011-9-17
角色表
@author: SIOP_09
'''
from app.chatServer.utils import dbaccess
from MySQLdb.cursors import DictCursor
dbaccess=dbaccess


def updateDontTalk(pid,flg):
    '''更改角色禁言状态
    @param pid: int 角色id
    @param flg: int 0不禁言   1禁言
    '''
    sql="UPDATE  tb_character SET donttalk=%s WHERE id=%s"%(flg,pid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getInfoByid(characterid):
    '''根据角色id获取角色信息'''
#    SQL_NO_CACHE
    sql="SELECT  id,nickname,profession,`level` FROM tb_character WHERE id="+str(characterid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if data:
        return data
    return None


def getAllInfo():
    '''获取所有角色信息'''
    sql="SELECT * FROM tb_character"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if data:
        return data
    return None
    
    
    