#coding:utf8
'''
Created on 2011-6-28

@author: lan
'''
from app.scense.component.Component import Component

class CharacterRankComponent(Component):
    '''角色军衔组件
    @param _glory: int 角色的荣耀值，影响角色的军衔
    @param rank: int 角色的军衔  
    '''
    def __init__(self,owner):
        '''角色军衔初始化'''
        Component.__init__(self, owner)
        self._glory = 0
        self._rank = 0
        
    def getGlory(self):
        '''获取角色的荣耀值'''
        return self._glory
    
    def setGlory(self,glory):
        '''设置角色的荣耀值'''
        self._glory = glory
        
    def updateGlory(self,glory):
        '''更新角色的荣耀值'''
        self._glory = glory
    
    def getRank(self):
        '''获取角色的军衔'''
        return self._rank
    
    def getRankName(self):
        '''获取军衔名称'''
        return u'浮云'
        
    def setRank(self,rank):
        '''设置角色的军衔'''
        self._rank = rank
        
    def updateRank(self,rank):
        '''更新角色的军衔'''
        self._rank = rank
    
    
    
    
