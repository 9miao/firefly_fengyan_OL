#coding:utf8
'''
Created on 2011-3-31

@author: sean_lan
'''
from app.scense.core import User
from app.scense.core.UserManager import UsersManager
from app.scense.core.character.PlayerCharacter import PlayerCharacter
from app.scense.utils import dbaccess
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.language.Language import Lg

def loginToServer(dynamicId,username ,password):
    '''登陆服务器
    @param dynamicId: int 客户端动态ID
    @param username: str 用户名
    @param password: str 用户密码
    '''
    
    did = dbaccess.getUserIdByUserNamePassword(username ,password)
    if not did:
        return{'result':False,'message':Lg().g(149)}
    user=UsersManager().getUserByID(did)
    if user:
        user.disconnectClient()
        UsersManager().dropUser(user)
    userNew = User.User(did, username, dynamicId)
    UsersManager().addUser(userNew)
    UserCharacterList = userNew.getUserCharacterListInfo()
    lastCharacter = userNew.getLastCharacter()
    data = {'len':len(UserCharacterList),'userId':did,'defaultId':lastCharacter,'UserCharacterList':UserCharacterList}
    return{'result':True,'message':Lg().g(25),'data':data}
    
def activeNewPlayer(dynamicId,userId,nickName,profession):
    '''
    创建角色
    arguments=(userId,nickName,profession)
    userId用户ID
    nickName角色昵称
    profession职业选择
    '''
    user=UsersManager().getUserByID(userId)
    if user is None:
        return {'result':False,'message':Lg().g(18)}
    result = user.creatNewCharacter(nickName, profession)
    return result

def roleLogin(dynamicId,userId,characterId):
    '''角色登陆
    @param userId: int 用户id
    @param characterId: 角色的id 
    '''
    user=UsersManager().getUserByID(userId)
    if dynamicId != user.getDynamicId():
        return {'result':False,'message':Lg().g(18)}
    if not user:
        return {'result':False,'message':Lg().g(18)}
    user.dropAllCharacter()
    PlayersManager().dropPlayerByID(characterId)
    player = PlayerCharacter(characterId,dynamicId=dynamicId)
    PlayersManager().addPlayer(player)
    if not player.status.getLifeStatus():
        player.status.updateLifeStatus( 1)
        player.attribute.updateHp(int(player.attribute.getMaxHp()*0.01)+1)
        player.attribute.updateMp(int(player.attribute.getMaxMp()*0.01)+1)
    data = {}
    data['placeId'] = player.baseInfo.getTown()
#    player.quest.pushPlayerQuestProcessList()
    user.updateLastCharacter(characterId)
    return {'result':True,'message':Lg().g(25),'data':data}
    
def deleteRole(dynamicId,userId,characterId,password):
    '''删除角色
    @param userId: int 用户id
    @param characterId: 角色的id 
    @param password: string 用户的密码
    '''
    user=UsersManager().getUserByID(userId)
    if dynamicId != user.getDynamicId():
        return {'result':False,'message':Lg().g(18)}
    if user is None:
        return {'result':False,'message':Lg().g(18)}
    res = dbaccess.checkUserPassword(userId, password)
    if not res:
        return {'result':False,'message':Lg().g(150)}
    data = user.deleteCharacter(characterId)
    return data
