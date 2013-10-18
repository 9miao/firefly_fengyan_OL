#coding:utf8
'''
Created on 2011-3-17

@author: sean_lan
'''
from app.scense.utils import dbaccess

def addPlayer(username ,password , email):
    '''注册新用户'''
    result = dbaccess.hasRepeatUserName(username)
    if result :
        return 1
    result = dbaccess.addRegist(username, password, email)
    if not result:
        return 2
    else:
        return 3
    