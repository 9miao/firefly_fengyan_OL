#coding:utf8
'''
Created on 2012-6-25
GM命令处理
@author: Administrator
'''
from firefly.server.globalobject import GlobalObject
from app.chatServer.core.ChaterManager import ChaterManager

def doGmCommand(characterId,content):
    if content.startswith('\\'):
        chater = ChaterManager().getChaterByCharacterId(characterId)
        if chater:
            roomId = chater.getRoomId()
            if roomId<5000:
                childnode = 200000 + roomId
#                chatroot.callChild(201000,'GmCommand',characterId,content)
                GlobalObject().root.callChild("scense_1000","GmCommand",characterId,content)
                return True
    return False