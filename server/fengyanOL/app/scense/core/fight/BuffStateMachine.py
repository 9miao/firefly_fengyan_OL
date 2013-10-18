#coding:utf8
'''
Created on 2011-10-7
buff 状态机
@author: lan
'''

class BuffStateMachine(object):
    '''buff管理'''
    
    __buffPool = {}#buff池
    
    def __init__(self,owner):
        '''初始化状态机'''
        self.__owner = owner
        
    def getNowAttribute(self):
        '''获取当前'''