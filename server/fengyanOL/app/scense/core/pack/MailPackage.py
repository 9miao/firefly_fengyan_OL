#coding:utf8
'''
Created on 2011-4-1

@author: sean_lan
'''
from app.scense.component.pack.BasePackage import BasePackage

class MailPackage(BasePackage):
    '''邮件包裹栏
    '''
    def __init__(self, size = 4):
        '''
        @param size: int 包裹的大小
        '''
        BasePackage.__init__(self, size)