#coding:utf8
'''
Created on 2011-11-15

@author: lan
'''
from app.scense.utils import dbaccess
from app.scense.utils import util

def updateUserInfo(userId,props):
    '''更新角色信息'''
    sql = "update `tb_user_character` set"
    sql = util.forEachUpdateProps(sql, props)
    sql += " where id = %d" % userId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()