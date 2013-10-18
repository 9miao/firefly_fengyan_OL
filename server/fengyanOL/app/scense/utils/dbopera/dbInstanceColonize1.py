#coding:utf8
'''
Created on 2011-12-21
副本殖民信息表操作
@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor 
from twisted.python import log

#-------------------------------获取-----------------------------------------#

def getInstanceColonizeByid(id):
    '''根据副本id获取副本殖民信息
    @param id: int 副本id
    '''
    sql="SELECT * FROM  tb_instance_colonize1 WHERE enable=1 and instanceid="+str(id)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def getColonizeResistByid(instanceid):
    '''获取卫冕次数'''
    sql="select resist from tb_instance_colonize1 WHERE enable=1 and instanceid="+str(instanceid)
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data[0]


def getGuildClolonizeNumbers(gid):
    '''根据国id查找该国殖民数量
    @param gid: int 国id
    '''
    sql="SELECT COUNT(id) FROM tb_instance_colonize1 WHERE enable=1 and gid="+str(gid)
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data[0]

def getlogBydesc(laird,page,counts):
    '''根据领主id获取排序后的入侵记录
    @param page: int 当前页数
    @param counts: int 每页多少条信息
    '''
    
    try:
        sql="SELECT * FROM tb_instance_colonize1 WHERE ENABLE=1 and pid="+str(laird)+" ORDER BY typeid desc"
        sql+=" limit "+str((page-1)*counts)+","+str(counts)+""
        sql1="SELECT CEILING(COUNT(*)/"+str(counts)+") AS t FROM tb_instance_colonize1 WHERE ENABLE=1 and pid="+str(laird) #一共多少页
        cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
        cursor.execute(sql)
        data=cursor.fetchall()#当前页的信息
        cursor.execute(sql1)
        result2=cursor.fetchone() #共几页
        cursor.close()
        if not data:
            return None,0
        return data,result2['t']
    except:
        log.err(u'dbInstanceColonize1->getlogBydesc(laird=%s,page=%s,counts=%s)'%(laird,page,counts))
    

def getAllenableTrue():
    '''获取所有正在占领中的副本殖民信息列表'''
    sql="SELECT * FROM tb_instance_colonize1 WHERE ENABLE=1 and typeid=0"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if not data:
        return None
    return data

def getAllUserid():
    '''获取所有角色id'''
    sql="SELECT DISTINCT pid FROM tb_instance_colonize1 where enable=1"
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if not data:
        return None
    return data

def getAllInstanceidList(pid):
    '''根据角色id获取副本id列表'''
    sql="SELECT instanceid FROM tb_instance_colonize1 WHERE enable=1 and typeid=0 and  pid="+str(pid)
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if not data or len(data)<1:
        return None
    val=[]
    for item in data:
        val.append(item[0])
    return val



def getIsDefence(instanceid,pid):
    '''是否存在保卫记录（根据副本id和角色id）并且enable=0'''
    sql="SELECT count(*) as t FROM tb_instance_colonize1 WHERE enable=0 and pid="+str(pid)+" and instanceid="+str(instanceid)
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return False
    if data[0]<1:
        return False
    return True

def getInfo(instanceid,pid):
    '''获取殖民信息，通过副本id和角色id'''
    sql="SELECT * FROM tb_instance_colonize1 WHERE enable=1 and pid="+str(pid)+" and instanceid="+str(instanceid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone() 
    cursor.close()
    if not data:
        return None
    return data


