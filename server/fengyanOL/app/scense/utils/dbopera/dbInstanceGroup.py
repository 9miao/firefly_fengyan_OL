#coding:utf8
'''
Created on 2011-11-21
副本组（跟传送阵相联系）
@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

def getAllInfo():
    '''获取所有副本组信息'''
    sql="SELECT * FROM tb_instance_group"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return data
     

def getInstanceGroupBycszid(id):
    '''根据传送门id获取副本组列表'''
    sql="SELECT * FROM tb_instance_group WHERE csz="+str(id)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return data

#def getInstanceGroupByid(id):
#    '''根据副本组id获取副本组信息'''
#    sql="SELECT * FROM tb_instance_group WHERE id="+str(id)
#    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
#    cursor.execute(sql)
#    data = cursor.fetchall()
#    cursor.close()
#    return data

#def getFristInstanceBy(id):
#    '''根据副本id获取副本组id
#    @param id: int 副本id
#    '''
#    sql="SELECT id FROM  tb_instance_group WHERE levela="+str(id)+" OR levelb="+str(id)+" OR levelc="+str(id)
#    cursor = dbaccess.dbpool.cursor()
#    cursor.execute(sql)
#    data = cursor.fetchone()
#    cursor.close()
#    if not data:
#        return None
#    return data[0]
#def getInfoByFristid(id):
#    '''根据副本组的id获取副本信息
#    @param id: int 副本组中难度最低的那个副本的id
#    @param return: [] 副本组信息
#    '''
#    sql=" select * from tb_instance_group where id="+str(id)+""
#    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
#    cursor.execute(sql)
#    data = cursor.fetchone()
#    cursor.close()
#    if not data:
#        return None
#    return data