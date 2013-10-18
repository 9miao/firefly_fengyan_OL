##coding:utf8
#'''
#Created on 2012-4-12
#
#@author: Administrator
#'''
#from serverconfig.publicnode import publicnodeHandle
#from app.scense.core.PlayersManager import PlayersManager
#
#@publicnodeHandle
#def recTimerSignal(pid,signaltype):
#    '''定时信号
#    @param pid: int 角色的id
#    @param signaltype: int 信号的类型
#    '''
#    player = PlayersManager().getPlayerByID(pid)
#    if player:
#        player.afk.rectimersignal(signaltype)
#    