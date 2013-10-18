#coding:utf8
'''
Created on 2011-11-11
@author: SIOP_09
'''
from app.scense.core.Item import Item

class CardItem:
    '''牌子北面的东西'''

    
    
    
    
    def __init__(self,id=0,count=1,coin=0,coupon=0):
        '''
        @param id: 物品的模板id
        @param count: int 物品的数量
        @param coin: int 游戏币
        @param coupon: int 绑定钻
        '''
        self.item=None #存储一个物品的实例
        self.coin=0 #游戏币
        self.coupon=0 #绑定钻
        
        if id>0 and count>0:
            item1=Item(id)
            item1.pack.setStack(count)
            self.item=item1
        elif coin>0:
            self.coin=coin
        elif coupon>0:
            self.coupon=coupon
            
    def getValue(self):
        return {"item":self.item,"coin":self.coin,"coupon":self.coupon}
        
        
    