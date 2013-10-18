#coding:utf8
'''
Created on 2011-6-14

@author: SIOP_09
'''
from app.scense.core.singleton import Singleton



def getAllId():
        '''获取所有副本的Id序列'''
        from app.scense.utils.dbopera import dbInstanceInfo
        list=[]
        list=dbInstanceInfo.getAllInstanceid()
        return list
    
class InstanceManager(object):
    '''副本管理器
    '''
    __metaclass__ = Singleton

    
    def __init__(self):
        '''初始化场景管理器
        '''
        self._instances={} #存储副本实例 {'动态id':副本实例，'动态id':副本实例}
        self._tag = 1000
#        list=getAllId()  #获取所有副本Id序列
#        for l in list:
#            self._instances[l]={}
        

    def addTranscript(self,transcript):
        '''添加一个副本实例
        @param transcript: Transcript object 副本实例
        '''
        transcript._tag=self.tag
        if self._instances.has_key(transcript._tag):
            raise Exception(u"系统记录冲突，此副本动态id已经存在")
        self._instances[transcript._tag] = transcript
        self.tag+=1
        return self._instances[transcript._tag]
              
    def addInstance(self,id,tag):
        '''根据副本 Id添加副本实例到副本管理器中
        @param id: int 副本的Id
        @param return: 返回副本管理器中的这个副本实例
        '''
        from app.scense.core.instance.Instance import Instance
        instance1=Instance(id)#创建一个副本对象
        if not instance1.templateInfo:            
            return None   #检索数据库中是否有此副本Id
        self._tag += 1
        instance1._tag= self._tag
        if self._instances.has_key(instance1._tag):
            raise Exception(u"系统记录冲突,此副本动态id已经存在")
        self._instances[instance1._tag]=instance1
        return self._instances[instance1._tag]
    
#    def getInstanceById(self,id):
#        return loader.getById("Instances", id, "*")
    
        
    def getInstanceByIdTag(self,tag):
        '''根据副本id及动态Id获取副本实例
        @param id: int 副本的id
        @param tag: int 副本的动态id
        '''
        return self._instances.get(tag,None)
    
    
    def dropInstance(self,transcript):
        '''删除副本实例
        @param transcript: Transcript object 副本实例
        '''
        key = None
        sd=self._instances.get(transcript._tag,None)
        if sd:
            del self._instances[transcript._tag]
            
    def dropInstanceById(self,tag):
        '''根据副本Id删除副本实例
        @param id: int 副本的id
        @param tag: int 副本的动态id  
        '''
        sd=self._instances.get(tag,None)
        if sd:
            del self._instances[tag]
        
    def pushAllInstanceInfo(self,rate):
        '''推送所有副本中的信息
        @param rate: int 移动的频率
        '''
        for item in self._instances.values():
            for l in item._Scenes.values():
                l.pushSceneInfo(rate)
           
        