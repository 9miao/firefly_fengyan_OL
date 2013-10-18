#coding:utf8
'''
Created on 2012-3-19
场景服务器管理者
@author: Administrator
'''
from twisted.python import log
import threading
from firefly.utils.singleton import Singleton
import subprocess

class  Fam:
    """副本"""
    
    def __init__(self,famId,observer):
        '''初始化副本
        @param famId: int 副本的id
        @param observer: FamSer Object 副本观察者
        '''
        self.id = famId
        self.observer = observer
        self._clients = set()
        
    def addClient(self,clientId):
        '''添加一个副本
        @param clientId: int 客户端的ID
        '''
        self._clients.add(clientId)
        
    def dropClinet(self,clientId):
        '''删除一个客户端
        @param clientId: int 客户端的ID
        '''
        self._clients.remove(clientId)
        if self.getClientCnt()==0:
            self.observer.dropFam(self.id)
        
    def getClientCnt(self):
        '''获取副本中客户端的数量'''
        return len(self._clients)

class  FamSer:
    """副本服务"""
    
    MAXFAM = 200 #最大副本管理数量
    ALERTCNT = 100 #警戒值
    
    def __init__(self,famserId,observer):
        '''初始化副本服务
        @param famserId: int 副本服务的编号
        @param observer: FamSerManager Object 副本服务观察者
        '''
        self.id = famserId
        self.observer = observer
        self._fams = {}
        self._lock = threading.RLock()
        
    def addFam(self,fam):
        '''添加一个副本'''
        self._lock.acquire()
        try:
            nowcnt = self.getFamserCnt()
            if nowcnt == self.ALERTCNT:#当达到警戒值时开启新的服务
                self.observer.startFamServer()
            elif nowcnt == self.MAXFAM:
                return False
            self._fams[fam.id] = fam
            return True
        finally:
            self._lock.release()
        
    def getFamserCnt(self):
        '''获取副本服务中的副本的数量'''
        return len(self._fams)
        
    def creatFam(self,clientId):
        '''创建一个副本'''
        fam = Fam(self.observer._famtag,self)
        fam.addClient(clientId)
        result = self.addFam(fam)
        if result:
            self.observer._famtag += 1
            return fam.id
        return fam.id
    
    def leaveFam(self,famId,clientId):
        '''离开副本
        @param famId: int 副本的Id
        @param clientId: int 客户端的Id
        '''
        fam = self._fams.get(famId)
        if fam:
            fam.dropClinet(clientId)
        
    def dropFam(self,famId):
        '''删除一个副本
        @param famId: int 副本的id
        '''
        try:
            del self._fams[famId]
        except Exception as e:
            log.msg(str(e))

class FamSerManager:
    """副本服务管理器"""
    
    __metaclass__ = Singleton
    INITSERCNT = 1#初始化时的副本服务的个数
    
    def __init__(self):
        '''初始化
        @param famtag: int 副本的动态ID
        @param sertag: int 副本服务的动态编号
        '''
        self._famtag = 5000
        self._sertag = 1
        self._famsers = {}
        self.initFams()
        
    def initFams(self):
        '''初始化所有的公共场景'''
        pass
#        for i in range(self.INITSERCNT):
##            self.startFamServer()
        
    def getFamsCnt(self):
        '''获取服务中管理的副本的数量'''
        return len(self._famsers)
        
    def addFamSer(self,famSerId):
        '''添加一个场景服务器'''
        famser = FamSer( famSerId, self)
        self._famsers[famser.id] = famser
        self._sertag += 1
        
    def startFamServer(self):
        '''开启一个场景服务器'''
        from app.gate.utils import dbaccess
        servername = dbaccess.servername
        self._sertag += 1
        subprocess.Popen('python ./servers/SceneServer/src/startSceneServer.pyc \
        -named famserver_%d -servername %s'%(self._sertag,servername),shell=True)
        
    def getPropertyFamser(self):
        '''获取性能最佳的副本服务'''
        _list = self._famsers.keys()
        _list.sort(key= lambda famId: self._famsers[famId].getFamserCnt())
        if not _list:
            return -1
        return _list[0]
        
    def createNewFam(self,clientId):
        '''创建一个新的副本
        @return: 副本服的编号，和副本的ID
        '''
        famserTag = self.getPropertyFamser()
        if famserTag<0:
            return -1,-1
        famser = self._famsers[famserTag]
        famId = famser.creatFam(clientId)
        return famserTag,famId
        
    def leaveFam(self,famserId,famId,clientId):
        '''离开副本'''
        famser = self._famsers[famserId]
        famser.leaveFam(famId,clientId)
        
        
        
        
        
        