#coding:utf8
'''
Created on 2011-9-26
行会战副本接口
@author: lan
'''
from app.scense.applyInterface.playerInfo import CanDoServer
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.battlefieldarea.battleAreaManager import BattleAreaManager
from app.scense.core.scene.SceneManager import SceneManager_new
from app.scense.core.language.Language import Lg

def enterGuildBattleField(dynamicId,characterId):
    '''进入行会战副本
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    res = CanDoServer(characterId)
    if not res['result']:
        return res        
    player = PlayersManager().getPlayerByID(characterId)
    if  not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if not player.status.getLifeStatus():
        return {'result':False,'message':Lg().g(97)}
    if player.baseInfo.getState()==1:
        return {'result':False,'message':Lg().g(98)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    battleArea = BattleAreaManager().getGuildBattleAreaIdByGuildId(guildId)
    if not battleArea:
        return {'result':False,'message':Lg().g(99)}
    nowSceneId = battleArea.enterGuildBattleField(guildId,characterId)
    if not nowSceneId:
        return {'result':False,'message':Lg().g(100)}
    lastscene = SceneManager_new().getSceneById(player.baseInfo.getLocation())
    lastscene.dropPlayer(player.baseInfo.id)
    player.baseInfo.setState(2)
    data = {'placeId':nowSceneId}
    return {'result':True,'data':data}
    

    
    
        
        