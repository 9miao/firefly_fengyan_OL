#coding:utf8
'''
Created on 2011-9-24

@author: lan
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

dbaccess = dbaccess

ALL_PUBLICSCENE_INFO = {}#所有的公共场景信息
ALL_INSTANCESCEN_INFO = {}#所有副本场景的信息

def getAllPublicSceneInfo():
    '''获取公共场景信息'''
    global ALL_PUBLICSCENE_INFO
    sql="SELECT * FROM tb_publicscene"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for scene in result:
        ALL_PUBLICSCENE_INFO[scene['id']] = scene

def getALlInstanceSceneInfo():
    '''获取所有副本场景的信息'''
    global ALL_INSTANCESCEN_INFO
    sql="SELECT * FROM tb_scene"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for scene in result:
        ALL_INSTANCESCEN_INFO[scene['id']] = scene

def getStringInSceneByFilename(fname,value,sname):
    '''根据列名和值获取场景列名信息
    @param fname:str 约束字段名称
    @param value: str or int 约束字段值
    @param sname: str 查询字段名称 *为全部
    '''
    sql="select "+sname+" from tb_scene where "+fname+"="+str(value)+""
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result
