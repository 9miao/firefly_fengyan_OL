#coding:utf8
'''
Created on 2012-3-13
副本殖民组件
@author: jt
'''
from app.scense.component.pack.BasePackage import BasePackage
from app.scense.component.Component import Component
from app.scense.utils.dbopera import db_package,dbClearance,dbInstance_record_id
from app.scense.utils import dbaccess
from app.scense.netInterface.pushPrompted import pushPromptedMessage
import copy
from app.scense.core.Item import Item
from app.scense.core.language.Language import Lg


class InstanceColonizeComponent(Component):
    '''副本殖民组件
    '''
    INITSIZE = 6

    def __init__(self,owner):
        '''
        @param owner: obj 角色实例
        '''
        Component.__init__(self, owner)
        self.pack=BasePackage(30,packageType = 5) #殖民仓库，只存放殖民掉落的装备
        self.clearances = set([])#角色已经通关的副本的ID
        self.GroupClearances = set([])#角色已经通关的副本组
#        self.initData()
        
    def initData(self):
        characterId = self._owner.baseInfo.id
        itemsPackInfo = db_package.getItemsInstancePackage(characterId)
        self.clearances = set(dbClearance.getClearanceRecord(characterId))
        self.GroupClearances = set(dbClearance.getGroupRecord(characterId))
        for itemInfo in itemsPackInfo:
            if itemInfo['itemId']==-1:
                continue
            item = Item(id =itemInfo['itemId'])
            self.pack.putItemByPosition(itemInfo['position'], item)
    
    
    def putNewItemInPackage(self,item):
        '''放置一个新的物品到包裹栏中
        @param item: Item object 物品实例
        @param position: int 物品的位置
        @param packageType: int 包裹的类型
        @param state: int 是否及时的推送获取物品消息
        '''
        package=self.pack
        characterId = self._owner.baseInfo.id
        position=package.findSparePositionForItem()
        return package.putItemInPackDB(item, position, characterId)
    
    def getOneItemInPackByPosition(self,position):
        '''取出一个物品放到背包中
        @param position: int 包裹的位置
        '''
        characterId = self._owner.baseInfo.id
        packget = self._owner.pack._package.getPackageByType(1)
        spaceCnt = packget.findSparePositionNum()
        if spaceCnt<1:
            return False
        item = self.pack.getItemByPosition(position)
        if not item:
            return False
        result1 = self.pack.deleteItemInPackage(position, tag=0)
        if result1:
            nowposition = packget.findSparePositionForItem()
            result2 = packget.putItemInPackDB(item, nowposition, characterId)
            if result2:
                return True
        return False
    
    def putAllItemsInPack(self):
        '''将所有的物品移动到包裹'''
        requiredCnt = len(self.pack._items)
        packget = self._owner.pack._package.getPackageByType(1)
        spaceCnt = packget.findSparePositionNum()
        if spaceCnt < requiredCnt:
            return False
        characterId = copy.deepcopy(self._owner.baseInfo.id)
        itemList = self.pack._items
        for item in itemList:
            position = item.get('position',-1)
            itemCom = item.get('itemComponent')
            if position <0 or not itemCom:
                return False
            self.pack.getItemByPosition(position)
            nowposition = packget.findSparePositionForItem()
            result = packget.putItemInPackDB(itemCom, nowposition, characterId)
            if result:
                self.pack.deleteItemInPackage(position, tag=0)
            else:
                return False
        return True
        
    def updateSizeByPosition(self,position):
        '''根据位置扩张包裹
        @param position: int 包裹的位置
        '''
        size = position + 1
        
        self.updateSize(size)
    
    def updateSize(self,size):
        '''修改包裹最大个数
        @param size: int 包裹的大小
        '''
        self.pack.setSize(size)

    def packageExpansion(self,position):
        '''包裹扩充'''
        package = self.pack
        PurposeSize = position +1
        start = package.getSize()-self.INITSIZE
        if start<0:
            return {'result':False,'message':u'坑爹呢！'}
        end = PurposeSize - package.getSize()
        cost = 0
        while end>0:
            start += 1
            cost += start*2
            end -=1
        if self._owner.finance.getGold()<cost:
            return {'result':False,'message':Lg().g(190)}
        self._owner.finance.updateGold(self._owner.finance.getGold()-cost)
        self._owner.updatePlayerInfo()
        package.setSize(PurposeSize)
        dbaccess.updatePlayerInfo(self._owner.baseInfo.id, {'famPackSize':PurposeSize})
        pushPromptedMessage(Lg().g(352)%cost,[self._owner.getDynamicId()])
        return {'result':True,'message':Lg().g(352)%cost}
        
    def getFamItemInfo(self):
        '''获取包裹信息'''
        info = {}
        info['items'] = self.pack.getItemList()
        info['size'] = self.pack.getSize()
        return info
    
    def isFamClean(self,instanceId):
        '''判断副本是否通关
        '''
        return instanceId in self.clearances
    
    def addClean(self,instanceId):
        '''添加副本通关记录
        '''
        if instanceId not in self.clearances:
            characterid = self._owner.baseInfo.id
            self.clearances.add(instanceId)
            dbInstance_record_id.insertInstanceRecord(characterid, instanceId)
            return True
        return False
    
    def addGroupClear(self,groupId):
        '''添加副本组通关记录
        '''
        if groupId not in self.GroupClearances:
            characterid = self._owner.baseInfo.id
            self.GroupClearances.add(groupId)
            dbaccess.insertInstanceRecord(characterid, groupId)
            return True
        return False
        
        
    def isGroupClean(self,groupId):
        '''判断副本组是否通关
        '''
        return groupId in self.GroupClearances
#        from core.instance.InstanceGroupManage import InstanceGroupManage
#        groupInfo = InstanceGroupManage().getcityidBygroupid(groupId)
#        if not groupInfo:
#            return False
#        for instanceId in (groupInfo['levela'],groupInfo['levelb'],groupInfo['levelc']):
#            if instanceId in self.clearances:
#                return True
#        return False
        
