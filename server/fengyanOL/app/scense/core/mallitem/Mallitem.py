#coding:utf8
'''
Created on 2011-6-24

@author: SIOP_09
'''
from app.scense.utils import dbaccess

class Mallitem():
    '''
            商城类
    '''
    
    def __init__(self,itemid):
        self._itemid=-1 #商品模板Id
        self._tag=-1 #标签分类
        self._promotion=-1 #促销分类
        self._rmb=-1 #钻价格(人民币价格)
        self._coupon=-1 #魔晶价格(礼券价格)
        self._restrict=-1 #购买上限(针对用户)
        self._resettime=-1 #限量商品累计购买数量的清空时间间隔（单位：小时）
        self._up=-1 #商品自动上架的时间
        self._down=-1 #商品自动下架的时间
        self._onoff=-1 #上下架开关 为开的话 根据时间自动上架下架;为关闭状态的话 商品为下架状态 1:打开 2:关闭
        self.initmallitem(itemid)
    
    def initmallitem(self,itemid):
        info=dbaccess.getMallItemById(id)
        