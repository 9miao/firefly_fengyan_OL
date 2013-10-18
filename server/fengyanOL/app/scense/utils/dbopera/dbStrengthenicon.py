#coding:utf8
'''
Created on 2011-9-27
冷却时间
@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor



def getAll():
    '''获取所有强化冷却时间信息'''
    global all
    sql="SELECT * FROM tb_strengthenicon"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    all={}
    if not result or len(result)<1:
        return None
    else:
        for item in result:
            all[item.get('pid')]=item
    return all
    
def getByPid(pid):
    '''根据角色id获取冷却时间
    '''
    sql="SELECT * FROM tb_strengthenicon WHERE pid=%s"%pid
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def add(pid,ctime,counts):
    '''添加强化领冷却'''
    sql="insert  into `tb_strengthenicon`(`pid`,`ctime`,`counts`) values (%s,'%s',%s)"%(pid,ctime,counts)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def update(pid,ctime,counts):
    '''更新角色强化时间'''
    sql="UPDATE tb_strengthenicon SET ctime='%s',counts=%s WHERE pid=%s"%(ctime,counts,pid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
