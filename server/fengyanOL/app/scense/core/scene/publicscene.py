#coding:utf8
'''
Created on 2011-11-17
公共场景类
@author: lan
'''
from twisted.python import log
from app.scense.utils.dbopera import dbScene
from app.scense.core.scene.baseScene import BaseScene

class PublicScene(BaseScene):
    '''公共场景'''
    
    def __init__(self,id):
        '''
        @param id: int 公共场景的id
        '''
        BaseScene.__init__(self, id, type = 1)
        
    def initSceneInfo(self):
        '''按照公共场景初始化场景信息'''
        sceneInfo = dbScene.ALL_PUBLICSCENE_INFO.get(self._id,{})
        if not sceneInfo:
            log.err('public scene %d does not exist'%self._id)
            return
        self._name = sceneInfo['name']
        self._type = sceneInfo['type']
        self._levelRequired = sceneInfo['levelRequired']
        self._memberRequired = sceneInfo['memberRequired']
        self._height = sceneInfo['height']
        self._width = sceneInfo['width']
        self._init_X = sceneInfo['init_X']
        self._init_Y = sceneInfo['init_Y']
        self._resourceid = sceneInfo['resourceid']
        self._npclist = eval('['+sceneInfo['npclist']+']')
        self._portals = eval('['+sceneInfo['portals']+']')
        
    
        
        