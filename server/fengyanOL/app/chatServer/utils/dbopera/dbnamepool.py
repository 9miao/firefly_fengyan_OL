#coding:utf8
'''
Created on 2012-3-2

@author: sean_lan
'''
from app.chatServer.utils import dbaccess
import random

dbaccess = dbaccess
NAMEPOOL = []

def getNamePool():
    '''获取随机名称库'''
    global NAMEPOOL
    sql = "SELECT name FROM tb_namepool"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    NAMEPOOL = result
    
def getRandomName():
    '''获取随机名称'''
    data = random.choice(NAMEPOOL)
    return data[0]
    

    
    
    