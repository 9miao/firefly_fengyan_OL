#coding:utf8
'''
Created on 2009-12-2

@author: wudepeng
'''
from app.scense.netInterface.pushObjectNetInterface import pushApplyMessage
from app.scense.component.Component import Component
import math
from app.scense.utils import dbaccess
from app.scense.utils.DataLoader import loader, connection
import datetime
from twisted.internet import reactor

from app.scense.protoFile.practice import practiceFinsihed_pb2
from app.scense.core.language.Language import Lg

reactor = reactor

def practiceFinsihed(characterId,topicID=100001):
    '''修炼完成休息通知'''
    response = practiceFinsihed_pb2.PracticeFinsihed()
    response.message = Lg().g(438)
    msg = response.SerializeToString()
    pushApplyMessage(topicID,msg,[characterId])

class CharacterPracticeComponent(Component):
    '''
    classdocs
    '''


    def __init__(self, owner):
        '''
        Constructor
        '''
        Component.__init__(self, owner)
        self._monsterId = 0 #修炼的怪物的id
        self._countHit = 0 #修炼的攻击次数
        self._startTime = u"" #修炼的开始时间
        self._endTime = u"" #修炼的结束时间

    def getMonsterId(self):
        return self._monsterId

    def setMonsterId(self, monsterId):
        self._monsterId = monsterId

    def getCountHit(self):
        return self._countHit

    def setCountHit(self, countHit):
        self._countHit = countHit

    def getStartTime(self):
        return self._startTime

    def setStartTime(self, startTime):
        self._startTime = startTime

    def getEndTime(self):
        return self._endTime

    def setEndTime(self, endTime):
        self._endTime = endTime


    def getMonsterPracticeExp(self, monsterId):
        '''
              获取一个怪物修炼经验奖励
        @param monsterId: 怪物id
        '''
        result = self.getSingleMonsterPracticeExp(monsterId)
        if not result[0]:
            return {'result':result[0], 'reason':result[1]}
        expBonus = result[1]
        monsterLevel = result[2]
        return {'result':True, 'data':{'expBonus':expBonus,'monsterLevel':monsterLevel}}

    def getSingleMonsterPracticeExp(self, monsterId):
        id = self._owner.baseInfo.id

        monsterInfo = loader.getById('npc', monsterId, ['monsterGroupId', 'levelGroup'])
        if not monsterInfo:
            return False, Lg().g(439)
        levelList = list(monsterInfo['levelGroup'].split(';'))
        groupId = monsterInfo['monsterGroupId']
        tempList = []
        for level in levelList:
            level = int(level)
            tempList.append(level)
        caughtLevel = tempList[0]
        cursor = connection.cursor()
        cursor.execute("select expBonus from `monster_instance` where level=%d and groupId=%d" % (caughtLevel, groupId))
        monsterInstance = cursor.fetchone()
        cursor.close()
        if not monsterInstance:
            return False, Lg().g(439)
        expBonus = monsterInstance['expBonus']
        return True, expBonus,caughtLevel

    def pratice(self, monsterId, singleExpBonus, monsterCount,monsterLevel):
        '''
                     修炼怪物
        @param monsterId: 怪物id
        @param singleExpBonus: 每个怪得到的经验奖励
        @param monsterCount: 修炼怪物数量
        @param monsterLevel: 修炼怪物等级
        '''
        id = self._owner.baseInfo.id
        energy = self._owner.attribute.getEnergy()
        if energy == 0:
            return {'result':False, 'message':Lg().g(440)}
        coin = self._owner.finance.getCoin()
        exp = self._owner.level.getExp()
        status = 2#修炼状态
        costEnergy = monsterCount * 1
        totalExp = singleExpBonus * monsterCount
        costCoin = int(math.pow(monsterLevel,1.1)*9*(1+(monsterLevel/150.0)))*monsterCount
        duration = 60 * 3 * monsterCount
        energy -= costEnergy
        coin -= costCoin
        exp += totalExp
        if energy < 0:
            return {'result':False, 'message':Lg().g(440)}
        if coin < 0:
            return {'result':False, 'message':Lg().g(267)}
        dbaccess.updatePlayerInfo(id, {'status':status, 'coin':coin, 'energy':energy})
        startTime = datetime.datetime.now()
        finishTime = startTime + datetime.timedelta(minutes = 3 * monsterCount)
        dbaccess.updatePlayerPracticeRecord(id, {'monsterId':monsterId, 'countHit':monsterCount, \
                                                 'startTime':str(startTime), 'finishTime':str(finishTime), \
                                                 'singleExpBonus':singleExpBonus})
        reactor.callLater(int(duration), self.doWhenPracticeFinsihed, {'status':1, 'exp':exp})

        self._owner.baseInfo.setStatus(status)
        self._owner.attribute.setEnergy(energy)
        self._owner.finance.setCoin(coin)

        return {'result':True, 'data':{'status':self._owner.baseInfo.getStatus()}}

    def doWhenPracticeFinsihed(self, attrs):
        '''当修炼结束时'''
        id = self._owner.baseInfo.id
        practiceRecord = dbaccess.getPlayerPracticeRecord(id)
        monsterId = practiceRecord[2]
        countHit = practiceRecord[3]
        finishTime = practiceRecord[5]
        now = datetime.datetime.now()

        if not finishTime or (finishTime - now).seconds < 0:
            return
        self._owner.level.updateExp(attrs['exp'])
#        if not self._owner.level.updateLevel():
#            dbaccess.updatePlayerInfo(id, attrs)
        self._owner.baseInfo.setStatus(1)

        npc = loader.getById('npc', monsterId, '*')
        if npc:
#            for i in range(0, countHit):
#                self._owner.quest.onSuccessKillOneMonster(monsterId)
            
            self.placePracticeItems(countHit, npc)

        practiceFinsihed(id)

    def terminatePractice(self):
        '''
                     终止玩家修炼
        '''
        id = self._owner.baseInfo.id
        exp = self._owner.level.getExp()

        record = dbaccess.getPlayerPracticeRecord(id)
        monsterId = record[2]
        startTime = record[4]
        finishTime = record[5]
        singleExpBonus = record[6]
        now = datetime.datetime.now()
        currentCountHit = int((now - startTime).seconds / (60 * 3))
        int((finishTime - startTime).seconds / 60)
        currentExp = currentCountHit * singleExpBonus
        monster = loader.getById('npc', monsterId, '*')
        if not monster:
            return {'result':False, 'message':Lg().g(441)}

        for i in range(0, currentCountHit):
            pass
#            self._owner.quest.onSuccessKillOneMonster(monsterId)
#            break
#        if item:
#            self._owner.pack.putOneItemIntoTempPackage(item, currentCountHit)
#            pushMessage(str(self._owner.baseInfo.id),'newTempPackage')
#        self.placePracticeItems(currentCountHit, monster)

        monsterName = monster['name']
        self._owner.level.setExp(exp + currentExp)
        dbaccess.updatePlayerInfo(id, {'status':1})
        self._owner.baseInfo.setStatus(1)
        return {'result':True, 'data':{'monsterName':monsterName, 'currentExp':currentExp, \
                                      'currentCountHit':currentCountHit, 'status':self._owner.baseInfo.getStatus(), \
                                      'level':self._owner.level.getLevel()}}

    def immediateFinishPractice(self, payType, payNum):
        '''立即完成修炼'''
        id = self._owner.baseInfo.id
        gold = self._owner.finance.getGold()
        coupon = self._owner.finance.getCoupon()
        exp = self._owner.level.getExp()
        if payType == 'gold':
            gold -= payNum
        else:
            coupon -= payNum
        if gold < 0 :
            return {'result':False, 'reason':u'您的黄金不够'}
        if coupon < 0:
            return {'result':False, 'reason':u'您的礼券不够'}
        record = dbaccess.getPlayerPracticeRecord(id)
        countHit = record[3]
        totalExp = record[3] * record[6]
        exp += totalExp
        monster = loader.getById('npc', record[2], '*')
        monsterName = monster['name']

        for i in range(0,countHit):
            self._owner.quest.onSuccessKillOneMonster(record[2],'battle')
#            break
#            if item:
#                self._owner.pack.putOneItemIntoTempPackage(item,1)
        self.placePracticeItems(countHit, monster)

        self._owner.level.setExp(exp)
        if not self._owner.level.updateLevel():
            dbaccess.updatePlayerInfo(id, {'status':1, 'gold':gold, 'coupon':coupon, 'exp':exp})
        else:
            dbaccess.updatePlayerInfo(id, {'status':1, 'gold':gold, 'coupon':coupon})

        self._owner.baseInfo.setStatus(1)
        self._owner.finance.setGold(gold)
        self._owner.finance.setCoupon(coupon)

        return {'result':True, 'data':{'monsterName':monsterName, 'totalExp':totalExp, 'countHit':countHit, \
                                      'gold':gold, 'coupon':coupon, 'status':self._owner.baseInfo.getStatus(), \
                                      'level':self._owner.level.getLevel()}}

    def getPracticeInfo(self):
        '''获取玩家修炼的信息'''
        id = self._owner.baseInfo.id

        record = dbaccess.getPlayerPracticeRecord(id)
        monsterName = loader.getById('npc', record[2], ['name'])
        if not monsterName:
            return {'result':False, 'reason':u'没有找到修炼的怪物'}
        monsterName = monsterName['name']
        countHit = record[3]
        finishTime = record[5]
        seconds = (finishTime - datetime.datetime.now()).seconds
        singleMonsterExpBonus = record[6]
        totalExp = singleMonsterExpBonus * countHit

        return {'countHit':countHit, 'seconds':seconds, 'totalExp':totalExp, 'monsterName':monsterName}

    def placePracticeItems(self, countHit, monster):
        '''放置修炼掉落的物品'''
        self._owner.pack.setTempPackage()
#        ret = self._owner.pack._tempPackage.isTempPackageFull()
        ret = (False,1)
        if not ret[0]:
            for i in range(0, countHit):
                dropConfigId = self._owner.dropping.getDropConfigOnNpc(monster)
                item = self._owner.dropping.getItemByDropping(dropConfigId)[0]
                if item:
                    self._owner.pack.putNewItemInTemPackage(item)
                    self._owner.pack.setTempPackage()
