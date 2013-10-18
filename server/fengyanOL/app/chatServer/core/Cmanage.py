'''
Created on 2012-6-13

@author: jt
'''
from firefly.utils.singleton import Singleton

class Cmanage(object):
    '''�����¼
    '''
    __metaclass__ = Singleton


    def __init__(self):
        '''
        Constructor
        '''
        self.manage={}
        
        