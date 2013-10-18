#coding:utf8
'''
Created on 2012-8-9

@author: Administrator
'''

from firefly.server.globalobject import GlobalObject
from app.gate.core.VCharacterManager import VCharacterManager

#============================创建队伍=============================

def TransferPlayerCreate(data,dynamicId,pid,pos,gkType):
    '''传递角色
    '''
    player = data[0]
    zuiduinode = 9999
    d = GlobalObject().root.callChild("scense_1000",4301,player,dynamicId, pid,pos,gkType)
    return d
    
def ErorrBack(reason):
    '''错误处理
    '''
    return

def CreateZuDui(dynamicId,pid,pos,gkType):
    '''创建队伍
    '''
    vplayer = VCharacterManager().getVCharacterByClientId(dynamicId)
    if not vplayer or vplayer.getLocked():#判断是否存在角色或者角色是否被锁定
        return
#    nownode = vplayer.getNode()
    d = GlobalObject().root.callChild("scense_1000",610,dynamicId, pid)
    d.addErrback(ErorrBack)
    d.addCallback(TransferPlayerCreate,dynamicId,pid,pos,gkType)
    return d

#============================加入队伍=============================

def TransferPlayerJoin(data,dynamicId,pid,pos,gkType):
    '''传递角色
    '''
    player = data[0]
    zuiduinode = 9999
    d = GlobalObject().root.callChild("scense_1000",4303,player,dynamicId, pid,pos,gkType)
    return d
    
def JoinDuiWu(dynamicId,pid,pos,dwId):
    '''加入队伍
    '''
    vplayer = VCharacterManager().getVCharacterByClientId(dynamicId)
    if not vplayer or vplayer.getLocked():#判断是否存在角色或者角色是否被锁定
        return
#    nownode = vplayer.getNode()
    d = GlobalObject().root.callChild("scense_1000",610,dynamicId, pid)
    d.addErrback(ErorrBack)
    d.addCallback(TransferPlayerJoin,dynamicId,pid,pos,dwId)
    return d
    

    

    