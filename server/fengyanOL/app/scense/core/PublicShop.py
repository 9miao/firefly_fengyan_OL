#coding:utf8
'''
Created on 2011-8-16
公共商店类
@author: lan
'''
from app.scense.core.Item import Item
from app.scense.component.pack.BasePackage import BasePackage
from app.scense.utils.dbopera import dbShop

class PublicShop:
    
    def __init__(self,id):
        '''
        @param id: int 商店的编号
        @param shoppack: 商店包裹
        '''
        self._id = id
        self.shopitems = []
        self.itemList = []
        self.initShopData()
        
    def initShopData(self):
        '''初始化商店信息
        '''
        self.itemList = dbShop.getShopInfo(self._id)
        for _item in self.itemList:
            item = Item(itemTemplateId = _item['item'])
            item.baseInfo.setItemPrice(_item['coinPrice'])
            itemInfo = {}
            itemInfo['item'] = item
            itemInfo['overTime'] = 0
            self.shopitems.append(itemInfo)
            
    def getPublicShopInfo(self):
        '''获取公共商店信息'''
        return self.shopitems
    
    def getRepurchaseInfo(self,characterId):
        '''获取角色回购的物品的信息'''
        repurchaseItems = []
        data = dbShop.getPlayerRepurchaseInfo(characterId)
        for _item in data:
            itemInfo = {}
            itemInfo['item'] = Item(id = _item[1])
            itemInfo['item'].baseInfo.setItemPrice(int(itemInfo['item'].baseInfo.getItemPrice()*1.5))
            itemInfo['overTime'] = 10800 - _item[-1].seconds
            repurchaseItems.append(itemInfo)
        return repurchaseItems
        
        
        
        