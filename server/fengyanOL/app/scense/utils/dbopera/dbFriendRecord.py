#coding:utf8
'''
Created on 2011-11-24
好友祝福限制表
@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

def addRecord(characterid):
    '''添加角色祝福记录
    @param characterid: int 当前角色id
    '''
    sql="insert  into `tb_friend_record`(`character`,`count`) values ("+str(characterid)+",1)"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getRecord(id):
    '''获取角色祝福次数
    @param id: int 当前角色id
    '''
    sql="SELECT * FROM tb_friend_record WHERE characterid="+str(id)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return 0
    return result.get('count',0)

def updateRecord(id,count):
    '''更改角色祝福次数
    @param id: int 角色id
    @param count: int 祝福次数  正数+ 负数- 
    '''
    sql="UPDATE tb_friend_record SET `count`=`count`+"+str(count)+" WHERE characterid="+str(id)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def delRecordAll():
    '''设置所有角色祝福次数为0 (备注：每天12点的时候服务器自动调用)'''
    sql="UPDATE tb_friend_record SET `count`=0"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
    