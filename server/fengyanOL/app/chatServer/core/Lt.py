#coding:utf8
'''
Created on 2011-11-29
聊天内容管理器
@author: SIOP_09
'''
from firefly.utils.singleton import Singleton



class Lt(object):
    '''记录聊天内容'''
    __metaclass__ = Singleton

    def __init__(self):
        self.info=""
        
    def add(self,uid,uname,context):
        '''添加聊天记录
        @param uid: string 角色主键id
        @param uname: string 角色名称
        @param context: string 聊天内容
        '''
        self.info+="( %s )%s: %s"%(uid,uname,context)+"<br/> "
    def get(self):
        '''获取聊天记录'''
        val= self.info
        self.info=""
        return val
        
    