#coding:utf8
'''
Created on 2011-12-8
强化管理器
@author: SIOP_09
'''
from firefly.utils.singleton import Singleton
from app.chatServer.utils.dbopera import dbPunish,dbStrengthen

class StrengthenManager():
    '''强化数据管理器'''

    __metaclass__ = Singleton
    def __init__(self):
        self.Probability={} #强化成功率{强化等级:data,3:object} data={}
        self.Gain={} #强化收益，格式同成功率
        self.Punish={} #失败惩罚,格式同成功率
        self.updateAll() #更新强化数据
        
    def updateAll(self):
        '''更新强化数据'''
        self.Punish=dbPunish.getAll() #获取所有惩罚信息  self.Punish.get("1")
        self.Gain=dbStrengthen.getGainAll() #获取所有强化增益 self.Gain.get("1#2") 1:强化等级 2装备颜色
        self.Probability=dbStrengthen.getProbabilityAll() #获取所有强化几率  self.Probability.get("3")
        
    def getPunishInfo(self,qlevel):
        '''获取失败惩罚信息
        @param qlevel: int 装备当前强化等级(强化失败之前的强化等级)
        '''
        return self.Punish.get(str(qlevel+1),None)
        
    def getGainInfo(self,qlevel,color):
        '''获取强化收益信息
        @param qlevel: int 装备当前强化等级(强化成功之后的强化等级)
        @param color: int 装备颜色        
        '''
        return self.Gain.get(str(qlevel)+"#"+str(color),None)
    def getProbabilityInfo(self,qlevel):
        '''获取强化成功率
        @param qlevel: int 装备当前强化等级(强化之前)
        '''
        return self.Probability.get(str(qlevel+1),None)