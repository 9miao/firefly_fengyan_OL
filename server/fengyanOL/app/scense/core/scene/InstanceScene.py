#coding:utf8
'''
Created on 2011-11-21

@author: lan
'''
from twisted.python import log
from app.scense.utils.dbopera import dbScene
from app.scense.core.scene.baseScene import BaseScene

class InstanceScene(BaseScene):
    '''副本场景'''
    
    def __init__(self,id,group = 0):
        '''
        @param id: int 公共场景的id
        '''
        BaseScene.__init__(self, id, type = 2,group = group)
        
    def initSceneInfo(self):
        '''按照公共场景初始化场景信息'''
        sceneInfo = dbScene.ALL_INSTANCESCEN_INFO.get(self._id,{})
        if not sceneInfo:
            log.err('instance scene %d does not exist'%self._id)
            return
        self._name = sceneInfo['name']
        self._type = sceneInfo['type']
        self._levelRequired = sceneInfo['levelRequired']
        self._memberRequired = sceneInfo['memberRequired']
        self._height = sceneInfo['areaHeight']
        self._width = sceneInfo['areaWidth']
        self._init_X = sceneInfo['initPointX']
        self._init_Y = sceneInfo['initPointY']
        self._resourceid = sceneInfo['resourceid']
        self._npclist = eval('['+sceneInfo['npclist']+']')
        self._portals = eval('['+sceneInfo['portals']+']')
        monstersInfo = eval('['+sceneInfo['monsters']+']')
        for monster in monstersInfo:
            templateId = monster.get('id')
            positionX,positionY = monster.get('position')
            matrixId = monster.get('matrixId',100009)
            rule = monster.get('rule',[])
            self.produceMonster(templateId, positionX=positionX,\
                                 positionY=positionY,matrixId=matrixId,\
                                 rule = rule)
        
        
        
        