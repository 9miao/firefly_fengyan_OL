#coding:utf8
'''
Created on 2011-4-18

@author: sean_lan
'''
#from core.SceneManager import SceneManager
from app.scense.core.scene.SceneManager import SceneManager_new
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.shop.mall import Mall
from app.scense.core.toplist.TopList import TopList
from app.scense.netInterface import pushObjectNetInterface
from app.scense.applyInterface import defencelog_app
from twisted.python import log

def addMonster(characterId,argument):
    '''在场景中添加一个怪物'''
    try:
        templateId = 0
        if len(argument):
            templateId = int(argument[0])
        player = PlayersManager().getPlayerByID(characterId)
        sceneId = player.baseInfo.getLocation()
        nowScene = SceneManager_new().getSceneById(sceneId)
        if len(argument)==3:
            nowScene.produceMonster(templateId,\
                            positionX=int(argument[1]),positionY = int(argument[2]))
        else:
            nowScene.produceMonster(templateId)
    except Exception:
        return
    
def cleanMonsters(characterId,argument):
    '''清除场景中的怪物'''
    try:
        player = PlayersManager().getPlayerByID(characterId)
        sceneId = player.baseInfo.getLocation()
        nowScene = SceneManager_new().getSceneById(sceneId)
        nowScene.cleanMonster()
    except Exception:
        return

#def killself(characterId,argument):
#    '''自杀'''
#    player = PlayersManager().getPlayerByID(characterId)
#    player.attribute.updateHp(0)
#    player.attribute.updateMp(0)
#    player.status.updateLifeStatus(0)
#    player.teamcom.pushTeamMemberInfo()
#    pushLifeStatus(player.getDynamicId())
    
def finishedTask(characterId,argument):
    '''完成任务'''
    player = PlayersManager().getPlayerByID(characterId)
    player.quest.finishedTask(int(argument[0]))
    
def addItem(characterId,argument):
    '''添加一个物品'''
    player = PlayersManager().getPlayerByID(characterId)
    if len(argument)==2:
        player.pack.putNewItemsInPackage(int(argument[0]),int(argument[1]))
    else:
        player.pack.putNewItemsInPackage(int(argument[0]),1)
    
def printTest(characterId,argument):
    '''测试'''
    #print characterId,'ok',argument
    
def updateLastDonate(characterId,argument):
    '''更新上次捐献时间'''
    import datetime
    day = datetime.date(2011,11,01)
    player = PlayersManager().getPlayerByID(characterId)
    player.guild.updateLastDonate(day)
    
def initMemory(characterId,argument):
    ''''刷新从数据库读取的数据'''
    from app.scense.serverconfig.confighandle import initDBData
    from app.scense.core.instance.InstanceManager import InstanceManager
    from app.scense.core.shop.shopmanager import ShopManager
    SceneManager_new().__init__()
    InstanceManager().__init__()
    ShopManager().__init__()
    Mall().__init__()
    initDBData()
    log.msg(u"刷新从数据库读取的数据")

#def kill(characterId,argument):
#    '''杀死其他人'''
#    from app.scense.utils import dbaccess
#    if len(argument)<1:
#        return 
#    toId = dbaccess.getCharacterIdByNickName(argument[0])
#    player = PlayersManager().getPlayerByID(toId[0])
#    player.attribute.updateHp(0)
#    player.attribute.updateMp(0)
#    player.status.updateLifeStatus(0)
#    player.teamcom.pushTeamMemberInfo()
#    pushLifeStatus(player.getDynamicId())
    
def LevelUp(characterId,argument):
    '''升级'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    player.level.updateLevel(int(argument[0]))
    player.updatePlayerInfo()
    
def addexp(characterId,argument):
    '''升级'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    player.level.addExp(int(argument[0]))
    player.updatePlayerInfo()
    
def ta(characterId,argument):
    '''更新排行榜'''
    TopList().updateAll()
    
def jiangli(characterId,argument):
    '''更新生成奖励'''
    defencelog_app.updatets()
    log.msg(u"更新殖民奖励")
    
def addPet(characterId,argument):
    '''添加一个宠物'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.pet.addPet(int(argument[0]))
    
    
def addGold(characterId,argument):
    '''添加金币'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.finance.addGold(int(argument[0]))
    player.updatePlayerInfo()
    
def tasktest(characterId,argument):
    '''任务测试'''
    player = PlayersManager().getPlayerByID(characterId)
    if len(argument)<1:
        return 
    try:
        player.quest.questtestNpcStatu(int(argument[0]))
    except Exception:
        pass
    
def helpme(characterId,argument):
    '''帮助'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    s = globals()
    helps = []
    for key,item in s.items():
        if type(item)==type(helpme):
            info = "\\"+key + ":" + item.func_doc+"\n"
            helps.append(info)
    helpstr = ""
    helpstr = helpstr.join(helps)
    pushObjectNetInterface.pushEnterMessage(helpstr.decode('utf8'), [player.getDynamicId()])


def addguildexp(characterId,argument):
    '''添加行会经验'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.guild.addGuildExp(int(argument[0]))
    
def addCoin(characterId,argument):
    '''添加金币'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.finance.addCoin(int(argument[0]))
    player.updatePlayerInfo()
    
    
