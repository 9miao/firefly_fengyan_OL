#coding:utf8
'''
Created on 2011-3-27
@author: sean_lan
'''
from app.scense.component.pack.BasePackage import BasePackage

class Package(object):
    '''包裹栏
    @param _equipPagePack: BasePackage object  包裹一般物品分页
    @param _taskPagePack: BasePackage object  任务物品分页
    '''
    LIMIT = 30
    MAXPAGE = 5
    def __init__(self,size=150):
        '''
        @param size: int 包裹的大小
        '''
        self._PropsPagePack = BasePackage(size,packageType=1)#背包
        self._taskPagePack = BasePackage(150,packageType=2)#任务包裹
        
    def setSize(self,size):
        '''设置包裹大小'''
        self._PropsPagePack.setSize(size)
        
    def getPackageByType(self,packType):
        '''根据包裹类型获取包裹实例'''
        if packType==1:
            return self._PropsPagePack
        return self._taskPagePack
        
    def getPropsPagePack(self):
        '''获取全部物品包裹'''
        return self._PropsPagePack
    
    def getTaskPagePackItem(self):
        '''获取任务物品分页包裹物品列表信息'''
        return self._taskPagePack
    
    def putItemInPackage(self,position,item,packType):
        '''初始化包裹栏
        @param position: int 放置的位置
        @param item: Item Object 物品实例
        '''
        if packType==1:
            pack = self.getPropsPagePack()
        else:
            pack = self.getTaskPagePackItem()
        pack.putItemByPosition(position, item)
        
    def getCategoryPageItemInfo(self,packType,page):
        ''''获取包裹分页的信息'''
        data = {}
        if packType==1:
            pack = self.getPropsPagePack()
        else:
            pack = self.getTaskPagePackItem()
        itemList = pack.getItemList()
        data['itemList'] = [{'position':itemInfo['position']%self.LIMIT,\
                             'itemComponent':itemInfo['itemComponent']}\
                             for itemInfo in itemList if\
                             itemInfo['position']>=(page-1)*self.LIMIT and\
                             itemInfo['position']<page*self.LIMIT]
        data['packageSize'] = pack.getSize()-(self.LIMIT*(page-1))
        if data['packageSize']>self.LIMIT:
            data['packageSize'] = self.LIMIT
        data['packCategory'] = packType
        data['curpage'] = page
        data['totalsize'] = pack.getSize()
        data['maxpage'] = self.MAXPAGE
        return data
        
    def canPutItem(self,item,count):
        '''检测包裹是否足以放下物品
        @param item: Item Object 物品的实例
        @param count: int 物品的数量
        '''
        return self._PropsPagePack.canPutItem(item, count)
        
        
    
    