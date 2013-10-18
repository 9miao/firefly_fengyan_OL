#coding:utf8
'''
Created on 2012-9-4

@author: Administrator
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

ALL_FIGURE_CONFIG = {}

def getAllFigureInfo():
    '''获取所有新手奖励的信息'''
    global ALL_FIGURE_CONFIG
    sql = "SELECT * FROM tb_figure_config"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    for figure in result:
        ALL_FIGURE_CONFIG[figure['figure']] = figure['source']

