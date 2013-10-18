#coding:utf8
'''
Created on 2011-4-2

@author: sean_lan
'''

class DropConfig(object):
    '''
    掉落生成配置
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._primaryItemId = 1 #直接指定物品ID:  物品1为指定物品 = 1
        self._primaryItemRate = 0 #直接指定物品机率  = 0
        self._primaryItemAttributeID = 0 #直接指定物品固定附加属性id = 0
        self._primaryItemAttributeLV = -1 #固定附加属性 LV -1 时忽略此值,使用上下限 = -1
        self._primaryItemAttributeLowerBound = 0 #直接指定物品附加属性下限 = 0
        self._primaryItemAttributeUpperBound = 0 #直接指定物品附加属性上限 = 0
        self._primaryItemAttributeRate = -1 #直接指定掉落物品附加属性几率 
        self._secondaryItemRate = 0 #备用掉落的掉落的几率 = 0
        self._secondaryItemAttributeID = 0 #备用掉落的附加属性ID = 0
        self._secondaryItemAttributeLV = -1 #备用掉落的物品附加属性等级 = -1
        self._secondaryItemAttributeLowerBound = 0 #备用掉落物品附加属性下限
        self._secondaryItemAttributeUpperBound = 0 #备用掉落物品附加属性上限
        self._secondaryItemLevelLowerBound = 0 #备用掉落的等级下限 = 0
        self._secondaryItemLevelUpperBound = 0 #备用掉落等级上限 = 0
        self._secondaryItemTypeFilter = 0 #备用掉落物品类型过滤 = 0
        
    def getPrimaryItemId(self):
        return self._primaryItemId 
    
    def setPrimaryItemId(self,primaryItemId):
        self._primaryItemId = primaryItemId
        
    def getPrimaryItemRate(self,primaryItemRate):
        return self._primaryItemRate
    
    def setPrimaryItemRate(self,primaryItemRate):
        self._primaryItemRate = primaryItemRate
        
    def getPrimaryItemAttributeID(self):
        return self._primaryItemAttributeID
    
    def setPrimaryItemAttributeID(self,primaryItemAttributeID):
        self._primaryItemAttributeID = primaryItemAttributeID
        
    def getPrimaryItemAttributeLV(self):
        return self._primaryItemAttributeLV
    
    def setPrimaryItemMFLV(self,primaryItemAttributeLV):
        self._primaryItemAttributeLV = primaryItemAttributeLV
        
    def getPrimaryItemAttributeLowerBound(self):
        return self._primaryItemAttributeLowerBound
    
    def setPrimaryItemAttributeLowerBound(self,bound):
        self._primaryItemAttributeLowerBound = bound
        
    def getPrimaryItemAttributeUpperBound(self):
        return self._primaryItemAttributeUpperBound
    
    def setPrimaryItemAttributeUpperBound(self,primaryItemAttributeUpperBound):
        self._primaryItemAttributeUpperBound = primaryItemAttributeUpperBound
        
    def getPrimaryItemAttributeRate(self):
        return self._primaryItemAttributeRate
    
    def setPrimaryItemAttributeRate(self,rate):
        self._primaryItemAttributeRate = rate
        
    def getSecondaryItemRate(self):
        return self._secondaryItemRate
    
    def setSecondaryItemRate(self,secondaryItemRate):
        self._secondaryItemRate = secondaryItemRate
    
    def getSecondaryItemAttributeID(self):
        return self._secondaryItemAttributeID
    
    def setSecondaryItemAttributeID(self,secondaryItemAttributeID):
        self._secondaryItemAttributeID = secondaryItemAttributeID
        
    def getSecondaryItemAttributeLV(self):
        return self._secondaryItemAttributeLV
    
    def setSecondaryItemAttributeLV(self,secondaryItemAttributeLV):
        self._secondaryItemAttributeLV = secondaryItemAttributeLV
        
    def getSecondaryItemLevelLowerBound(self):
        return self._secondaryItemLevelLowerBound
    
    def setSecondaryItemLevelLowerBound(self,secondaryItemLevelLowerBound):
        self._secondaryItemLevelLowerBound = secondaryItemLevelLowerBound
        
    def getSecondaryItemLevelUpperBound(self):
        return self._secondaryItemLevelUpperBound
    
    def setSecondaryItemLevelUpperBound(self,secondaryItemLevelUpperBound):
        self._secondaryItemLevelUpperBound = secondaryItemLevelUpperBound
        
    def getSecondaryItemTypeFilter(self):
        return self._secondaryItemTypeFilter
    
    def setSecondaryItemTypeFilter(self,secondaryItemTypeFilter):
        self._secondaryItemTypeFilter = secondaryItemTypeFilter
    
    