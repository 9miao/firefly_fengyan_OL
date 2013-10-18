#coding:utf8
'''
Created on 2012-3-2

@author: sean_lan
'''
from twisted.internet import reactor
from app.gate.utils.dbopera import dbshieldword,dbnamepool,dbuser, dbNobilityAstrict,db_language_login
from app.gate.bridge.famsermanger import FamSerManager
from app.gate.bridge.scenesermanger import SceneSerManager
from app.gate.bridge.netservermanager import NetSerManager
from twisted.python import log

import datetime
reactor = reactor

def initAlldata():
    '''初始化常用数据，从数据库读入到内存中
    '''
    dbshieldword.getAll_ShieldWord()
    dbnamepool.getNamePool()
    db_language_login.initLoginLanguagePack()
    NetSerManager()
    SceneSerManager()
    FamSerManager()

def writePlayerDBInfo():
    '''将所有在线角色的数据写入数据库
    '''
    
    from firefly.server.globalobject import GlobalObject
    childs = GlobalObject().root.childsmanager._childs.keys()
    for node in childs:
        if 200000<node:
            GlobalObject().root.callChild("scense_1000",21)
    reactor.callLater(24*3600, writePlayerDBInfo)
    
def addEnergyOnline(energy):
    '''更新在线角色的活力
    @param energy: int 活力值
    '''
    from firefly.server.globalobject import GlobalObject
    childs = GlobalObject().root.childsmanager._childs.keys()
    for node in childs:
        if 200000<node:
            GlobalObject().root.callChild("scense_1000",20,energy)
    
def addEnergyPerDay():
    '''每天8点加点90活力'''
    energy = 200
    try:
        dbuser.updateAllPlayersEnergy(energy)
        addEnergyOnline(energy)
    except Exception,e:
        try:
            log.err(str(e))
        except:
            pass
    reactor.callLater(24*3600,addEnergyPerDay)
    
def update23():
    '''为24点更新排行提前更新数据库'''
    from firefly.server.globalobject import GlobalObject
    try:
        GlobalObject().root.callChild("scense_1000",61)#更新表
    except Exception,e:
        print e
    reactor.callLater(24*3600,update23)
    
def update24():
    '''每天晚上24点进行的操作'''
    from firefly.server.globalobject import GlobalObject
    try:
        dbNobilityAstrict.clear()#每天晚上24点清除官爵领取兑换限制
        
        childs = GlobalObject().root.childsmanager._childs.keys()
        for node in childs:
            if 200000<node:
                GlobalObject().root.callChild("scense_1000",60)#清空所有官爵领取、贡献的限制信息和领取次数
                
    except Exception,e:
        print e
    reactor.callLater(24*3600,update24)
    
    
def differTime(h,m,s):
    '''到达预设时间执行函数  return与当前时间相差的秒数
    @param h,m,s: int 预设 时,分,秒 
    return int 秒数
    '''
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second
    old=h*3600+m*60+s #预设时间 据0点得秒数
    young=hour*3600+minute*60+second #当前时间据0点得秒数
    
    if old>=young:
        return old-young
    else:
        return 24*3600-(young-old)
    
    
def doService():
    '''启动服务器时需要启动的服务：
    '''
    initAlldata()
    reactor.callLater(differTime(8,0,0), addEnergyPerDay)
    reactor.callLater(differTime(23,50,0),update23)
    reactor.callLater(differTime(24,0,0), update24)
    
    
    