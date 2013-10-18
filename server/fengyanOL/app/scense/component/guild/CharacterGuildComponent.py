#coding:utf8
'''
Created on 2011-4-6

@author: sean_lan
'''
from app.scense.component.Component import Component
from app.scense.core.guild.GuildManager import GuildManager
from app.scense.utils.dbopera import dbGuild,dbVIP
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
import datetime
from app.scense.core.instance.ColonizeManage import ColonizeManage
from app.scense.core.guild.Guild import pushGuildLevelUpMessage
from app.scense.serverconfig.chatnode import chatnoderemote
from app.scense.core.language.Language import Lg
import math
#from netInterface.pushObjectNetInterface import pushCorpsApplication

ADDGUILDTASKTYPE = 105



class CharacterGuildComponet(Component):
    '''角色的行会组件'''
    
    MAXLEVEL = 10
    CREATECOIN = 10000
    
    def __init__(self,owner,id =0,name='',contribution = 0):
        '''初始化
        @param id: int 角色的行会id
        @param name: str 行会的名称
        @param contribution: int 角色的贡献度
        '''
        Component.__init__(self, owner)
        self.id = id
        self.contribution = contribution
        self.post = 0
        self.defaultDonate = 0
        self.joinTime = datetime.date(2011,11,1)
        self.lastDonate = datetime.date(2011,11,1)
        self.leaveTime = None
        self.donatetimes = 0
        self.successTimes = 0#国胜利次数
        self.failTimes = 0#国战失败次数
        self.coinBound = 0#国战金币奖励
        self.prestigeBound = 0#国战的声望战奖励
        self.guildBattleLastTime = datetime.date.today()
        
        self.wish_0_times = 0#使用四叶草许愿的次数
        self.wish_1_times = 0#使用郁金香许愿的次数
        self.wish_2_times = 0#使用蝴蝶兰许愿的次数
        self.wish_3_times = 0#使用紫罗兰许愿的次数
        self.wish_4_times = 0#使用曼陀罗许愿的次数
        self.recordDate = datetime.date.today()#进行许愿的记录时间
        
        self.initGuildInfo()
        
    def initGuildInfo(self):
        '''初始化行会信息'''
        characterId = self._owner.baseInfo.id
        data = dbGuild.getCharacterGuild(characterId)
        wishRecordData = dbGuild.getCharacterWishRecord(characterId)
        if data:
            self.setID(data['guildId'])
            self.setContribution(data['contribution'])
            self.setPost(data['post'])
            self.setLastDonate(data['lastDonate'])
            if (datetime.date.today()-data['lastDonate']).days>=1:
                self.updateDonatetimes(0)
            else:
                self.setDonatetimes(data['donatetimes'])
        else:
            self.setID(0)
            self.setContribution(0)
            self.setPost(0)
            self.setLastDonate(datetime.date(2011,11,1))
        if wishRecordData:
            self.wish_0_times = wishRecordData.get('wish_0_times',0)
            self.wish_1_times = wishRecordData.get('wish_1_times',0)
            self.wish_2_times = wishRecordData.get('wish_2_times',0)
            self.wish_3_times = wishRecordData.get('wish_3_times',0)
            self.wish_4_times = wishRecordData.get('wish_4_times',0)
            self.recordDate = wishRecordData.get('recordDate',0)
            
    def setID(self,id):
        '''设置角色行会ID'''
        self.id = id
    
    def getID(self):
        '''获取行会id'''
        return self.id
    
    def updateID(self,id):
        '''更新行会id'''
        self.id = id
        self.initGuildInfo()
        
    def setLeaveTime(self,leavetime):
        '''设置上次离开国的时间
        @param leavetime: datetime 
        '''
        self.leaveTime = leavetime
        
    def getLeaveTime(self):
        '''获取离开国的时间
        '''
        return self.leaveTime
    
    def getCanJoinTime(self):
        '''获取能够加入国的时间（小时）
        '''
        goalhour = 0
        now = datetime.datetime.now()
        if not self.leaveTime:
            goalhour = 0
        else:
            dddelta = now - self.leaveTime
            daydelta = dddelta.days
            secondsdelta = dddelta.seconds
            if daydelta>=1:
                goalhour = 0
            else:
                surplusseconds = 86400.0- secondsdelta
                goalhour = int(math.ceil(surplusseconds/3600))
        return goalhour
    
        
    def getUnionType(self):
        '''获取阵营类型'''
        guild = GuildManager().getGuildById(self.id)
        if guild:
            utype = guild.camp
            return utype
        return 0
        
    def getUnionTypeStr(self):
        '''获取行会阵营'''
        guild = GuildManager().getGuildById(self.id)
        if guild:
            utype = guild.camp
            return {1:Lg().g(336),2:Lg().g(337)}.get(utype,Lg().g(338))
        return Lg().g(338)
        
    def getGuildName(self):
        '''获取行会的名称'''
        guild = GuildManager().getGuildById(self.id)
        if guild:
            return guild.getGuildName()
        return None
    
    def setContribution(self,contribution):
        '''设置角色的行会贡献度
        @param contribution: int 角色的贡献度
        '''
        self.contribution = contribution
        
    def updateContribution(self,contribution):
        '''更新捐献值
        @param contribution: int 捐献值
        '''
        self.contribution = contribution
        dbGuild.updateCharacterGuildInfo(self._owner.baseInfo.id, {'contribution':contribution})
        dbGuild.updateGuildPost(self.id)
        
    def addContribution(self,contribution):
        '''添加捐献值'''
        self.contribution += contribution
        dbGuild.updateCharacterGuildInfo(self._owner.baseInfo.id, {'contribution':self.contribution})
        dbGuild.updateGuildPost(self.id)
    
    def setPost(self,post):
        '''设置职务'''
        self.post = post
        
    def getPost(self):
        '''获取职务'''
        guild = GuildManager().getGuildById(self.id)
        if not guild:
            return 0
        if self._owner.baseInfo.id==guild.president:
            self.post = 4
        elif self._owner.baseInfo.id in eval("["+guild.veterans+"]"):
            self.post = 3
        elif self._owner.baseInfo.id in eval("["+guild.staffOfficers+"]"):
            self.post = 2
        elif self._owner.baseInfo.id in eval("["+guild.senators+"]"):
            self.post = 1
        else:
            self.post = 0
        return self.post
    
    def setJoinTime(self,joinTime):
        '''设置加入时间
        @param joinTime: date 加入的时间
        '''
        self.joinTime = joinTime
        
    def getJoinTime(self):
        '''获取加入时间'''
        return self.joinTime
    
    def setLastDonate(self,lastDonate):
        '''设置上次捐献的时间'''
        self.lastDonate = lastDonate
        
    def getLastDonate(self):
        '''获取上次捐献的时间'''
        return self.lastDonate
    
    def updateLastDonate(self,lastDonate):
        '''更新上次领取奖励的时间'''
        self.lastDonate = lastDonate
        dbGuild.updateCharacterGuildInfo(self._owner.baseInfo.id, {'lastDonate':str(lastDonate)})
    
    def setDonatetimes(self,donatetimes):
        '''设置已经捐献的次数
        @param donatetimes: int 捐献的次数
        '''
        self.donatetimes = donatetimes
        
    def getDonatetimes(self):
        '''获取当日捐献次数
        '''
        return self.donatetimes
    
    def updateDonatetimes(self,donatetimes):
        '''更新捐献次数'''
        self.donatetimes = donatetimes
        dbGuild.updateCharacterGuildInfo(self._owner.baseInfo.id, {'donatetimes':donatetimes})
    
    def updateGuildRelation(self,prot):
        '''更新角色与行会关系
        @param prot: dict {'key':value}
        '''
        result = dbGuild.updateCharacterGuildInfo(self._owner.baseInfo.id, prot)
        return result
        
    def getGuildInfo(self):
        '''获取行会基本信息'''
        if not self.id:
            return {'result':False,'message':Lg().g(339)}
#        if self.id>0 and not GuildManager()._guilds.has_key(self.id):
#            GuildManager().addGuildById(self.id)
        guild = GuildManager().getGuildById(self.id)
        if not guild:
            return {}
        return guild.guildinfo
    
    def AppliJionGuild(self,guildId):
        '''申请加入国'''
        if self.getID():
            return {'result':False,'message':Lg().g(340)}
        surplushours = self.getCanJoinTime()
        if surplushours:
            return {'result':False,'message':Lg().g(647)%surplushours}
        if dbGuild.checkHasApply(guildId, self._owner.baseInfo.id):
            return {'result':False,'message':Lg().g(341)}
        guild = GuildManager().getGuildById(guildId)
        if self._owner.level.getLevel()<guild.levelrequired:
            return {'result':False,'message':Lg().g(342)}
        if not guild:
            return {'result':False,'message':Lg().g(343)}
        result = guild.JointGuild(self._owner.baseInfo.id)
        self._owner.quest.specialTaskHandle(ADDGUILDTASKTYPE)
        return result
    
    def UnsubscribeJionGuild(self,guildId):
        '''取消申请'''
        if not dbGuild.checkHasApply(guildId, self._owner.baseInfo.id):
            return {'result':False,'message':Lg().g(344)}
        dbGuild.delGuildApplyJoinRecord(guildId, self._owner.baseInfo.id)
        return {'result':True}
        
    def creatGuild(self,corpsName,camp):
        '''创建行会
        @param corpsName: 国的名称
        '''
        if self.getID():
            return {'result':False,'message':Lg().g(340)}
        surplushours = self.getCanJoinTime()
        if surplushours:
            return {'result':False,'message':Lg().g(647)%surplushours}
        if self._owner.finance.getCoin()<self.CREATECOIN:
            return {'result':False,'message':Lg().g(345)}
        if self._owner.level.getLevel()<12:
            return {'result':False,'message':Lg().g(346)}
        if self.id:
            return {'result':False,'message':Lg().g(347)}
        guildId = GuildManager().creatGuild(corpsName, self._owner.baseInfo.id,camp)
        if guildId == -1:
            return {'result':False,'message':Lg().g(348)}
        if guildId:
            self.updateID(guildId)
            chatnoderemote.callRemote('updateGuild',self._owner.baseInfo.id,guildId,1)#同步聊天角色中的行会
            self._owner.updatePlayerInfo()
            self._owner.quest.specialTaskHandle(ADDGUILDTASKTYPE)
            self._owner.finance.addCoin(-self.CREATECOIN)
            return {'result':True,'message':Lg().g(349)}
        return {'result':False,'message':Lg().g(350)}
    
    def leaveGuild(self):
        '''离开国'''
        guild = GuildManager().getGuildById(self.id)
        gid=self.id
        if not guild:
            return {'result':False,'message':Lg().g(79)}
        data = guild.leaveGuild(self._owner.baseInfo.id)
        if data.get('result',False):
            self.updateID(0)
            self.setLeaveTime(datetime.datetime.now())
            chatnoderemote.callRemote('updateGuild',self._owner.baseInfo.id,gid,0)#同步聊天角色中的行会
            self._owner.updatePlayerInfo()
        return data
        
    def Donate(self,technology):
        '''捐献'''
        nowdate = datetime.date.today()
        limittime = 1
        if self.getPost()>0:
            limittime = 2
        if (nowdate - self.getLastDonate()).days<1 and self.getDonatetimes()>=limittime:
            msg = Lg().g(351)
            pushOtherMessage(905,msg,[self._owner.getDynamicId()])
            return {'result':False,'message':Lg().g(351)}
        guild = GuildManager().getGuildById(self.id)
        if not guild:
            return {'result':False,'message':Lg().g(339)}
        operator = self._owner.baseInfo.id
        coinCount = self._owner.level.getLevel()*250
        if self._owner.finance.getCoin()<coinCount:
            msg = Lg().g(88)
            pushOtherMessage(905,msg,[self._owner.getDynamicId()])
            return {'result':False,'message':Lg().g(88)}
        data = guild.Donate(operator,coinCount,technology)
        if data.get('result',False):
            self.addContribution(coinCount)
            self._owner.finance.updateCoin(self._owner.finance.getCoin()-coinCount)
            if (nowdate - self.getLastDonate()).days>1:
                self.updateLastDonate(nowdate)
            self.updateDonatetimes(self.getDonatetimes()+1)
            self._owner.updatePlayerInfo()
        else:
            msg = data.get('message')
            pushOtherMessage(905,msg,[self._owner.getDynamicId()])
        return data
        
    def GetCorpsMemberOrAppliListInfo(self,getType,searchCriteria,curPage):
        '''获取获取成员列表或申请列表
        @param getType: int //0获取国成员列表1按条件查找国成员2获取申请列表3按条件查找申请成员
        @param searchCriteria: str//搜索条件
        @param curPage: int 当前页面号
        '''
        guild = GuildManager().getGuildById(self.id)
        if not guild:
            return {'result':False,'message':Lg().g(339)}
        if getType ==0:
            data = guild.getGuildMemberInfo(curPage)
        elif getType ==1:
            data = guild.searchGuildMemberInfo(searchCriteria,curPage)
        elif getType==2:
            data = guild.getApplyList(curPage)
        else:
            data = guild.searchApplyJoinGuildInfo(searchCriteria)
        data['setType'] = getType
        return {'result':True,'data':data}
        
    def AcceptOrRefuseApply(self,operType,appliId):
        '''拒绝或同意申请
        @param operType: int 操作类型 0 接受 1 拒绝
        @param appliId: int 申请ID
        '''
        guild = GuildManager().getGuildById(self.id)
        if not guild:
            return {'result':False,'message':Lg().g(339)}
        post = self.getPost()
        if post ==0:
            return {'result':False,'message':Lg().g(81)}
        if operType==0:
            data = guild.acceptGuildApply(self._owner.baseInfo.id,appliId)
            reason = {0:Lg().g(80),-1:Lg().g(81),-2:Lg().g(82),\
                      -3:Lg().g(83),-4:Lg().g(84)}
            if data ==1:
                result = {'result':True,'message':Lg().g(85)}
            else:
                result = {'result':False,'message':reason[data]}
        else:
            data = guild.refuseGuildApply(self._owner.baseInfo.id,appliId)
            reason = {0:Lg().g(80),-1:Lg().g(81),-4:Lg().g(84)}
            if data ==1:
                result = {'result':True,'message':Lg().g(85)}
            else:
                result = {'result':False,'message':reason[data]}
        return result
        
    def getGuildLevel(self):
        '''获取行会的等级'''
        guild = GuildManager().getGuildById(self.id)
        if not guild:
            return 0
        return guild.getGuildLevel()
        
    def addGuildExp(self,exp):
        '''添加国经验'''
        guild = GuildManager().getGuildById(self.id)
        if guild:
            result = guild.addExp(exp)
            if result:
                self.addContribution(exp)
        else:
            raise Exception(Lg().g(339))
        
    def pushGuildLevelUp(self):
        '''获取行会升级消息'''
        guild = GuildManager().getGuildById(self.id)
        if guild:
            lastonline = self._owner.lastOnline
            leveluptime = guild.levelupTime
            if leveluptime>lastonline:
                level = guild.level
                sendList = [self._owner.getDynamicId()]
                pushGuildLevelUpMessage(level, sendList)
                
    def ObtainFortressReward(self):
        '''获取国领地奖励
        '''
        #判断是否领取过今天的奖励
        if self.lastDonate.date()==datetime.date.today():
            return {'result':False,'msgId':658}
        guild = GuildManager().getGuildById(self.id)
        if not guild:
            return {'result':False,'msgId':659}
        coinBound = guild.level * 10000
        self._owner.finance.addCoin(coinBound)
        lastDonate = datetime.datetime.now()
        self.updateLastDonate(lastDonate)
        return {'result':True,'msgId':660}
    
    def getGuildAttrExt(self):
        '''获取国苏醒的加成'''
        info = {}
        guild = GuildManager().getGuildById(self.id)
        if guild:
            info = guild.getGuildAttrExt()
        return info
    
    def getHeroCan(self):
        '''看是否能进入英雄副本'''
        info = self.getGuildAttrExt()
        return info.get('yingxion',False)
    
    def getDifficultCan(self):
        '''看是否能进入困难副本'''
        info = self.getGuildAttrExt()
        return info.get('kunnan',False)
    
    def UseXingYun(self,usetype):
        '''
        @param usetype: int 0四叶草1郁金香2蝴蝶兰3紫罗兰4曼陀罗
        '''
        self.clearWishRecord()
        if usetype not in [0,1,2,3,4]:
            return {'result':False,'msgID':651}
        CONS_CONFIG = {0:0,1:10,2:15,3:20,4:30}
        goldcons = CONS_CONFIG.get(usetype)
        guild = GuildManager().getGuildById(self.id)
        if not guild:
            return {'result':False,'msgID':79}
        if self._owner.finance.getGold()<goldcons:
            return {'result':False,'msgID':652}
        characterId = self._owner.baseInfo.id
        viplevel = self._owner.baseInfo._viptype
        nowtimes=getattr(self,'wish_%d_times'%usetype)
        result = dbVIP.vipCertification('wish_%d_times'%usetype, viplevel,
                                        nowtimes=nowtimes)
        if not result:
            return {'result':False,'msgID':655}
        setattr(self, 'wish_%d_times'%usetype, nowtimes+1)
        dbGuild.updateCharacterWishRecord(characterId, {'wish_%d_times'%usetype:nowtimes+1})
        self._owner.finance.addGold(-goldcons)
        usename = self._owner.baseInfo.getName()
        xingyunadd = guild.UseXingYun(usetype,usename)
        self._owner.petShop.addXy(xingyunadd)
        return {'result':True}
    
    def refleshGuildBattleInfo(self):
        '''更新角色的国战信息
        '''
        thisTime = datetime.date.today()
        if self.guildBattleLastTime == thisTime:
            return
        self.coinBound = 0
        self.prestigeBound = 0
        self.successTimes = 0
        self.failTimes = 0
        self.guildBattleLastTime = thisTime
        
    def updateGuildBattle(self,mapping):
        '''更新国战的信息
        '''
        self.refleshGuildBattleInfo()
        self.coinBound += mapping.get('coinBound',0)
        self.prestigeBound += mapping.get('prestigeBound',0)
        self.successTimes += mapping.get('successTimes',0)
        self.failTimes += mapping.get('failTimes',0)
        
    def getGuildBattleInfo(self):
        '''获取国战信息
        '''
        self.refleshGuildBattleInfo()
        info = {}
        info['coinBound'] = self.coinBound
        info['prestigeBound'] = self.prestigeBound
        info['successTimes'] = self.successTimes
        info['failTimes'] = self.failTimes
        return info
    
    def updateGuildBattleInfo(self,successTimes,failTimes,coinBound,prestigeBound):
        '''更新角色的战斗信息
        '''
        self.successTimes += successTimes
        self.failTimes += failTimes
        self.coinBound += coinBound
        self.prestigeBound += prestigeBound
        
    def addSuccessTimes(self):
        '''添加战斗胜利场数
        '''
        self.successTimes += 1
        
    def addFailTimes(self):
        '''添加战斗失败场数
        '''
        self.failTimes += 1
        
    def clearWishRecord(self):
        '''重新清理许愿记录
        '''
        tihsday = datetime.date.today()
        if self.recordDate==tihsday:
            return
        characterId = self._owner.baseInfo.id
        self.recordDate=tihsday
        self.wish_0_times = 0
        self.wish_1_times = 0
        self.wish_2_times = 0
        self.wish_3_times = 0
        self.wish_4_times = 0
        props = {'recordDate':str(tihsday),'wish_0_times':0,
                 'wish_1_times':0,'wish_2_times':0,
                 'wish_3_times':0,'wish_4_times':0}
        dbGuild.updateCharacterWishRecord(characterId, props)
        
    
        
    
    
