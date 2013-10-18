#coding:utf8
'''
Created on 2011-10-31
人物携带效果类
@author: lan
'''

from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbEffect
from app.scense.component.effect.effect import Effect
import datetime
from app.scense.netInterface.pushObjectNetInterface import pushApplyMessage

from app.scense.protoFile.playerInfo import GetBuffListInfo_pb2
from app.scense.core.language.Language import Lg

def pushCharacterEffectList(sendList,infolist):
    '''推送角色的效果列表信息'''
    
    response = GetBuffListInfo_pb2.GetBuffListInfoResponse()
    for info in infolist:
        effectInfo = response.buffInfo.add()
        for item in info.items():
            setattr(effectInfo,item[0],item[1])
    msg = response.SerializeToString()
    pushApplyMessage(222, msg, sendList)

class CharacterEffectComponent(Component):
    
    '''
    effect component for character
    '''
    MAXEFFECT = 5#最大buff效果个数
    
    def __init__(self,owner):
        '''
        Constructorj
        '''
        Component.__init__(self,owner)
        self._skill_effect = [] #技能所产生的效果
        self._item_effect = [] #使用技能携带的效果
#        self.initEffect()
        
    def initEffect(self):
        '''初始化角色的效果信息'''
        effectsList = dbEffect.getCharacterEffect(self._owner.baseInfo.id)
        for effect in effectsList:
            self.putItemEffect(effect)
        self.pushEffectListInfo()
        
    def putItemEffect(self,effect):
        '''添加一个物品使用的效果'''
        e = Effect(effect, self._owner)
        if e.IsEffective():
            self._item_effect.append(e)
        
    def addNewEffect(self,effectId):
        '''添加一个效果'''
        for effect in self._item_effect:
            if effectId==effect._id:
                raise Exception(Lg().g(289))
        effectInfo = dbEffect.ALL_EFFECT_INFO.get(effectId)
        for effect in self._item_effect:
            if effect.getEffectType()==effectInfo.get('effectType',1):
                effect.destroyEffect(statu = 0)
        data = {}
        data['id'] = 0
        data['effectID'] = effectId
        data['surplus'] = effectInfo['surplus']
        data['startTime'] = datetime.datetime.now()
        e = Effect(data, self._owner)
        e.InsertItemIntoDB()
        self._item_effect.append(e)
        if e.getEffectTriggerType()==2:
            e.doHotEffect()
        self._owner.updatePlayerInfo()#推送角色信息
        self.pushEffectListInfo()
        
    def dropItemEffect(self,effect,statu = 1):
        '''清除一个物品使用效果'''
        try:
            self._item_effect.remove(effect)
            if statu:
                self._owner.updatePlayerInfo()
                self.pushEffectListInfo()
        except Exception:
            pass
        
    
    
    def getEffectInfo(self):
        '''获取buff效果'''
        info = {}
        for effect in self._item_effect:
            if not effect._effective:
                self.dropItemEffect(effect,statu =0)
            if effect.getEffectTriggerType()==1:
                try:
                    exec(effect.getBuffEffect())
                except Exception:
                    pass
        return info
    
    def getEffectListInfo(self):
        '''获取角色效果列表信息'''
        infolist = []
        for effect in self._item_effect:
            info = effect.formatEffectInfo()
            infolist.append(info)
        return infolist
    
    def pushEffectListInfo(self):
        '''推送角色效果列表信息'''
        infolist = self.getEffectListInfo()
        pushCharacterEffectList([self._owner.getDynamicId()], infolist)
        
    def doEffectHot(self):
        '''执行效果处理'''
        for effect in self._item_effect:
            if effect.getEffectTriggerType()==2:
                effect.doHotEffect()
        self.pushEffectListInfo()
    
    def startAllEffectTimer(self):
        '''启动所有的特效BUFF定时器
        '''
        for effect in self._item_effect:
            effect.startTimer()
        
    def stopAllEffectTimer(self):
        '''停止所有的特效BUFF定时器
        '''
        for effect in self._item_effect:
            effect.stopTimer()
    
    def getFashion(self):
        '''获取角色的时装的ID
        '''
        fashion = 0
        for effect in self._item_effect:
            if effect._effectType==9:
                fashion = effect._EffectId
                break
        return  fashion
    
    def getMounts(self):
        '''获取角色的坐骑
        '''
        mounts = 0
        for effect in self._item_effect:
            if effect._effectType==10:
                mounts = effect._EffectId
                break
        return  mounts
        
        
        
        
        
    
    
    