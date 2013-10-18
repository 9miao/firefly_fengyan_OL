#coding:utf8
'''
Created on 2012-5-16

@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
dbpool=dbaccess.dbpool
from twisted.python import log

def getBypid(pid,page,counts):
    '''根据角色id获得封爵历史
    @param pid: int 角色id
    @param page: int 当前页数
    @param count: int 每页记录数量
    '''
    sql="SELECT * FROM tb_nobility_history WHERE pid=%s ORDER BY levels"%pid
    
    sql+=" limit "+str((page-1)*counts)+","+str(counts)+""
    
    sql1="SELECT CEILING(COUNT(*)/"+str(counts)+") AS t FROM tb_nobility_history where pid="+str(pid)+" order by levels"  #一共多少页
    
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    
    cursor.execute(sql1)
    result2=cursor.fetchone() #共几页
    cursor.close()

    if not result1:
        return [None,0]
    return [result1,result2['t']]

def add(pid,context,level):
    '''添加爵位省钱记录
    @param pid: int 角色id
    @param context: string 内容
    @param level: int 爵位等级
    '''
    sql="insert  into `tb_nobility_history`(`pid`,`context`,`levels`) values (%s,'%s',%s)"%(pid,context,level)
    try:
        cursor = dbpool.cursor()
        count = cursor.execute(sql)
        dbpool.commit()
        cursor.close()
        if count>=1:
            return True
        return False
    except:
        log.err(sql)
    