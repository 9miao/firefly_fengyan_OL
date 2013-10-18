#coding:utf8
'''
Created on 2011-12-8
强化管理器
@author: SIOP_09
'''
from app.scense.utils.dbopera import dbStrengthenicon
from app.scense.applyInterface import configure
from app.scense.component.Component import Component
import datetime
import math
from app.scense.netInterface import pushObjectNetInterface

class IconTime(Component):
    '''强化数据管理器'''

    def __init__(self,owner):
        Component.__init__(self, owner)
        self.owner=owner
        self.pid=owner.baseInfo.id#角色id
        self.ctime=None#记录时间
        self.counts=0#秒数间隔（剩余秒数）
        info=dbStrengthenicon.getByPid(self.pid)#剩余时间记录
        if info:
            self.ctime=info['ctime']
            self.counts=info['counts']
            
        
    def clearCd(self):
        '''减少cd时间'''
        ss=self.getTime()#获取剩余冷却时间
        z=0#花费钻石数量
        if ss>0:
            cdzuan=int(math.ceil(ss/60.0))#需要花费的钻石数量
            gold=self.owner.finance.getGold()#角色当前拥有的钻石数量
            if gold==0:
                return False
            elif gold>=cdzuan:
                z=cdzuan
            elif gold<cdzuan and gold>0:
                z=gold
        self.counts=self.counts-z*60
        if self.counts<0:
            self.counts=0
        self.owner.finance.updateGold(self.owner.finance.getGold()-z)
        pushObjectNetInterface.StrengthenTime2120(self.pid, self.getTime())
        return True
    
    def getZongTime(self):
        '''获取最大冷却时间'''
        
        viplevel=self.owner.baseInfo.getType()#获取角色vip等级
        plevel=self.owner.level.getLevel()#角色等级
        return configure.m(int((plevel*0.5)+(viplevel+1)*20))
    
    def isdraw(self):
        '''是否能够进行强化
        @param counts: int 距离秒数
        ''' 
        zong=self.getZongTime()#最大
        sy=self.getTime()#当前
        if zong>sy:
            return True
        return False

        
    def add(self,wd):
        '''添加或者修改强化冷却时间，返回剩余秒数
        @param wd: int 物品等级
        '''
        sj=int((wd+5)*0.5)#增加的冷却时间(分钟)
        if self.ctime:
            tlist=configure.getchatimeTime(self.ctime,self.counts)
            ctime=tlist[1]
            ss=tlist[0]
            self.counts=ss+configure.m(sj)
            self.ctime=ctime
            pushObjectNetInterface.StrengthenTime2120(self.pid, self.getTime())
            return self.counts
        else:
            self.counts=configure.m(sj)
            self.ctime=datetime.datetime.now()
            pushObjectNetInterface.StrengthenTime2120(self.pid, self.getTime())
            return self.counts
    
    def getTime(self):
        '''获取角色强化剩余冷却时间'''
        if self.ctime:
            s=configure.getchaTime(self.ctime,self.counts)#与当前时间相差秒数
            return s
        else:
            return 0
        
    def dbupdate(self):
        '''下线处理中，将信息记录到数据库中'''
        if self.ctime:
            tlist=configure.getchatimeTime(self.ctime,self.counts)
            ss=tlist[0]
            if ss<1:
                return
            
            if dbStrengthenicon.getByPid(self.pid):#如果有记录
                dbStrengthenicon.update(self.pid, self.ctime, self.counts)#修改
            else:
                dbStrengthenicon.add(self.pid, self.ctime, self.counts)