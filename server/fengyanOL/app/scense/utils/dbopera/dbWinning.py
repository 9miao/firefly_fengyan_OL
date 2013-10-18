#coding:utf8
'''
Created on 2011-12-21
连胜查询
@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor 

def add(pid):
    '''添加连胜纪录'''
    sql="INSERT  INTO `tb_winning`(`pid`,`count`) VALUES ("+str(pid)+",1)"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def update(pid):
    sql="UPDATE tb_winning SET COUNT=COUNT+1 WHERE pid="+str(pid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def set0(pid):
    sql="UPDATE tb_winning SET COUNT=0 WHERE pid="+str(pid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def getAll():
    sql="SELECT * FROM tb_winning"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    list={}
    if not data:
        return list
    else:
        for item in data:
            list[item['pid']]=item
        return list
    
