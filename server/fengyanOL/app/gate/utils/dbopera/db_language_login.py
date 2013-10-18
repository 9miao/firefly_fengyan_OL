#coding:utf8
'''
Created on 2012-7-23

@author: Administrator
'''
from app.gate.utils import dbaccess

LOGIN_LANGUAGE = {}

def initLoginLanguagePack():
    '''初始化登陆相关语言包
    '''
    global LOGIN_LANGUAGE
    sql = "SELECT * FROM tb_language_login"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for lang in result:
        LOGIN_LANGUAGE[lang[0]] = lang
        
def getLanguageStr(tag):
    '''获取登陆对应的消息字符串
    '''
    lang = LOGIN_LANGUAGE.get(tag)
    if lang:
        return lang[1]
    return u''

