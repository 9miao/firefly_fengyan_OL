#coding:utf8
'''
Created on 2011-11-6
效果类
@author: lan
'''
import datetime
from app.scense.utils.dbopera import dbEffect
from twisted.python import log
from twisted.internet import reactor

reactor = reactor

class Effect(object):
    '''效果类'''
    
    def __init__(self,data,owner):
        '''初始化效果类'''
        self._id = data['id']#buff的id
        self._EffectId = data['effectID'] #效果模板的id
        self._surplus = data['surplus'] #效果的剩余值
        self._startTime = data['startTime'] #效果开始的时间
        self._effectType = 0
        self._owner = owner #效果拥有者的Id
        self._effective = 1 #buff是否还有效
        self.timer = None#buff的定时对象
        self.initEffect()
        
    def initEffect(self):
        '''初始化效果'''
        effectInfo = dbEffect.ALL_EFFECT_INFO.get(self._EffectId)
        self._effectType = effectInfo['effectType']
        if effectInfo.get('continuedType',1)==1:#如果是限时类的效果
            surplusTime = self.getSurplusTime()
            if surplusTime>0:
                self.timer = reactor.callLater(surplusTime,self.destroyEffect)
            else:
                self.destroyEffect()
                
    def startTimer(self):
        '''启动定时器
        '''
        effectInfo = dbEffect.ALL_EFFECT_INFO.get(self._EffectId)
        if effectInfo.get('continuedType',1)==1:#如果是限时类的效果
            surplusTime = self.getSurplusTime()
            self.timer = reactor.callLater(surplusTime,self.destroyEffect)
        
    def stopTimer(self):
        '''停止并清除定时器
        '''
        if self.timer:
            self.timer.cancel()
        self.timer = None
                
    def IsEffective(self):
        '''检测效果是否是有效的'''
        return bool(self._effective)
    
    def getSurplus(self):
        '''获取剩余值'''
        return self._surplus
    
    def getSurplusTime(self):
        '''获取剩余时间'''
        effectInfo = dbEffect.ALL_EFFECT_INFO.get(self._EffectId)
        totaltime = effectInfo.get('totaltime',0)
        nowtime = datetime.datetime.now()
        delta = nowtime - self._startTime
        interval = delta.days*86400 + delta.seconds
        surplusTime = totaltime - interval
        return surplusTime
        
    def InsertItemIntoDB(self):
        '''写入信息到数据库'''
        effect = {}
        effect['id'] = self._EffectId
        effect['surplus'] = self._surplus
        instanceId = dbEffect.addNewItemEffct(self._owner.baseInfo.id, effect)
        self._id = instanceId
        
    def destroyEffect(self,statu = 1):
        '''清除当前效果'''
        self._effective = 0
        try:
            self.timer.cancel()
        except Exception ,e:
            pass
        self._owner.effect.dropItemEffect(self,statu=statu)
        self.destroyInDB()
        
    def destroyInDB(self):
        '''销毁在数据库中的记录'''
        self._effective = 0
        dbEffect.delCharacterEffect(self._owner.baseInfo.id, self._EffectId)
        
    def updateEffectInfo(self,surplus):
        '''更新效果信息'''
        self._surplus = surplus
        if surplus<=0:
            self.destroyEffect()
            return
        self._surplus = surplus
        dbEffect.updateEffectInfo(self._owner.baseInfo.id, self._EffectId, surplus)
        
    def getEffectTriggerType(self):
        '''获取效果的触发类型'''
        effectInfo = dbEffect.ALL_EFFECT_INFO.get(self._EffectId)
        return effectInfo.get('triggerType',1)
    
    def getEffectType(self):
        '''获取效果类型'''
        effectInfo = dbEffect.ALL_EFFECT_INFO.get(self._EffectId)
        return effectInfo.get('effectType',1)
    
    def restoreHpAfterFight(self):
        '''战后恢复血量'''
        
        hpNeed = self._owner.attribute.getMaxHp()- self._owner.attribute.getHp()
        surplus = self._surplus - hpNeed
        if self._surplus<hpNeed:
            hpNeed = self._surplus
            surplus = 0
        self._owner.attribute.addHp(hpNeed)
        surplus = self._owner.pet.restorationPetHP(surplus)
        self.updateEffectInfo(surplus)
        
    def restoreMpAfterFight(self):
        '''战后恢复蓝'''
        mpNeed = self._owner.attribute.getMaxMp()- self._owner.attribute.getMp()
        surplus = self._surplus - mpNeed
        if self._surplus<mpNeed:
            mpNeed = self._surplus
            surplus = 0
        self.updateEffectInfo(surplus)
        self._owner.attribute.addMp(mpNeed)
        
    def doHotEffect(self):
        '''效果触发'''
        script = self.getBuffEffect()
        try:
            exec(script)
        except Exception:
            pass
#            log.err(repr("策划坑爹啊,物品使用buff效果填写出错了:%d"%self._EffectId))
    
    def getBuffEffect(self):
        '''获取buff效果描述'''
        effectInfo = dbEffect.ALL_EFFECT_INFO.get(self._EffectId)
        return effectInfo.get('effectScript','')
        
    def formatEffectInfo(self):
        '''格式化效果信息'''
        effectInfo = dbEffect.ALL_EFFECT_INFO.get(self._EffectId)
        info = {}
        info['buffId'] = self._EffectId
        info['buffName'] = effectInfo.get('name','')
        info['buffDes'] = effectInfo.get('description','')
        info['type'] = effectInfo.get('type','')
        info['icon'] = effectInfo.get('icon','')
        info['timeAndCountFlag'] = effectInfo.get('continuedType','')
        if info['timeAndCountFlag']==1:
            info['timeOrCount'] = int(self.getSurplusTime())
        else:
            info['timeOrCount'] = int(self.getSurplus())
        return info
        
        