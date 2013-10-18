#coding:utf8
'''
Created on 2013-8-30

@author: jt
'''
from firefly.server.globalobject import GlobalObject,remoteserviceHandle

@remoteserviceHandle('gate')
def pushData(cid,data,sendList):
    '''向网页客户端发送信息'''
    GlobalObject().netfactory.pushObject(cid,data,sendList)
