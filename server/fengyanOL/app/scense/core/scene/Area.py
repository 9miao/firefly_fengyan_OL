#coding:utf8
'''
Created on 2011-6-16

@author: SIOP_09
'''
from app.scense.core.scene.Scene import Scene
from app.scense.utils import dbaccess
class Area(object):
    '''地图区域类 存放场景列表'''


    def __init__(self,id):
        '''初始化Area地图区域
        '''
        self._id=id   #区域Id
        self._name=""  #区域名称
        self._sceneids={} #场景列表
        self.initArea(id);
        
    def getSceneById(self,id):
        '''根据场景Id获取场景实例'''
        if self._sceneids.has_key(id):
            return self._sceneids[id]
        return None
               
    def initArea(self,id):
        '''初始化地图区域
        @param id: int 区域id
        '''
        sceneids=dbaccess.getSceneIdsByAreas(id)

        for item in sceneids:
            self._sceneids[item]=Scene(item)
        
    def getName(self):
        '''获取区域地图名称'''
        return self._name
    def setName(self,name):
        '''设置区域地图名称'''
        self._name=name
        
    def getId(self):
        '''获取区域地图id'''
        return self._id
    def setId(self,id):
        '''设置区域地图id'''
        self._id=id
    
    def getSceneids(self):
        '''获取区域地图的所有场景'''
        return self._sceneids
    