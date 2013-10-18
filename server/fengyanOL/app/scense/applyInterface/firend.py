#coding:utf8
'''
Created on 2011-4-14

@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbReport
from app.scense.utils.dbopera import dbFriend
from app.scense.serverconfig.chatnode import chatnoderemote
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.language.Language import Lg

def addPlayerFriend(dynamicId,characterId,friendName,friendType,isSheildedMail=0):
    '''添加好友
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param friendName: string 对方的昵称
    @param friendType: int(1,2) 好友的类型 1:好友  2:黑名单
    @param isSheildedMail: 是否屏蔽邮件
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
        
    friendId = dbaccess.getCharacterIdByNickName(friendName)#返回好友角色id [id]
    if not friendId:
        msg =Lg().g(75)
        pushObjectNetInterface.pushOtherMessage(905,msg, [player.getDynamicId()])
        return {'result':False,'message':Lg().g(68)}
    pyid=-1 #关系好友动态id -1表示角色没有在线   其他表示角色动态id
    py1=PlayersManager().getPlayerByID(friendId[0])
    
    if py1 and py1.friend.getTypeByid(characterId)==0:#如果好友在线
        pyid=py1.getDynamicId()
    result = player.friend.addFriend(characterId,friendId[0],friendType,pyid)
    if result:
        pushObjectNetInterface.pushOtherMessage(905, result['message'], [player.getDynamicId()])
        return {'result':True,'message':Lg().g(69)}

    return {'result':False,'message':Lg().g(70)}
    
def getPlayerFrinds(dynamicId,characterId,friendType=1,ziduan=0,guize=0):
    '''获取角色好友信息
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param friendType: 好友类型(1,2,3)1:好友  2:黑名单  3:全部   4:仇敌
    @param ziduan: int  1按角色名称,0角色等级，2行会名称  3最近登录时间
    @param guize: int 排序规则 1正序   0倒序
    '''
    
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    friendInfo= player.friend.getFriendAll(characterId,friendType,ziduan,guize)
    return {'result':True,'friends':friendInfo}
    
def removePlayerFriend(dynamicId,characterId,friendId):
    '''删除好友
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param friendId: int 好友编号
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.friend.deleteFriend(characterId,friendId) 
    if result:
        if result.get('result'):
            chatnoderemote.callRemote('dropfriend',characterId,friendId)#删除好友
            pushObjectNetInterface.pushOtherMessage(905, Lg().g(71), [player.getDynamicId()])
    return result

def searchCharacterByName(dynamicId,characterId,nickname):
    '''根据昵称获取角色信息
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param nickname: string 角色的昵称
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = dbaccess.getCharecterInfoByNickName(nickname)
    if data:
        return {'result':True,'message':Lg().g(72),'data':data}
    return {'result':False,'message':Lg().g(73),'data':None}

def selectFriends(name,ziduan,guize):
        '''查找好友
        @param name: string 好友的角色的昵称(名字)
        @param ziduan: int  1按角色名称,0角色等级，2行会名称  3最近登录时间
        @param guize: int 排序规则 1正序   0倒序
        '''
#        from utils.dbopera import dbFriend
        result=dbFriend.selectFriend(name, ziduan, guize)
#        from core.PlayersManager import PlayersManager
        
        if result:
            for i in range(len(result)):
                cid=result[i].get("id",0)
                if cid>0:
                    if PlayersManager().getPlayerByID(cid):
                        result[i]['zx']=True
                        continue
                result[i]['zx']=False
            return {'result':True,'message':Lg().g(74),'friends':result}
        
        return {'result':False,'message':Lg().g(75),'friends':None}

def s_blacklist(dynamicId,characterId):
    '''获取黑名单列表
    @param dynamicId: int 角色动态id
    @param characterId: int 角色id
    '''
    
    data = dbFriend.getBlackList(characterId,1)
    if not data:
        return {'result':True,'message':Lg().g(76),'data':data}
    return {'result':True,'message':Lg().g(85),'data':data}

def updataSheildedMail(characterId,fid,friendType):
    '''加入黑名单
    @param characterId: int 角色id
    @param fid: int 好友id
    @param isSheildedMail: int 是否屏蔽邮件 0.不屏蔽邮件 1.屏蔽
    @param friendType: int 关系类型 1.好友 2.黑名单 4.仇敌
    '''
    isSheildedMail=0
    if friendType==2:
        isSheildedMail=1
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data=player.friend.updataSheildedMail(characterId,fid,isSheildedMail,friendType)
    return data
def AddReport(cid,tocid,context):
    '''添加举报
    @param int: cid 当前角色id
    @param int: tocid 被举报人角色id(倒霉的那个人)
    @param string: context 举报信息
    '''
    data=dbReport.add(cid, tocid, context)
    return data

def setShowMesFlag(did,cid,tp):
    '''设置好友提示
    @param id: int 当前角色id
    @param cid:int 好友角色id
    @param tp: int 是否提示 0不提示 1 提示 
    '''
    return dbFriend.setShowMesFlag(did, cid, tp)
