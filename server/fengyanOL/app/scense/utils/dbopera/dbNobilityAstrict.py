#coding:utf8
'''
Created on 2012-5-16
领取俸禄限制
@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

dbpool=dbaccess.dbpool


def add(pid,istrue,isgx,counts):
    '''添加记录'''
    sql="insert  into `tb_nobility_astrict`(`pid`,`istrue`,`isgx`,`counts`) values (%s,%s,'%s',%s);"%(pid,istrue,isgx,counts)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False
    
def getInfoBypid(pid):
    '''根据角色id获取官爵系统限制信息
    @param pid: int 角色id
    '''
    sql="SELECT * FROM tb_nobility_astrict WHERE pid=%s"%pid
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    if data:
        return data
    return None

def getBypid(pid):
    '''判断是否能够领取俸禄
    return bool
    '''
    sql="SELECT * FROM tb_nobility_astrict WHERE pid=%s AND istrue=1"%pid;
    cursor = dbpool.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    if data:
        return True
    return False

def getAll():
    '''获取所有有爵位的信息'''
    sql="SELECT * FROM tb_nobility_astrict";
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    lists={}
    if result:
        for item in result:
            lists[item['pid']]=item
        return lists
    return lists


def upate(pid,state):
    '''更改领取状态
    @param pid: int 角色id
    @param state: int　-1不能领取    1能够领取
    '''
    sql="UPDATE tb_nobility_astrict SET istrue=%s WHERE pid=%s"%(state,pid)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False
    
def upategx(pid,state):
    '''更改上交贡献状态
    @param pid: int 角色id
    @param state: int　-1不能领取    1能够领取
    '''
    sql="UPDATE tb_nobility_astrict SET isgx='%s' WHERE pid=%s"%(state,pid)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False
    
def updateInfo(pid,istrue,isgx,counts):
    '''更新所有限制信息'''
    sql="UPDATE tb_nobility_astrict SET istrue=%s,isgx='%s',counts=%s WHERE pid=%s"%(istrue,isgx,counts,pid)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False

def clear():
    '''清零，设置所有角色状态为1(可领取)'''
    sql="UPDATE tb_nobility_astrict SET istrue=1,`isgx`='[]',`counts`=0"
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False