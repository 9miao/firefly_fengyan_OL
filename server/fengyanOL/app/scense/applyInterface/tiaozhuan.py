#coding:utf8
'''
Created on 2012-12-7
传送门场景跳转
@author: lan
'''
from app.scense.core.map.MapManager import MapManager
from app.scense.utils.dbopera import dbMap
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.language.Language import Lg
from app.scense.serverconfig.chatnode import chatnoderemote
#from app.scense.serverconfig.publicnode import publicnoderemote
from app.scense.applyInterface import defencelog_app,instance_app

def tiaozhuan(dynamicId,characterid,csz):
    '''场景间的跳转或者进入副本
    '''
    player = PlayersManager().getPlayerByID(characterid)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    doorinfo = dbMap.ALL_DOOR_INFO.get(csz)#获取传送门的信息
    lastscene = MapManager().getMapId(player.baseInfo.getTown())
    if doorinfo.get('functionType')==1:#跳转场景
        placeId = doorinfo.get('nextmap')
        position = (doorinfo.get('init_x'),doorinfo.get('init_y'))
        player.baseInfo.setTown( placeId)
        player.baseInfo.setState(0)
        PlayersManager().addPlayer(player)
        defencelog_app.isReward(player.baseInfo.id, player.getDynamicId())
        scene = MapManager().getMapId(placeId)
        scenename = scene.getSceneName()
        chatnoderemote.callRemote('JoinRoom',characterid,placeId,scenename)
        scene.addPlayer(characterid)
        player.quest.setNpcList(scene._npclist)
        player.baseInfo.initPosition(position)
        scene.pushEnterPlace([dynamicId])
        result = {'result':True}
    else:
        instanceId = doorinfo.get('famID')
        result = instance_app.enterInstance1(player,dynamicId, characterid, instanceId,0)
    if result.get('result'):
        lastscene.dropPlayer(characterid)
        
    
    
    
    
    
