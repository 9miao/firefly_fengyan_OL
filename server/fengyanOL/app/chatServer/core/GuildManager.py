#coding:utf8
'''
Created on 2011-2-14

@author: sean_lan
'''
from firefly.utils.singleton import Singleton


class GuildManager:
    '''行会成员单例管理'''
    __metaclass__ = Singleton

    def __init__(self):
        self.g={}#key:国 id value:set([角色动态id,角色动态id,角色动态id,角色动态id,角色动态id])


    def getpidListBygid(self,gid):
        '''根据行会id获取角色id列表'''
        if self.g.has_key(gid):
            return self.g[gid]
        return []
    
    def getdtidListBygid(self,gid):
        '''根据行会id获取角色动态太id列表'''
        if self.g.has_key(gid):
            return self.g.get(gid)
    

    def add(self,pid,gid):
        '''把角色加入行会
        @param pid: int 角色动态id
        @param gid: int 行会id
        '''
        if not self.g.has_key(gid):
            self.g[gid]=set([])
        self.g.get(gid).add(pid)#添加角色到行会中
        
    def delete(self,pid,gid):
        '''把角色从行会中删除
        @param pid: int 角色动态id
        @param gid: int 行会id
        '''
        if self.g.has_key(gid):#如果有这个行会
            if pid in self.g[gid]:#如果行会中有这个角色
                self.g[gid].remove(pid)
        
        
            
    
            