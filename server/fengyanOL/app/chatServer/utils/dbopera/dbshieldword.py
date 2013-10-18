#coding:utf8
'''
Created on 2012-3-2

@author: sean_lan
'''
from app.chatServer.utils import dbaccess

dbaccess = dbaccess
SHIELDWORD = []

def getAll_ShieldWord():
    global SHIELDWORD
    sql = "SELECT sword FROM tb_shieldword;"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    SHIELDWORD = result

def checkIllegalChar(chars):
    '''检测是否包含非法字符
    @param chars: str 源字符
    '''
    for word in SHIELDWORD:
        if chars.find(word[0])!=-1:
            return False
    return True

def replaceIllegalChar(chars):
    '''替换非法字符
    @param chars: str 源字符
    '''
    for word in SHIELDWORD:
        chars = chars.replace(word[0],'*'*len(word[0]))
    return chars


