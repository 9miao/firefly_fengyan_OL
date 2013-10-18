#coding:utf8
'''
Created on 2011-12-8
强化管理器
@author: SIOP_09
'''
from app.scense.core.singleton import Singleton
from app.scense.utils.dbopera import dbStrengthenicon
from app.scense.applyInterface import configure

class StrengthenIconManager():
    '''强化数据管理器'''

    __metaclass__ = Singleton
    def __init__(self):
        self.qhtime={}#{角色id:{数据库信息}}
        self.updateAll()
        
    def updateAll(self):
        '''更新强冷却时间'''
        info=dbStrengthenicon.getAll()
        if info:
            self.qhtime=info
        
    def getZongTime(self,pid):
        '''根据角色id获取最大冷却时间'''
        from app.scense.core.PlayersManager import PlayersManager
        player=PlayersManager().getPlayerByID(pid)
        viplevel=player.baseInfo.getType()#获取角色vip等级
        return configure.m((viplevel+1)*20)
    
    def isdraw(self,pid):
        '''是否能够进行强化
        @param counts: int 距离秒数
        ''' 
        zong=self.getZongTime(pid)#最大
        sy=self.getByPid(pid)#当前
        if zong>sy:
            return True
        return False

        
    def add(self,pid):
        '''添加或者修改强化冷却时间
        @param counts: int 冷却秒数
        '''
        import datetime,time
        ctime=datetime.datetime.fromtimestamp(time.time())
        ss=self.getByPid(pid)#强化剩余冷却时间
        if self.qhtime.has_key(pid):
            self.qhtime.get(pid)['counts']=ss+configure.m(5)
            self.qhtime.get(pid)['ctime']=ctime
            dbStrengthenicon.update(pid, ctime, self.qhtime.get(pid)['counts'])
        else:
            self.qhtime[pid]={"pid":pid,"ctime":ctime,"counts":configure.m(5)}
            dbStrengthenicon.add(pid, ctime, configure.m(5))
    
    def deleteByid(self,pid):
        '''清除一个倒计时'''
        if self.qhtime.has_key(pid):
            self.qhtime[pid]['counts']=0
            
    
    def getByPid(self,pid):
        '''获取角色强化剩余冷却时间'''
        if self.qhtime.has_key(pid):
            info=self.qhtime.get(pid)
            s=configure.getchaTime(info['ctime'],info['counts'])#与当前时间相差秒数
            if s<1:
                self.deleteByid(pid)
            return s
        else:
            return 0