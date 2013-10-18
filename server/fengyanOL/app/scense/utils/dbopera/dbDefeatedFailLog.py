#coding:utf8
'''
Created on 2012-2-13
@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

#------------------------------添加--------------------------------------------------#

def addLog(groupid, name, pid, pname,sbid,sbname):
    '''添加侵略失败记录
    @param groupid: int 殖民副本组id
    @param name: str 副本组名称
    @param pid: int 领主角色id
    @param pname: int 领主角色名称
    @param sbid: int 挑战失败角色id
    @param sbname: str 挑战失败角色名称
    '''
    sql="INSERT  INTO `tb_defeated_fail_log`(`groupid`,`name`,`pid`,`pname`,`sb`) VALUES (%s,'%s',%s,'%s',\"%s:u'%s'\")"%(groupid,name,pid,pname,sbid,sbname)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def addLogTrue(groupid, name, pid, pname,cgid,cgname):
    '''添加侵略成功记录
    @param groupid: int 殖民副本组id
    @param name: str 副本组名称
    @param pid: int 领主角色id
    @param pname: int 领主角色名称
    @param cgid: int 挑战成功角色id
    @param cgname: str 挑战成功角色名称
    '''
    sql="INSERT  INTO `tb_defeated_fail_log`(`groupid`,`name`,`pid`,`pname`,`cgid`,`cgname`) VALUES (%s,'%s',%s,'%s',%s,'%s')"%(groupid,name,pid,pname,cgid,cgname)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False


def updateLogTrue(groupid, pid,cgid,cgname):
    '''更改添加侵略成功记录
    @param groupid: int 殖民副本组id
    @param pid: int 领主角色id
    @param cgid: int 挑战成功角色id
    @param cgname: str 挑战成功角色名称
    '''
    sql="UPDATE tb_defeated_fail_log SET cgid=%s,cgname='%s' WHERE groupid=%s AND pid=%s"%(cgid,cgname,groupid,pid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False


def addSbLog(groupid, pid,sbid,sbname):
    '''添加侵略失败记录
    @param groupid: int 殖民副本组id
    @param name: str 副本组名称
    @param pid: int 领主角色id
    @param pname: int 领主角色名称
    @param sbid: int 挑战失败角色id
    @param sbname: str 挑战失败角色名称
    '''
    sql="UPDATE tb_defeated_fail_log SET sb=CONCAT(sb,\",%s:u'%s'\") WHERE  groupid=%s AND pid=%s"%(sbid,sbname,groupid,pid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

#------------------------------删除--------------------------------------------------#

def delLog(defeatedlogid):
    '''删除侵略失败记录'''
    sql="DELETE FROM tb_defeated_fail_log WHERE defeatedlogid="+str(defeatedlogid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def delAll():
    '''删除所有入侵失败记录'''
    sql="DELETE FROM tb_defeated_fail_log"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

#------------------------------查询--------------------------------------------------#
def getBy(defeatedlogid):
    '''根据保卫表主键id获取入侵者名单
    @param defeatedlogid: int 保卫表主键id
    '''
    sql="SELECT * FROM tb_defeated_fail_log WHERE defeatedlogid="+str(defeatedlogid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if not data:
        return None
    return data

def getAllCount(defeatedlogid):
    '''根据保卫表主键id获取入次数
    @param defeatedlogid: int 保卫表主键id
    '''
    sql="SELECT count(id) as t FROM tb_defeated_fail_log WHERE defeatedlogid="+str(defeatedlogid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return 0
    return data['t']

def isLogByColonizeAndPid(colonizeid,pid):
    '''根据保卫表主键id和挑战失败者角色id，返回此条记录
    @param colonizeid: int 保卫表主键id
    @param pid: int 挑战失败者角色id
    '''
    sql="SELECT * FROM tb_defeated_fail_log WHERE defeatedlogid="+str(colonizeid)+" AND defeatedid="+str(pid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def ishave(groupid,pid):
    '''根据殖民副本组id和角色id判断挑战表中是否有此记录
    @param groupid: int 殖民副本组id
    @param pid: int 角色id
    '''
    sql="select * from tb_defeated_fail_log where groupid=%s and pid=%s"%(groupid,pid)
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return False
    return True
    

def updateFailLogByid(id,va):
    '''根据挑战失败表主键id,更新时间'''
    sql="UPDATE tb_defeated_fail_log SET times='"+va+"' where id="+str(id)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

#------------------------------将数据复制到新表--------------------------------------#

def copyto():
    '''将数据复制到tb_defeated_fail_log1'''
    sql1="delete from tb_defeated_fail_log1"
    sql="INSERT INTO tb_defeated_fail_log1 SELECT * FROM tb_defeated_fail_log"
    cursor = dbaccess.dbpool.cursor()
    coun1t = cursor.execute(sql1)
    dbaccess.dbpool.commit()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1) and (coun1t>=1):
        return True
    return False


def getlogBydesc(pid,page,counts):
    '''获取挑战记录
    @param pid: int 角色id
    @param page: int 当前页数
    @param counts: int 每页条数
    '''
    
    sql="SELECT * FROM tb_defeated_fail_log1 WHERE pid=%s"%pid
    sql+=" limit "+str((page-1)*counts)+","+str(counts)+""
    sql1="SELECT CEILING(COUNT(*)/"+str(counts)+") AS t FROM tb_defeated_fail_log1 WHERE  pid=%s"%pid #一共多少页
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()#当前页的信息
    cursor.execute(sql1)
    result2=cursor.fetchone() #共几页
    cursor.close()
    if not data:
        return None,0
    return data,result2['t']

