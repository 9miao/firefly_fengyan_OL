#coding:utf8
'''
Created on 2011-6-30
角色死亡复活处理
@author: lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.scene.publicscene import PublicScene
from app.scense.core.instance.InstanceManager import InstanceManager
from app.scense.netInterface.pushObjectNetInterface import pushEnterPlace
from app.scense.core.scene.SceneManager import SceneManager_new
from app.scense.core.language.Language import Lg
#from core.SceneManager import SceneManager
    
def playerReviveInPlace(dynamicId,characterId):
    '''角色原地复活'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if player.status.getLifeStatus():
        return {'result':False,'message':Lg().g(185)}
    player.status.updateLifeStatus(1)
    player.attribute.updateHp(player.attribute.getMaxHp())
    player.attribute.updateMp(player.attribute.getMaxMp())
    player.teamcom.pushTeamMemberInfo()
    return {'result':True,'message':Lg().g(186)}
    
def playerBackRevive(dynamicId,characterId):
    '''角色回城复活
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if player.status.getLifeStatus():
        return {'result':False,'message':Lg().g(185)}
#    player.baseInfo.setState(0)
#    data = enterPlace(dynamicId,characterId,1000)
#    if not data.get('result',False):
#        return data
    state = player.baseInfo.getState()
    if state==0:
        lastscene = SceneManager_new().getSceneById(player.baseInfo.getLocation())
        lastscene.dropPlayer(player.baseInfo.id)
    else:
#        id=player.baseInfo.getInstanceid() #副本id
        tag=player.baseInfo.getInstancetag() #副本动态Id
        instance=InstanceManager().getInstanceByIdTag(tag) #获取副本实例
        old=instance._Scenes[player.baseInfo.getLocation()] #获取当前角色所在副本中的场景
        old.dropPlayer(player.baseInfo.id) #从当前场景中移除角色
    
    gotoSence = SceneManager_new().getSceneById(1000)
    if not gotoSence:
        scene = PublicScene(1000)
        SceneManager_new().addScene(scene)
#    else:
#        areaid = gotoSence.getAreaid()
    gotoSence.addPlayer(player)
#    player.baseInfo.setAreaid(areaid)
    player.baseInfo.setPosition(gotoSence.baseInfo.getInitiaPosition())
    player.baseInfo.setLocation(1000)
    player.baseInfo.setState(0)
    player.status.updateLifeStatus(1)
    player.attribute.updateHp(int(player.attribute.getMaxHp()*0.01)+1)
    player.attribute.updateMp(int(player.attribute.getMaxMp()*0.01)+1)
    
    pushEnterPlace(1000,dynamicId)
    player.teamcom.pushTeamMemberInfo()
    return {'result':True,'message':Lg().g(186)}
    
def askforRevive(dynamicId,characterId):
    '''请求复活
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if player.status.getLifeStatus():
        return {'result':False,'message':Lg().g(185)}
    if not player.teamcom.amITeamMember():
        return {'result':False,'message':u'不是队伍成员没有求助对象'}
    sendList = [p.dynamicId for p in player.teamcom.getMyTeamMember()]
    sendList.remove(player.dynamicId)
#    nickname = player.baseInfo.getNickName()
#    pushAskForRevive(characterId,nickname,sendList)
    return {'result':True,'message':u'发送成功耐心等待'}
    
def ReviveTeamMember(dynamicId,characterId,victimerId,paytype):
    '''复活队友
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param victimerId: int 复活者的id
    @param paytype: int 支付类型 1 物品 2 金币
    '''
    player = PlayersManager().getPlayerByID(characterId)
    toplayer = PlayersManager().getPlayerByID(victimerId)
    if not player or not player.CheckClient(dynamicId):
        data = {'faildtype':0,'goldprice':0}
        return {'result':False,'message':Lg().g(18),'data':data}
    if not toplayer:
        data = {'faildtype':0,'goldprice':0}
        return {'result':False,'message':Lg().g(66),'data':data}
    if not player.teamcom.IsMyTeamMember(victimerId):
        data = {'faildtype':0,'goldprice':0}
        return {'result':False,'message':Lg().g(250),'data':data}
    if toplayer.status.getLifeStatus():
        data = {'faildtype':0,'goldprice':0}
        return {'result':False,'message':Lg().g(185),'data':data}
    if paytype==1:
        if True:
            data = {'faildtype':1,'goldprice':100}
            return {'result':False,'message':Lg().g(248),'data':data}
    else:
        if True:
            data = {'faildtype':2,'goldprice':100}
            return {'result':False,'message':Lg().g(88),'data':data}
    toplayer.status.updateLifeStatus(1)
    toplayer.attribute.updateHp(int(player.attribute.getMaxHp()*0.01)+1)
    toplayer.attribute.updateMp(int(player.attribute.getMaxMp()*0.01)+1)
    player.teamcom.pushTeamMemberInfo()
    return {'result':True,'message':Lg().g(249)}
