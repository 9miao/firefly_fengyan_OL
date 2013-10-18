#coding:utf8
'''
Created on 2011-7-11

@author: SIOP_09
'''
from app.scense.utils import dbaccess
class InstanceActivation:
    '''
            副本激活类
    '''


    def __init__(self,id):
        '''初始化副本激活类
        @param id: int 副本激活类的Id        
        '''
        self.id=id
        self.characterlevel=-1 #角色等级限制
        self.guildlevel=-1 #行会等级限制
        self.successid=-1 #角色成就限制
        self.instanceid=-1 #已通关的副本Id
        self.accepttaskid=-1 #已接受的任务Id
        self.finishtaskid=-1 #已完成的任务Id
        self.itemsid=-1 #已获得的物品id
        self.inintInstanceActivation(id)
    def inintInstanceActivation(self,id):
        '''初始化副本激活类'''
        info=dbaccess.getInstanceActivationInfo('id', id)
        if not info:
            return
        self.characterlevel=info['characterlevel']
        self.guildlevel=info['guildlevel']
        self.successid=info['successid']
        self.instanceid=info['instanceid']
        self.accepttaskid=info['accepttaskid']
        self.finishtaskid=info['finishtaskid']
        self.itemsid=info['itemsid']