#coding:utf8
'''
Created on 2011-6-21
新手引导
@author: lan
'''
from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbBeginner
import registered
from app.scense.core import User
from app.scense.core.UserManager import UsersManager
from app.scense.core.character.PlayerCharacter import PlayerCharacter
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

def beginnersLogin():
    '''新手注册'''
    beginnerId = dbBeginner.creatBeginner()
    if not beginnerId:
        return {'result':False}
    return {'result':True,'data':beginnerId}

def getRandomName(_conn):
    '''获取随机昵称'''
    if _conn.transport.client[1]=='192.168.1.254':
        return {'result':True,'data':u'耗子你妹啊'}
    data = dbBeginner.getRandomName()
    return {'result':True,'data':data[1]}

def beginnersRegist(dynamicId,beginnerId,nickname):
    '''新手注册'''   
    
    if len(nickname)<2 or len(nickname)>20:
        return {'result':False,'message':Lg().g(20)}
    for word in dbaccess.All_ShieldWord:
        if nickname.find(word[0])!=-1:
            return {'result':False,'message':Lg().g(21)}
    result1 = dbaccess.getCharacterIdByNickName(nickname)
    result2 = dbBeginner.getBeginnerByNickName(nickname)
    if result1 or result2:
        return {'result':False,'message':Lg().g(22)}
    result = dbBeginner.updateBeginnerNickname(beginnerId,nickname)
    if not result:
        return {'result':False}
    return {'result':True}

def RecordStepID(dynamicId,beginnerId,recordId):
    '''记录新手引导步骤'''
    dbBeginner.updateRecordId(beginnerId, recordId)
    return {'result':True}

def FinalRegist(dynamicId,username,password,nickname,profession):
    '''最终注册'''
    email = 'xxxxxxxx@163.com'
    if len(username)<4 or len(username)>8:
        return {'result':False,'message':Lg().g(20)}
    result = registered.addPlayer(username, password, email)
    if result==1:
        return {'result':False,'message':Lg().g(22)}
    elif result==2:
        return {'result':False,'message':Lg().g(23)}
    userId = dbaccess.getUserIdByUserNamePassword(username ,password)
    userNew = User.User(userId, username, dynamicId)
    UsersManager().addUser(userNew)
    result = userNew.creatNewCharacter(nickname, profession)
    if not result.get('result',False):
        return {'result':False,'message':Lg().g(24)}
    data = result.get('data',None)
    if not data:
        return {'result':False,'message':Lg().g(24)}
    characterId = data.get('newCharacterId',0)
    player = PlayerCharacter(characterId,dynamicId=dynamicId)
#    player.pack.putNewItemsInPackage(27, 1)#放置新手引导中获得的的物品
#    player.pack.putNewItemsInPackage(28, 1)#放置新手引导中获得的的物品
    PlayersManager().addPlayer(player)
    data = {}
    data['userId'] = userId
    data['characterId'] = characterId
    data['placeId'] = player.baseInfo.getTown()
    return {'result':True,'message':Lg().g(25),'data':data}

def GMInfo4000(dynamicId,characterId,gmmsg):
    '''gm消息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    characterName = player.baseInfo.getName()
    dbBeginner.insertGMmsg(characterName, gmmsg)
    msg = Lg().g(26)
    pushOtherMessage(905, msg, [dynamicId])
    return {'result':True}





    