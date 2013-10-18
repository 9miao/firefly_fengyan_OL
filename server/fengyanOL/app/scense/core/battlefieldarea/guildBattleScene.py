#coding:utf8
'''
Created on 2011-9-24
战场（行会战场景）
@author: lan
'''
from app.scense.component.scene.baseSceneComponet import BaseSceneComponent

class GuildBattleScene(BaseSceneComponent):
    '''行会战场景'''
    
    def __init__(self,id,owner):
        '''初始化行会战场景
        @param id: int 场景的id
        '''
        BaseSceneComponent.__init__(self,id, owner)
        self.setPkType(4)#场景战斗类型为国战斗
        
    def FightInScene(self,targetID,now_X):
        '''行会战场景战斗'''
        
    def pushSceneInfo(self):
        '''推送场景信息'''
        pass
    
    