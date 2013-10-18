#coding:utf8
'''
Created on 2011-8-16
公共商店类
@author: lan
'''
from app.scense.core.Item import Item
from app.scense.utils.dbopera import dbShop
import math

PAGELIMIT = 15#商店商品分页个数

class PublicShop:
    
    def __init__(self,id):
        '''
        @param id: int 商店的编号
        @param shoppack: 商店包裹
        '''
        self._id = id
        self.shopitems = {}
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
            itemInfo['id'] = item.baseInfo.getItemTemplateId()
            itemInfo['item'] = item
            itemInfo['overTime'] = 0
            self.shopitems[itemInfo['id']]= itemInfo
            
    def getPublicShopInfo(self,index):
        '''获取公共商店信息'''
        maxPage = int(math.ceil(len(self.shopitems)*1.0/PAGELIMIT))
        items = self.shopitems.values()[(index-1)*PAGELIMIT:index*PAGELIMIT]
        if 1 > maxPage:
            maxPage = 1
        return {'shopCategory':0,'curPage':index,'maxPage':maxPage,'items':items}
    
    def getRepurchaseInfo(self,characterId):
        '''获取角色回购的物品的信息'''
        repurchaseItems = []
        data = dbShop.getPlayerRepurchaseInfo(characterId)
        for _item in data:
            itemInfo = {}
            itemInfo['item'] = Item(id = _item[1])
            itemInfo['item'].baseInfo.setItemPrice(int(itemInfo['item'].baseInfo.getItemPrice()/0.7))
            itemInfo['overTime'] = 10800 - _item[-1].seconds
            repurchaseItems.append(itemInfo)
        return {'shopCategory':1,'curPage':1,'maxPage':1,'items':repurchaseItems}
        
    def getShopItemsById(self,itemId):
        '''获取商店物品信息
        @param itemId: int 物品的id
        '''
        return self.shopitems.get(itemId,None)
        
        
        