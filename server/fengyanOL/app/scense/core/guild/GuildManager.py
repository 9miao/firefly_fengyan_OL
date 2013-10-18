#coding:utf8
'''
Created on 2011-9-17
行会管理器
@author: lan
'''
from app.scense.core.singleton import Singleton
from app.scense.core.guild.Guild import Guild
from app.scense.utils.dbopera import dbGuild
import math

class GuildManager(object):
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化行会管理器'''
        self._guilds = {}
        self.guildIdList = []
        self.initGuildManager()
        
    def initGuildManager(self):
        '''初始化国管理器'''
        allsysguildInfo = dbGuild.getAllSysGuildInfo()
        allguildInfo = dbGuild.getAllGuildInfo()
        for guildinfo in allsysguildInfo+allguildInfo:
            self.addGuildByInfo(guildinfo)
            self.guildIdList.append(guildinfo['id'])
        
    def addGuildByInfo(self,guildinfo):
        '''根据id添加一个行会到管理器
        @param guildID: int 行会的id
        '''
        guildId = guildinfo['id']
        if self._guilds.has_key(guildId):
            raise Exception("系统记录冲突")
        guild = Guild('guild%d'%guildId)
        guild.id = guildId
        guild.initGuildData(guildinfo)
        self._guilds[guildId] = guild
        
    def initAllGuild(self):
        '''更新所有的国信息
        '''
        guildlist = self.guildIdList
        for guildId in guildlist:
            guild = Guild('guild%d'%guildId)
            guild.id = guild
            self._guilds[guildId] = guild
        
    def getGuildById(self,guildId):
        '''根据ID获取行会实例'''
        guild = self._guilds.get(guildId)
        if not guild:
            guild = Guild('guild%d'%guildId)
            guild.id = guildId
            if  not guild.get('name'):
                guild = None
            else:
                self._guilds[guildId] = guild
        return guild
    
    def getGuildListInfo(self,characterId,getType,curPage,searchCriteria):
        '''获取国列表
        @param characterId: int 角色的id
        @param getType: int 获取类型  0获取所有1搜索
        @param curPage: int 当前页数
        @param searchCriteria: str 搜索条件
        '''
        limit = 5
        data = {}
        guildlist =self.guildIdList
        data['curPage'] = curPage
        if getType ==0:
            data['maxPage'] = int(math.ceil(len(guildlist)/float(limit)))
            if data['maxPage']<1:
                data['maxPage']=1
            data['corpsInfo'] = dbGuild.getGuildInfoList(characterId, curPage, limit)
            for corpsInfo in data['corpsInfo']:
                guildInfo = self.getGuildById(corpsInfo['id']).guildinfo
                corpsInfo['corpsImg'] = guildInfo['emblemLevel']
                corpsInfo['level'] = guildInfo['level']
                corpsInfo['memberCount'] = corpsInfo['memberCount'] + ((guildInfo['emblemLevel']-1)*30)
                corpsInfo['bugle'] = guildInfo['bugle']
                corpsInfo['nickname'] = guildInfo['presidentname']
                corpsInfo['levelrequired'] = guildInfo['levelrequired']
                
        else:
            data['corpsInfo'] = dbGuild.searchGuildByName(characterId, searchCriteria,curPage,limit)
            data['maxPage'] = int(math.ceil(len(data['corpsInfo'])/float(limit)))
            if data['maxPage']<1:
                data['maxPage']=1
            for corpsInfo in data['corpsInfo']:
                guildInfo = self.getGuildById(corpsInfo['id']).guildinfo
                corpsInfo['corpsImg'] = guildInfo['emblemLevel']
                corpsInfo['level'] = guildInfo['level']
                corpsInfo['memberCount'] = corpsInfo['memberCount'] + ((guildInfo['emblemLevel']-1)*30)
                corpsInfo['bugle'] = guildInfo['bugle']
                corpsInfo['nickname'] = guildInfo['presidentname']
                corpsInfo['levelrequired'] = guildInfo['levelrequired']
        return data
        
    def creatGuild(self,guildName,president,camp):
        '''创建行会
        @param guildName: str 行会的名称
        @param president: int 会长的id
        '''
        if dbGuild.checkHasGuildByName(guildName):
            return -1
        gid = dbGuild.creatGuild(guildName, president,camp)
        if not gid:
            return 0
        dbGuild.insertCharacterGuildInfo(president, gid, post=4)
        guild = Guild('guild%d'%gid)
        guild.id = gid
        guildinfo = dbGuild.getGuildInfoById(gid)
        guild.initGuildData(guildinfo)
        nowguildlist = self.guildIdList
        nowguildlist.append(gid)
        self.self.guildIdList=nowguildlist
        self._guilds[gid] = guild
        return gid
        
    
    
    
    
    