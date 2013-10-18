#coding:utf8
'''
Created on 2012-2-15
殖民奖金记录表
@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

def addLog(name,type,price,defencecount,clearancecount,pid,ismax,reward,tid):
    '''添加殖民奖励记录表
    @param name: 城镇或者副本名称
    @param type: 0副本 1城镇
    @param price: 单次通关奖励
    @param defencecount: 入侵次数
    @param clearancecount: 通关次数
    @param pid: 角色id
    @param ismax: 金币奖励的最大是是否达到 0没有达到    1达到
    @param reward: 奖励金币数量
    '''
    sql="insert  into `tb_defence_bonus`(`name`,`type`,`price`,`defencecount`,`clearancecount`,`pid`,`ismax`,`reward`,`tid`) values ('"+name+"',"+str(type)+","+str(price)+","+str(defencecount)+","+str(clearancecount)+","+str(pid)+","+str(ismax)+","+str(reward)+","+str(tid)+")"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def addCityLog(name,pid,reward,tid,type=1):
    '''添加殖民奖励记录表
    @param name: 城镇或者副本名称
    @param type: 0副本 1城镇
    @param pid: 角色id
    @param reward: 奖励金币数量
    @param tid: int 副本或者城市id
    '''
    sql="insert  into `tb_defence_bonus`(`name`,`type`,`pid`,`reward`,`tid`) values ('"+name+"',"+str(type)+","+str(pid)+","+str(reward)+","+str(tid)+")"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False


def delAll():
    '''删除所有奖励'''
    sql="delete from `tb_defence_bonus` "
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def delBypid(pid):
    '''根据角色id删除该角色所获得的奖励'''
    sql="delete from `tb_defence_bonus` where pid="+str(pid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False
    
def delByid(id):
    '''根据主键id 删除奖励'''
    sql="delete from `tb_defence_bonus` where id="+str(id)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False


def getByid(id):
    '''根据保卫奖励表主键id获取奖励信息'''
    sql="select * from tb_defence_bonus where id="+str(id)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def getAllBonusBypid(pid):
    '''根据角色id获取保卫奖励表中的所有奖励的游戏币数量'''
    sql="SELECT SUM(reward) FROM tb_defence_bonus WHERE pid="+str(pid)
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return 0
    return data[0]

def getInfoByPid(pid):
    '''获得所有奖励信息，听过角色id
    @param pid: int 获得奖励的角色id
    '''
    sql="SELECT * FROM tb_defence_bonus  WHERE pid="+str(pid)+" ORDER BY type desc"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()#当前页的信息
    cursor.close()
    if not data:
        return None
    return data

def getRewardList(pid,page,counts):
    '''根据角色id，获取保卫奖励，分页
    @param pid: int 角色id
    @param page: int 当前页
    @param counts: int 总页数
    '''
    sql="SELECT * FROM tb_defence_bonus  WHERE pid="+str(pid)+" ORDER BY type desc"
    sql+=" limit "+str((page-1)*counts)+","+str(counts)+""
    sql1="SELECT CEILING(COUNT(*)/"+str(counts)+") AS t FROM tb_defence_bonus  WHERE pid="+str(pid)+"" #一共多少页
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()#当前页的信息
    cursor.execute(sql1)
    result2=cursor.fetchone() #共几页
    cursor.close()
    if not data:
        return None,0
    return data,result2['t']

def getCountBypid(pid):
    '''根据角色id，返回此角色是否有保卫奖励'''
    sql="SELECT count(*) as t FROM tb_defence_bonus WHERE  pid="+str(pid)
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return False
    if data[0]<1:
        return False
    return True

def getAllPid():
    '''获取所有获得奖励的角色id'''
    sql="SELECT DISTINCT pid FROM tb_defence_bonus"
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    list=[]
    if data and len(data)>0:
        for item in data:
            list.append(item[0])
        return list
    return None