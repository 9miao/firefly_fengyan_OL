#coding:utf8
'''
Created on 2011-7-11

@author: SIOP_09
'''
from app.scense.utils import dbaccess
class InstanceClose:
    '''
            副本激活类
    '''


    def __init__(self,id):
        '''初始化副本激活类
        @param id: int 副本激活类的Id        
        '''
        self.id=id
        self.attackboss=-1 #击败某个boss
        self.taskid=-1 #完成某项任务
        self.inintInstanceClose(id)
    def inintInstanceClose(self,id):
        '''初始化副本激活类'''
        info=dbaccess.getInstanceCloseInfo('id', id)
        if not info:
            return 
        self.attackboss=info['attackboss']
        self.taskid=info['taskid']