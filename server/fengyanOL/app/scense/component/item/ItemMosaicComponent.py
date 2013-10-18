#coding:utf8
'''
Created on 2012-5-18
物品镶嵌信息
@author: Administrator
'''
from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbItems
from app.scense.util import gs
from app.scense.core.language.Language import Lg

class ItemMosaicComponent(Component):
    """物品镶嵌信息
    """
    
    def __init__(self,owner):
        '''初始化
        @param slot_1: int 插槽1的宝石ID
        @param slot_2: int 插槽1的宝石ID
        @param slot_3: int 插槽1的宝石ID
        @param slot_4: int 插槽1的宝石ID
        '''
        Component.__init__(self, owner)
        self.slot_1 = 0
        self.slot_2 = 0
        self.slot_3 = 0
        self.slot_4 = 0
        
    def issolt(self):
        '''是否已经镶嵌'''
        if (self.slot_1+self.slot_2+self.slot_3+self.slot_4)>0:
            return True
        return False
        
    def setSlot(self,slot_1,slot_2,slot_3,slot_4):
        '''设置插槽
        '''
        self.slot_1 = slot_1
        self.slot_2 = slot_2
        self.slot_3 = slot_3
        self.slot_4 = slot_4
        
    def getMosaicInfo(self):
        '''获取镶嵌的信息'''
        slotinfo = {}
        if self._owner.baseInfo.getItemBodyType()==-1:
            return slotinfo
        for position in range(1,5):
            gemtemplate = getattr(self,'slot_%d'%position)
            slotinfo['xqItemId%d'%position] = gemtemplate
            if gemtemplate:
                slotinfo['xqDes%d'%position] = dbItems.ALL_GEMINFO[gemtemplate]['effectdesc']
            else:
                slotinfo['xqDes%d'%position] = Lg().g(353)
        return slotinfo
            
    def getSlotAttr(self):
        '''获取插槽中宝石属性加成'''
        attr = {}
        if self.slot_1:
            attr = gs.addDict(eval(dbItems.ALL_GEMINFO[self.slot_1]['effect']),attr)
        if self.slot_2:
            attr = gs.addDict(eval(dbItems.ALL_GEMINFO[self.slot_2]['effect']),attr)
        if self.slot_3:
            attr = gs.addDict(eval(dbItems.ALL_GEMINFO[self.slot_3]['effect']),attr)
        if self.slot_4:
            attr = gs.addDict(eval(dbItems.ALL_GEMINFO[self.slot_4]['effect']),attr)
        return attr
        
    def checkCanMosaic(self,gemId,position):
        '''检测是否能镶嵌
        '''
        if getattr(self,'slot_%d'%position):
            return {'result':False,'message':Lg().g(354)}#镶嵌位已经镶嵌了宝石
        gemtype = dbItems.ALL_GEMINFO[gemId]['type']
        for pp in range(1,5):#检测是否有相同类型的宝石
            gemtemplate = getattr(self,'slot_%d'%pp)
            if not gemtemplate:
                continue
            thistype = dbItems.ALL_GEMINFO[gemtemplate]['type']
            if thistype == gemtype:
                return {'result':False,'message':Lg().g(355)}
        return {'result':True}
        
    def Mosaic(self,gemId,position):
        '''镶嵌
        @param gemId: int 宝石的ID
        @param position: int 镶嵌的位置
        '''
        result = self.checkCanMosaic(gemId, position)
        if not result.get('result'):
            return result
        setattr(self,'slot_%d'%position,gemId)
        dbItems.updateItemInfo(self._owner.baseInfo.id, 'slot_%d'%position, gemId)
        return {'result':True}
        
    def removal(self,position):
        '''摘除
        @param position: int 摘除的位置
        @return: int 摘除宝石的ID
        '''
        gemtemplate = getattr(self,'slot_%d'%position)
        if not gemtemplate:
            return 0
        setattr(self,'slot_%d'%position,0)
        dbItems.updateItemInfo(self._owner.baseInfo.id, 'slot_%d'%position,0)
        return gemtemplate
        
    def getItemGemLevel(self):
        '''获取物品的宝石的最高等级'''
        high = 0
        for pos in [1,2,3,4]:
            gemId = getattr(self,'slot_%d'%pos)
            if gemId:
                nowlevel = dbItems.ALL_GEMINFO[gemId].get('level',0)
                if nowlevel>high:
                    high=nowlevel
            if high>=14:
                break
        return high
        
        
        
