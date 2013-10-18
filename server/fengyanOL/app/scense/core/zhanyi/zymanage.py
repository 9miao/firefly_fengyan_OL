#coding:utf8
'''
Created on 2013-1-8
战役管理
@author: lan
'''
from app.scense.core.singleton import Singleton
from app.scense.utils.dbopera import db_zhanyi
from zhanyi import ZhanYi


class ZYManage:
    '''战役管理器
    '''
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化
        '''
        self.zhanyiSet = {}#所以的章节
        self.initData()
        
    def initData(self):
        '''初始化所以战役的信息
        '''
        for zhanyiID in db_zhanyi.ALL_ZHANYI_INFO:
            zhanyi = ZhanYi(zhanyiID)
            self.zhanyiSet[zhanyiID] = zhanyi
        
    def getZhanYiInfoById(self,yid):
        '''根据战役的ID获取战役的信息
        '''
        zhanyi = self.zhanyiSet.get(yid)
        return zhanyi
        
        
        
        
        
        