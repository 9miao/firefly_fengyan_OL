#coding:utf8
'''
Created on 2011-10-31
物品使用效果类
@author: lan
'''
from app.scense.component.Component import Component

class ItemEffectComponent(Component):
    
    '''
    effect component for item
    '''


    def __init__(self,owner):
        '''
        Constructor
        '''
        Component.__init__(self,owner)
        self._effect = None #物品上所产生的效果
        
    def getEffect(self):
        return self._effect
    
    def setEffect(self,effect):
        self._effect = effect
        
    def getItemEffect(self):
        '''获取物品模版效果'''
        return self._owner.baseInfo.getItemTemplate()['effectId']
    