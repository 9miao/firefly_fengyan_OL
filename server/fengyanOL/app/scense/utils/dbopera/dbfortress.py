#coding:utf8
'''
Created on 2012-9-10

@author: Administrator
'''
from app.scense.utils import dbaccess,util
from MySQLdb.cursors import DictCursor

def getAllFortressInfo():
    '''获取所有要塞的占领信息
    '''
    sql = "SELECT * from tb_fortress";
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    return result

def updateFortressInfo(fortressId,props):
    '''更新要塞的信息
    '''
    sqlstr = "update `tb_fortress` set"
    sqlstr = util.forEachUpdateProps(sqlstr, props)
    sqlstr += " where id = %d" % fortressId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sqlstr)
    dbaccess.dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False



