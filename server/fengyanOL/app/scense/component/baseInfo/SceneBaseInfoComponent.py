#coding:utf8
'''
Created on 2011-4-6

@author: sean_lan
'''
from app.scense.component.baseInfo.BaseInfoComponent import BaseInfoComponent

class SceneBaseInfoComponent(BaseInfoComponent):
    '''场景的基础属性组件
    '''
    def __init__(self,owner,sid,name = '',sceneType = 0,areaHeight = 570,areaWidth = 1000,adjacencyId=[]):
        '''初始化
        @param id: int 场景的id
        @param name:string 场景的名称
        @param sceneType: int 场景的类型
        @param areaHeight: int 场景的高度限制
        @param areaWight: int 场景的宽度限制
        '''
        BaseInfoComponent.__init__(self, owner, sid, name)
        self.sceneType = sceneType
        self.areaHeight = areaHeight
        self.areaWidth = areaWidth
        self.adjacencyId = adjacencyId
        self.initialPosition = (300,400)
        
    def getInitiaPosition(self):
        '''获取地图初始化点'''
        return self.initialPosition
        
    def setInitiaPosition(self,position):
        '''设置地图初始化点'''
        self.initialPosition = position
        
    def getSceneType(self):
        '''获取场景类型
        '''
        return self.sceneType
    
    def setSceneType(self,sceneType):
        '''设置场景类型
        '''
        self.sceneType = sceneType
        
    def getAreaHeight(self):
        '''获取场景高度'''
        return self.areaHeight
    
    def setAreaHeight(self,areaHeight):
        '''设置场景高度'''
        self.areaHeight = areaHeight
        
    def getAreaWidth(self):
        '''获取场景宽度'''
        return self.areaWidth
    
    def setAreaWidth(self,areaWidth):
        '''设置场景宽度'''
        self.areaWidth = areaWidth
        
    def getAdjacencyId(self):
        '''获取邻接场景的模板id
        '''
        return self.adjacencyId
    
    def setAdjacencyId(self,adjacencyId):
        '''设置邻接场景的模板的id
        @param adjacencyId: []int 邻接场景的模板id列表
        '''
        self.adjacencyId = adjacencyId
        
    