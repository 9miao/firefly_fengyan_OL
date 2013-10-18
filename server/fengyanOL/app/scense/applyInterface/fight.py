#coding:utf8
'''
Created on 2011-4-15
@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.map.MapManager import MapManager
from app.scense.core.instance.InstanceManager import InstanceManager
from app.scense.core.fight.fight_new import DoFight
from app.scense.applyInterface.playerInfo import CanDoServer
from app.scense.core.language.Language import Lg


def FightInScene(dynamicId,characterId,monsterId):
    '''副本战斗
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param monsterId: int 碰撞的怪物在场景中的id
    '''
    res = CanDoServer(characterId)
    if not res['result']:
        return res        
    player = PlayersManager().getPlayerByID(characterId)
    if  not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if not player.status.getLifeStatus():
        return {'result':False,'message':Lg().g(97)}
    if player.baseInfo.getState()==1:  #如果角色在副本
        dtid=player.baseInfo.getInstancetag() #副本动态Id
        instance=InstanceManager().getInstanceByIdTag(dtid) #获取副本实例
        sceneId = player.baseInfo.getLocation()
        nowScene = instance._Scenes[sceneId]#获取场景实例
    else:
        town=player.baseInfo.getTown()
        nowScene=MapManager().getMapId(town)
#        return {'result':False,'message':Lg().g(64)}
    data = nowScene.FightInScene(monsterId,int(player.baseInfo.getPosition()[0]),
                                 characterId)
    if data.get('result'):
        player.baseInfo.setStatus(4)   #角色状态设置为战斗状态
    return data
#    return {'result':True,'message':Lg().g(67),'data':data}

def quitFight(dynamicId,characterId):
    '''退出战斗
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id 
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    player.baseInfo.setStatus(1)   #离开战斗状态
    player.msgbox.AfterFightMsgHandle()#战后消息处理
    player.updatePlayerInfo()
    player.effect.doEffectHot()
    player.attribute.PromptHP()
    data = {'placeId':player.baseInfo.getLocation()}
    return {'result':True,'message':Lg().g(65),'data':data}

def getAllCardInfo(dynamicId,characterId):
    '''获取所有卡片的信息
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    
    if player.baseInfo.getState()==1:  #如果角色在副本
#        id=player.baseInfo.getInstanceid() #副本模板Id
        dtid=player.baseInfo.getInstancetag() #副本动态Id
        instance=InstanceManager().getInstanceByIdTag(dtid)#获取副本实例
        data = instance.cards.getAllCardInfo(characterId)
    else:
        data = {'result':False}
    return data

def TurnCard(dynamicId,characterId,cardId):
    '''翻转卡片
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param cardId: int 被翻转卡片的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if player.baseInfo.getState()==1:  #如果角色在副本
#        id=player.baseInfo.getInstanceid() #副本模板Id
        dtid=player.baseInfo.getInstancetag() #副本动态Id
        instance=InstanceManager().getInstanceByIdTag(dtid) #获取副本实例
        data = instance.cards.turnCard(characterId,player.baseInfo.getNickName(),cardId)
    else:
        data = {'result':False}
    return data
    
def FightWithPlayer(dynamicId,characterId,tid):
    '''玩家PK
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param tid: int 对方的id
    '''
    res = CanDoServer(characterId)
    if not res['result']:
        return res
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    toplayer = PlayersManager().getPlayerByID(tid)
    if not toplayer:
        return {'result':False,'message':Lg().g(66)}
    guildid = player.guild.getID()
    tguildid = toplayer.guild.getID()
    town = player.baseInfo.getTown()
    ttown = toplayer.baseInfo.getTown()
    if not player.pvp.checktime():
        return {'result':False,'message':u"PK战斗CD中"}
    if not toplayer.pvp.checktime():
        return {'result':False,'message':u"对方PK战斗CD中"}
    if town!=ttown:
        return {'result':False,'message':u"不在统一场景无法进行战斗"}
    if player.guild.getID()== toplayer.guild.getID() or 0 in [guildid,tguildid]:
        return {'result':False,'message':u"不允许本国之间战斗"}
    level = player.level.getLevel()
    tlevel = player.level.getLevel()
    if level<25 or tlevel<25:
        return {'result':False,'message':u"低于25级不能进行战斗"}
    player.pvp.recordtime()
    toplayer.pvp.recordtime()
    data = DoFight([player], [toplayer], now_X=550)
    #战后的处理
    battleresult = data.battleResult
    nowscene = MapManager().getMapId(ttown)#获取当前场景
    if battleresult==1:#如果主动方胜利
        nowscene.dropPlayer(tid)#在当前场景中移除被攻击的玩家
        toscene = MapManager().getMapId(1000)#扔回其他场景
        toscene.addPlayer(tid)
        toscene.pushEnterPlace([toplayer.dynamicId])
        toplayer.baseInfo.setTown(1000)
    else:
        nowscene.dropPlayer(characterId)#在当前场景中移主动攻击的玩家
        toscene = MapManager().getMapId(1000)#扔回其他场景
        toscene.addPlayer(characterId)
        toscene.pushEnterPlace([player.dynamicId])
        player.baseInfo.setTown(1000)
    return {'result':True,'data':data,'sendlist':[dynamicId,toplayer.dynamicId]}


