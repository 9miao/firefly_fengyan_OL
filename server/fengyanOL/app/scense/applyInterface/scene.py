#coding:utf8
'''
Created on 2011-4-14

@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.instance.InstanceManager import InstanceManager
from app.scense.core.map.MapManager import MapManager
from app.scense.core.language.Language import Lg
    
def moveInScene(dynamicId,characterId,sceneId,x,y):
    '''在场景中移动
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param x: int 移动到的x坐标
    @param y: int 移动到的y坐标 
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    if x==-1 and y==-1:
        if player.baseInfo.getState()==1:  #如果角色在副本
            sceneId = player.baseInfo.getLocation() #获取角色所在场景Id
#            id=player.baseInfo.getInstanceid() #副本模板Id
            dtid=player.baseInfo.getInstancetag() #副本动态Id
            instance=InstanceManager().getInstanceByIdTag(dtid) #获取副本实例
            sceneId = instance._Scenes.keys()[0]
            nowScene = instance._Scenes[sceneId]#获取场景实例
            nowScene.pushNowScenePosition(dynamicId,characterId)
        else:
            scene = MapManager().getMapId(sceneId)
            scene.pushNowScenePosition(dynamicId,characterId)
        return
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if player.baseInfo.getStatus()!=1:
        return {'result':False,'message':u'您正处于%s状态'%player.baseInfo.getStatusName()}
    player.baseInfo.updateDestination((x,y))
    
    


