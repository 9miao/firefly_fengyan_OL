#coding:utf8
'''
Created on 2011-5-3

@author: sean_lan
'''
from app.scense.component.baseInfo.BaseInfoComponent import BaseInfoComponent

class GuildBaseInfoComponent(BaseInfoComponent):
    '''行会的基础信息组件'''
    def __init__(self,owner,id=0,name=''):
        BaseInfoComponent.__init__(self, owner,id,name)
        
    def getName(self):
        '''获取行会名称'''