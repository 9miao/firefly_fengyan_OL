#coding:utf8
'''
Created on 2012-2-13
@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

#------------------------------查询--------------------------------------------------#
def getBy(defeatedlogid):
    '''根据保卫表主键id获取入侵者名单
    @param defeatedlogid: int 保卫表主键id
    '''
    sql="SELECT * FROM tb_defeated_fail_log1 WHERE defeatedlogid="+str(defeatedlogid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if not data:
        return None
    return data

def getAllCount(defeatedlogid):
    '''根据保卫表主键id获取入次数
    @param defeatedlogid: int 保卫表主键id
    '''
    sql="SELECT count(id) as t FROM tb_defeated_fail_log1 WHERE defeatedlogid="+str(defeatedlogid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return 0
    return data['t']

def isLogByColonizeAndPid(colonizeid,pid):
    '''根据保卫表主键id和挑战失败者角色id，返回此条记录
    @param colonizeid: int 保卫表主键id
    @param pid: int 挑战失败者角色id
    '''
    sql="SELECT * FROM tb_defeated_fail_log1 WHERE defeatedlogid="+str(colonizeid)+" AND defeatedid="+str(pid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def updateFailLogByid(id,va):
    '''根据挑战失败表主键id,更新时间'''
    sql="UPDATE tb_defeated_fail_log1 SET times='"+va+"' where id="+str(id)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False
