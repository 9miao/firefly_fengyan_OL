#coding:utf8
'''
Created on 2012-12-20
角色的pvp信息
@author: lan
'''
from app.scense.component.Component import Component
import time

class CharacterPVPComponent(Component):
    '''角色的PVP信息
    '''
    
    DELTATIME = 600#战斗CD 90秒
    def __init__(self, owner):
        Component.__init__(self, owner)
        self.pk_lasttime = None
        
    def recordtime(self):
        '''记录战斗时间
        '''
        self.pk_lasttime = time.time()
        
    def checktime(self):
        '''检测战斗时间
        '''
        if not self.pk_lasttime:
            return True
        if time.time() - self.pk_lasttime >= self.DELTATIME:
            return True
        return False
    
    def clearCD(self):
        '''清除PVP战斗CD
        '''
        self.pk_lasttime = None
            
    
    
    
    
