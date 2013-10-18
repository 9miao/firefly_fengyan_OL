#coding:utf8
'''
Created on 2011-11-23

@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

def getAllInstanceid():
    '''获取所有副本id'''
    sql="select id from tb_instanceinfo"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    list=[]
    if result:
        for item in result:
            list.append(item[0])
    if len(list)==0:
        return None
    return list
            
def getInstanceInfoById(instanceId):
    '''根据副本的Id获取副本的信息
    @param instanceId: int 副本的id
    '''
    sql = "SELECT * FROM tb_instanceinfo WHERE id = %d"%instanceId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getAllInfo():
    '''获取所有副本信息'''
    sql="select * from tb_instanceinfo"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    sList={}
    for item in result:
        sList[item['id']]=item
    return sList
    
    
    
    
    
        