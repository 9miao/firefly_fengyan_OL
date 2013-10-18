#coding:utf8
'''
Created on 2012-12-6
地图管理器
@author: lan
'''

from twisted.python import log
from app.scense.core.singleton import Singleton
from app.scense.core.map.CityMap import CityMap
from app.scense.utils.dbopera import dbMap

class MapManager:
    '''城镇场景管理器
    '''
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化区域管理器
        '''
        self._maps = {}  #存储地图中所有的区域实例
        self.initAllMaps()
        
    def initAllMaps(self):
        '''初始化所有的地图
        '''
        for mapid in dbMap.ALL_MAP_INFO.keys():
            scene = CityMap(mapid)
            self.addMap(scene)
            
    def addMap(self,scene):
        '''添加一个场景到场景管理器中
        @param scene: Scene object 场景实例
        '''
        sceneId = scene.getID()
        if self._maps.has_key(sceneId):
            log.err("Scene ID conflict: %d"%sceneId)
            return
        self._maps[sceneId] = scene
        
    def getMapId(self,sceneId):
        '''根据场景的ID获取场景实例
        '''
        return self._maps.get(sceneId,None)
        
    def dropMap(self,scene):
        '''删除场景实例
        @param scene: Scene object 场景实例
        '''
        sceneId = scene.getID()
        try:
            del self._maps[sceneId]
        except Exception,e:
            log.err("%s!Scene ID %d"%(e,sceneId))
            
    def dropMapId(self,sceneId):
        '''根据场景Id移除场景
        @param sceneId: int 场景的ID
        '''
        try:
            del self._maps[sceneId]
        except Exception,e:
            log.err("%s!Scene ID %d"%(e,sceneId))
        
    def pushAllSceneInfo(self,rate):
        '''推送所有场景中的信息
        @param rate: int 移动的频率
        '''
        for scene in self._maps.values():
            scene.pushSceneInfo(rate)
            
    def produceMonster(self):
        '''生成怪物
        '''
        for scene in self._maps.values():
            scene.produce()
        
    
    
            
            