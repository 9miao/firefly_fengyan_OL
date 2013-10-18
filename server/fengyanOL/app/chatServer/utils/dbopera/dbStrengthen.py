#coding:utf8
'''
Created on 2011-9-27
强化
@author: SIOP_09
'''
from app.chatServer.utils import dbaccess
from MySQLdb.cursors import DictCursor

def getProbability(level):
    '''根据强化等级获取强化成功率
    @param level: int 物品当前强化等级
    '''
    sql="SELECT * FROM tb_aptitude WHERE qlevel="+str(level+1)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def getGain(level,pz):
    '''获取强化装备收益
    @param level: int  物品的强化等级
    @param pz: int 物品的品质
    '''
    sql="SELECT * FROM tb_aptitude_gain WHERE qlevel="+str(level)+" AND color="+str(pz)
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def getProbabilityAll():
    '''获取所有的强化成功率数据'''
    sql="SELECT * FROM tb_aptitude"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data={}
    if not result or len(result)<1:
        return None
    else:
        for item in result:
            qlevelstr=str(item.get('qlevel',-1))
            data[qlevelstr]=item
#    #print str(data["1"])#将装备强化到1级所需要的成功率
    return data

def getGainAll():
    '''获取所有强化成功只有的收益值'''
    sql="SELECT * FROM tb_aptitude_gain"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data={} #存储格式{'1#1':{'color': 1L, 'sp': 1L, 'wq': 1L, 'qlevel': 1L, 'fj': 1L},'2#3':{}, ......  }
    if not result or len(result)<1:
        return None
    else:
        for item in result:
            colorstr=str(item.get("color",-1))
            qlevelstr=str(item.get('qlevel',-1))
            data[qlevelstr+"#"+colorstr]=item
    del result
#    #print str(data.get("1#2")) #获取强化等级为1颜色为2的装备的收益值
    return data
