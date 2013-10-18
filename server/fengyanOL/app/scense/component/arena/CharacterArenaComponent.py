#coding:utf8
'''
Created on 2012-7-1
角色的竞技场信息
@author: Administrator
'''
from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbarena
import datetime,math
from app.scense.utils.dbopera.dbVIP import vipCertification
from app.scense.serverconfig.node import pushObjectByCharacterId,pushObjectToAll

from app.scense.protoFile.arena import JingJiCD3701_pb2,JingJiRankInfo3702_pb2
from app.scense.core.language.Language import Lg


def psuhCharacterArenaCD(CD,CharacterId):
    '''推送角色竞技场CD'''
    response = JingJiCD3701_pb2.JingJiCDResponse()
    response.cdTime = CD
    msg = response.SerializeToString()
    pushObjectByCharacterId(3701, msg, [CharacterId])
    
def pushArenaGonggao(msg):
    '''推送竞技场公告
    '''
    response = JingJiRankInfo3702_pb2.JingJiRankInfoResponse()
    response.anStr = msg
    msg = response.SerializeToString()
    pushObjectToAll(3702, msg)
    

def getTimeStrByTimedelta(lasttime):
    '''根据时间差获取时间字符创
    '''
    delta = datetime.datetime.now()-lasttime
    deltasecond = delta.days*86400+delta.seconds
    deltastr = ''
    if deltasecond<60:
        deltastr = Lg().g(226)
    elif 60<= deltasecond <3600:
        mins = deltasecond/60
        deltastr = Lg().g(227)%mins
    elif 3600<=deltasecond<86400:
        hour = deltasecond/3600
        deltastr = Lg().g(228)%hour
    else:
        days = delta.days
        deltastr = Lg().g(229)%days
    return deltastr

def getRankingCoinBound(rank):
    '''获取排名奖励
    '''
    coinbound = 0
    if rank==1:
        coinbound = 600000
    elif rank==2:
        coinbound = 480000
    elif rank==3:
        coinbound = 430000
    elif rank==4:
        coinbound = 380000
    elif rank==5:
        coinbound = 330000
    elif rank==6:
        coinbound = 280000
    elif rank==7:
        coinbound = 230000
    elif rank==8:
        coinbound = 180000
    elif rank==9:
        coinbound = 130000
    elif rank==10:
        coinbound = 100000
    elif 10<rank<=120:
        coinbound = 100000-((int(rank/10)*10)*200)-rank*500
    else:
        coinbound = 10000
    return coinbound


class CharacterAreanaComponent(Component):
    '''角色竞技场信息    
    @param score: int 竞技场积分
    '''
    CD = 600
    
    def __init__(self,owner):
        '''初始化
        '''
        Component.__init__(self, owner)
        self.score = 0
        self.liansheng = 0
        self.lastresult = 0
        self.lasttime = None
        self.ranking = 0
        self.surplustimes = 15
        self.buytimes = 0
        self.receive = 0
        self.recorddate = None
        self.initArenaData()
        
    def initArenaData(self):
        '''初始化竞技场信息
        '''
        characterId = self._owner.baseInfo.id
        data = dbarena.getCharacterArenaInfo(characterId)
        self.score = data['score']
        self.liansheng = data['liansheng']
        self.lastresult = data['lastresult']
        self.lasttime = data['lasttime']
        self.ranking = data['ranking']
        self.surplustimes = data['surplustimes']
        self.buytimes = data['buytimes']
        self.recorddate = data['recorddate']
        self.receive = data['receive']
        if self.recorddate != datetime.date.today():#如果不是当天的数据则重置
            self.resetArenaData()
        
    def pushIcon(self):
        '''推送领奖图标'''
        if self._owner.icon.iconlist.has_key(self._owner.icon.ARENA_AWARD):
            return
        level = self._owner.level.getLevel()
        if not self.receive and level>=15:
            self._owner.icon.addIcon(self._owner.icon.ARENA_AWARD,0,state = 0)
            
    def resetArenaData(self):
        '''重置竞技场信息
        '''
        characterId = self._owner.baseInfo.id
        self.liansheng = 0
        self.lastresult = 0
        self.surplustimes = 15
        self.buytimes = 0
        self.receive = 0
        self.recorddate = datetime.date.today()
        props = {'recorddate':str(self.recorddate),'liansheng':0,
                'lastresult':0,'surplustimes':15,'buytimes':0,'receive':0}
        dbarena.updateCharacterArenaInfo(characterId, props)
        
    def getArenaInfo(self):
        '''获取角色竞技场信息
        '''
        self.pushIcon()
        self.getRanking()
        info = {}
        info['name'] = self._owner.baseInfo.getName()
        info['jifen'] = self.score
        info['weiwang'] = self._owner.finance.getPrestige()
        info['paiming'] = self.ranking
        info['liansheng'] = self.liansheng
        info['surplustimes'] = self.surplustimes
        info['addCount'] = self.buytimes
        info['reqCoin'] = (self.buytimes+1)*10
        seconds = self.getReceiveTime()
        coinbound = getRankingCoinBound(self.ranking)
        info['jiangli'] = Lg().g(230)%(self.ranking,coinbound)
        info['obtainTime'] = seconds
        return info
    
    def pushArenaCD(self):
        '''推送竞技场CD
        '''
        CharacterId = self._owner.baseInfo.id
        CD = self.getCD()
        psuhCharacterArenaCD(CD, CharacterId)
    
    def getRanking(self):
        '''获取自己的排名
        '''
        characterId = self._owner.baseInfo.id
        self.ranking = dbarena.getCharacterArenaRank(characterId)
        return self.ranking
    
    def getRivalList(self):
        '''获取对手列表
        '''
        ranking = self.ranking
        ranklist = []
        if ranking<=10:
            targetranking = ranking-1
            if targetranking>0:
                ranklist.append(targetranking)
        else:
            while ranking>10 and len(ranklist)<5:
                ranking -= 5
                if ranking>0:
                    ranklist.append(ranking)
        for p in range(0,5-len(ranklist)):
            targetranking = self.ranking+5*(1+p)
            ranklist.append(targetranking)
        data = dbarena.getCharacterRivalList(ranklist)
        return data
    
    def getBattleRecordList(self):
        '''获取战报信息
        '''
        characterId = self._owner.baseInfo.id
        recorddata = dbarena.getCharacterBattleLog(characterId)
        recordLoglist = []
        for record in recorddata:
            logmsg = []
            logmsg.append(getTimeStrByTimedelta(record['recordtime']))
            fname = record['tiaozhanname']
            tname = record['yingzhanname']
            try:
                fname = fname.decode('utf8')
                tname = tname.decode('utf8')
            except:
                pass
            if record['tiaozhan']==characterId:
                msg =Lg().g(231)+ u"<a href = 'event:%d?%s'><u><font color = '#00FF00'>%s</font></u></a> "%\
                (record['yingzhan'],tname,tname)
                logmsg.append(msg)
                if record['success']:
                    msg = Lg().g(232)
                else:
                    msg = Lg().g(233)
                logmsg.append(msg)
            else:
                msg = Lg().g(234)%(record['tiaozhan'],fname,fname)
                logmsg.append(msg)
                if record['success']:
                    msg = Lg().g(235)
                else:
                    msg = Lg().g(236)
                logmsg.append(msg)
                
            rankingChange = record['rankingChange']
            if record['rankingChange']:
                logmsg.append(Lg().g(237)%rankingChange)
            else:
                logmsg.append(Lg().g(238))
            logstr = ''.join(logmsg)
            recordLoglist.append(logstr)
        return recordLoglist
        
    def getArenaAllInfo(self):
        '''获取竞技场所有的信息
        '''
        if self.recorddate != datetime.date.today():#如果不是当天的数据则重置
            self.resetArenaData()
        arenaInfo = self.getArenaInfo()
        drList = self.getRivalList()
        battleInfoList = self.getBattleRecordList()
        arenaInfo['drList'] = drList
        arenaInfo['battleInfoList'] = battleInfoList
        return arenaInfo
        
    def getCD(self):
        '''获取战斗CD
        '''
        nowtime = datetime.datetime.now()
        delta = nowtime - self.lasttime
        deltasecond = delta.days*86400+delta.seconds
        if deltasecond>self.CD:
            return 0
        else:
            return self.CD - deltasecond
    
    def clearCD(self):
        '''清除竞技场冷却时间
        '''
        CD = self.getCD()
        if CD<0:
            return {'result':False,'message':Lg().g(239)}
        reqgold = int(math.ceil(CD*1.0/60))
        if self._owner.finance.getGold()<reqgold:
            return {'result':False,'message':Lg().g(190)}
        self.lasttime = datetime.datetime(2012,6,20,12)
        self._owner.finance.consGold(reqgold,3)#竞技场冷却时间
        characterId = self._owner.baseInfo.id
        props = {'lasttime':str(self.lasttime)}
        dbarena.updateCharacterArenaInfo(characterId, props)
        self.pushArenaCD()
        return {'result':True}
    
    def AddSurplustimes(self):
        '''添加竞技场剩余次数'''
        viplevel = self._owner.baseInfo._viptype
        nowtimes = self.buytimes
        if not vipCertification('arenatimes', viplevel,nowtimes = nowtimes):
            return {'result':False,'message':Lg().g(217)}
        reqGold = (self.buytimes+1)*10
        if reqGold>self._owner.finance.getGold():
            return {'result':False,'message':Lg().g(190)}
        self._owner.finance.consGold(reqGold,12)#添加剩余次数
        self.buytimes +=1
        self.surplustimes +=1
        characterId = self._owner.baseInfo.id
        props = {'buytimes':1,'surplustimes':self.surplustimes}
        dbarena.updateCharacterArenaInfo(characterId, props)
        reqCoin = (self.buytimes+1)*10
        info = {'bCount':self.surplustimes,'addCount':self.buytimes,'reqCoin':reqCoin}
        return {'result':True,'data':info}
    
    
    def afterFight(self,result,toplayer):
        '''战斗结果处理
        '''
        self._owner.finance.addCoin(500,state=0)
        self._owner.finance.addPrestige(2,state=0)
        self.surplustimes -=1
        if result==1:#战斗胜利
            self.liansheng +=1
            characterId = self._owner.baseInfo.id
            tocharacterId = toplayer.baseInfo.id
            fname = self._owner.baseInfo.getName()
            tname = toplayer.baseInfo.getName()
            success = 1
            rankingChange = toplayer.arena.getRanking()
            if rankingChange<self.ranking:#战胜比自己排名高的人时互换排名
                dbarena.updateCharacterArenaInfo(characterId, {'ranking':rankingChange,
                                                           'surplustimes':self.surplustimes,
                                                           'liansheng':self.liansheng})
                dbarena.updateCharacterArenaInfo(tocharacterId, {'ranking':self.ranking})
            else:
                rankingChange = 0
                dbarena.updateCharacterArenaInfo(characterId, {'surplustimes':self.surplustimes,
                                                           'liansheng':self.liansheng})
            dbarena.insertBattleLog(characterId, tocharacterId,\
                                     fname, tname, success, rankingChange)
            msg = ''
            if self.liansheng==10:
                msg = Lg().g(240)%(fname)
            if rankingChange==1:
                msg = Lg().g(241)%(fname)
            if msg:
                self.pushGonggao(msg)
            self._owner.msgbox.putFightMsg(Lg().g(242))
        else:
            self.liansheng +=0
            characterId = self._owner.baseInfo.id
            tocharacterId = toplayer.baseInfo.id
            fname = self._owner.baseInfo.getName()
            tname = toplayer.baseInfo.getName()
            success = 0
            rankingChange = 0
            dbarena.updateCharacterArenaInfo(characterId, {'surplustimes':self.surplustimes,
                                                           'liansheng':self.liansheng})
            dbarena.insertBattleLog(characterId, tocharacterId,\
                                     fname, tname, success, rankingChange)
            self._owner.msgbox.putFightMsg(Lg().g(243))
            
    def pushGonggao(self,msg):
        '''推送竞技场公告
        '''
        pushArenaGonggao(msg)
        
        
    def doFight(self,characterId):
        '''执行战斗
        @param characterId: int 对手的ID
        '''
        if self.getCD()>0:
            return {'result':False,'message':Lg().g(244)}
        if self.surplustimes<=0:
            return {'result':False,'message':Lg().g(245)}
        from app.scense.core.character.PlayerCharacter import PlayerCharacter
        from app.scense.core.PlayersManager import PlayersManager
        from app.scense.core.fight.fight_new import DoFight
        player = PlayersManager().getPlayerByID(characterId)
        if not player:
            player = PlayerCharacter(characterId)
        nowHp = self._owner.attribute.getHp()
        player.attribute.Restoration()
        self._owner.attribute.Restoration()
        fig = DoFight([self._owner], [player], 550)
        self.afterFight(fig.battleResult,player)
        self._owner.attribute.setHp(nowHp)
        self.lasttime = datetime.datetime.now()#更新最后战斗的时间
        pid = self._owner.baseInfo.id
        props = {'lasttime':str(self.lasttime)}
        dbarena.updateCharacterArenaInfo(pid, props)
        self.pushArenaCD()
        self._owner.quest.specialTaskHandle(122)#成功后的特殊任务通知
        data = {'message':Lg().g(246),'fight':fig}
        bound = {'coin':500,'popularity':2,'name':self._owner.baseInfo.getName()}
        return {'result':True,'data':data,'bound':bound}
    
    def getReceiveTime(self):
        '''获取领取奖励剩余时间
        '''
        deltaseconds = 0
        if self.receive:
            nowtime = datetime.datetime.now()
            tomorrow = datetime.date.today()+datetime.timedelta(days = 1)
            lastReceivetime = datetime.datetime(tomorrow.year,tomorrow.month,tomorrow.day)
            deltatime = lastReceivetime - nowtime
            deltaseconds = deltatime.seconds
        return deltaseconds
            
    def getArenaBound(self):
        '''获取竞技场的奖励
        '''
        if self.receive:
            return 0
        self.getRanking()
        coinbound = getRankingCoinBound(self.ranking)
        return coinbound
    
    def receiveAward(self):
        '''获取竞技场奖励
        '''
        if self.receive:#如果已经领取过，则不再领取
            return False
        self.getRanking()
        coinbound = getRankingCoinBound(self.ranking)
        self._owner.finance.addCoin(coinbound)
        self.receive = 1
        self._owner.icon.removeIcon(self._owner.icon.ARENA_AWARD)
        characterId = self._owner.baseInfo.id
        props = {'receive':self.receive}
        dbarena.updateCharacterArenaInfo(characterId, props)
        return True
            
        
