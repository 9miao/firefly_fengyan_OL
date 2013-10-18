#coding:utf8
'''
Created on 2011-12-8
强化管理器
@author: SIOP_09
'''
from app.scense.core.singleton import Singleton
from app.scense.utils.dbopera import dbNobilityAstrict,dbNobilityContribution

class NobitityManage():
    '''角色领取俸禄管理'''

    __metaclass__ = Singleton
    def __init__(self):
        self.all={}
        self.gx={}#记录角色点击多少次贡献钻石
        
    def updateAll(self):
        '''更新'''
        self.all=dbNobilityAstrict.getAll()
        self.gx=dbNobilityContribution.getAll()
        
    def addGx(self,pid):
        '''点击次数加1'''
        if self.gx.has_key(pid):
            self.gx[pid]=self.gx[pid]+1#增加点击次数(内存)
            dbNobilityContribution.updateAdd(pid)#增加点击次数（数据库）
        else:
            self.gx[pid]=2#新建点击记录（内存）
            dbNobilityContribution.add(pid)#新建点击记录（数据库）
            
    def getGx(self,pid):
        '''获取角色点击次数'''
        if self.gx.has_key(pid):
            return self.gx[pid]
        else:
            return 1
        
    def getByidWW(self,pid):
        '''是否能够上交贡献换取威望'''
        if self.all.has_key(pid):#如果有值
            istrue=self.all.get(pid,-1)['isgx']
            if istrue>0:
                return True
            else:
                return False
        else:#如果领取俸禄限制表中没有记录此角色
            flg=dbNobilityAstrict.add(pid)#添加记录
            if flg:
                self.all[pid]={'pid':pid,'istrue':1,'isgx':1}
                return True
        
    def getByPid(self,pid):
        '''根据角色返回能否领取
        @param pid: int 角色id
        '''
        if self.all.has_key(pid):#如果有值
            istrue=self.all.get(pid,-1)['istrue']
            if istrue>0:
                return True
            else:
                return False
        else:#如果领取俸禄限制表中没有记录此角色
            flg=dbNobilityAstrict.add(pid)#添加记录
            if flg:
                self.all[pid]={'pid':pid,'istrue':1,'isgx':1}
                return True
        
    def clear(self):
        '''设置所有角色俸禄可领取状态为1(每天23:59分)'''
        dbNobilityAstrict.clear()
    
    def setByid(self,pid,state):
        '''设置角色俸禄是否可以领取 
        @param pid: int 角色id
        @param state: int 是否可领取状态  -1不可领取   1可领取
        '''
        if self.all.has_key(pid):#如果此角色有爵位
            self.all[pid]['istrue']=state#设置俸禄是否可以领取(内存中改变)
        dbNobilityAstrict.upate(pid, state)#（数据库中改变）
        
    def setByWW(self,pid,state):
        '''设置是否可以上交贡献换取威望'''
        if self.all.has_key(pid):#如果此角色有爵位
            self.all[pid]['isgx']=state#设置俸禄是否可以领取(内存中改变)
        dbNobilityAstrict.upategx(pid, state)#（数据库中改变）
            
        
   
    