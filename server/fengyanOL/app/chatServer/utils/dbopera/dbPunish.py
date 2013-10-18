#coding:utf8
'''
Created on 2011-12-2
强化失败的惩罚与奖励
@author: SIOP_09
'''
from app.chatServer.utils import dbaccess
from MySQLdb.cursors import DictCursor

def getInfo(qlevel):
    '''根据强化等级获得惩罚于奖励信息
    @param qlevel: int 装备当前强化等级
    '''
    sql="SELECT * FROM  tb_punish WHERE qlevel="+str(qlevel)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def getAll():
    '''获取所有强化失败之后的惩罚信息(找不到的话，说明次强化等级没有惩罚)'''
    sql="SELECT * FROM  tb_punish"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data={}
    if not result or len(result)<1:
        return None
    else:
        for item in result:
            qlevelstr=str(item.get("qlevel",-1))
            data[qlevelstr]=item
    return data

