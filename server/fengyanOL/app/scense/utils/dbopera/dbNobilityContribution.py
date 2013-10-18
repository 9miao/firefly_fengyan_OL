#coding:utf8
'''
Created on 2012-5-17
俸禄贡献钻点击次数
@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

dbpool=dbaccess.dbpool

def getAll():
    '''获取所有角色点击次数'''
    sql="SELECT * FROM tb_nobility_contribution"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    lists={}
    if result:
        for item in result:
            lists[item['pid']]=item['counts']
        return lists
    return lists

def add(pid):
    '''添加记录'''
    sql="insert  into `tb_nobility_contribution`(`pid`,`counts`) values (%s,%s)"%(pid,2)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False

def updateAdd(pid):
    '''增加该角色点击贡献次数'''
    sql="UPDATE tb_nobility_contribution SET counts=counts+1 WHERE pid=%s"%pid
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False
