#coding:utf8
'''
Created on 2011-10-24

@author: lan
'''
from app.scense.core.singleton import Singleton

class ShopManager:
    '''商店管理器'''
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化商店管理器
        @param _shops: 
        '''
        self._shops = {}
        
    def addShop(self,shop):
        '''添加一个商店
        @param shop: PublicShop Object
        '''
        self._shops[shop._id] = shop
        
    def dropShopByID(self,shopID):
        '''删除商店
        @param shopID: int 商店的id
        '''
        try:
            del self._shops[shopID]
        except Exception:
            pass
        
    def getShopByID(self,shopID):
        '''根据商店的id获取商店'''
        return self._shops.get(shopID,None)
    
    
    