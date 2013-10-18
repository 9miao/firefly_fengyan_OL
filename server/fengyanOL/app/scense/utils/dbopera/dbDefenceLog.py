#coding:utf8
'''
Created on 2012-2-13

@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

#def addLog(firstid,succeedid,succeedname,laird):
#    '''添加保卫记录
#    @param firstid: 副本组第一个副本id
#    @param succeedid: 殖民成功角色id
#    @param succeedname: 殖民成功角色名称
#    '''
#    sql="INSERT tb_defence_log(firstid,succeedid,succeedname,laird) VALUES ("+str(firstid)+","+str(succeedid)+",'"+succeedname+"',"+str(laird)+")"
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if(count >= 1):
#        return True
#    return False

#def delLog(firstid):
#    '''删除所有保卫记录
#    @param firestid: 副本组第一个副本id
#    '''
#    sql="delete from tb_defence_log where firstid="+str(firstid)
#    sql1="delete from tb_defeated_fail_log where firstid="+str(firstid)
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    count1 = cursor.execute(sql1)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if(count >= 1 and count1>=1):
#        return True
#    return False

#def updateLog(firstid,pid,isflg):
#    '''更改保卫记录（更改当前占领副本角色的启用）
#    @param firstid: int 第一个副本id
#    @param pid: int 占领副本的角色id
#    @param isflg: int 0表示没有启用  1表示启用
#    '''
#    sql="UPDATE tb_defence_log SET ENABLE="+str(isflg)+" WHERE firstid="+str(firstid)+" and laird="+str(pid)
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if(count >= 1):
#        return True
#    return False

#def enableFalse(firstid):
#    '''设置所有的保卫开启状态为关闭
#    @param firstid: int 副本组第一个副本的id
#    '''
#    sql="UPDATE tb_defence_log SET ENABLE=0"
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if(count >= 1):
#        return True
#    return False

#def getlog(firstid,laird):
#    '''获取守卫记录，根据副本id和领主角色id
#    @param firstid: int 副本id
#    @param laird: int 领主角色id
#    '''
#    sql="SELECT * FROM tb_defence_log WHERE enable=1 and firstid="+str(firstid)+" AND laird="+str(laird)
#    cursor = dbaccess.dbpool.cursor()
#    cursor.execute(sql)
#    result = cursor.fetchone()
#    cursor.close()
#    if result==None:
#        return None
#    return result

#def getlogBydesc(laird,page,counts):
#    '''根据领主id获取排序后的入侵记录
#    @param page: int 当前页数
#    @param counts: int 每页多少条信息
#    '''
#    sql="SELECT * FROM tb_defence_log AS d WHERE ENABLE=1 ORDER BY typeid desc"
#    sql+=" limit "+str((page-1)*counts)+","+str(counts)+""
#    sql1="SELECT CEILING(COUNT(*)/"+str(counts)+") AS t FROM tb_defence_log AS d WHERE ENABLE=1  " #一共多少页
#    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
#    cursor.execute(sql)
#    data=cursor.fetchall()#当前页的信息
#    cursor.execute(sql1)
#    result2=cursor.fetchone() #共几页
#    cursor.close()
#    if not data:
#        return None,0
#    return data,result2['t']


#def getAllenableTrue():
#    '''获取所有正在占领中的副本殖民信息列表'''
#    sql="SELECT * FROM tb_defence_log WHERE ENABLE=1 and typeid=0"
#    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
#    cursor.execute(sql)
#    data=cursor.fetchall()
#    cursor.close()
#    if not data:
#        return None
#    return data


#def getAllUserid():
#    '''获取所有角色id'''
#    sql="SELECT DISTINCT laird FROM tb_defence_log where enable=1"
#    cursor=dbaccess.dbpool.cursor()
#    cursor.execute(sql)
#    data=cursor.fetchall()
#    cursor.close()
#    if not data:
#        return None
#    return data

#def getAllInstanceidList(pid):
#    '''根据角色id获取副本id列表'''
#    sql="SELECT firstid FROM tb_defence_log WHERE enable=1 and typeid=0 and  laird="+str(pid)
#    cursor=dbaccess.dbpool.cursor()
#    cursor.execute(sql)
#    data=cursor.fetchall()
#    cursor.close()
#    if not data:
#        return None
#    return data

def getCountBypid(pid):
    '''根据角色id，返回此角色是否有保卫奖励'''
    sql="SELECT count(*) as t FROM tb_defence_log WHERE enable=1 and laird="+str(pid)
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return False
    if data[0]<1:
        return False
    return True