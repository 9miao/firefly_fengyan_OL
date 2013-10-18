#coding:utf8
'''
Created on 2012-9-6
要争夺的城镇
@author: Administrator
'''
from app.scense.utils.dbopera import dbfortress
import datetime,time
from app.scense.serverconfig.chatnode import chatnoderemote 
from twisted.internet import reactor
reactor = reactor

SIGN_START_HOURS = 8
SIGN_START_MINUTE = 0
SIGN_END_HOURS = 18
SIGN_END_MINUTE = 00

WAR_START_HOURS = 19
WAR_START_MINUTE = 0

WAR_FIRST_HOURS = 19
WAR_FIRST_MINUTE = 10

WAR_SECOND_HOURS = 19
WAR_SECOND_MINUTE = 40

WAR_END_HOURS = 20
WAR_END_MINUTE = 0

def IsSignUpTime():
    sj=int(time.strftime("%H%M"))
    if sj>SIGN_START_HOURS*100+SIGN_START_MINUTE and sj<SIGN_END_HOURS*100+SIGN_END_MINUTE:
        return True
    return False

def IsWarTime():
    sj=int(time.strftime("%H%M"))
    if sj>WAR_START_HOURS*100+WAR_START_MINUTE and sj<WAR_END_HOURS*100+WAR_END_MINUTE:
        return True
    return False

def IsFirstWar():
    sj=int(time.strftime("%H%M"))
    if sj>=WAR_START_HOURS*100+WAR_START_MINUTE and sj<WAR_FIRST_HOURS*100+WAR_FIRST_MINUTE+20:
        return True
    return False

def IsSecondWar():
    sj=int(time.strftime("%H%M"))
    if sj>=WAR_FIRST_HOURS*100+WAR_FIRST_MINUTE+20 and sj<WAR_END_HOURS*100+WAR_END_MINUTE:
        return True
    return False

def IsFightTime():
    sj=int(time.strftime("%H%M"))
    if sj>=WAR_FIRST_HOURS*100+WAR_FIRST_MINUTE and sj<WAR_FIRST_HOURS*100+30:
        return True
    elif sj>=WAR_SECOND_HOURS*100+WAR_SECOND_MINUTE and sj<WAR_END_HOURS*100+WAR_END_MINUTE:
        return True
    return False


class Fortress():
    
    def __init__(self,id,name,mc):
        '''初始化城镇要塞对象
        @param id: int 城镇的ID
        @param name: str 城镇的名称
        @param kimori: int 城镇防守方的国的ID
        @param siege: int 攻城方的国的ID
        @param applyTime: datetime 发动的时间 
        @param kimoriScore: int 防守方的分数
        @param siegeScore:  int 攻城方的分数
        @param fightlog: list({}) 挑战信息字符串列表
        @param kimoriMembers: list({})领主国的参战成员列表
        @param siegeMembers: list({})挑战国的参战成员列表
        @param battleInfoList: list({})国战斗中的信息
        @param autoList: 自动参战的角色的角色ID列表
        '''
        self.id = id
        self.sceneId = 0
        self.name = ''
        self.kimori = 0
        self.siege = 0
        self.isOccupied = 0
        self.applyTime = None
        self.kimoriScore = 0
        self.siegeScore = 0
        self.fightlog = []
        self.kimoriMembers = []
        self.siegeMembers = []
        self.battleInfoList = []
        self.autoList = []
        
    def initData(self,data):
        '''初始化行会数据'''
        for keyname in self.__dict__.keys():
            if not keyname.startswith('_'):
                setattr(self,keyname,data.get(keyname))
        self.kimoriScore = 0
        self.siegeScore = 0
        self.fightlog = []
        self.kimoriMembers = []
        self.siegeMembers = []
        self.battleInfoList = []
                
        
    def ClearingFight(self):
        '''国战战后结算
        '''
        from app.scense.core.guild.GuildManager import GuildManager
        info = {}
        info['applyTime']=str(datetime.datetime.now())
        if not self.siege:
            info['kimori']=self.kimori
            winner = info['kimori']
            Loser = 0
        else:
            #守城方的分数大于攻城方的分数
            if self.kimoriScore>self.siegeScore:
                info['kimori']=self.kimori
                winner = info['kimori']
                Loser = self.siege
            else:
                self.kimori = self.siege
                info['kimori']=self.siege
                winner = info['kimori']
                Loser = self.kimori
        self.kimoriScore = 0
        self.siegeScore = 0
        self.isOccupied = 1
        info['kimoriScore'] = 0
        info['siegeScore'] = 0
        info['siege'] = 0
        info['isOccupied'] = 1
        self.addFightlog(info['kimori'], 2)
        guild1 = GuildManager().getGuildById(winner)
        guild2 = GuildManager().getGuildById(Loser)
        if guild1:
            guild1.addExp(3500)
            msg = u"%s国成功征战%s，成为其国领地！"%(guild1.get('name'),self.name)
            chatnoderemote.callRemote('pushSystemToInfo',msg)
        if guild2:
            guild1.addExp(1500)
        
        dbfortress.updateFortressInfo(self.id, {'kimori':info['kimori'],
                                                'isOccupied':1,'siege':0})
        
    def getForTressInfo(self):
        '''获取当个要塞的信息
        '''
        from app.scense.core.guild.GuildManager import GuildManager
        info = {}
        info['id'] = self.id
        kimoriguild = GuildManager().getGuildById( self.kimori)
        siegeguild = GuildManager().getGuildById( self.siege)
        if kimoriguild:#领主国的名称
            info['kimoriname'] = kimoriguild.get('name')
            info['kimoriemblem'] = kimoriguild.get('emblemLevel')
        else:
            info['kimoriname'] = u''
            info['kimoriemblem'] = 0
        if siegeguild:#挑战国的名称
            info['siegename'] = siegeguild.get('name')
            info['siegeemblem'] = siegeguild.get('emblemLevel')
        else:
            info['siegename'] = u''
            info['siegeemblem'] = 0
            
        if not IsSignUpTime():
            info['fortressstatus'] = 1#等待征战
        elif IsWarTime():
            info['fortressstatus'] = 2#征战中
        else:
            if not (kimoriguild and siegeguild):#判断征战状态
                info['fortressstatus'] = 0#可以征战
            else:
                info['fortressstatus'] = 1#等待征战
        return info
    
    def getNextFightTime(self):
        '''获取下次征战的时间
        '''
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        old=WAR_START_HOURS*3600+WAR_START_MINUTE*60 #预设时间 据0点得秒数
        young=hour*3600+minute*60+second #当前时间据0点得秒数
        
        if old>=young:
            return old-young
        else:
            return 24*3600-(young-old)
    
    def SignUp(self,guild):
        '''征战报名
        @param guild: 国的ID
        '''
        props = {}
        if self.kimori and self.siege:
            return {'result':False,'msgID':649}
        if not self.kimori:
            self.kimori = guild
            props['kimori'] = guild
        else:
            self.siege = guild
            props['siege'] = guild
        self.addFightlog(guild, 1)
        dbfortress.updateFortressInfo(self.id, props)
        return {'result':True,'msgID':650}
        
    def updateDataInDB(self):
        props = {}
        props['kimori'] = self.kimori
        props['siege'] = self.siege
        dbfortress.updateFortressInfo(self.id, props)
        
    def getRound(self):
        '''获取当前战斗回合数
        '''
        if IsSecondWar():
            return 2
        elif IsFirstWar():
            return 1
        return 0
    
    def getBattleRemainTime(self):
        '''获取战斗剩余时间
        '''
        if self.getRound()==1:
            h = WAR_FIRST_HOURS
            m = WAR_FIRST_MINUTE+20
        else:
            h = WAR_END_HOURS
            m = WAR_END_MINUTE
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        old=h*3600+m*60 #预设时间 据0点得秒数
        young=hour*3600+minute*60+second #当前时间据0点得秒数
        
        if old>=young:
            return old-young
        else:
            return 24*3600-(young-old)
        
    def cancelParticipate(self,guildId,chId,chName,chLevel):
        '''角色取消参战
        '''
        if guildId==self.kimori:
            camp = 'kimoriMembers'
            memberslist = self.kimoriMembers
        else:
            camp = 'siegeMembers'
            memberslist = self.siegeMembers
        info = {'memberId':chId,'memberName':chName,'memberLevel':chLevel}
        if not info in memberslist:
            return False
        memberslist.remove(info)
        if camp == 'kimoriMembers':
            self.kimoriMembers = memberslist
        else:
            self.siegeMembers = memberslist
        return True
    
    def Participate(self,guildId,chId,chName,chLevel):
        '''角色参战
        '''
        if not IsWarTime():
            return False
        if guildId==self.kimori:
            camp = 'kimoriMembers'
            memberslist = self.kimoriMembers
        else:
            camp = 'siegeMembers'
            memberslist = self.siegeMembers
        info = {'memberId':chId,'memberName':chName,'memberLevel':chLevel}
        if info in memberslist:
            return False
        memberslist.append(info)
        if camp == 'kimoriMembers':
            self.kimoriMembers = memberslist
        else:
            self.siegeMembers = memberslist
        return True
    
    def addFightlog(self,guildId,logtype):
        '''添加战斗日志
        @param guildId: 国的ID
        @param logtype: 日志类型  1 申请   2 占领
        '''
        from app.scense.core.guild.GuildManager import GuildManager
        guild = GuildManager().getGuildById(guildId)
        if not guild:
            return
        gname = guild.get('name')
        thisTime = str(datetime.datetime.now())
        scenename = self.get('name')
        if logtype==1:
            logstr = u'%s\n%s国申请征战%s成功！将于次日19:00:00开始国战。'%(thisTime,gname,scenename)
        else:
            logstr = u'%s\n%s国成功占领%s'%(thisTime,gname,scenename)
        loglist = self.get('fightlog')
        loglist.append(logstr)
        
        
    def addBattleInfo(self,roleId1,roleName1,roleId2,roleName2,sucObCoin):
        '''添加国战斗信息
        '''
        info = {'roleId1':roleId1,'roleName1':roleName1,'roleId2':roleId2,
                'roleName2':roleName2,'sucObCoin':sucObCoin}
        battleInfoList = self.battleInfoList
        battleInfoList.append(info)
        props = {'battleInfoList':battleInfoList}
        self.battleInfoList = battleInfoList

        
        
    def battleResultHandle(self,battleResult):
        '''每场战斗的处理
        '''
        if battleResult==1:#防守方胜利
            self.kimoriScore += 10
            self.incr('kimoriScore', 10)
        else:
            self.siegeScore += 10
            self.incr('siegeScore', 10)
        
        
    def MatchRival(self):
        '''匹配对手
        '''
        kimoriMembers = self.kimoriMembers
        siegeMembers = self.siegeMembers
        info = {}
        if not (kimoriMembers and siegeMembers):
            return info
        actor = kimoriMembers[0]
        defendslist = [member for member in siegeMembers if
                        abs(member['memberLevel']-actor['memberLevel'])<5]
        if defendslist:
            defender = defendslist[0]
        else:
            defender = siegeMembers[0]
        kimoriMembers.remove(actor)
        siegeMembers.remove(defender)
        ##{'memberId':chId,'memberName':chName,'memberLevel':chLevel}
        #自动参战的处理
        if actor.get('memberId') in self.get('autoList'):
            kimoriMembers.append(actor)
        if defender.get('memberId') in self.get('autoList'):
            siegeMembers.append(actor)
        self.kimoriMembers = kimoriMembers
        self.siegeMembers = siegeMembers
        info['actor'] = actor
        info['defender'] = defender
        return info
    
    def doFight(self):
        '''开始国战
        '''
        if not IsFightTime():
            thisRound = self.getRound()
            if thisRound==0:
                self.ClearingFight()
            return
        RivalInfo = self.MatchRival()
        if not RivalInfo:
            reactor.callLater(30,self.doFight)
            return
        
        from app.scense.core.character.PlayerCharacter import PlayerCharacter
        from app.scense.core.fight.fight_new import Fight
        from app.scense.core.fight.battleSide import BattleSide
        from app.scense.netInterface import pushObjectNetInterface
#        from app.scense.serverconfig.publicnode import publicnoderemote
        
        actor = RivalInfo['actor']
        defender = RivalInfo['defender']
        player = PlayerCharacter(actor['memberId'])
        player.attribute.Restoration()#角色满状态
        toplayer = PlayerCharacter(defender['memberId'])
        toplayer.attribute.Restoration()#角色满状态
        
        challengers = BattleSide([player])
        defenders = BattleSide([toplayer])
        data = Fight(challengers, defenders, 550)
        data.DoFight()
        battleResult = data.battleResult
        pplist = [actor['memberId'],defender['memberId']]
        if battleResult==1:
            pId = player.baseInfo.getId()
            pname = player.baseInfo.getName()
            pcoin = player.level.getLevel()*100
            pweiwang = 2
            tId = toplayer.baseInfo.getId()
            tname = toplayer.baseInfo.getName()
            tcoin = 1000
            tweiwang = 0
        else:
            pId = toplayer.baseInfo.getId()
            pname = toplayer.baseInfo.getName()
            pcoin = toplayer.level.getLevel()*100
            pweiwang = 2
            tId = player.baseInfo.getId()
            tname = player.baseInfo.getName()
            tcoin = 1000
            tweiwang = 0
        #战后处理
        self.battleResultHandle(battleResult)
        #战斗奖励发放
        gm1 = 'player.finance.addCoin(%d);player.finance.addPrestige(%d);\
        player.guild.updateGuildBattleInfo(%d,%d,%d,%d)'%(pcoin,pweiwang,1,0,pcoin,pweiwang)
        gm2 = 'player.finance.addCoin(%d);\
        player.guild.updateGuildBattleInfo(%d,%d,%d,%d)'%(tcoin,0,1,tcoin,0)
#        publicnoderemote.callRemote("updateplayerInfo",pId,gm1)
#        publicnoderemote.callRemote("updateplayerInfo",tId,gm2)
        #添加国战斗信息
        self.addBattleInfo(pId, pname, tId, tname, pcoin)
        #战斗消息推送处理
        msg = u'%s: %d金币   %d威望  \n%s: %d金币  %d威望'%(pname,pcoin,pweiwang,tname,tcoin,tweiwang)
        zy = self.sceneId
        pushObjectNetInterface.getzudui_4308(data, pplist, msg,zy)
        reactor.callLater(30,self.doFight)
        
    def autoJoin(self,characterId):
        '''自动加入战斗
        '''
        autoList = self.get('autoList')
        result = False
        if characterId not in autoList:
            autoList.append(characterId)
            result = True
        self.autoList = autoList
        return result
        
    def cancelAutoJoin(self,characterId):
        '''取消自动加入战斗
        '''
        autoList = self.get('autoList')
        result = False
        if characterId in autoList:
            autoList.remove(characterId)
            result = True
        self.autoList = autoList
        return result
        
        
        
        
    
    
        
            
    