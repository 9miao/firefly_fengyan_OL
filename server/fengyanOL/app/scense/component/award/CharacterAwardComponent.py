#coding:utf8
'''
Created on 2012-4-7
角色奖励
@author: Administrator
'''
from app.scense.component.Component import Component
from app.scense.core.Item import Item
from app.scense.utils.dbopera import dbAward,dbCharacter, dbVIP,dbAfk

import datetime
from app.scense.core.language.Language import Lg


class CharacterAwardComponent(Component):
    '''角色奖励'''
    
    def __init__(self,owner):
        '''初始化
        @param awardstep: int 角色的奖励步骤
        @param dayawardtime: int 角色每日奖励领取次数
        @param viplevellibao: int vip礼包等级
        '''
        Component.__init__(self, owner)
        self.awardstep = 0
        self.viplevellibao = 0
        self.dayawardtime = None
        
    def setViplevellibao(self,lingquguo,state = 1):
        '''已领取的vip礼包等级'''
        viplevel = self._owner.baseInfo._viptype
        viplibaoid,libaovip = dbVIP.getViplibaod(viplevel, lingquguo)
        self.viplevellibao = lingquguo
        if viplibaoid:
            self._owner.icon.addIcon(self._owner.icon.VIP_AWARD,0,state = state)
        
    def setDayAwardTime(self,datet,state = 1):
        '''设置上次领取每日奖励的时间'''
        self.dayawardtime = datet
        nowday = datetime.datetime.today()
        if nowday.day != self.dayawardtime.day:
            self._owner.icon.addIcon(self._owner.icon.DAY_AWARD,0,state = state)
            
    def updateDayAwardTime(self):
        '''更新任务奖励时间
        '''
        self.dayawardtime = datetime.datetime.today()
        self._owner.icon.removeIcon(self._owner.icon.DAY_AWARD)
        dbCharacter.updatePlayerInfoByprops(self._owner.baseInfo.id,
                                            {'dayawardtime':str(self.dayawardtime)})
        
    def setAwardStep(self,setp,state = 1):
        '''获取奖励步骤
        @param setp: int 奖励步骤
        '''
        self.awardstep = setp
        award = dbAward.ALL_NOVICE_AWARD.get(setp)
        if award:
            self._owner.icon.addIcon(self._owner.icon.NEW_AWARD,
                                     award.get('totaltime'),state = state)
        
    def updateAwardStep(self):
        '''更新任务奖励步骤
        @param step: int 任务步骤
        '''
        nowstep = self.awardstep +1
        self._owner.icon.removeIcon(self._owner.icon.NEW_AWARD)
        self.setAwardStep(nowstep)
#        dbCharacter.updatePlayerInfoByprops(self._owner.baseInfo.id, 
#                                            {'novicestep':self.awardstep})
        
    def updateVIPAward(self,libaovip):
        '''更新已领取vip礼包的等级
        @param libaovip: int vip 礼包的等级
        '''
        characterId = self._owner.baseInfo.id
        self.setViplevellibao(libaovip)
        dbAfk.updateCharacterTurnRecord(characterId, {'viplevellibao':libaovip})
        
    def getAwardInfo(self,r_type):
        '''获取奖励信息'''
        awardInfo = {}
        if r_type == self._owner.icon.NEW_AWARD:#新手在线奖励
            award = dbAward.ALL_NOVICE_AWARD.get(self.awardstep)
            if award:
                iteminfo = eval('['+award.get('item')+']')
                awardInfo['gold'] = award.get('coin')
                awardInfo['zuan'] = award.get('gold')
                awardInfo['tili'] = award.get('energy')
                awardInfo['itemInfo'] = []
                awardInfo['rewardDes'] = award.get('rewardDes')
                for _item in iteminfo:
                    itemtemplate,count = _item
                    item = Item(itemTemplateId = itemtemplate)
                    item.pack.setStack(count)
                    awardInfo['itemInfo'].append(item)
        elif r_type == self._owner.icon.DAY_AWARD:#每日登陆奖励
            nowday = datetime.datetime.today()
            if nowday.day != self.dayawardtime.day:
                awardInfo['gold'] = self._owner.level.getLevel()*1500+80000
                awardInfo['rewardDes'] = Lg().g(270)
        elif r_type == self._owner.icon.VIP_AWARD:#VIP奖励
            viplevel = self._owner.baseInfo._viptype
            libaoId,libaovip = dbVIP.getViplibaod(viplevel, self.viplevellibao)
            if libaoId:
                award = dbVIP.ALLLIBAO.get(libaoId)
                if award:
                    iteminfo = eval('['+award.get('itembound')+']')
                    awardInfo['gold'] = award.get('coinbound')
                    awardInfo['zuan'] = award.get('goldbound')
                    awardInfo['tili'] = award.get('energybound')
                    awardInfo['itemInfo'] = []
                    awardInfo['rewardDes'] = award.get('awarddes')
                    for _item in iteminfo:
                        itemtemplate,count = _item
                        item = Item(itemTemplateId = itemtemplate)
                        item.pack.setStack(count)
                        awardInfo['itemInfo'].append(item)
        elif r_type == self._owner.icon.ARENA_AWARD:
            coinbound = self._owner.arena.getArenaBound()
            if coinbound:
                awardInfo['gold'] = coinbound
                awardInfo['rewardDes'] = Lg().g(271)
        return awardInfo
    
    def receiveAward(self,r_type):
        '''领取奖励
        @param r_type: int 领取奖励的类型
        '''
        if r_type == self._owner.icon.NEW_AWARD:
            icon = self._owner.icon.getIconByType(self._owner.icon.NEW_AWARD)
            if icon and icon.getSurplustime()<=0:
                awardInfo = self.getAwardInfo(r_type)
                self._owner.finance.addCoin(awardInfo.get('gold',0))
                self._owner.finance.Recharge(awardInfo.get('zuan',0))#充值
                self._owner.attribute.addEnergy(awardInfo.get('tili',0))
                itemlist = awardInfo.get('itemInfo',[])
                for item in itemlist:
                    self._owner.pack.putNewItemInPackage(item)
                self.updateAwardStep()
                return True
        elif r_type == self._owner.icon.DAY_AWARD:
            awardInfo = self.getAwardInfo(r_type)
            if not awardInfo:
                return False
            self._owner.finance.addCoin(awardInfo.get('gold',0))
            self.updateDayAwardTime()
            return True
        elif r_type == self._owner.icon.ARENA_AWARD:
            return self._owner.arena.receiveAward()
        return False
            
        
    
