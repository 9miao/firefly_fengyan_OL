#coding:utf8
'''
Created on 2011-3-27

@author: sean_lan
'''
from app.scense.component.Component import Component
from app.scense.core.pack.ShopPackage import ShopPackage
from app.scense.core.Item import Item
from app.scense.utils import util
from app.scense.utils.DataLoader import loader, connection
from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbShop
import random,math
import datetime
import time
from twisted.internet import reactor
from app.scense.netInterface.pushObjectNetInterface import pushUpdatePlayerInfo
from app.scense.netInterface.pushPrompted import pushPromptedMessage
from app.scense.core.shop.shopmanager import ShopManager
from app.scense.core.language.Language import Lg

reactor = reactor

class CharacterShopComponent(Component):
    '''
    character shop component
    个人商点类
    '''

    def __init__(self, owner):
        '''
        Constructor
        @param shopPackage: ShopPackage object 商店包裹类
        @param REFRESHSHOPITEMSTIME: int 物品自动刷新的时间 
        '''
        Component.__init__(self, owner)
        self.shopPackage = ShopPackage()
        self.REFRESHSHOPITEMSTIME = 3600
    
    def initShopItems(self):
        '''初始化商店物品
        '''
        self.shopPackage.clearAllShopPackage()
        for shopType in range(1,4):
            items = self.updateShopItems(shopType)
            for item in items:
                self.shopPackage.putItemInShopPackage(shopType, item)
        dbaccess.updateRefreshShopTime(self._owner.baseInfo.id)
        reactor.callLater(self.REFRESHSHOPITEMSTIME,self.initShopItems)
    
    def getShopPackage(self,shopType):
        '''获取商店物品信息
        @param shopType: int 商店类型  1武器 2防具 3材料 4 杂货
        '''
        if shopType==1:
            shopPackage = self.shopPackage.weaponShopPackage
        elif shopType==2:
            shopPackage = self.shopPackage.armorShopPackage
        elif shopType==3:
            shopPackage = self.shopPackage.materialShopPackage
        else:
            shopPackage = self.shopPackage.groceriesShopPackage
        if not shopPackage.getItems():
            self.initShopItems()
        return shopPackage

    def updateShopItems(self, shopType):
        '''获取商店物品
        @param shopType: (int) 商店类型
        '''
        list = []
        shopInfo = loader.get('shop', 'id', shopType, '*')
        if not shopInfo:
            return list
        shopInfo = shopInfo[0]
        count = shopInfo['count']
        for i in range(0, count):
            item = Item(27)
            list.append(item)
#            item = self.getOneShopItem(shopInfo)
#            while not item:
#                item = self.getOneShopItem(shopInfo)
#            if item:
#                list.append(item)
        return list

    def getOneShopItem(self, shopInfo):
        '''得到一个商店物品'''
        negtiveDelta = (self._owner.level.getLevel() - shopInfo['qualityLevelNegtiveDelta']) / 3
        positiveDelta = (self._owner.level.getLevel() + shopInfo['qualityLevelPositiveDelta']) / 3
        qualityLevel = random.randint(negtiveDelta, positiveDelta)
        goodTypes = shopInfo['goodsType'].split(';')
        types = []
        tempTypes1 = []#存放>1000的临时数组
        tempTypes2 = []#存放<=1000临时数组
        for elm in goodTypes:
            elm = int(elm)
            types.append(elm)
            if elm > 1000:
                tempTypes1.append(elm)
            else:
                tempTypes2.append(elm)
        for type1 in tempTypes1:
            for type2 in tempTypes2:
                type = type1 + type2
                types.append(type)
        all_ItemTemplate = dbaccess.all_ItemTemplate.values()
        itemTemplateList = [itemTemplate for itemTemplate in all_ItemTemplate if itemTemplate['qualityLevel']==qualityLevel]#dbaccess.all_ItemTemplate#loader.get('item_template', 'qualityLevel', qualityLevel, '*')
        shopItemList = []
        for itemTemplate in itemTemplateList:
            if itemTemplate['type'] in types:
                shopItemList.append(itemTemplate)
        if len(shopItemList) == 0:
            return None
        r = random.randint(0, len(shopItemList))
        if r > 0:
            r -= 1
        itemTemplate = shopItemList[r]
        #计算附加属性
        exAttrCount = self.getShopItemExtraAttrCount(shopInfo)
        extraAttributes = []
        name = u''
        for i in range(0, exAttrCount):
            attribute = self.getShopItemExtraAttr(shopInfo)
            flag = 0
            for elm in extraAttributes:
                if elm['id'] == attribute['id']:
                    attribute = self.getShopItemExtraAttr(shopInfo)
                    continue
                else:
                    flag += 1
                    continue
            if flag == len(extraAttributes):
                extraAttributes.append(attribute)
            name += attribute['name']

        info = {}
        info['itemTemplateInfo'] = itemTemplate
        info['extraAttributeList'] = extraAttributes
        bindType = itemTemplate['bind']
        bindTypeDesc = u''
        if bindType == 0:
            bindTypeDesc = Lg().g(465)
        elif bindType == 1:
            bindTypeDesc = Lg().g(466)
        elif bindType == 2:
            bindTypeDesc = Lg().g(467)
        else:
            bindTypeDesc = u""
        info['bindType'] = bindTypeDesc
        if name == u'':
            info['name'] = itemTemplate['name']
        else:
            info['name'] = name + Lg().g(139) + itemTemplate['name']
        #价格
        extraAttribute = ''
        for elm in extraAttributes:
            extraAttribute += str(elm['id']) + ","
        info['sellPrice'] = self.getShopItemPrice(itemTemplate['id'], extraAttribute)
        #层叠数
        if itemTemplate['stack'] <> -1:
            info['stack'] = 10
        else:
            info['stack'] = 1
        return info

    def getShopItemExtraAttrCount(self, shopInfo):
        '''得到商店物品附加属性数量'''
        characterLevel = self._owner.level.getLevel()

        cursor = connection.cursor()
        sql = "select countRatio from `shop_extra_attr_count_config` where type=%d and characterLevel=%d"\
            % (shopInfo['extraAttrCountConfigType'], characterLevel)
        cursor.execute(sql)
        countRatio = cursor.fetchone()['countRatio']
        cursor.close()
        ratios = countRatio.split(';')
        count = 0
        i = 0
        for ratio in ratios:
            i += 1
            ratio = int(ratio)
            r = random.randint(0, 100000)
            if r < ratio:
                count = len(ratios) - i + 1
                break
            else:
                continue
        return count

    def getShopItemExtraAttr(self, shopInfo):
        '''得到商店物品附加属性'''
        characterLevel = self._owner.level.getLevel()

        cursor = connection.cursor()
        sql = "select parameterMin,parameterMax from `shop_extra_attr_level_config` where type=%d and characterLevel=%d"\
            % (shopInfo['extraAttrLevelConfigType'], characterLevel)
        cursor.execute(sql)
        result = cursor.fetchone()
        min = result['parameterMin']
        max = result['parameterMax']
        r = random.randint(min, max)
        cursor.execute("select level from `exattribute_level` where value>=%d" % r)
        level = cursor.fetchone()['level']
        cursor.execute("select * from `extra_attributes` where level=%d" % level)
        tempAttributeList = cursor.fetchall()
        r1 = random.randint(0, len(tempAttributeList) - 1)
        attributeInfo = tempAttributeList[r1]

        attributeInfo['attributeEffects'] = []
        if attributeInfo['effects'] <> '-1' or attributeInfo['effects'] <> u'-1':
            effects = attributeInfo['effects'].split(';')
            for effect in effects:
                effect = int(effect)
                description = loader.getById('effect', effect, ['description'])['description']
                attributeInfo['attributeEffects'].append(description)
        else:
            script = attributeInfo['script']
            script = util.parseScript(script)
            attributeInfo['attributeEffects'].append(script)

        return attributeInfo

    def getShopItemPrice(self, itemTemplateId, extraAttribute):
        '''获取商店物品的购买价格'''
        #all_ItemTemplate = dbaccess.all_ItemTemplate.values()
        sellPrice = dbaccess.all_ItemTemplate[itemTemplateId]['buyingRateCoin']#loader.getById('item_template', itemTemplateId, ['buyingRateCoin'])['buyingRateCoin']
        extraAttributes = eval('[' + extraAttribute + ']')
        for extraAttrId in extraAttributes:
            extraAttrId = int(extraAttrId)
            isValidExtraAttrID = loader.getById('extra_attributes', extraAttrId, ['id'])
            if((extraAttrId != -1) and isValidExtraAttrID):
                eAttribute = loader.getById('extra_attributes', extraAttrId, ['level'])
                cursor = connection.cursor()
                cursor.execute("select price from exattribute_level where level=%d" % eAttribute['level'])
                value = cursor.fetchone()
                cursor.close()
                sellPrice += int(value['price'])
        return sellPrice
    
    def immediateRefreshShopItems(self,shopType,payType,payCount):
        '''刷新商店物品
        @param shopType: int 商店类型
        @param payType: int 支付类型  1:金币 2:礼券
        @param payCount: int 支付数量
        '''
        if payType==1:
            gold = self._owner.finance._gold - payCount
            if gold>0:
                self._owner.finance.updateGold(gold)
            else:
                return {'result':False,'message':Lg().g(88)}
        else:
            coupon = self._owner.finance._coupon - payCount
            if coupon>0:
                self._owner.finance.updateGold(gold)
            else:
                return {'result':False,'message':Lg().g(190)}
        
        if shopType == 1:#武器屋
            package = self.shopPackage.weaponShopPackage()
        elif shopType == 2:#防具屋
            package = self.shopPackage.armorShopPackage()
        elif shopType == 3:#材料店
            package = self.shopPackage.materialShopPackage()
        elif shopType == 4:#杂货店
            package = self.shopPackage.groceriesShopPackage()
        package.clearPackage()
        return self.getShopItems(shopType)
    
    def getRefreshShopTime(self):
        '''获取商店刷新时间'''
        now = time.mktime(datetime.datetime.now().timetuple())
        lastTime = time.mktime(dbaccess.getRefreshShopTime(self._owner.baseInfo.id).timetuple())
        refreshTime = self.REFRESHSHOPITEMSTIME - int(now - lastTime)
        return refreshTime
    
    def buyItemInMyshop(self,imteTemplateID,buyNum,npcId):
        '''购买商店物品'''
        shop = ShopManager().getShopByID(npcId)
        if not shop:
            return {'result':False,'message':Lg().g(468)}
        itemInfo = shop.getShopItemsById(imteTemplateID)
        if not itemInfo:
            return {'result':False,'message':Lg().g(189)}
        SurplusCoin = self._owner.finance.getCoin() - itemInfo['item'].baseInfo.getItemFinalyPrice()*buyNum
        if SurplusCoin<0:
            return {'result':False,'message':Lg().g(88)}
        result = self._owner.pack.putNewItemsInPackage(imteTemplateID,buyNum)
        if not result:
            return {'result':False,'message':Lg().g(16)}
        self._owner.finance.updateCoin(SurplusCoin)
        self._owner.updatePlayerInfo()
        msg = Lg().g(193)
        pushPromptedMessage(msg, [self._owner.getDynamicId()])
        return {'result':True,'message':Lg().g(193)}
        
    def RepurchaseItem(self,itemId):
        '''回购物品'''
        if  not dbShop.checkSellItem(itemId, self._owner.baseInfo.id):
            return {'result':False,'message':Lg().g(469)}
        item = Item(id = itemId)
        price = int(item.baseInfo.getItemPrice()/0.7)*item.pack.getStack()
        SurplusCoin = self._owner.finance.getCoin() - price
        if SurplusCoin<0:
            return {'result':False,'message':Lg().g(88)}
        result = self._owner.pack.putNewItemInPackage(item)
        if result==1:
            return {'result':False,'message':Lg().g(377)}
        self._owner.finance.updateCoin(SurplusCoin)
        pushUpdatePlayerInfo(self._owner.getDynamicId())
        dbShop.delSellItem(itemId)
        msg = Lg().g(195)
        pushPromptedMessage(msg, [self._owner.getDynamicId()])
        return {'result':True,'message':Lg().g(195)}
        
    def buyConsItem(self,tocharacterId,consID,itemCount,itemId,price,buyType):
        '''购买寄卖物品
        @param tocharacterId: int 角色的id
        @param consID: int 物品寄卖的ID
        @param itemId: int 物品的id
        @param price: int 物品的价格
        @param itemCount: int 物品的数量
        @param buyType: int 购买类型   1 金币 2钻
        '''
        
        characterId = self._owner.baseInfo.id
        package = self._owner.pack._package.getWholePagePack()
        position = package.findSparePositionForItem()
        
        if position==-1:
            return {'result':False,'message':Lg().g(16)}
        
        if buyType==1:
            the_coin = self._owner.finance.getCoin() - price
            to_coin = int(math.ceil(price*(1-0.1)))
        else:
            the_coin = self._owner.finance.getGold() - price
            to_coin = price
        if the_coin<0:
            return {'result':False,'message':Lg().g(190)}
        item = Item(id = itemId)
        item.pack.setStack(itemCount)
        item.InsertItemIntoDB(characterId = characterId)
        newitemId = item.baseInfo.getId()
        result = dbaccess.dbbuyConsItem(characterId, tocharacterId, consID, newitemId, the_coin, to_coin, position, buyType)
        if not result:
            return {'result':True,'message':Lg().g(470)}
        item = Item(id = newitemId)
        item.pack.setStack(itemCount)
        item.InsertItemIntoDB(characterId = characterId)
        package.putItemByPosition(position, item)
        if buyType==1:
            self._owner.finance.setCoin(the_coin)
        else:
            self._owner.finance.setGold(the_coin)
        return {'result':True,'message':Lg().g(193)}
    