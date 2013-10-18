#coding:utf8
'''
Created on 2012-2-25
本地服务(客服端发送过来的需要经过gateserver处理的消息)
@author: sean_lan
'''
from twisted.internet import defer,threads
from twisted.python import log

from firefly.utils.services import CommandService

class LocalService(CommandService):
    
    def callTargetSingle(self,targetKey,*args,**kw):
        '''call Target by Single
        @param conn: client connection
        @param targetKey: target ID
        @param data: client data
        '''
        target = self.getTarget(targetKey)
        
        self._lock.acquire()
        try:
            if not target:
                log.err('the command '+str(targetKey)+' not Found on service')
                return None
            if targetKey not in self.unDisplay:
                log.msg("call method %s on service[single]"%target.__name__)
            defer_data = target(targetKey,*args,**kw)
            if not defer_data:
                return None
            if isinstance(defer_data,defer.Deferred):
                return defer_data
#            d = defer.Deferred()
#            d.callback(defer_data)
        finally:
            self._lock.release()
        return defer_data
    
    def callTargetParallel(self,targetKey,*args,**kw):
        '''call Target by Single
        @param conn: client connection
        @param targetKey: target ID
        @param data: client data
        '''
        self._lock.acquire()
        try:
            target = self.getTarget(targetKey)
            if not target:
                log.err('the command '+str(targetKey)+' not Found on service')
                return None
            log.msg("call method %s on service[parallel]"%target.__name__)
            d = threads.deferToThread(target,targetKey,*args,**kw)
        finally:
            self._lock.release()
        return d
    
localservice = LocalService('localservice')
localservice.addUnDisplayTarget("pushData")
localservice.addUnDisplayTarget("pushObject")


def localserviceHandle(target):
    '''服务处理
    @param target: func Object
    '''
    localservice.mapTarget(target)
    
