#coding:utf8
'''
Created on 2011-6-14
殖民连胜纪录管理
@author: SIOP_09
'''
from app.scense.core.singleton import Singleton
from twisted.python import log
from app.scense.utils.dbopera import dbWinning, dbInstance_colonize_title



class WinManager(object):
    '''副本连胜管理
    '''
    __metaclass__ = Singleton

    
    def __init__(self):
        '''初始化场景管理器
        '''
        #self.win={}#存放连胜纪录 {1:{'id':1,'pid':100001,'counts':2}}
        self.win=dbWinning.getAll()#存放连胜纪录 {1:{'id':1,'pid':100001,'count':2}} key=pid #角色id
    
    def updatethis(self,wins):
        self.win=wins
        

    def add(self,pid):
        '''添加连胜纪录'''
#        from serverconfig.publicnode import publicnoderemote
        if self.win.has_key(pid):
            item= self.win[pid]
            item['count']=item['count']+1
            if not dbWinning.update(pid):
                log.err(u"WinManager.add中修改连胜纪录错误,角色id:%s"%pid)
        else:
            self.win[pid]={'count':1,'pid':pid}
            if not dbWinning.add(pid):
                log.err(u"WinManager.add中添加连胜纪录错误,角色id:%s"%pid)
#        publicnoderemote.callRemote('public_winning_WinManager',self.win)
    def set0(self,pid):
#        from serverconfig.publicnode import publicnoderemote
        if self.win.has_key(pid):
            item=self.win[pid]
            if item['count']!=0:
                item['count']=0
                if not dbWinning.set0(pid):
                    log.err(u"WinManager.set0中清零纪录错误,角色id:%s"%pid)
        
#        publicnoderemote.callRemote('public_winning_WinManager',self.win)
        
    def getcount(self,pid):
        if self.win.has_key(pid):
            return self.win[pid]['count'] #返回殖民连胜次数
        else:
            return 0
        
    def getName(self,pid):
        '''根据角色id获取称号,没有称号返回false'''
        count=0 #
        if self.win.has_key(pid):
            count=self.win[pid]['count'] #返回殖民连胜次数
        name=dbInstance_colonize_title.getname(count)
        return name