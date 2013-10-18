#coding:utf8
'''
Created on 2011-6-28

@author: lan
'''
from app.scense.component.Component import Component
from app.scense.utils import dbaccess

class CharacterStatusComponent(Component):
    '''角色的状态组件'''
    
    def __init__(self,owner):
        '''初始化角色的状态'''
        Component.__init__(self, owner)
        self._pkStatus = 1      #角色的PK状态 1:和平 2:杀戮
        self._lifeStatus = 1    #角色的生死状态 1:正常 0：死亡  默认为 1 
        self._behaviorStatus = 1      #状态: 1:正常 2:修炼中 3:训练中 6:卖艺中
        self._isLevelUp = 0     #判断是否有升级消息要推送  0：无 1：有
        
    def getPkStatus(self):
        '''获取角色的PK状态'''
        return self._pkStatus
    
    def setPkStatus(self,pkStatus):
        '''设置角色的PK状态'''
        self._pkStatus = pkStatus
        
    def updatePkStatus(self,pkStatus):
        '''更新角色的PK状态'''
        self._pkStatus = pkStatus
        
    def getLifeStatus(self):
        '''获取角色的生死状态'''
        return self._lifeStatus
    
    def setLifeStatus(self,lifeStatus):
        '''设置角色的生死状态'''
        self._lifeStatus = lifeStatus
        
    def updateLifeStatus(self,lifeStatus):
        self._lifeStatus = lifeStatus
        dbaccess.updateCharacter(self._owner.baseInfo.id, 'lifeStatus', lifeStatus)
        
    def getBehaviorStatus(self):
        '''获取角色的行为状态'''
        return self._behaviorStatus
    
    def setBehaviorStatus(self,behaviorStatus):
        '''设置角色的行为状态'''
        self._behaviorStatus = behaviorStatus
        
    def updateBehaviorStatus(self,behaviorStatus):
        '''更新角色的行为状态'''
        self._behaviorStatus = behaviorStatus
    
    def getIsLevelUp(self):
        '''获取是否有升级消息的状态'''
        return self._isLevelUp
    
    def setIsLevelUp(self,isLevelUp):
        '''设置是否有升级消息的状态'''
        self._isLevelUp = isLevelUp
    
    