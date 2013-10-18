#coding:utf8
'''
Created on 2011-8-15

@author: lan
'''
from app.scense.component.Component import Component

from app.scense.utils.dbopera import dbAfk
from app.scense.utils.dbopera.dbVIP import vipCertification
from app.scense.utils.dbopera import dbVIP
import datetime
from app.scense.netInterface.pushObjectNetInterface import pushCorpsApplication,pushOtherMessageByCharacterId

from twisted.internet import reactor
from app.scense.core.language.Language import Lg

reactor = reactor

MININGTYPE = {1:8,
              2:12,
              3:16,
              4:24}

MININGMODE = {1:{'pre':1,'level':1,'cons':0},
              2:{'pre':1.2,'level':2,'cons':2},
              3:{'pre':1.5,'level':3,'cons':20},
              4:{'pre':2,'level':5,'cons':50}}

TRAINTYPE = {1:8,
             2:12,
             3:16,
             4:24}

TRAINMODE = {1:{'pre':1,'level':1,'cons':0},
              2:{'pre':1.2,'level':2,'cons':2},
              3:{'pre':1.5,'level':3,'cons':20},
              4:{'pre':2,'level':5,'cons':50}}

ENERGY_TIME = 1800#在线精力奖励间隔时间
ENERGY_ADD = 5#在线精力奖励增量

#def sendTimerSingal(timeout,pid,signaltype):
#    '''发送定时器的消息让publicserver 执行定时器，当时间到达后将消息发送回来
#    @param pid: int 角色的id
#    @param signaltype: int 定时消息类型 1挖矿 2训练
#    '''
#    publicnoderemote.callRemote('TimerSingalRec',timeout,pid,signaltype)
    
def minusDatetimeForSecond(dtime1,dtime2):
    '''求两个日期时间的秒差'''
    deltas = dtime1 - dtime2
    days = deltas.days
    seconds = deltas.seconds
    return 86400*days + seconds

class CharacterAFKComponent(Component):
    '''角色点石成金，军营挂机'''
    
    def __init__(self,owner):
        '''初始化
        @param miningstart: datetime 开始挖矿的时间
        @param turncointimes: int 换取金币的次数
        @param miningtype: int 挖矿的类型
        @param trainstart: datetime 开始训练的时间
        @param traintype: int 训练的类型
        @param trainId: int 训练列表  其中0表示角色的id
        @param turnexptimes: int 换取经验的次数
        @param miningmode: int 挖掘模式
        @param trainmode: int 挂机模式
        @param turnenergytimes: int 获取体力的次数
        @param meditationtime: datetime 开始冥想的时间
        '''
        Component.__init__(self, owner)
        self.miningstart = None
        self.turncointimes = 0
        self.miningtype = 1
        self.miningmode = 1
        self.ismining = False
        self.trainstart = None
        self.traintype = 1
        self.trainId = 0
        self.trainmode = 1
        self.istrain = False
        self.turnexptimes = 0
        self.turnenergytimes = 0
        self.meditationtime = None
        self.finishedMining = 0
        self.finishedTrain = 0
        self.miningtimer = None#挖掘的定时器
        self.traintimer = None#训练的定时器
        self.guajitimer = None#挂机的定时器
        self.goalexp = 0
        self.energytimer = None
        self.energystarttime = None
        
    def startMiningTimer(self):
        '''开启挖掘定时器
        '''
        if self.ismining:
            miningType = self.miningtype
            miningtime = MININGTYPE.get(miningType)*3600
            nowday = datetime.datetime.now()
            miningstart = self.miningstart
            seconddelta = miningtime - minusDatetimeForSecond(nowday, miningstart)
            self.miningtimer = reactor.callLater(seconddelta,self.rewardMiningBound)
            
    def startTrainTimer(self):
        '''开启挖掘定时器
        '''
        if self.istrain:
            trainType = self.traintype
            nowday = datetime.datetime.now()
            traintime = TRAINTYPE.get(trainType)*3600
            trainstart = self.trainstart
            seconddelta2 = traintime - minusDatetimeForSecond(nowday, trainstart)
            seconddelta2 = max(seconddelta2,0) 
            self.traintimer = reactor.callLater(seconddelta2,self.getTrainBound)
        
    def stopMiningTimer(self):
        '''停止挖掘定时器
        '''
        if self.miningtimer:
            try:
                self.miningtimer.cancel()
            except Exception,e:
                print e
        self.miningtimer = None
            
    def stopTrainTimer(self):
        '''停止挖掘定时器
        '''
        if self.traintimer:
            try:
                self.traintimer.cancel()
            except Exception,e:
                print e
        self.traintimer = None
            
    def stopGuaJiTimer(self):
        '''停止挂机的定时器
        '''
        if self.guajitimer:
            try:
                self.guajitimer.cancel()
            except Exception,e:
                print e
            self.guajitimer = None
        self.goalexp = 0
        self._owner.baseInfo.setStatus(1)
        
        
    def initAFKData(self):
        '''初始化数据内容'''
        characterId = self._owner.baseInfo.id
        miningdata = dbAfk.getCharacterMining(characterId)
        traindata = dbAfk.getCharacterTrainData(characterId)
        turnrecord = dbAfk.getCharacterTurnRecord(characterId)
        nowday = datetime.datetime.now()
        if not turnrecord:
            dbAfk.InsertCharacterTurnRecord(characterId)
        else:
            turncoindate = turnrecord[2]
            if nowday.date() == turncoindate.date():
                self.turncointimes = turnrecord[1]
            turnexpdate = turnrecord[4]
            if nowday.date() == turnexpdate.date():
                self.turnexptimes = turnrecord[3]
            turnengpdate = turnrecord[6]
            if nowday.date() == turnengpdate.date():
                self.turnenergytimes = turnrecord[5]
            finishedWJdate = turnrecord[8]
            if nowday.date() == finishedWJdate.date():
                self.finishedMining = turnrecord[9]
            finishedTRdate = turnrecord[10]
            if nowday.date() == finishedTRdate.date():
                self.finishedTrain = turnrecord[11]
            self._owner.award.setViplevellibao(turnrecord[7],state=0)
        if miningdata:
            miningstart = miningdata[3]
            miningType = miningdata[2]
            miningmode = miningdata[4]
            sptime = MININGTYPE.get(miningType)
            miningtime = MININGTYPE.get(miningType)*3600
            seconddelta = miningtime - minusDatetimeForSecond(nowday, miningstart)
            if seconddelta< 0:
                miningpre = MININGMODE.get(miningmode)['pre']
                coinBound = int(self._owner.level.getLevel()*300*sptime*miningpre)
                self._owner.finance.addCoin(coinBound,state =0)
                dbAfk.delCharacterMining(characterId)
            else:
                self.miningstart = miningstart
                self.miningtype = miningType
                self.miningmode = miningmode
                self.ismining = True
                self.startMiningTimer()
#                sendTimerSingal(seconddelta,characterId, 1)
        if traindata:
            trainstart = traindata[2]
            trainType = traindata[3]
            trainId = traindata[1]
            trainmode = traindata[4]
            sptime = TRAINTYPE.get(trainType)
            traintime = TRAINTYPE.get(trainType)*3600
            seconddelta2 = traintime - minusDatetimeForSecond(nowday, trainstart)
            if seconddelta2< 0:
                trainpre = TRAINMODE.get(trainmode)['pre']
                expBound = int(self._owner.level.getLevel()*300*sptime*trainpre)
                if trainId == 0:
                    self._owner.level.addExp(expBound,state = 0)
                else:
                    pet = self._owner.pet.getPet(trainId)
                    if pet:
                        pet.level.addExp(expBound)
                dbAfk.delCharacterTrain(characterId)
            else:
                self.trainstart = trainstart
                self.traintype = trainType
                self.trainId = trainId
                self.trainmode = trainmode
                self.istrain = True
                self.startTrainTimer()
        self.startEnergyTimer()
                
    def getMiningBound(self):
        '''获取挖矿的奖励'''
        sptime = MININGTYPE.get(self.miningtype)
        miningper = MININGMODE.get(self.miningmode)['pre']
        coinBound = int(self._owner.level.getLevel()*300*sptime*miningper)
        return coinBound
        
    def rewardMiningBound(self):
        '''获取挖掘奖励'''
        characterId = self._owner.baseInfo.id
        coinBound = self.getMiningBound()
        self._owner.finance.addCoin(coinBound)
        dbAfk.delCharacterMining(characterId)
        self.miningstart = None
        self.miningtype = 0
        self.miningmode = 1
        self.ismining = False
        return coinBound
        
    def getTrainBound(self):
        '''获取训练的奖励'''
        sptime = TRAINTYPE.get(self.traintype)
        trainper = TRAINMODE.get(self.trainmode)['pre']
        try:
            expBound = int(self._owner.level.getLevel()*600*sptime*trainper)
        except Exception:
            expBound = 0
        return expBound
        
    def rewardTrainBound(self):
        '''获取训练的奖励'''
        characterId = self._owner.baseInfo.id
        expBound = self.getTrainBound()
        if self.trainId == 0:
            self._owner.level.addExp(expBound)
        else:
            self._owner.pet.getPet(self.trainId).level.addExp(expBound)
        dbAfk.delCharacterTrain(characterId)
        self.trainId = []
        self.trainstart = None
        self.traintype = 0
        self.trainmode = 1
        self.istrain = False
        return expBound
                
    def rectimersignal(self,signaltype):
        '''定时信号接受的处理
        @param signaltype: int 信号的类型
        '''
        if signaltype==1:
            self.rewardMiningBound()
        elif signaltype==2:
            self.rewardTrainBound()
            
    def doMining(self,miningtype):
        '''执行挖矿
        @param miningtype: int 挖矿的类型
        '''
        if self.ismining:
            return {'result':False,'message':Lg().g(209)}
        characterId = self._owner.baseInfo.id
        self.ismining = True
        self.miningtype = miningtype
        self.miningstart = datetime.datetime.now()
        dbAfk.InsertCharacterMining(characterId, miningtype, str(self.miningstart))
        self.startMiningTimer()
        self._owner.daily.noticeDaily(20,0,1)#通知每日目标
        self._owner.schedule.noticeSchedule(8)#成功后的日程目标通知
        self._owner.quest.specialTaskHandle(119)#成功后的特殊任务通知
        return {'result':True}
    
    def updateMiningMode(self,mmode):
        '''更改加强模式'''
        if not self.ismining:
            return {'result':False,'message':Lg().g(210)}
        if self.miningmode<=mmode:
            return {'result':False,'message':Lg().g(211)}
        goldcons = MININGMODE.get(mmode)['cons']
        nowgold = self._owner.finance.getGold()
        golddelta = nowgold - goldcons
        if golddelta < 0:
            return {'result':False,'message':Lg().g(190)}
        characterId = self._owner.baseInfo.id
        self._owner.finance.updateGold(golddelta)
        self.miningmode = mmode
        props = {'miningmode':mmode}
        dbAfk.updateCharacterMining(characterId, props)
        return {'result':True}
        
    def doTrain(self,trainType,ttype,memberId):
        '''开始训练'''
        if self.istrain:
            return {'result':False,'message':Lg().g(212)}
        characterId = self._owner.baseInfo.id
        self.istrain = True
        if ttype == 0:
            self.trainId = 0
        else:
            pet = self._owner.pet.getPet(memberId)
            if not pet:
                return {'result':False,'message':Lg().g(159)}
            self.trainId = memberId
        self.traintype = trainType
        self.trainstart = datetime.datetime.now()
        dbAfk.InsertCharacterTrain(characterId,self.trainId,trainType,str(self.trainstart))
        self.startTrainTimer()
        self._owner.daily.noticeDaily(22,0,-1)#通知每日目标
        self._owner.schedule.noticeSchedule(7)#成功后的日程目标通知
        self._owner.quest.specialTaskHandle(124)#成功后的特殊任务通知
        return {'result':True}
    
    def updateTrainMode(self,tmode):
        '''更改加强模式'''
        if not self.istrain:
            return {'result':False,'message':Lg().g(213)}
        if self.trainmode<=tmode:
            return {'result':False,'message':Lg().g(211)}
        goldcons = TRAINMODE.get(tmode)['cons']
        nowgold = self._owner.finance.getGold()
        golddelta = nowgold - goldcons
        if golddelta < 0:
            return {'result':False,'message':Lg().g(190)}
        characterId = self._owner.baseInfo.id
        self._owner.finance.updateGold(golddelta)
        self.trainmode = tmode
        props = {'trainmode':tmode}
        dbAfk.updateCharacterMining(characterId, props)
        return {'result':True}
        
    def getWaJueInfo(self):
        '''获取挖掘信息'''
        info = {}
        if not self.ismining:
            info['remainTime'] = 0
        else:
            miningtime = MININGTYPE.get(self.miningtype)*3600
            info['remainTime'] = int(miningtime - minusDatetimeForSecond(\
                                            datetime.datetime.now(),self.miningstart))
        info['runningTask'] = self.ismining
        nowtimes = self.turncointimes + 1
        viplevel = self._owner.baseInfo._viptype
        vipperm = dbVIP.VIPPERM.get(viplevel)
        info['coinbound'] = 20000#可获得的金币数量
        info['goldreq'] = nowtimes*2#当前所需消耗钻的数量
        info['sptimes'] = vipperm.get('turncointimes',0)+1-self.turncointimes
        return info
        
    def dianshichengjin(self):
        '''点石成金'''
        characterId = self._owner.baseInfo.id
        nowtimes = self.turncointimes + 1
        #VIP权限限制
        viplevel = self._owner.baseInfo._viptype
        if not vipCertification('turncointimes', viplevel,nowtimes= self.turncointimes):
            return {'result':False,'message':Lg().g(215)}
        coinboud = 20000#self._owner.level.getLevel()*3980
        goldcons = nowtimes *2
        nowgold = self._owner.finance.getGold()
        golddelta = nowgold - goldcons
        if golddelta < 0:
            return {'result':False,'message':Lg().g(216)}
        self._owner.finance.consGold(goldcons,11)#点石成金消耗钻
        self._owner.finance.addCoin(coinboud)
        self.turncointimes += 1
        if self.turncointimes ==1:
            props = {'turncoindate':str(datetime.datetime.now()),
                     'turncointimes':self.turncointimes}
            dbAfk.updateCharacterTurnRecord(characterId, props)
        else:
            props = {'turncointimes':self.turncointimes}
            dbAfk.updateCharacterTurnRecord(characterId, props)
        return {'result':True,'data':coinboud}
    
    def buyEnergy(self):
        '''购买体力'''
        viplevel = self._owner.baseInfo._viptype
        if not vipCertification('turnenergytimes', viplevel,nowtimes= self.turnenergytimes):
            return {'result':False,'message':Lg().g(217),'failType':0}
        characterId = self._owner.baseInfo.id
        energyboud = 40
        goldcons = (self.turnenergytimes+1)*20
        nowgold = self._owner.finance.getGold()
        golddelta = nowgold - goldcons
        if golddelta < 0:
            return {'result':False,'message':Lg().g(190),'failType':1}
        self._owner.finance.consGold(goldcons,7)#购买活力消耗钻
        self._owner.attribute.addEnergy(energyboud)
        self.turnenergytimes += 1
        if self.turnenergytimes ==1:
            props = {'turnenergydate':str(datetime.datetime.now()),
                     'turnenergytimes':self.turnenergytimes}
            dbAfk.updateCharacterTurnRecord(characterId, props)
        else:
            props = {'turnenergytimes':self.turnenergytimes}
            dbAfk.updateCharacterTurnRecord(characterId, props)
        return {'result':False,'message':Lg().g(218),'failType':0}
        
    
    def JiaJiXunLian(self,ttype,memberId):
        '''加急训练'''
        viplevel = self._owner.baseInfo._viptype
        if not vipCertification('turnexptimes', viplevel,nowtimes= self.turnexptimes):
            return {'result':False,'message':Lg().g(219)}
        characterId = self._owner.baseInfo.id
        nowtimes = self.turnexptimes + 1
        expbound = 30000#self._owner.level.getLevel()*1000
        goldcons = nowtimes *2
        nowgold = self._owner.finance.getGold()
        golddelta = nowgold - goldcons
        if golddelta < 0:
            return {'result':False,'message':Lg().g(220)}
        self._owner.finance.consGold(goldcons,10)#加急训练消耗钻
        if ttype == 0:
            self._owner.level.addExp(expbound)
        else:
            self._owner.pet.getPet(memberId).level.addExp(expbound)
        self.turnexptimes += 1
        if self.turnexptimes ==1:
            props = {'turnexpdate':str(datetime.datetime.now()),
                     'turnexptimes':self.turnexptimes}
            dbAfk.updateCharacterTurnRecord(characterId, props)
        else:
            props = {'turnexptimes':self.turnexptimes}
            dbAfk.updateCharacterTurnRecord(characterId, props)
        self._owner.schedule.noticeSchedule(13)#成功后的日程目标通知
        return {'result':True,'data':expbound}
    
    def FinishedMining(self):
        '''立即结束挖掘'''
        if not self.ismining:
            return {'result':False,'message':Lg().g(221)}
        viplevel = self._owner.baseInfo._viptype
        if not vipCertification('finishedMining', viplevel,nowtimes= self.finishedMining):
            return {'result':False,'message':Lg().g(222)}
        characterId = self._owner.baseInfo.id
        goldcons = 10*MININGTYPE.get(self.miningtype)
        nowgold = self._owner.finance.getGold()
        golddelta = nowgold - goldcons
        if golddelta < 0:
            return {'result':False,'message':Lg().g(190)}
        self.finishedMining +=1
        if self.finishedMining ==1:
            props = {'miningdate':str(datetime.datetime.now()),
                     'finishedMining':self.finishedMining}
            dbAfk.updateCharacterTurnRecord(characterId, props)
        else:
            props = {'finishedMining':self.finishedMining}
            dbAfk.updateCharacterTurnRecord(characterId, props)
        self._owner.finance.consGold(goldcons,5)#立即完成挖掘消耗钻
        coinbound = self.rewardMiningBound()
        self.stopMiningTimer()
        msg = u'获得%d金币'%(coinbound)
        return {'result':True,'message':msg}
        
    def FinishedTrain(self):
        '''立即结束训练'''
        if not self.istrain:
            return {'result':False,'message':Lg().g(223)}
        viplevel = self._owner.baseInfo._viptype
        if not vipCertification('finishedTrain', viplevel,nowtimes= self.finishedTrain):
            return {'result':False,'message':Lg().g(222)}
        characterId = self._owner.baseInfo.id
        goldcons = 10*TRAINTYPE.get(self.traintype)
        nowgold = self._owner.finance.getGold()
        golddelta = nowgold - goldcons
        if golddelta < 0:
            return {'result':False,'message':Lg().g(190)}
        self.finishedTrain +=1
        if self.finishedTrain ==1:
            props = {'traindate':str(datetime.datetime.now()),
                     'finishedTrain':self.finishedTrain}
            dbAfk.updateCharacterTurnRecord(characterId, props)
        else:
            props = {'finishedTrain':self.finishedTrain}
            dbAfk.updateCharacterTurnRecord(characterId, props)
        self._owner.finance.consGold(goldcons,9)#立即完成训练消耗钻
        expbound = self.rewardTrainBound()
        self.stopTrainTimer()
#        sendTimerSingal(0, characterId, -1)
        msg = u'获得%d经验'%expbound
        return {'result':True,'message':msg}
    
    def getAramListInfo(self):
        '''获取训练的列表'''
        info = {}
        if self.trainId ==0 and self.istrain:
            traintime = TRAINTYPE.get(self.traintype)*3600
            info['roleRunningFlag'] = True
            info['roleRunTime'] = int(traintime-minusDatetimeForSecond(\
                                        datetime.datetime.now(),self.trainstart))
        else:
            info['roleRunningFlag'] = False
            info['roleRunTime'] = 0
        info['petAramInfo'] = []
        for petId,pet in self._owner.pet.getPets().items():
            petInfo = {}
            petInfo['petId'] = petId
            petInfo['resPetId'] = pet.templateInfo.get('resourceid',0)
            petInfo['petName'] = pet.baseInfo.getName()
            petInfo['petLevel'] = pet.level.getLevel()
            petInfo['icon'] = pet.templateInfo.get('icon',0)
            petInfo['type'] = pet.templateInfo.get('type',0)
            petInfo['runningFlag'] = True if self.trainId == petId else False
            if self.istrain and self.trainId == petId:
                traintime = TRAINTYPE.get(self.traintype)*3600
                petInfo['remainTime'] = int(traintime-minusDatetimeForSecond(\
                                        datetime.datetime.now(),self.trainstart))
            else:
                petInfo['remainTime'] = 0
            info['petAramInfo'].append(petInfo)
        nowtimes = self.turnexptimes + 1
        viplevel = self._owner.baseInfo._viptype
        vipperm = dbVIP.VIPPERM.get(viplevel)
        info['expbound'] = 30000#可获得的经验数量
        info['goldreq'] = nowtimes*2#当前所需消耗钻的数量
        info['sptimes'] = vipperm.get('turnexptimes',0)+1-self.turnexptimes
        return info
    
    def startMeditation(self,state=0):
        '''开始冥想'''
        if self.guajitimer:
            msg = u"你正处于冥想"
            return {'result':False,'message':msg}
        else:
            self._owner.baseInfo.setStatus(3)
            self.meditationtime = datetime.datetime.now()
            if self._owner.baseInfo._viptype==0:
                goaltime = 32400
            else:
                goaltime = 86400
            guaJiInfo = {'exp':0,'time':goaltime}
            self.guajitimer = reactor.callLater(15,self.doMeditationBound,state)
            pushCorpsApplication(self._owner.baseInfo.id, 8,'','','',guaJiInfo=guaJiInfo)
            return {'result':True,'message':Lg().g(224)}
        
    def doMeditationBound(self,state):
        '''进行挂机经验奖励的处理
        '''
        exppercent = 1
        if state:
            exppercent = 1.1
        timedd = datetime.datetime.now() - self.meditationtime
        timesecond = timedd.days*86400 + timedd.seconds
        goaltime = 32400 if self._owner.baseInfo._viptype==0 else 86400
        if timesecond>=goaltime:
            self.stopMeditation()
            return
        level = self._owner.level.getLevel()
        expbound = int(level*1.0/10*level*exppercent)
        self.goalexp += expbound
        self._owner.level.addExp(expbound)
        msg = u"+%d%s"%(expbound,Lg().g(499))
        pushOtherMessageByCharacterId(msg, [self._owner.baseInfo.id])
        self.guajitimer = reactor.callLater(15,self.doMeditationBound,state)
        
    def stopMeditation(self):
        '''停止冥想
        @param state: int 停止冥想的原因 1主动停止 2离线停止
        '''
        self.stopGuaJiTimer()
        return {'result':True,'message':u''}
    
    def getMeditationInfo(self):
        '''获取冥想信息'''
        if not self.guajitimer:
            msg = u"你未处于冥想状态"
            return {'result':False,'message':msg}
        else:
            timedd = datetime.datetime.now() - self.meditationtime
            timesecond = timedd.seconds
            return {'result':True,'message':u'','expStr':u'1000',
                    'zhanliStr':u'1000','gujiTime':int(timesecond)}
            
    def startEnergyTimer(self):
        '''开始在线活力奖励定时器,每30分钟增加5点活力
        '''
        if not self.energystarttime:
            tt = ENERGY_TIME
        else:
            nowtime = datetime.datetime.now()
            tdelta = minusDatetimeForSecond(nowtime,self.energystarttime)
            tt = ENERGY_TIME - tdelta
            if tt<=0:
                tt = 1
        self.energytimer = reactor.callLater(tt,self.onlineEnergyBound)
        
    def stopEnergyTimer(self):
        '''停止在线活力奖励定时器
        '''
        if self.energytimer:
            try:
                self.energytimer.cancel()
            except Exception,e:
                print e
            self.energytimer = None
        
            
    def onlineEnergyBound(self):
        '''在线活力奖励
        '''
        self._owner.attribute.addEnergy(5)
        self.energystarttime = datetime.datetime.now()
        tt = ENERGY_TIME
        self.energytimer = reactor.callLater(tt,self.onlineEnergyBound)
    
        
