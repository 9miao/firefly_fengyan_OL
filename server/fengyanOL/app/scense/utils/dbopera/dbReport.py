#coding:utf8
'''
Created on 2011-8-29

@author: SIOP_09
'''
from app.scense.utils import dbaccess

def add(cid,tocid,context):
    '''添加举报
    @param int: cid 当前角色id
    @param int: tocid 被举报人角色id(倒霉的那个人)
    @param string: context 举报信息
    '''
    sql="INSERT  INTO `tb_report`(`characterid`,`tocharacterid`,`context`) VALUES ("+str(cid)+","+str(tocid)+",'"+context+"')"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

