#coding:utf8
'''
Created on 2012-2-21
副本组理器
@author: jt
'''
from app.scense.core.singleton import Singleton
from app.scense.utils.dbopera import dbInstanceGroup, dbPublicscene
from twisted.python import log

class InstanceGroupManage(object):
    '''副本组管理器'''
    __metaclass__ = Singleton

    def __init__(self):
        '''初始化'''
        self.leveltoid={} # 根据副本id查找副本组id key:副本id,value:副本组id
        self.csztoid={}#根据传送阵id查找副本组id    key：传送阵id,value:副本组id
        self.idtoinfo={}#根据副本组id获取副本组信息        key:副本组id，value:副本信息
        self.idtocity={}#根据副本组id获取城市id     key:副本组id,value：城市id
        self.initGroup()#初始化副本组
        self.a()
        
    def initGroup(self):
        data=dbInstanceGroup.getAllInfo() #副本组信息
        for item in data:
            id=item['id']#副本组id
            csz=item['csz']#传送阵id
            a=item['levela']#简单难度副本id
            b=item['levelb']#中等难度副本id
            c=item['levelc']#困难难度副本id
            price=item['price']#单次通关奖励
            max=item['maxcost'] #最高奖励
            self.leveltoid[a]=id
            self.leveltoid[b]=id
            self.leveltoid[c]=id
            if not self.csztoid.has_key(csz):
                self.csztoid[csz]=[]
            self.csztoid[csz].append(id) #向传送阵添加副本组id
            self.idtoinfo[id]=item #添加副本组信息
            
            
            
            
    def a(self):
        dataList=dbPublicscene.Allinfo.values()#获取所有城镇的信息
        for item in dataList: #迭代所有城镇信息
            pList=eval("["+str(item['portals'])+"]")
            if len(pList)<1: #如果城镇里面没有副本
                continue
            for it in pList: #迭代所有传送门id
                groupList=self.getInstanceGroupBycszid(it) #获得传送门通往的所有副本组信息
                for i in groupList: #遍历所有副本组信息  i['id']:副本组id
#                    item['id']#城市id
#                    i['id']#副本组id
                    self.idtocity[i['id']]=item['id']
    
    
    def getcityidBygroupid(self,instanceid):
        '''根据副本id获取城市id'''
        groupid=self.getFristInstanceBy(instanceid)
        if self.idtocity.has_key(groupid):
            return self.idtocity[groupid]
        return 0
            
                
    def getInstanceGroupByid(self,id):
        '''根据副本组id获取副本信息'''
        return self.idtoinfo[id] #return {id:,csz:,levela:price:maxcost:}
    
    def getInstanceidByGroupid(self,groupid):
        '''根据副本组id获取副本id'''
        gin= self.idtoinfo[groupid]
        return gin['levela']
    
    def getHardByinstanceid(self,id):
        '''根据副本id获取副本难度 0普通 1困难 2英雄'''
        groupid=self.getFristInstanceBy(id)
        data=self.getInstanceGroupByid(groupid)
        if data:
            if data['levela']==id:
                return 0
            elif data['levelb']==id:
                return 1
            elif data['levelc']==id:
                return 2
        return -1
    
    
    def getFristInstanceBy(self,id):
        '''根据副本id获取副本组id'''
        if self.leveltoid.has_key(id):
            return self.leveltoid[id] #return int
        else:
            log.err(u"根据副本id获取副本组id错误 - 副本id %s"%id)
            return False
        
#    def getInstanceidGroupByid(self,id):
#        '''根据副本id获取副本组id'''
#        return self.getFristInstanceBy(id)
    
    def getInstanceGroupBycszid(self,id):
        '''根据传送门id获取副本组列表'''
        cList=[] #副本组信息
        for i in self.csztoid[id]: #i副本组id
            cList.append(self.getInstanceGroupByid(i))
        return cList
            
    