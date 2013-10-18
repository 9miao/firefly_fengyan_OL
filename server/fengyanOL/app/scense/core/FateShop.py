#coding:utf8
'''
Created on 2012-6-7
命格商店
@author: Administrator
'''
from app.scense.core.singleton import Singleton
from app.scense.component.fate.Fate import Fate
from app.scense.utils.dbopera import dbCharacterFate
import math

class FateShop:
    '''命格商店
    @param fates: 所有的在线成员
    '''
    __metaclass__ = Singleton

    def __init__(self):
        '''初始化'''
        self.fates = []
        self.initShop()
        
    def initShop(self):
        '''初始化商店'''
        for fateinfo in dbCharacterFate.FATE_TEMPLATE.values():
            if fateinfo['quality']>0:
                fate = Fate(templateId = fateinfo['id'])
                self.fates.append(fate)
            
    def getShopInfo(self,page,limit = 8):
        '''获取星运商店信息'''
        info = {}
        info['fatelist'] = self.fates[(page-1)*limit:page*limit]
        maxpage = int(math.ceil(len(self.fates)*1.0/limit))
        info['nowpage'] = page
        info['maxpage'] = maxpage if maxpage else 0
        return info
        
        
            
        