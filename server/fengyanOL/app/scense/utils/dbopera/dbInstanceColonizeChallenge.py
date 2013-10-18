#coding:utf8
'''
Created on 2011-12-21
副本殖民挑战怪物信息表
@author: SIOP_09
'''
from app.scense.utils import dbaccess
#from MySQLdb.cursors import DictCursor

def getAllColonizeChallenge():
    '''获得所有殖民对应怪物表'''
    sql="SELECT mosterid,instanceid FROM tb_instance_colonize_challenge"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    list={}
    if data and len(data)>0:
        for item in data:
            list[item[1]]=item
    return list


def getAllMosterName():
    '''根据殖民副本组id获取怪物名称'''
    sql="SELECT icc.instanceid ,m.nickname  FROM tb_instance_colonize_challenge AS icc,tb_monster AS m WHERE icc.mosterid=m.id"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    list={}
    if data or len(data)>1:
        for item in data:
            list[item[0]]=item 
    return list