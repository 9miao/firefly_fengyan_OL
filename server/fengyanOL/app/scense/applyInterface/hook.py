#coding:utf8

'''
Created on 2011-8-29
@author: SIOP_09
'''

from app.scense.utils.dbopera import dbHook
import datetime
import time

def getHookByid(id):
    '''根据角色id获取挂机信息
    @param id: int  角色id    
    '''
    result=dbHook.getHookByid(id)
    if not result:
        return None
    nowtime=datetime.datetime.fromtimestamp(time.time()) #系统当前时间
    down=result['atime']
    s1=(down-nowtime).days*24*3600 
    s2=(down-nowtime).seconds
    hours=s2//3600
    m=s2%3600
    m1=m//60
    s=m%60
