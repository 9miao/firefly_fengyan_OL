#coding:utf8
'''
Created on 2012-8-9

@author: Administrator
'''
from firefly.server.globalobject import GlobalObject
from app.gate.core.VCharacterManager import VCharacterManager

def getOtherPlayerInfo(dynamicId,pid,tid,request_proto):
    '''获取其他角色的信息
    '''
    tvplayer = VCharacterManager().getVCharacterByCharacterId(tid)
    if tvplayer:
        nownode = 201000#tvplayer.getNode()
    else:
        vplayer = VCharacterManager().getVCharacterByClientId(dynamicId)
        if not vplayer:
            return
        else:
            nownode = 201000 #vplayer.getNode()
    d = GlobalObject().root.callChild("scense_1000",221,dynamicId,request_proto)
    return d
    