#coding:utf8
'''
Created on 2012-7-17
爬塔，角色的爬塔记录和信息
@author: Administrator
'''
from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbtower
from app.scense.utils.dbopera import dbVIP
import datetime

from app.scense.core.fight.fight_new import Fight
from app.scense.core.fight.battleSide import BattleSide
from app.scense.core.character.Monster import Monster

from app.scense.applyInterface import dropout
from app.scense.core.language.Language import Lg

#爬塔刷新次数消耗的钻
FLUSH_CONS = {1:0,2:100,3:150,4:200,5:250,6:300,7:350,8:400,9:450,10:500,11:550}

def minusDatetimeForSecond(dtime1,dtime2):
    '''求两个日期时间的秒差'''
    deltas = dtime1 - dtime2
    days = deltas.days
    seconds = deltas.seconds
    return 86400*days + seconds

class CharacterTowerComponent(Component):
    
    def __init__(self,owner):
        '''初始化爬塔信息
        '''
        Component.__init__(self, owner)
        self.climbtimes = 0#角色今天爬过的次数
        self.nowLayers = 1#角色当前所在的层数
        self.high = 0#角色爬过的最高层数
        self.recordDate = datetime.date.today()
        self.inited = False#是否初始化过
        self.lasttime = None#上次爬塔的时间
        
    def initTowerInfo(self):
        '''初始化角色的爬塔数据
        '''
        nowdate = datetime.date.today()
        if nowdate != self.recordDate:#如果到了第二天，重置爬塔信息
            self.resetTowerRecord()
            self.inited = True
            return
        if self.inited:#如果已经初始化过，则不在进行初始化
            return
        self.inited = True
        characterId = self._owner.baseInfo.id
        initdata = dbtower.getCharacterTowerInfo(characterId)
        nowdate = datetime.date.today()
        self.high = initdata['high']
        if initdata['recordDate']!=nowdate:
            self.resetTowerRecord()
        else:
            self.climbtimes = initdata['climbtimes']
            self.nowLayers = initdata['nowLayers']
        
    def resetTowerRecord(self):
        '''重置角色的爬塔记录
        '''
        self.climbtimes = 0
        self.nowLayers = 1
        characterId = self._owner.baseInfo.id
        nowdate = datetime.date.today()
        self.climbtimes = 0
        self.nowLayers = 1
        self.recordDate = nowdate
        props = {'climbtimes':0,'nowLayers':1,'recordDate':str(nowdate)}
        dbtower.updateCharacterTowerRecord(characterId, props)
        
    def flushTowerRecord(self):
        '''刷新爬塔记录
        '''
        if self.nowLayers ==1:
            return {'result':False,'message':Lg().g(493)}
        viplevel = self._owner.baseInfo._viptype
        if not dbVIP.vipCertification('climbtimes', viplevel,nowtimes= self.climbtimes):
            return {'result':False,'message':Lg().g(494)}
        goldcons = FLUSH_CONS.get(self.climbtimes+1)
        if goldcons and goldcons> self._owner.finance.getGold():#判断消耗
            return {'result':False,'message':Lg().g(190)}
        else:
            self._owner.finance.consGold(goldcons,12,
                        consDesc=u'刷新克洛塔消耗%d钻'%goldcons)#刷新克洛塔#(-goldcons)#扣除消耗的钻
        self.climbtimes +=1
        self.nowLayers = 1
        characterId = self._owner.baseInfo.id
        props = {'climbtimes':self.climbtimes,'nowLayers':1}
        dbtower.updateCharacterTowerRecord(characterId, props)
        return {'result':True,'message':Lg().g(495)}
        
    def getSurplusTime(self):
        '''获取剩余时间'''
        return 50
        
    def getTowerInfo(self):
        '''获取当前塔层信息
        '''
        layer = self.nowLayers
        towerinfo = dbtower.ALL_TOWER_INFO.get(layer)
        if not towerinfo:
            towerinfo = dbtower.ALL_TOWER_INFO.get(layer -1)
        viplevel = self._owner.baseInfo._viptype
        info = {}
        info['layer'] = layer#当前层数
        info['monsterinfo'] = towerinfo['monsterdesc']#怪物信息
        info['boundInfo'] = towerinfo['boundinfo']#奖励信息\
        info['surplus'] = dbVIP.VIPPERM[viplevel].get('climbtimes') - self.climbtimes#次数
        info['gold'] = FLUSH_CONS.get(self.climbtimes+1)#消耗的钻
        return info
        
    def doTowerBound(self,layer):
        '''执行爬塔成功后的奖励
        @param layer: int 塔的层数
        '''
        towerinfo = dbtower.ALL_TOWER_INFO.get(layer)
        if not towerinfo:
            return {'result':False,'message':Lg().g(496)}
        expbound = towerinfo.get('expbound',0)
        dropoutid = towerinfo.get('dropoutid',1)
        if not dropoutid:
            dropoutIitem = None
        else:
            dropoutIitem = dropout.getDropByid(dropoutid)
        boundinfo = {'exp':expbound,'item':dropoutIitem}
        if expbound:
            self._owner.level.addExp(expbound)
        if dropoutIitem:
            self._owner.pack.putNewItemInPackage(dropoutIitem)
        return boundinfo
        
    def succedHandle(self):
        '''爬塔成功后的处理
        '''
        props = {}
        self.nowLayers +=1
        if self.high < self.nowLayers:
            self.high = self.nowLayers
            props['high'] = self.nowLayers
        props['nowLayers'] = self.nowLayers
        characterId = self._owner.baseInfo.id
        dbtower.updateCharacterTowerRecord(characterId, props)
        
    def climb(self):
        '''开始爬塔
        '''
        nowtime = datetime.datetime.now()
        if self.lasttime and minusDatetimeForSecond(nowtime, self.lasttime)<=30:
            return {'result':False,'message':Lg().g(497)}
        self.lasttime = nowtime
        layer = self.nowLayers
        towerinfo = dbtower.ALL_TOWER_INFO.get(layer)
        if not towerinfo:
            return {'result':False,'message':Lg().g(498)}
        monsterlist,eyes = towerinfo.get('rule',[[15001],[5]])
        matrixid = towerinfo.get('matrixid',100001)
        deffen = []
        for index in range(len(monsterlist)):
            monster = Monster(id = 1000+index,templateId = monsterlist[index])
            deffen.append(monster)
        challengers = BattleSide([self._owner])
        defenders = BattleSide(deffen)
        defenders.setMatrixPositionBatch(eyes)
        fig = Fight( challengers, defenders, 550)
        fig.DoFight()
        bounds = {}
        if fig.battleResult == 1:#胜利
            self.succedHandle()#胜利后的处理
            bounds = self.doTowerBound(layer)#进行胜利后的奖励处理
        else:#失败后的处理
            pass
        msg = u''
        msglist = []
        exp = bounds.get('exp')
        item = bounds.get('item')
        bounds['name'] = self._owner.baseInfo.getName()
        if exp:
            msglist.append(Lg().g(499)+u'：%d\n'%exp)
        if item:
            msglist.append(Lg().g(500)+u'：%s'%item.baseInfo.getName())
        if msglist:
            msg = msg.join(msglist)
        else:
            msg = Lg().g(143)
        data = {'message':msg,'fight':fig,'bound':bounds}
        return {'result':True,'data':data}
        
    def autoclimb(self):
        '''自动爬塔
        '''
        if self.high <=1 or self.nowLayers !=1:
            return {'result':False,'message':Lg().g(501)}
        boundmsglist = []
        for layer in range(1,self.high):
            bounds = self.doTowerBound(layer)#进行胜利后的奖励处理
            self.nowLayers = layer+1
            exp = bounds.get('exp')
            item = bounds.get('item')
            msg = ''
            if exp:
                boundmsglist.append(Lg().g(502)%(layer,exp))
            if item:
                boundmsglist.append(Lg().g(503)%(layer,item.baseInfo.getName()))
            boundmsglist.append(msg)
        props = {}
        props['nowLayers'] = self.nowLayers
        characterId = self._owner.baseInfo.id
        dbtower.updateCharacterTowerRecord(characterId, props)
        return {'result':True,'data':boundmsglist}
        
        
        
        

        