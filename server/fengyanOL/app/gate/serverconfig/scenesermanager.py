#coding:utf8
'''
Created on 2012-3-8

@author: sean_lan
'''
import subprocess
import os

from firefly.utils.singleton import Singleton

SCENES = [1000,1100,1200,1300,1400,1500]

class SceneSer:
    '''场景服务器'''
    
    def __init__(self,insId):
        '''
        @param _id: int 城镇服务器的ID
        @param _charactercnt: int 当前服务器承载的角色数量
        '''
        self._id = insId
        self._charactercnt = 0
        self._characters = set([])
        
    def addNewClient(self,clientId):
        '''添加一个新的客户端'''
        self._charactercnt += 1
        self._characters.add(clientId)
        
    def dropClient(self,clientId):
        '''移除一个客户端
        @param clientId: int 客户端 的id
        '''
        self._charactercnt -=1
        self._characters.remove(clientId)

class SceneSerManager:
    '''副本服务器管理器'''
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化副本类'''
        self.sceneserspool = {}
        
    def initSceneSerPool(self):
        '''初始化场景服务池'''
        
        
    def addInsServer(self,insser):
        '''添加一个新的副本服务器到副本服务器管理组中'''
        self.sceneserspool[insser.get('insID')] = insser
        self.tag +=1

    def startNewInsServer(self,sceneID):
        '''开启一个新的副本服务器'''
        servername = 'sceneserver_%d'%sceneID
        subprocess.Popen('python '+os.getcwd()+\
                         '/startSceneServer.py -named %s &'%servername,shell=True) 
        self.addInsServer()
        
        
        
        