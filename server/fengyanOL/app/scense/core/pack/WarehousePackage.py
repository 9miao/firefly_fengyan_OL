#coding:utf8
'''
Created on 2011-3-29

@author: sean_lan
'''
from app.scense.component.pack.BasePackage import BasePackage

class WarehousePackage(BasePackage):
    '''仓库
    '''
    def __init__(self,size = 36):
        '''
        @param size: int 包裹的大小
        '''
        BasePackage.__init__(self, size)
        self.setPackageType(2)