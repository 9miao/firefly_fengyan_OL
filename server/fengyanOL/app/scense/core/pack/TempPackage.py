#coding:utf8
'''
Created on 2011-3-29

@author: sean_lan
'''
from app.scense.component.pack.BasePackage import BasePackage

class TempPackage(BasePackage):
    '''临时包裹栏
    '''
    def __init__(self, size):
        '''
        @param size: int 包裹的大小
        '''
        BasePackage.__init__(self, size)
        self.setPackageType(1)
    
    