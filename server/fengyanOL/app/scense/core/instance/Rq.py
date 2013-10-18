#coding:utf8
'''
Created on 2012-7-11

@author: jt
'''

class Rq():
    '''殖民入侵记录表'''


    def __init__(self,inid,name,pid,pname):
        ''''''
        self.inid=0#副本组或者城市的id
        self.name=u''#副本或者城市的名称
        self.pid=0#占领者的角色id
        self.pname=u''#占领者的角色名称
        self.cgid=0#挑战成功者的角色id
        self.cgname=u''#挑战成功者的角色名称
        self.sb={}#挑战失败者得角色id和名称 key:角色id,value:角色名称
    def addSb(self,tid,tname):
        '''添加挑战失者败记录
        @param tid: int 挑战者id
        @param tname: str 挑战者名称
        '''
        self.sb[tid]=tname
        
    def getSb(self):
        '''获取挑战失败记录'''
        return self.sb
    
    def addCg(self,cid,cname):
        '''添加挑战成功记录
        @param cid: int 挑战成功者id
        @param cname: int 挑战成功者名称
        '''
        self.cgid=cid
        self.cgname=cname
    
    def getCg(self):
        '''获取挑战成功的角色信息'''
        return [self.cgid,self.cgname]
            
        