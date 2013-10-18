#coding:utf8
'''
Created on 2011-4-11

@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.character.PlayerCharacter import PlayerCharacter
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.instance.InstanceManager import InstanceManager
from app.scense.core.scene.SceneManager import SceneManager_new
from app.scense.applyInterface import icon_app
from app.scense.applyInterface import friendRecord_app

from app.scense.applyInterface.packageInfo import EQUIPPOSITION
from app.scense.core.language.Language import Lg

def CanDoServer(characterId):
    '''是否能进行操作
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if player is None:# or not player.checkClientID(message):
        return {'result':False, 'message':Lg().g(18)}
    status = player.baseInfo.getStatusName()
    if not status:
        return {'result':True}
    else:
        return {'result':False, 'message':Lg().g(173)%status}

def getPlayerInfo(dynamicId,characterId):
    '''获取角色信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.formatInfo()
    hasBuyCount = player.afk.turnenergytimes
    info = {'playerInfo':data,'hasBuyCount':hasBuyCount}
    return {'result':True,'message':u'获取信息成功','data':info}
    
#def getOtherPlayerInfo(dynamicId,characterId,otherCharacterId):
#    '''获取其他角色的信息
#    @param dynamicId: int 客户端的id
#    @param characterId: int 角色的id
#    @param otherCharacterId: 其他角色的id
#    '''
#    toPlayer = PlayersManager().getPlayerByID(otherCharacterId)
#    if not toPlayer:
#        return {'result':False,'message':u'角色不在线'}
#    data = toPlayer.formatInfo()
#    return {'result':True,'message':u'获取信息成功','data':data}

def addPoint(dynamicId,characterId,manualStr,manualVit,manualDex):
    """角色加点
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param manualStr: int 角色添加的力量点
    @param manualVit: int 角色添加的体质点
    @param manualDex: int 角色添加的灵巧点  
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.attribute.addAttributePoint(manualStr , manualVit ,manualDex)
    return data

def GetOtherRoleInfo(dynamicId,characterId,roleId):
    '''获取其他玩家的信息
    '''
#    player = PlayersManager().getPlayerByID(characterId)
#    if not player or not player.CheckClient(dynamicId):
#        return {'result':False,'message':Lg().g(18)}
    toplayer = PlayersManager().getPlayerByID(roleId)
    if not toplayer:
        try:
            toplayer=PlayerCharacter(roleId)
        except:
            return{'result':True,'message':Lg().g(75)}
    playerInfo = toplayer.formatInfo()
    package = toplayer.pack.getEquipmentSlot()
#    packageItemInfo = package.getPackageItemInfo()
    equipmentList = package.getItemList()
    keys_copy = dict([(items['position'],items) for items in equipmentList])
    equipmentList_copy = []
    for position in EQUIPPOSITION:
        item = keys_copy.get(position,None)
        equipmentList_copy.append(item)
    data = {'packageItemInfo':equipmentList_copy,'playerInfo':playerInfo}
    return {'result':True,'message':u'查看角色信息','data':data}
    
def updateSpirit(pid,contxt):
    '''修改角色心情
    @param pid: int 角色id
    @param context: str 心情
    '''
    player=PlayersManager().getPlayerByID(pid)
    if player.baseInfo.updateSpirit(contxt):
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(175), [player.getDynamicId()])
    else:
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(176), [player.getDynamicId()])
    return {'result':True,'message':u''}
    
def celebrateAddExp(tid,pid,typeid):
    '''因祝福而增加角色经验
    @param pid: int 当前升级角色id
    @param tid: int 点击祝福的好友角色id
    @param typeid: int 祝福方式 0:错误 1:恭喜 2:鄙视
    '''
    
    count=friendRecord_app.getRecord(tid)#获取祝福好友当天祝福次数
    if count>=friendRecord_app.count:
        return {'result':False,'message':Lg().g(177),'name':''}
#    player=PlayersManager().getPlayerByID(pid) #升级角色
#    if not player:
#        return {'result':False,'message':u'对方已经下线，不能祝福'}
#    name=player.baseInfo.getNickName()#升级角色名称
#    dyid=player.getDynamicId() #升级角色的动态id
    player1=PlayersManager().getPlayerByID(tid)
#    if not player:
#        return {'result':False,'message':Lg().g(18)}
    name1=player1.baseInfo.getNickName()#祝福好友角色名称
#    level= player.level.getLevel()
    exp=50 #升级角色获得的经验
    exp1=50 #祝福好友角色获得的经验
    zf=u""
    if typeid==2:
        zf+=name1+Lg().g(179)%str(exp)
    elif typeid==1:
        zf+=name1+Lg().g(180)%str(exp)
    elif typeid==0:
        return {'result':False,'message':u'祝福方式传0(代表错误)!','name':''}
#    player.level.addExp(exp) #给升级角色添加经验
    player1.level.addExp(exp1) #给祝福好友添加经验
#    pushObjectNetInterface.pushOtherMessage(905, zf, [dyid])
    friendRecord_app.addZF(tid)#添加角色祝福次数
    if typeid==2:
        return {'result':False,'message':Lg().g(181)%str(exp1),'name':name1}
    elif typeid==1:
        return {'result':False,'message':Lg().g(182)%str(exp1),'name':name1}
    
def _pushSceneInfo(dynamicId,characterId):
    '''推送场景信息'''
    player=PlayersManager().getPlayerByID(characterId)
    if player.baseInfo.getState()==1:  #如果角色在副本
#        id=player.baseInfo.getInstanceid() #副本模板Id
        dtid=player.baseInfo.getInstancetag() #副本动态Id
        instance=InstanceManager().getInstanceByIdTag(dtid) #获取副本实例
        sceneId = player.baseInfo.getLocation()
        oldscene = instance._Scenes[sceneId]#获取场景实例
    else:
        sceneId = player.baseInfo.getTown()
        oldscene = SceneManager_new().getSceneById(sceneId)
    if oldscene:
        oldscene.pushEnterPlace([dynamicId])
    
def initplayerInfo(dynamicId,characterId):
    '''请求初始化角色信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player=PlayersManager().getPlayerByID(characterId)
    player.afk.initAFKData()
    player.quest.pushPlayerScenceNpcQuestStatus()#推送任务状态
    player.quest.pushPlayerQuestProcessList()#推送任务追踪信息
    player.instance.initData()
    player.arena.pushIcon()
    player.icon.pushGameTopIcon()
    icon_app.onland(characterId)
    player.schedule.noticeSchedule(1)#每日登陆日程
    player.arena.pushArenaCD()
    player.tower.initTowerInfo()
    
    
def AddHuoLi(dynamicId,pid):
    '''给角色增加体力值'''
    player= PlayersManager().getPlayerByID(pid)
    if not player:
        return {'result':False,'message':Lg().g(18),'failType':0}
    if player.attribute.getEnergy()>160:#角色当前活力值
        return {'result':False,'message':Lg().g(183),'failType':0}
    result = player.afk.buyEnergy()
    return result
    
    
    
    
    