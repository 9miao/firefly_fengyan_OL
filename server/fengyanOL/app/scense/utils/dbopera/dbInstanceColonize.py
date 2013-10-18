#coding:utf8
'''
Created on 2011-12-21
副本殖民信息表操作
@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor 
from twisted.python import log

#-------------------------------修改-----------------------------------------#
#def updateGuild(pid,gid,gname):
#    '''修改角色所属国'''
#    sql="UPDATE tb_instance_colonize SET gid="+str(gid)+",gname='"+gname+"' WHERE pid="+str(pid)
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#
#def updateInstanceColonizeById(instanceid,pid,pname,gid,gname,resist=0):
#    '''根据副本id修改殖民信息'''
#    sql="UPDATE tb_instance_colonize SET pid="+str(pid)+",pname='"+pname+"',gid="+str(gid)+",gname='"+gname+"',resist="+str(resist)+" WHERE instanceid="+str(instanceid)
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#
#def updateInstanceColonizeBygroupId(instanceid,pid,pname,gid,gname):
#    '''根据副本id修改殖民信息'''
#    sql="UPDATE tb_instance_colonize SET pid="+str(pid)+",pname='"+pname+"',gid="+str(gid)+",gname='"+gname+"' WHERE instanceid="+str(instanceid)
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#
#def updateColonizeResistByid(instanceid):
#    '''根据副本id修改卫冕成功次数'''
#    sql="UPDATE tb_instance_colonize SET resist=resist+1 WHERE instanceid="+str(instanceid)+" and enable=1"
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#def updateColonizeCidByid(instanceid,cid):
#    '''更该殖民者'''
#    sql="UPDATE tb_instance_colonize SET resist=0,pid="+str(cid)+" WHERE instanceid="+str(instanceid)
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#
#def updateColonizeResisDaytByid(instanceid,days):
#    '''根据副本id修改殖民天数'''
#    sql="UPDATE tb_instance_colonize SET days="+str(days)+" WHERE instanceid="+str(instanceid)
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#
#
#def enableFalse(instanceid):
#    '''设置该副本所有的enable状态为关闭'''
#    sql="UPDATE tb_instance_colonize SET ENABLE=0 WHERE instanceid="+str(instanceid)
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#
#def enableFalseByInstanceidAndPid(instanceid,pid):
#    '''根据副本id和角色id设置enable状态为关闭'''
#    sql="UPDATE tb_instance_colonize SET ENABLE=0 WHERE instanceid="+str(instanceid)+" and pid="+str(pid)+""
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#
#def updateEnable(instanceid,pid):
#    '''根据副本id和角色id设置enable状态为开启'''
#    sql="UPDATE tb_instance_colonize SET ENABLE=1 WHERE instanceid="+str(instanceid)+" and pid="+str(pid)+""
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#
#def setClearancecount(count):
#    '''设置所有记录的通关次数为count'''
#    sql="UPDATE tb_instance_colonize SET clearancecount=0,suid=0,suname='无'"
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#
#def updateSuidSuname(instanceid,pid,uid,uname):
#    '''更改殖民成功角色id和成功名称'''
#    sql="UPDATE tb_instance_colonize SET suid="+str(uid)+",suname='"+uname+"' WHERE instanceid="+str(instanceid)+" AND pid="+str(pid)
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False
#
#def updateClearanceCount(instanceid):
#    '''对通关次数+1，通过副本id'''
#    sql="UPDATE tb_instance_colonize SET clearancecount=clearancecount+1 WHERE instanceid="+str(instanceid)+" AND ENABLE=1"
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False

#-------------------------------获取-----------------------------------------#

def getInstanceColonizeByid(id):
    '''根据副本组id获取副本殖民信息
    @param id: int 副本id
    '''
    sql="SELECT * FROM  tb_instance_colonize WHERE enable=1 and instanceid="+str(id)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def isinstance(id):
    '''根据副本组id获取副本殖民信息
    @param id: int 副本id
    '''
    sql="SELECT * FROM  tb_instance_colonize WHERE typeid=0 and instanceid="+str(id)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return False
    return True

def iscity(cityid):
    '''判断是否有这个城市殖民信息
    @param cityid: int 城市id
    '''
    sql="SELECT * FROM  tb_instance_colonize WHERE typeid=1 and  instanceid="+str(cityid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return False
    return True

def getColonizeResistByid(instanceid):
    '''获取卫冕次数'''
    sql="select resist from tb_instance_colonize WHERE enable=1 and instanceid="+str(instanceid)
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
    sql="SELECT COUNT(id) FROM tb_instance_colonize WHERE enable=1 and gid="+str(gid)
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
    sql="SELECT * FROM tb_instance_colonize WHERE ENABLE=1 and pid="+str(laird)+" ORDER BY typeid desc"
    sql+=" limit "+str((page-1)*counts)+","+str(counts)+""
    sql1="SELECT CEILING(COUNT(*)/"+str(counts)+") AS t FROM tb_instance_colonize WHERE ENABLE=1 and pid="+str(laird) #一共多少页
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()#当前页的信息
    cursor.execute(sql1)
    result2=cursor.fetchone() #共几页
    cursor.close()
    if not data:
        return None,0
    return data,result2['t']

def getAllenableTrue():
    '''获取所有正在占领中的副本殖民信息列表'''
    sql="SELECT * FROM tb_instance_colonize WHERE ENABLE=1 and typeid=0"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close() 
    if not data:
        return None
    return data

def getAllUserid():
    '''获取所有角色id'''
    sql="SELECT DISTINCT pid FROM tb_instance_colonize where enable=1"
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if not data:
        return None
    return data

def getAllInstanceidList(pid):
    '''根据角色id获取副本id列表'''
    sql="SELECT instanceid FROM tb_instance_colonize WHERE enable=1 and typeid=0 and  pid="+str(pid)
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
    sql="SELECT count(*) as t FROM tb_instance_colonize WHERE enable=0 and pid="+str(pid)+" and instanceid="+str(instanceid)
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
    sql="SELECT * FROM tb_instance_colonize WHERE enable=1 and pid="+str(pid)+" and instanceid="+str(instanceid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone() 
    cursor.close()
    if not data:
        return None
    return data

def getInfoFalse(instanceid,pid):
    '''获取殖民信息，通过副本id和角色id'''
    sql="SELECT * FROM tb_instance_colonize WHERE  pid="+str(pid)+" and instanceid="+str(instanceid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone() 
    cursor.close()
    if not data:
        return None
    return data

def getInstanceInfoListBypid(pid,page,counts=6):
    '''根据角色id获取殖民副本列表
    @param page: int 当前页数
    @param counts: int 每页条数
    '''
    try:
        sql="SELECT * FROM tb_instance_colonize WHERE pid="+str(pid)+" AND ENABLE=1 order by instanceid"
        sql+=" limit "+str((page-1)*counts)+","+str(counts)+""
        sql1="SELECT CEILING(COUNT(*)/"+str(counts)+") AS t FROM tb_instance_colonize where pid="+str(pid)+" AND ENABLE=1" #一共多少页
        cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
        cursor.execute(sql)
        data=cursor.fetchall()
        cursor.execute(sql1)
        result2=cursor.fetchone() #共几页
        cursor.close()
        if not data:
            return None,0
        return data,int(result2['t'])
    except:
        log.err(u'dbInstanceColonize->getInstanceInfoListBypid(pid=%s,page=%s,counts=6)'%(pid,page))


def getAllinstanceListBypid(pid):
    sql="SELECT * FROM tb_instance_colonize WHERE pid="+str(pid)+" AND ENABLE=1 order by instanceid"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if not data:
        return None
    return data


#-------------------------------添加-----------------------------------------#

def addInstanceColonize(instanceid,instancename,pid,pname,gid,gname,resist=0,days=0):
    '''添加殖民信息
    @param instanceid: int 副本组id
    @param pid: int 角色id
    @param pname: str 角色名称
    @param gid: int 国id
    @param gname: str 国名称
    @param resist: int 卫冕成功次数
    @param days: int 殖民天数
    '''
    if not isinstance(instanceid):
        sql="insert  into `tb_instance_colonize`(`instanceid`,`instancename`,`pid`,\
        `pname`,`gid`,`gname`,`resist`,`days`) values (%d,'%s',%d,'%s',%d,'%s',%d,%d);"%(instanceid,
                                                instancename,pid,pname,gid,gname,resist,days)
        cursor = dbaccess.dbpool.cursor()
        count = cursor.execute(sql)
        dbaccess.dbpool.commit()
        cursor.close()
        if count:
            return True
        return False

def addCityColonize(instanceid,instancename,pid,pname,gid,gname,resist=0,days=0):
    '''添加殖民信息
    @param instanceid: int 城市id
    @param pid: int 角色id
    @param pname: str 角色名称
    @param gid: int 国id
    @param gname: str 国名称
    @param resist: int 卫冕成功次数
    @param days: int 殖民天数
    '''
    
    if not iscity(instanceid):
        sql="insert  into `tb_instance_colonize`(`instanceid`,`instancename`,`typeid`,`pid`,\
        `pname`,`gid`,`gname`,`resist`,`days`) values (%d,'%s',%d,%d,'%s',%d,'%s',%d,%d);"%(instanceid,
                                                instancename,1,pid,pname,gid,gname,resist,days)
        cursor = dbaccess.dbpool.cursor()
        count = cursor.execute(sql)
        dbaccess.dbpool.commit()
        cursor.close()
        if count:
            return True
        return False

#-------------------------------删除-----------------------------------------#

#def delInstanceClolonize():
#    '''删除所有殖民信息'''
#    sql="DELETE FROM tb_instance_colonize"
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False

#------------------------------将数据复制到新表--------------------------------------#
def copyto():
    '''将数据复制到另一张表tb_instance_colonize1'''
    sql1="delete from tb_instance_colonize1"
    sql="INSERT INTO tb_instance_colonize1 SELECT * FROM tb_instance_colonize"
    cursor = dbaccess.dbpool.cursor()
    coun1t = cursor.execute(sql1)
    dbaccess.dbpool.commit()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count and coun1t:
        return True
    return False


#def delinfo(cityid,pid,typeid=0):
#    '''设置这个殖民地为未殖民
#    @param cityid: int 城市id或者副本id
#    @param pid: int 角色id
#    @param typeid: int 0表示副本殖民 1表示城镇殖民
#    '''
#    sql="DELETE FROM tb_instance_colonize WHERE instanceid=%s AND typeid=%s AND pid=%s"%(cityid,typeid,pid);
#    cursor = dbaccess.dbpool.cursor()
#    count = cursor.execute(sql)
#    dbaccess.dbpool.commit()
#    cursor.close()
#    if count:
#        return True
#    return False

    