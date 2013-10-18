#coding:utf8
'''
Created on 2011-3-29

@author: sean_lan
'''
from app.scense.component.Component import Component
from app.scense.utils import dbaccess
from twisted.python import log

class ItemAttributeComponent(Component):
    '''物品附加属性'''
    
    def __init__(self,owner,durability=-1,isBound=0,identification=1,strengthen=0,workout=0):
        '''初始化物品附加属性
        @param selfExtraAttributeId: []int list 物品自身附加属性
        @param dropExtraAttributeId: []int list 物品掉落时的附加属性 
        @param durability: int 物品的耐久度
        @param identification: int 物品的辨识状态   0:未辨识  1:辨识 
        '''
        Component.__init__(self,owner)
        self.durability = durability #当前耐久
        self.isBound = isBound
        self._identification = identification
        self.strengthen=strengthen #强化等级
        self.workout=workout #成长度
        self.extPhysicalAttack=0 #附加物理攻击力
        self.extPhysicalDefense=0 #附加物理防御力
        self.extMagicAttack=0 #附加魔法攻击力
        self.extMagicDefense=0 #附加魔法防御力
        self.extSpeedAdditional=0#附加攻速
        self.extHpAdditional=0#附加最大血量
    
    def getDurability(self):
        '''获取物品的耐久度'''
        return self.durability
    
    def setDurability(self,durability):
        '''设置物品的耐久度
        @param durability: int 物品的耐久度
        '''
        self.durability = durability
        
    def updateDurability(self,durability):
        '''更新物品的耐久度
        @param durability: int 物品的耐久度
        '''
        self.setDurability(durability)
        dbaccess.updateItemInfo(self._owner.baseInfo.id, 'durability', durability)
        
        
    def getStrengthen(self):
        '''获取物品的强化等级'''
        return self.strengthen
    
    def setStrengthen(self,count):
        self.strengthen = count
        self._owner.updateFJ()
    
    def updateStrengthen(self,count):
        '''更新物品的强化
        @param count: int 强化等级
        '''
        if self.strengthen!=count:
            self.strengthen = count
            result=dbaccess.updateItemInfo(self._owner.baseInfo.id, 'strengthen', count)
            if not result:
                log.err(u'强化后更改数据库数据的时候错误 item.attribute.updateStrengthen(count=%s)物品id=%s'%(count,self._owner.baseInfo.id))
            else:
                self._owner.updateFJ()
            
    def getWorkout(self):
        '''获取物品的成长度'''
        return self.workout
    
    def updateWorkout(self,count):
        '''更新物品的成长度
        @param count: int 物品的成长度
        '''
        self.workout=count
        dbaccess.updateItemInfo(self._owner.baseInfo.id, 'workout', count)
        
    def getExtAttack(self):
        '''获取物品附加攻击力'''
        return self.extAttack
        
    def getIsBound(self):
        '''获取物品绑定状态
        '''
        return self.isBound
    
    def setIsBound(self,isBound):
        '''设置物品绑定状态
        @param isBound: int(0,1) 物品绑定状态
        '''
        self.isBound = isBound
        
    def updateIsBound(self,isBound):
        '''更新物品绑定状态
        '''
        self.isBound = isBound
        dbaccess.updateItemInfo(self._owner.baseInfo, 'isBound', isBound)
        
    def getIdentification(self):
        '''获取物品辨识状态'''
        return self._identification
    
    def setIdentification(self,identification):
        '''设置物品辨识状态
        '''
        self._identification = identification
        
    def updateIdentification(self,identification):
        '''更新物品的辨识状态'''
        self._identification = identification
        dbaccess.updateItemInfo(self._owner.baseInfo, 'identification', identification)
        
        