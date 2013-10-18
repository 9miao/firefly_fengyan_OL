#coding:utf8
'''
Created on 2012-3-21

@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle
#from app.scense.serverconfig.dbnode import dbnoderemote
from app.scense.core.PlayersManager import PlayersManager
from app.scense.world.scene import Scene
from twisted.python import log
#from serverconfig.publicnode import publicnoderemote
from app.scense.core.instance.InstanceManager import InstanceManager
from app.scense.core.map.MapManager import MapManager
#from serverconfig.chatnode import chatnoderemote

#dbnoderemote = dbnoderemote

@nodeHandle
def NetConnLost_2(dynamicId):
    '''loginout'''
    player = PlayersManager().getPlayerBydynamicId(dynamicId)
    if not player:
        return True
    try:
        tag=player.baseInfo.getInstancetag() #副本动态Id
        InstanceManager().dropInstanceById(tag)#如果角色下线的时候在副本中，就清空副本
        player.afk.stopMeditation()#在线挂机结算
        player.updatePlayerDBInfo()
#        player.qhtime.dbupdate()#记录角色强化冷却时间
        player.nobility.dbupdate()#记录爵位限制信息
        player.petShop.dbupdate()#记录宠物商店信息
#        publicnoderemote.callRemote('dropPCharacter',player.baseInfo.id)
        PlayersManager().dropPlayer(player)
        state = player.baseInfo.getState()
        if state == 0:
            sceneId = player.baseInfo.getTown()
            scene = MapManager().getMapId(sceneId)
            scene.dropPlayer(player.baseInfo.id)
            if player.baseInfo.getState()==0:
                scene.dropPlayer(player.baseInfo.id)
                for petId,pet in player.pet._pets.items():
                    if pet.getFlowFlag():
                        scene.dropPet(petId)
    except Exception as ex:
        log.err(ex) 
    finally:
        return True
    

@nodeHandle
def updatecharacterEnergy_20(energy):
    '''更新在线角色的活力
    '''
    for player in PlayersManager()._players.values():
        player.attribute.addEnergy(energy)
        player.pushInfoChanged()
        
@nodeHandle
def writePlayerDBInfo_21():
    '''将在线的角色的信息写入数据库
    '''
    for player in PlayersManager()._players.values():
        player.WritePlayerDBInfo()

@nodeHandle
def writePlayerDBInfo_50():
    '''将在线的角色的信息写入数据库,并停止reactor
    '''
    from twisted.internet import reactor
    for player in PlayersManager()._players.values():
        player.WritePlayerDBInfo()
    reactor = reactor
    reactor.stop()




    