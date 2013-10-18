#coding:utf8
'''
Created on 2011-8-18
排队大厅
@author: lan
'''
from app.scense.core.singleton import Singleton
from app.scense.core.queueHall.AreaHall import AreaHall

class Hall:
    '''大厅单例'''
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''
        @param areahalls: dict 区域大厅
        '''
        self.areahalls = {}
        self.inintAreahalls()
        
    def inintAreahalls(self):
        '''初始化区域大厅'''
        areaIdList = [1,2,3]
        for areaId in areaIdList:
            self.areahalls[areaId] = AreaHall(areaId)
        
    def getAreaHallById(self,areaId):
        '''根据区域ID获取区域大厅实例'''
        return self.areahalls.get(areaId,None)
        