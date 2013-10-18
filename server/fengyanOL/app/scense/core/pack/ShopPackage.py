#coding:utf8
'''
Created on 2011-4-1

@author: sean_lan
'''
from app.scense.component.pack.BasePackage import BasePackage

class ShopPackage():
    '''商店包裹'''
    def __init__(self):
        '''商店包裹
        @param weaponShopPackage: BasePackage object 武器店包裹
        @param armorShopPackage:  BasePackage object 防具店包裹
        @param materialShopPackage: BasePackage object 材料店包裹
        @param groceriesShopPackage: BasePackage object 杂货店包裹
        '''
        self.weaponShopPackage = BasePackage(48)
        self.armorShopPackage = BasePackage(48)
        self.materialShopPackage = BasePackage(48)
        self.groceriesShopPackage = BasePackage(48)
        
    def putItemInShopPackage(self,shopType,item):
        '''放置一个物品到商店包裹中
        @param shopType: int 商店类型
        '''
        if shopType==1:
            position = self.weaponShopPackage.findSparePositionForItem()
            self.weaponShopPackage.putItemByPosition(position, item)
        elif shopType==2:
            position = self.armorShopPackage.findSparePositionForItem()
            self.armorShopPackage.putItemByPosition(position, item)
        elif shopType==3:
            position = self.materialShopPackage.findSparePositionForItem()
            self.materialShopPackage.putItemByPosition(position, item)
        elif shopType==4:
            position = self.groceriesShopPackage.findSparePositionForItem()
            self.groceriesShopPackage.putItemByPosition(position, item)
    
    def getShopPackage(self,shopType):
        '''获取商店包裹
        @param shopType: int 商店类型
        '''
        if shopType==1:
            return self.weaponShopPackage
        elif shopType==2:
            return self.armorShopPackage
        elif shopType==3:
            return self.materialShopPackage
        elif shopType==4:
            return self.groceriesShopPackage
        
        
    def clearAllShopPackage(self):
        '''清空所有的商店的包裹'''
        self.weaponShopPackage.clearPackage()
        self.armorShopPackage.clearPackage()
        self.materialShopPackage.clearPackage()
        self.groceriesShopPackage.clearPackage()
        
        
        
        
    
        