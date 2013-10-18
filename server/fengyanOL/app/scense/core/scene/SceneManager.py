#coding:utf8
'''
Created on 2011-11-18

@author: lan
'''

from twisted.python import log
from app.scense.core.singleton import Singleton

class SceneManager_new:
    '''城镇场景管理器
    '''
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化区域管理器
        '''
        self._scenes = {}  #存储地图中所有的区域实例
        
    def addScene(self,scene):
        '''添加一个场景到场景管理器中
        @param scene: Scene object 场景实例
        '''
        sceneId = scene.getID()
        if self._scenes.has_key(sceneId):
            log.err("Scene ID conflict: %d"%sceneId)
            return
        self._scenes[sceneId] = scene
        
    def getSceneById(self,sceneId):
        '''根据场景的ID获取场景实例
        '''
        return self._scenes.get(sceneId,None)
            
    def dropScene(self,scene):
        '''删除场景实例
        @param scene: Scene object 场景实例
        '''
        sceneId = scene.getID()
        try:
            del self._scenes[sceneId]
        except Exception,e:
            log.err("%s!Scene ID %d"%(e,sceneId))
            
    def dropSceneById(self,sceneId):
        '''根据场景Id移除场景
        @param sceneId: int 场景的ID
        '''
        try:
            del self._scenes[sceneId]
        except Exception,e:
            log.err("%s!Scene ID %d"%(e,sceneId))
        
    def pushAllSceneInfo(self,rate):
        '''推送所有场景中的信息
        @param rate: int 移动的频率
        '''
        for scene in self._scenes.values():
            scene.pushSceneInfo(rate)
    
    
    
    