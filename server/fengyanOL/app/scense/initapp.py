#coding:utf8
'''
Created on 2013-8-30
@author: jt
'''
from firefly.dbentrust.dbpool import dbpool
from firefly.dbentrust.memclient import mclient
from app.scense.utils import dbaccess
dbconfig = dbpool.config
dbconfig['maxWait']=5
dbaccess.dbpool.initPool(**dbconfig)
dbaccess.memclient = mclient
dbaccess.memdb = mclient.connection
from firefly.server.globalobject import GlobalObject
from app.scense.core.PlayersManager import PlayersManager
from twisted.python import log
import gc
from app.scense.utils.dbopera import dbScene,dbPortals,dbNpc,dbAward, dbStrengthen,\
        dbInstance_colonize_title,dbSchedule,dbdaily,dbGodhead,dbItems,dbMap,dbMonster
from app.scense.world.scene import Scene
from app.scense.core.instance.InstanceManager import InstanceManager
from app.scense.core.guild.GuildManager import GuildManager
from app.scense.core.map.MapManager import MapManager
from app.scense.serverconfig import serviceByStart
from twisted.internet import reactor


    
def doWhenStop():
    '''服务器关闭前的操作'''
    for player in PlayersManager()._players.values():
        try:
            player.updatePlayerDBInfo()
            PlayersManager().dropPlayer(player)
        except Exception as ex:
            log.err(ex)

GlobalObject().stophandler = doWhenStop


def loadModule():
    from app.scense.nodeapp import *
#    from app.scense.publicnodeapp import *
    from app.scense.chatnodeapp import *
    dbScene.getALlInstanceSceneInfo()
    dbScene.getAllPublicSceneInfo()
    dbPortals.getAllPortalsInfo()
    dbStrengthen.getAll()
    dbInstance_colonize_title.updateAll()#更新殖民头衔配置
    dbNpc.getAllNpcInfo()
    dbAward.getAllAwardInfo()
    dbSchedule.getAllScheduleBound()
    dbSchedule.getAllScheduleConfig()
    dbdaily.getAllDaily()
    dbGodhead.getAllGodhead()
    dbGodhead.getAllHeadtype()
    dbItems.getAllsetInfo()
    dbItems.getAllGemInfo()
    dbItems.getAllCompoundInfo()
    dbMonster.getAllMonsterInfo()
    dbMap.getAllDoorInfo()
    dbMap.getAllMonsterConfig()
    dbMap.getAllMapInfo()
    GuildManager()
    MapManager()
    serviceByStart.doService()
    updateInstanceInfo(1)
    updateSceneInfo(1)
    cleanMeM(1800)
    
def updateSceneInfo(rate):
    '''更新场景中角色的位置'''
    try:
        MapManager().pushAllSceneInfo(rate)
        MapManager().produceMonster()
#        InstanceManager().pushAllInstanceInfo(rate)
    finally:
        reactor.callLater(rate,updateSceneInfo,rate)    

def updateInstanceInfo(rate):
    '''更新副本场景角色的信息'''
    try:
        InstanceManager().pushAllInstanceInfo(rate)
    finally:
        reactor.callLater(rate,updateInstanceInfo,rate)
    
def cleanMeM(delta):
    '''内存清理
    '''
    gc.collect()
    reactor.callLater(delta,cleanMeM,delta)