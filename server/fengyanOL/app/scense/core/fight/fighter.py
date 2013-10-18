#coding:utf8
'''
Created on 2011-10-7
战斗成员类
@author: lan
'''
class Fighter(object):
    '''战斗成员'''
    
    def __init__(self):
        '''初始化战斗成员'''
        self.__baseAttribute = {}#角色的静态信息
        self.__buffMachine = None
        self.__owner = None