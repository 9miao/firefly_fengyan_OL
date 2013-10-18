#coding:utf8
'''
Created on 2012-3-23
副本池管理
@author: jt
'''
import copy

class InstancePoolManage():
    '''副本池管理'''


    def __init__(self):
        '''副本池管理'''
        self.list={}
        self.setAllId()
        
    def setAllId(self):
        '''将所有副本放入副本池中'''
        from app.scense.utils.dbopera import dbInstanceInfo
        from app.scense.core.instance.Instance import Instance
        list=dbInstanceInfo.getAllInstanceid()
        for item in list:
            self.list[item]=Instance(item)#实例化副本
            
    def CreateObjByid(self,id):
        '''根据副本id生成副本实例并返回此对象'''
        obj=self.list.get(id,None)#获取副本对象
        if obj:#如果有此副本
            return copy.deepcopy(obj)
        return None
        
    def getObjByid(self,id):
        '''根据副本id获取副本对象'''
        obj=self.list.get(id,None)
        if obj:
            return obj
        return None 