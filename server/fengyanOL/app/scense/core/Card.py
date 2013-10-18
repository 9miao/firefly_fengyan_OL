#coding:utf8
'''
Created on 2011-4-14
@author: sean_lan
'''

class Card:
    '''副本卡片'''
    def __init__(self,id=0,coin=0,coupon=0,itemBound=None):
        '''
        @param id: 卡片的id 牌子的位置
        @param instanceid: int 副本的id
        '''
        self.id = id#牌子的位置
        self.coin= coin #金币奖励
        self.coupon=coupon #绑定钻
        self.itemBound = itemBound #物品奖励
        self._isTurned = 0       #是否被翻开  0未翻开  1已翻开
        self.into()
            
    def into(self):
        '''初始化副本卡片'''
        
    def changeIsTurned(self):
        '''更新翻转后的状态'''
        self._isTurned = 1
        
    def getID(self):
        '''获取卡片的ID'''
        return self.id
        
    def IsTurned(self):
        '''是否已经翻开'''
        return self._isTurned
    
    def formatCardInfo(self):
        '''格式化卡片信息'''
        data = {}
#        data['isTurned'] = self.IsTurned()
        data['cardId'] = self.id
        data['coinBounds'] =self.coin #金币奖励
#        data['coupon']=self.coupon #绑定钻
        data['itemBound'] = self.itemBound
#        data["itemTemplateId"]=self.itemTemplateId #物品id
##        self.item = 0
##        itemInfo = {}
#        if self.itemBound:
#            itemInfo['itemTemplateId'] = self.itemBound.baseInfo.itemTemplateId
#            exattrList = []
#            selfattrList = []
#            itemInfo['extraAttributeList'] = exattrList
#            itemInfo['selfAttributeList'] = selfattrList
#            itemInfo['qualityLevel'] = 3
#        data['itemBound']= itemInfo
        return data
    
    
    
    