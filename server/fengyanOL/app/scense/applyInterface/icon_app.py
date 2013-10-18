#coding:utf8
'''
Created on 2011-9-27
图标管理
@author: SIOP_09
'''
from app.scense.netInterface import pushObjectNetInterface



icon={}


def onland(pid):
    '''登陆的时候推送图标'''
    from app.scense.utils.dbopera import dbDefenceBonus
    from app.scense.applyInterface import InstanceColonizeGuerdon

    data=dbDefenceBonus.getCountBypid(pid)
    if data:#如果有奖励
        add(pid, 1,False)
    else:
        clear(pid, 1,False)

#    data=InstanceColonizeGuerdon.iscoloBypid(pid)#角色是否有殖民地
#    if data:#如果有殖民地
#        add(pid, 2,False)
#    else:
#        clear(pid, 2,False)


def getBypid(pid):
    '''根据角色id推送图标信息'''
    if icon.has_key(pid) and len(icon[pid])>0:
        pushObjectNetInterface.pushGameTopTitle2400([pid],icon[pid])
    else:
        pushObjectNetInterface.pushGameTopTitle2400([pid],[])
        
def addList(list,typeid,flg=True):
    for pid in list:
        if not icon.has_key(pid):
            icon[pid]=[]
        if typeid==2:
            if icon[pid].count(2)==0:
                icon[pid].append(2)
            if icon[pid].count(3)>0:
                icon[pid].remove(3)
                
        elif typeid==3:
            if icon[pid].count(2)>0:
                icon[pid].remove(2)
            if icon[pid].count(3)==0:
                icon[pid].append(3)
        else:
            if icon[pid].count(typeid)==0:
                icon[pid].append(typeid)
#        if flg:
#            getBypid(pid)

def add(pid,typeid,flg=True):
    '''添加一个图标
    @param pid: int 角色id
    @param typeid: int 图标类型id 1殖民奖励  2殖民状态增强  3殖民状态流光溢彩
    @param flg:  bool 是否立刻发送修改后的图标信息  默认True (发送)
    '''
    from app.scense.core.PlayersManager import PlayersManager
    
    player=PlayersManager().getPlayerByID(pid)
    if player:
    
        if not icon.has_key(pid):
            icon[pid]=[]
        if typeid==2:
            if icon[pid].count(2)==0:
                icon[pid].append(2)
            player.icon.addIcon(2,0)
            if icon[pid].count(3)>0:
                icon[pid].remove(3)
            player.icon.removeIcon(3)
                
        elif typeid==3:
            if icon[pid].count(2)>0:
                icon[pid].remove(2)
                player.icon.removeIcon(2)
            if icon[pid].count(3)==0:
                icon[pid].append(3)
            player.icon.addIcon(3,0)
        else:
            if icon[pid].count(typeid)==0:
                icon[pid].append(typeid)
            player.icon.addIcon(typeid,0)
#    if flg:
#        getBypid(pid)
def clear(pid,typeid,flg=True):
    '''移除一个图标
    @param pid: int 角色id
    @param typeid: int 图标类型id
    @param dynameicId: int 角色动态id 1殖民奖励  2殖民状态增强  3殖民状态流光溢彩
    @param flg:  bool 是否立刻发送修改后的图标信息  默认True (发送)
    '''
    from app.scense.core.PlayersManager import PlayersManager
    player=PlayersManager().getPlayerByID(pid)
    
    if not icon.has_key(pid):
        icon[pid]=[]
    if icon[pid].count(typeid)>0:
        icon[pid].remove(typeid)
    player.icon.removeIcon(typeid)
#    if flg:
#        getBypid(pid)