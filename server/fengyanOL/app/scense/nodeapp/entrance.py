#coding:utf8
'''
Created on 2012-3-20
场景服务的入口
@author: Administrator
'''
import cPickle
from app.scense.utils.dbopera import dbMap
from app.scense.serverconfig.node import nodeHandle
from app.scense.serverconfig.chatnode import chatnoderemote
#from serverconfig.publicnode import publicnoderemote
#from world.scene import Scene
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.instance.ColonizeManage import ColonizeManage
from app.scense.core.map.MapManager import MapManager
from app.scense.core.character.PlayerCharacter import PlayerCharacter
import datetime
from app.scense.applyInterface import defencelog_app
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

def pushPlayerGonggaoXinxi(player):
    '''推送角色上线公告的信息
    @param player: PlayerCharacter Object 角色的实例
    @param sendtype: int 发送方式  1聊天 2公告
    '''
    sendstr = ""
    playername = player.baseInfo.getName()
    strlist = []
    viptype = player.baseInfo.getType()
    sendtype = 1
    if 0<viptype<3:
        sendtype = 1
        strlist.append(Lg().g(604))
    elif viptype >= 3:
        sendtype = 2
        strlist.append(Lg().g(604)+u',')
    post = player.guild.getPost()
    guildId = player.guild.getID()
    guildname = player.guild.getGuildName()
    if post==4:
        citylist = ColonizeManage().getCityList()[::-1]
        for city in citylist:
            if city.get('gid',-1)==guildId:
                sendtype = 2
                cityname = city.get('cityname')
                strlist.append(Lg().g(605)%(guildname,cityname))
                continue
    if strlist:
        sendstr = sendstr.join(strlist)+ Lg().g(606)%(playername)
        if sendtype == 1:
            chatnoderemote.callRemote('pushSystemchat',sendstr)
        else:
            chatnoderemote.callRemote('pushSystemToInfo',sendstr)

@nodeHandle
def enterPlace_601(dynamicId, characterId, placeId,force,player):
    '''进入场景'''
    state = 0
    if not player:
        player = PlayerCharacter(characterId,dynamicId = dynamicId)
        player.setlastOnline(datetime.datetime.now())
        pushPlayerGonggaoXinxi(player)
    else:
        player = cPickle.loads(player)
        player.startAllTimer()
        state = 1
    #判断是否满足进入场景的需求
    sceneInfo = dbMap.ALL_MAP_INFO.get(placeId,{})
    levelRequired = sceneInfo['level']
    if player.level.getLevel()<sceneInfo['level']:
        msg = Lg().g(607)%levelRequired
        pushOtherMessage(905, msg, [dynamicId])
        return {'result':False,'message':Lg().g(332)}
    player.baseInfo.setTown( placeId)
    player.baseInfo.setState(0)
    PlayersManager().addPlayer(player)
    defencelog_app.isReward(player.baseInfo.id, player.getDynamicId())
    scene = MapManager().getMapId(placeId)
    scenename = scene.getSceneName()
    chatnoderemote.callRemote('JoinRoom',characterId,placeId,scenename)
    scene.addPlayer(characterId)
    player.quest.setNpcList(scene._npclist)
    scene.pushEnterPlace([dynamicId])
#    if not state:
#        publicnoderemote.callRemote('addPcharacter',characterId,getNodeId())
#    else:
#        publicnoderemote.callRemote('updatePCharacterNodeId',characterId,getNodeId())
    return {'result':True,'message':'','data':{'placeId':placeId}}

@nodeHandle
def leaveScene_610(dynamicId,characterId):
    '''离开场景'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return None,0
    player.stopAllTimer()
    playerDumps = cPickle.dumps(player)
    player.startAllTimer()
    placeId = player.baseInfo.getTown()
    return playerDumps,placeId

#@nodeHandle
#def TurnToInstance_611(dynamicId,characterId,famId):
#    '''跳转到副本的处理
#    '''
#    player = PlayersManager().getPlayerByID(characterId)
#    if not player:
#        return {'result':False,'message':Lg().g(106)}
#    if player.baseInfo.getState()==0:
#        if player.attribute.getEnergy()<5:
#            msg = u'您的体力值不足'
#            pushOtherMessage(905, msg, [dynamicId])
#            return {'result':False,'message':msg}
#        instanceInfo = instance_app.allInfo.get(famId)
#        if not instanceInfo:
#            return {'result':False,'message':u'副本信息部存在'}
#        if player.level.getLevel()<instanceInfo['downlevle']:
#            return {'result':False,'message':Lg().g(332)}
#        Scene().dropPlayer(characterId)
#        for petId in player.matrix._matrixSetting.values():
#            if petId>0:
#                Scene().dropPet(petId)
#        player.stopAllTimer()
#        playerDumps = cPickle.dumps(player)
#        return {'result':True,'data':playerDumps}
#    else:
#        return {'result':False,'message':u'角色不在场景中'}
    
@nodeHandle
def DropCharacterInNode_612(dynamicId,characterId):
    '''移除角色在当前场景(副本)服务中的实例
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return False
    if player.baseInfo.getState()==0:
        placeId = player.baseInfo.getTown()
        scene = MapManager().getMapId(placeId)
        scene.dropPlayer(characterId)
        for petId in player.matrix._matrixSetting.values():
            if petId>0:
                scene.dropPet(petId)
    player.stopAllTimer()
    PlayersManager().dropPlayerByID(characterId)
    return True

