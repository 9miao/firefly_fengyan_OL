#coding:utf8
'''
Created on 2012-7-11

@author: jt
'''
from app.scense.core.instance.Rq import Rq
from app.scense.core.singleton import Singleton

class RqManage(object):
    '''入侵列表类'''

    __metaclass__ = Singleton

    def __init__(self):
        ''''''
        self.info={}#key:角色id value:{key副本id:valueRq}
        
    def addCg(self,iid,iname,pid,pname,cgid,cgname):
        '''添加挑战成功记录
        @param iid: int 副本组id
        @param iname: str 副本名称
        @param pid: int 领主id
        @param pname:  str 领主名称
        @param cgid: int 挑战成功角色id
        @param cgname: str 挑战成功角色名称
        '''
        if self.info.has_key(pid):#这个角色如果有入侵记录
            pinfo=self.info[pid]#角色的入侵记录   key:副本或者城市id  value：Rq类
            if pinfo.has_key(iid):#如果这个角色有这个副本或城市的入侵记录
                rr=pinfo.get(iid)#rr是Rq类
                rr.addCg(cgid, cgname)
            else:#如果此角色没有入侵记录
                pinfo[iid]=Rq(iid, iname, pid, pname)
                pinfo[iid].addCg(cgid, cgname)
        else:#如果此角色没有入侵记录
            self.info[pid]={}
            pinfo=self.info[pid]
            pinfo[iid]=Rq(iid, iname, pid, pname)
            pinfo[iid].addCg(cgid, cgname)
            
    def addSb(self,iid,iname,pid,pname,sid,sname):
        '''@添加挑战失败记录
        @param iid: int 副本组id
        @param iname: str 副本名称
        @param pid: int 领主id
        @param pname:  str 领主名称
        @param sid: int 挑战失败角色id
        @param sname: str 挑战失败角色名称
        '''
        if self.info.has_key(pid):#这个角色如果有入侵记录
            pinfo=self.info[pid]#角色的入侵记录   key:副本或者城市id  value：Rq类
            if pinfo.has_key(iid):#如果这个角色有这个副本或城市的入侵记录
                rr=pinfo.get(iid)#rr是Rq类
                rr.addSb(sid, sname)
            else:#如果此角色没有入侵记录
                pinfo[iid]=Rq(iid, iname, pid, pname)
                pinfo[iid].addSb(sid, sname)
        else:#如果此角色没有入侵记录
            self.info[pid]={}
            pinfo=self.info[pid]
            pinfo[iid]=Rq(iid, iname, pid, pname)
            pinfo[iid].addSb(sid, sname)
            
                
            
        
        
        