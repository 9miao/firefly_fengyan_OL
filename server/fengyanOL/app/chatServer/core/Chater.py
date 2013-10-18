#coding:utf8
'''
Created on 2011-2-14

@author: sean_lan
'''
from app.chatServer.utils.dbopera import dbFriend, dbGuild
from app.chatServer.utils.dbopera import dbCharacter
from app.chatServer.core.language.Language import Lg
ROOMNAME = {1000:u''}


class Chater:
    '''
    聊天成员类
    '''
    def __init__(self, characterId,dynamicId = -1,charactername = u'',profession = 1,level=0,donttalk=0):
        '''聊天成员类初始化
        @param characterId: int 角色的id
        @param charactername: str 角色的名称
        @param dynamicId: int 聊天客户端的ID
        @param roomId: int 房间号ID
        '''
        self.charactername = charactername #角色名称
        self.level=level #角色等级
        self.guildid=0 #国id
        self.profession =profession #职业编号
        self.dynamicId = dynamicId #角色动态id
        self.island=True #是否在线  False表示离线,True表示在线
        self.characterId = characterId #角色id
         
        self.blacklist=set(dbFriend.getAllbyTypeid(characterId, 2))#角色的黑名单 
        self.whitelist=set(dbFriend.getAllbyTypeid(characterId, 1))#角色的白名单(好友)
        self.scenename =Lg().g(106) #所在场景名称
        self.roomId = 0 #房间号码
        self.donttalk=donttalk # 0不禁言 1禁
        gid=dbGuild.getGuildidBypid(characterId)#通过角色id获取所属国
        if gid:
            self.guildid=gid
        if len(charactername)<1:
            info=dbCharacter.getInfoByid(characterId)#通过角色id获取角色信息
            if not info:
                print characterId
            self.charactername = info.get('nickname',charactername) #角色名称
            self.level=info.get('level',level) #角色等级
            self.donttalk=info.get('donttalk',0)# 0不禁言 1禁
            self.profession =info.get('profession',profession) #职业编号
        
        
    def isf(self,tid):
        '''获取该角色与当前玩家角色的关系
        return 0 无关系  1好友  2黑名单
        '''
        if  tid in self.blacklist: #是否在黑名单中
            return 2
        elif tid in self.whitelist:#是否在白名单中
            return 1
        return 0
        
        
    def getDynamicId(self):
        '''获取聊天的动态ID'''
        return self.dynamicId
    
    def getCharacterId(self):
        '''获取聊天成员的ID'''
        return self.characterId
        
    def getCharacterName(self):
        '''获取聊天成员的名称'''
        return self.charactername
    
    def getProfession(self):
        '''获取聊天成员的职业id
        '''
        return self.profession
    def getProfessionName(self):
        '''获取聊天职业名称'''
        return {0:u'新手',1:Lg().g(390),2:Lg().g(391),3:Lg().g(392),4:Lg().g(393)}.get(self.profession)
    
    def setSceneName(self,scenename):
        '''设置场景名称'''
        self.scenename = scenename
    
    def getSceneName(self):
        '''获取聊天成员所在的场景的名称'''
        return self.scenename
    
    def setRoomId(self,roomId):
        '''设置房间id'''
        self.roomId = roomId
        
    def getRoomId(self):
        '''获取房间ID'''
        return self.roomId
        
        
        
        
        

    
        
        
        
        
        
        