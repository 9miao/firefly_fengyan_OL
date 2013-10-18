#coding:utf8
'''
Created on 2012-3-19
场景服务器管理者
@author: Administrator
'''
from firefly.utils.singleton import Singleton
from twisted.internet import reactor
import subprocess
from twisted.python import log

reactor = reactor
Scenes = [1000]
UP = 80#每个场景服承载的角色上限

class  SceneSer:
    
    def __init__(self,sceneId):
        self.id = sceneId
        self._clients = set()
        
    def addClient(self,clientId):
        '''添加一个客户端到场景服务器'''
        self._clients.add(clientId)
        
    def dropClient(self,clientId):
        '''移除一个客户端'''
        self._clients.remove(clientId)
        
    def getClientCnt(self):
        '''获取场景中的客户端数量'''
        return len(self._clients)

class SceneSerManager:
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化'''
        self._scenesers = {}
        reactor.callLater(1,self.initScenes)
        
    def initScenes(self):
        '''初始化所有的公共场景'''
        pass
#        for sceneId in Scenes:
#            self.startSceneServer(sceneId)
        
    def addSceneSer(self,sceneId):
        '''添加一个场景服务器'''
        sceneser = SceneSer(sceneId)
        self._scenesers[sceneser.id] = sceneser
        
    def startSceneServer(self,sceneId):
        '''开启一个场景服务器'''
        from app.gate.utils import dbaccess
        servername = dbaccess.servername
        subprocess.Popen('python ./servers/SceneServer/src/startSceneServer.pyc \
        -named sceneserver_%d -servername %s'%(sceneId,servername),shell=True) 
        
    def getSceneServerById(self,sceneId):
        '''返回场景服务的实例'''
        return self._scenesers.get(sceneId)
        
    def addClient(self,sceneId,clientId):
        '''添加一个客户端'''
        sceneser = self.getSceneServerById(sceneId)
        if not sceneser:
            return False
        sceneser.addClient(clientId)
        return True
    
    def dropClient(self,sceneId,clientId):
        '''清除一个客户端'''
        sceneser = self.getSceneServerById(sceneId)
        if sceneser:
            try:
                sceneser.dropClient(clientId)
            except Exception,e:
                msg = "sceneId:%d-------clientId:%d"%(sceneId,clientId)
                log.err(msg)
        
    def getAllClientCnt(self):
        '''获取公共场景中所有的客户端数量'''
        return sum([ser.getClientCnt() for ser in self._scenesers])
    
    def getBsetScenNodeId(self,placeId):
        '''获取最佳的新手村服务的ID
        '''
        targetnode = placeId/100*100
        canuserlist = [sser for sser in self._scenesers.values() if \
                       sser.id/100*100==targetnode and sser.getClientCnt()< UP]
        if canuserlist:
            return 200000 + canuserlist[0].id
        else:
            serverlist = [sser for sser in self._scenesers.values() if sser.id/100*100==targetnode]
            slist = sorted(serverlist,reverse=False,key = lambda sser:sser.getClientCnt())
            if slist:
                return slist[0].id + 200000
            return 200000 + placeId
        
        