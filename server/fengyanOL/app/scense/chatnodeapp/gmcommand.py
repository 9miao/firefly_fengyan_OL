#coding:utf8
'''
Created on 2012-6-25
GM指令
@author: Administrator
'''

from app.scense.serverconfig.chatnode import chatnodeHandle
from app.scense.chatnodeapp import gmapp

@chatnodeHandle
def GmCommand(characterId,content):
    '''GM帮助指令
    @param funcname: str 指令名称
    '''
    commandStr = content[1:].split(' ')
    methodName = commandStr[0]
    argument = commandStr[1:]
    if methodName == 'reload':
        reload(gmapp)
        return
    try:
        doMethod = getattr(gmapp, methodName)
        doMethod(characterId,argument)
    except Exception as e:
        print e
        