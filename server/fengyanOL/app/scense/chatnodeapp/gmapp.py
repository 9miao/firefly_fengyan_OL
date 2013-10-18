#coding:utf8
'''
Created on 2012-6-25

@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager

def additem(characterId,argument):
    '''添加一个物品'''
    player = PlayersManager().getPlayerByID(characterId)
    if len(argument)==2:
        player.pack.putNewItemsInPackage(int(argument[0]),int(argument[1]))
    else:
        player.pack.putNewItemsInPackage(int(argument[0]),1)
        
def levelup(characterId,argument):
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
    
def addgold(characterId,argument):
    '''添加金币'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.finance.addGold(int(argument[0]))
    player.updatePlayerInfo()
    
def addcoin(characterId,argument):
    '''添加金币'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.finance.addCoin(int(argument[0]))
    player.updatePlayerInfo()
    
def vipup(characterId,argument):
    '''修改vip等级'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.baseInfo.updateType(int(argument[0]))
    player.updatePlayerInfo()

def addmorale(characterId,argument):
    '''添加斗气'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.finance.addMorale(int(argument[0]))
    player.updatePlayerInfo()
    
    
def cleancd(characterId,argument):
    '''清除竞技场CD'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.arena.clearCD()
    player.updatePlayerInfo()
    
def pusharena(characterId,argument):
    '''推送竞技场公告
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.arena.pushGonggao(u'龙兴你妹啊')
    
def pushicon(characterId,argument):
    '''推送图标
    '''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.icon.addIcon(int(argument[0]),0)
    
def clearicon(characterId,argument):
    '''清除图标
    '''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.icon.iconlist={}
    player.icon.pushGameTopIcon()
    
def removeicon(characterId,argument):
    '''移除图标
    '''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.icon.removeIcon(int(argument[0]))


def chongzhi(characterId,argument):
    '''充值'''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.finance.Recharge(int(argument[0]))

def addhuoli(characterId,argument):
    '''添加活力
    '''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.attribute.addEnergy(int(argument[0]))
    player.updatePlayerInfo()
    
def addxingyun(characterId,argument):
    '''添加幸运值
    '''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.petShop.addXy(int(argument[0]))
    player.updatePlayerInfo()

def addpet(characterId,argument):
    '''添加宠物
    '''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.pet.addPet(int(argument[0]))
    
def addhp(characterId,argument):
    '''添加兵力
    '''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    player.attribute.addHp(int(argument[0]))
    player.updatePlayerInfo()

def goto(characterId,argument):
    '''跳转场景
    @param characterId: int 角色的ID
    '''
    if len(argument)<1:
        return 
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return
    from app.scense.core.map.MapManager import MapManager
    placeId = int(argument[0])
    lastscene = MapManager().getMapId(player.baseInfo.getTown())
    scene = MapManager().getMapId(placeId)
    if not scene:
        return
    player.baseInfo.setTown( placeId)
    player.baseInfo.setState(0)
    player.baseInfo.initPosition((300,300))
    scene.addPlayer(characterId)
    player.quest.setNpcList(scene._npclist)
    dynamicId = player.dynamicId
    scene.pushEnterPlace([dynamicId])
    lastscene.dropPlayer(characterId)

