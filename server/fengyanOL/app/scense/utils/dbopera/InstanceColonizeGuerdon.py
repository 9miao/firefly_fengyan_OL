#coding:utf8
'''
Created on 2011-12-21
副本殖民奖励
@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

def addInstanceColonizeGuerdon(cid,coin,typeid):
    '''添加副本殖民奖励
    @param cid: int 角色id
    @param coin: int 获得的游戏币数量
    @param typeid: int 副本殖民奖励类型 1卫冕奖励 2其他角色通关获得的奖励
    '''
    sql="insert  into `tb_instance_colonize_guerdon`(`cid`,`coin`,`typeid`) values ("+str(cid)+","+str(coin)+","+str(typeid)+");"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False

def updateInstanceColonizeGuerdon(cid,typeid,coin):
    '''更新副本殖民奖励游戏币'''
    sql="UPDATE tb_instance_colonize_guerdon SET coin="+str(coin)+" WHERE cid="+str(cid)+" AND typeid="+str(typeid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False


def getInstanceColonizeGuerdon(cid,typeid):
    '''获取副本殖民奖励列表
    @param cid: int 角色id
    @param typeid: int 1卫冕奖励  2其他角色通过副本奖励
    '''
    sql="SELECT * FROM tb_instance_colonize_guerdon WHERE cid="+str(cid)+" and typeid="+str(typeid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def delInstanceColonizeGuerdonByid(id):
    '''删除副本殖民奖励
    @param id: int 副本殖民奖励表主键id
    '''
    sql="DELETE FROM tb_instance_colonize_guerdon WHERE id="+str(id)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False
    
