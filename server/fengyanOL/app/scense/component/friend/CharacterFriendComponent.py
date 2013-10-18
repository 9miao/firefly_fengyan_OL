#coding:utf8
'''
Created on 2011-3-31

@author: sean_lan
'''

from app.scense.component.Component import Component 
from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbFriend
from app.scense.core.language.Language import Lg


class CharacterFriendComponent(Component):
    '''
    friend component for character
    '''

    def __init__(self,owner):
        '''
        Constructor
        '''
        Component.__init__(self,owner)
        self._friendCount = 200#玩家拥有好友数量上限
        self._enermieCount=20 #玩家拥有黑名单角色数量上限
        self._friends = set([]) #好友 set[好友角色id,好友角色id,好友角色id]
        self._enermies = set([]) #黑名单  set[黑名单角色id,黑名单角色id,黑名单角色id]
        self.initFrined()
        
    def initFrined(self):
        self._friends = set(dbFriend.getFirendListByFlg(self._owner.baseInfo.id, 1))
        self._enermies = set(dbFriend.getFirendListByFlg(self._owner.baseInfo.id, 2))
     

    
    def getFriends(self):
        '''获取好友角色列表'''
        return list(self._friends)
    
    def setFriends(self,friends):
        '''设置好友角色列表'''
        self._friends = set(friends)
        
    def getEnermies(self):
        '''获取黑名单角色列表'''
        return list(self._enermies)
    
    def setEnermies(self,enermies):
        '''设置黑名单角色列表'''
        self._enermies = set(enermies)
        
    def getFriendAll(self,characterId,friendType,ziduan,guize):
        '''显示好友信息
        @param characterId: int 角色的id
        @param friendType: 好友类型(1,2,3)1:好友  2:黑名单  3:全部   4:仇敌
        @param ziduan: int  1按角色名称,0角色等级，2行会名称  3最近登录时间
        @param guize: int 排序规则 1正序   0倒序
        @param page: int 当前页数
        @param counts: int 每页多少条信息
        '''
        #['id','nickname','profession','level','name','LastonlineTime']
        result=dbFriend.getPlayerFriend(characterId, friendType, ziduan, guize)
        from app.scense.core.PlayersManager import PlayersManager
        list1=[]#在线
        list2=[]#不在线
        if result:
            for i in range(len(result)):
                cid=result[i].get("id",0)
                if cid>0:
                    player=PlayersManager().getPlayerByID(cid)
                    if player:#如果角色在线
                        result[i]['level']=player.level.getLevel()#角色等级
                        if player.guild.getID()!=0:
                            result[i]['name']=player.guild.getGuildName()#所属国的名字
                        result[i]['clue']= player.baseInfo.getSceneName()#场景名称
                        result[i]['zx']=1
                        if player.baseInfo.getState()>0: #如果在副本中
                            result[i]['scenename']=Lg().g(316)
                        else: #如果不在副本中
                            result[i]['scenename']=player.baseInfo.getSceneName()
                        list1.append(result[i])
                    else: #如果角色不在线
                        result[i]['scenename']=Lg().g(272)
                        result[i]['zx']=0
                        list2.append(result[i])
            return list1+list2
        return None
        
    def getTypeByid(self,playerId):
        '''返回playerid的角色有当前角色的关系
        @param playerId: int 关系好友角色id
        @param result: int 2黑名单关系    1好友关系    0没有关系
        '''
        if playerId in self.getEnermies():#如果在黑名单中
            return 2
        if playerId in self.getFriends():#如果在好友列表中
            return 1
        return 0
    
    def addFriend(self,characterId,playerId,friendType,pyid):
        '''添加一个好友或者黑名单
        @param characterId: int 角色的id
        @param friendType: int(1,2) 好友的类型 1:好友  2:黑名单
        @param playerId: int 好友或者黑名单角色id
        @param isSheildedMail: int 0不屏蔽邮件   1屏蔽邮件
        @param pyid: int 关系好友动态id -1表示没有  
        '''
        from app.scense.netInterface import pushObjectNetInterface
        from app.scense.serverconfig.chatnode import chatnoderemote
        if len(self.getFriends())>= self._friendCount:
            return {'result':False,'message':Lg().g(317)}
        if playerId ==self._owner.baseInfo.id:
            return {'result':False,'message':Lg().g(318)}

        if friendType==1:#添加好友
            chatnoderemote.callRemote('addWhitelist',characterId,playerId)#添加到白名单(好友)
            if playerId in self.getEnermies():#如果角色在黑名单中
                dbFriend.setType(characterId, playerId, friendType,0)
                self._enermies.remove(playerId)
                self._friends.add(playerId)
                self._owner.daily.noticeDaily(15,0,-1)
                return {'result':True,'message':Lg().g(319)}
            elif playerId in self.getFriends():#如果角色在好友中
                return {'result':False,'message':Lg().g(320)}
            else:
                self._owner.daily.noticeDaily(15,0,-1)
                dbaccess.addFriend(self._owner.baseInfo.id, playerId, friendType, 0)
                self._friends.add(playerId)
                if pyid>=0:
                    pushObjectNetInterface.pushaddPlayerFriendto(characterId, self._owner.baseInfo.getNickName(), [pyid])#推送反添加好友
                return {'result':True,'message':Lg().g(321)}
        else:#添加黑名单
            chatnoderemote.callRemote('addBacklist',characterId,playerId)#添加到黑名单
            if playerId in self.getFriends():#如果在好友列表中
                dbFriend.setType(characterId, playerId, friendType,1)
                self._friends.remove(playerId)
                self._enermies.add(playerId)
                return {'result':True,'message':Lg().g(322)}
            elif playerId in self.getEnermies():#如果角色已经在黑名单中
                return {'result':False,'message':Lg().g(323)}
            else:
                dbaccess.addFriend(self._owner.baseInfo.id, playerId, friendType, 1)
                self._enermies.add(playerId)
                return {'result':True,'message':Lg().g(324)}
        return {'result':True,'message':Lg().g(69),}
    
    def deleteFriend(self,characterId,friendId):
        '''删除好友
        @param playerId: 角色的id
        '''
        if friendId in self.getEnermies():#如果在黑名单中
            self._enermies.remove(friendId)
        if friendId in self.getFriends():#如果在好友列表中
            self._friends.remove(friendId)
        result = dbaccess.deletePlayerFriend(characterId,friendId)
        if not result:
            return {'result':False,'message':Lg().g(325)}
        return {'result':True,'message':Lg().g(326)}
        
    def updataSheildedMail(self,characterId,friendId,isSheildMail,friendType):
        '''更新好友邮件屏蔽状态
        @param playerId: int 好友的id
        @param isSheildedMail:int 是否屏蔽邮件 0.不屏蔽邮件 1.屏蔽
        '''
        if friendId not in [fri['friendId'] for fri in self._friends+self._enermies]:
            return {'result':False,'message':Lg().g(327)}
        result = dbaccess.updataSheildedMail(characterId,friendId,isSheildMail,friendType)
        if result:
            return {'result':True,'message':Lg().g(328)}
        return {'result':False,'message':Lg().g(329)}
    
    
    def selectFriends(self,name,ziduan,guize):
        '''查找好友
        @param name: string 好友的角色的昵称(名字)
        @param ziduan: int  1按角色名称,0角色等级，2行会名称  3最近登录时间
        @param guize: int 排序规则 1正序   0倒序
        '''
        result=dbFriend.selectFriend(name, ziduan, guize)
        from app.scense.core.PlayersManager import PlayersManager
        
        if result:
            for i in range(len(result)):
                cid=result[i].get("id",0)
                if cid>0:
                    if PlayersManager().getPlayerByID(cid):
                        result[i]['zx']=True
                        continue
                result[i]['zx']=False
            return result
        
        return None