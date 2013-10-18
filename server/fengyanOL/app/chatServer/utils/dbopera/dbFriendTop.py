#coding:utf8
'''
Created on 2011-11-15
最近联系人
@author: SIOP_09
'''
from app.chatServer.utils import dbaccess
#from twisted.python import log
from MySQLdb.cursors import DictCursor
dbaccess=dbaccess


def getReader(characterid):
    '''获取未读信息角色id
    @param characterid: int 角色id
    '''
    sql="SELECT * FROM tb_friend_chat WHERE characterid="+str(characterid)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def getFriendTop(characterid):
    '''获取最近联系人
    @param characterid: int 当前角色id
    '''
    sql="select friendsid from tb_friend_chat where characterid="+str(characterid)
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if data:
        return eval(data[0])
    return None

def updateFriendTop(characterid,friendsid,readersid):
    '''修改最近联系人
    @param characterid: int 当前角色id
    @param friendid: str 最近联系人角色id列表[x,y,z,.....]
    @param readersid: str 未读取的信息发送者角色id[x,y,t]
    '''
    sql="update tb_friend_chat set friendsid="+friendsid+",reader="+readersid+" where characterid="+str(characterid)
    cursor = dbaccess.dbpool.cursor()
    count=cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False    

def addFriendTop(characterid,friendid):
    '''添加最近联系人
    @param characterid: int 当前角色id
    @param friendid: str 最近联系人角色id列表[x,y,z,.....]
    '''
    sql="insert  into `tb_friend_chat`(`characterid`,`friendsid`) values ("+characterid+",'"+friendid+"')"
    cursor = dbaccess.dbpool.cursor()
    count=cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
    