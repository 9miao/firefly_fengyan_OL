#coding:utf8
'''
Created on 2012-3-14
商城类
@author: lan
'''
from app.scense.core.singleton import Singleton
import copy
 
from app.scense.utils.dbopera import dbMall
from app.scense.core.Item import Item
import math
 
class Mall:
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化商城'''
        self.all = {}#所有物品
        self.allpage=1
        self.rm = {}#热卖物品
        self.rmpage=1
        self.qh = {}#强化相关物品
        self.qhpage=1
        self.pet= {}#宠物相关物品
        self.petpage=1
        self.cx= {}#促销商品
        
        self.count=12#每页显示物品数量
        self.initData()
        
    def initData(self):
        '''初始化商城数据'''
        data = dbMall.getAllMallInfo()
        for item in data:
            if item['tag']==1:#强化相关商品
                self.qh[item['templateid']]=item
            elif item['tag']==2:#宠物相关商品
                self.pet[item['templateid']]=item
            
            if item['promotion']==1:#热卖商品
                self.rm[item['templateid']]=item
                
            if item['cx']>0:#促销商品
                    self.cx[item['templateid']]=item
            self.all[item['templateid']]=item
            
        self.allpage=self.getMaxPage(len(self.all))
        self.rmpage=self.getMaxPage(len(self.rm))
        self.qhpage=self.getMaxPage(len(self.qh))
        self.petpage=self.getMaxPage(len(self.pet))
        
        
    
    def getMaxPage(self,zong):
        '''获取商城的最大分页
        @param zong: int 数据条数
        '''
        return int(math.ceil(float(zong)/self.count))
    
    def getMaxPageByType(self,tag):
        '''根据商城标签获取商城的最大分页
        @param tag: int 商城物品的分类1热卖2所有3强化4宠物
        '''
        p=0
        if tag==1:
            p=self.rmpage
        elif tag==2:
            p=self.allpage
        elif tag==3:
            p=self.qhpage
        elif tag==4:
            p=self.petpage
        return p
            
    def getPageItems(self,page,type):
        '''获取指定页的商品
        @param page: int 页面数
        @param type: int 商城分页 1热卖 2所有 3强化 4宠物
        '''
        
        start = (page-1)*self.count
        end = page*self.count
        values=[]
        if type==1:#热卖
            values= self.rm.values()[start:end]
        elif type==2:#所有
            values= self.all.values()[start:end]
        elif type==3:#强化
            values= self.qh.values()[start:end]
        elif type==4:#宠物
            values= self.pet.values()[start:end]
        return values
    
    def getCXItemInfo(self):
        return self.cx.values()[0:3]
        
    def getItemPriceById(self,itemId):
        '''根据物品的模板ID获取商品的价格'''
        info = self.all.get(itemId)
        if info:
            return info.get('gold',0)
        return -1
        
    def getItemInfoById(self,itemId):
        '''根据物品的模板ID获取商品的信息'''
        info=self.all.get(itemId,None)
        return info
            
        
        
        
        