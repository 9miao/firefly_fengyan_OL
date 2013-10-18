#coding:utf8
'''
Created on 2012-5-17
官爵
@author: jt
'''
from app.scense.applyInterface import winning_app, friendRecord_app
from app.scense.serverconfig.node import nodeHandle
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.toplist.TopList import TopList
from app.scense.core.pray.PrayManage import PrayManage

@nodeHandle
def a_60():
    '''每天24点执行的操作'''
    winning_app.set0()#清空副本输入信息
    TopList().updateAll()#每天24点更新排行榜
    PrayManage().clean0()#清空祈祷次数
    friendRecord_app.clean() #每天晚上24点将所有角色的祝福次数设置为0
    for player in PlayersManager().getAll():
        player.nobility.clear() #清空所有官爵领取、贡献的限制信息和领取次数
        
        
@nodeHandle
def a_61():
    '''角色战力排行更新数据库'''
    TopList().upateAddzl()#更新数据库
