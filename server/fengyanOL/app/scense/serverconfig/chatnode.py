#coding:utf8
'''
Created on 2012-3-29

@author: Administrator
'''

from firefly.server.globalobject import GlobalObject

chatnoderemote = GlobalObject().remote['chat']

def chatnodeHandle(target):
    '''add service target
    @param target: func Object
    '''
    GlobalObject().remote['chat']._reference._service.mapTarget(target)
#    chatnodeservice.mapTarget(target)
    
def pushSystemInfo(strInfo):
    '''推送系统跑马灯消息'''
    chatnoderemote.callRemote('pushSystemToInfo',strInfo)
    
def pushSystemchat(strInfo):
    '''推送系统跑马灯消息'''
    chatnoderemote.callRemote('pushSystemchat',strInfo)
    

    