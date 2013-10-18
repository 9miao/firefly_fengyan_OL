#coding:utf8
'''
Created on 2011-4-6

@author: sean_lan
'''
from app.scense.component.Component import Component

class SceneGuildComponent(Component):
    '''场景的行会属性
    '''
    
    def __init__(self,owner,guildId):
        '''初始化
        @param communityId: int 行会的id
        '''
        Component.__init__(self,owner)
        self.guildId = guildId
        
    def getGuildId(self):
        '''获取场景行会属性的行会id
        '''
        return self.unionId
    
    def setGuildId(self,guildId):
        '''设置场景的行会属性id
        @param communityId: int 行会的id
        '''
        self.guildId = guildId
        