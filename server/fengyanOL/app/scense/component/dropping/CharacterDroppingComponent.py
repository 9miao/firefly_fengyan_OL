#coding:utf8
'''
Created on 2011-4-2

@author: sean_lan
'''
import random

from app.scense.component.Component import Component
from app.scense.core.Item import Item
from app.scense.utils.DataLoader import loader, connection
from app.scense.utils import dbaccess
from twisted.python import log

class CharacterDroppingComponent(Component):
    '''
    dropping component for character
    '''

    def __init__(self, owner, dropConfigId = -1):
        '''角色物品掉落组件
        Constructor
        '''
        Component.__init__(self, owner)
        self._dropConfigId = dropConfigId #掉落配置
        self._dropCoefficient = 100000 #玩家的掉落物品几率修正

    def getDropConfigId(self):
        return self._dropConfigId

    def setDropConfigId(self, dropConfigId):
        self._dropConfigId = dropConfigId

    def getDropCoefficient(self):
        return self._dropCoefficient

    def setDropCoefficient(self, dropCoefficient):
        self._dropCoefficient = dropCoefficient

    def getItemByDropping(self, dropConfigId):
        '''
                     根据掉落配置得到物品
        @param dropConfigId: 掉落配置id
        '''
        dropConfig = loader.getById('drop_config', dropConfigId, '*')
        if not dropConfig or len(dropConfig.items()) == 0:
            log.err( _why= 'no item for the dropconfig dropConfigId(%d) characterId(%d)'%(dropConfigId,self._owner.baseInfo.id))
            return None
        itemTemplate = self.getDropItemTemplate(dropConfig)
#        itemTemplate = dbaccess.all_ItemTemplate[1]
        if itemTemplate:
            isBound = 0
            if itemTemplate['bindType']==1:
                isBound = 1
            itemTemplate['id'] = 27
            dropItem = Item(itemTemplateId =itemTemplate['id'])
            dropItem.attribute.setIsBound(isBound)
#            itemId = dropItem.InsertItemIntoDB(characterId = self._owner.baseInfo.id)
#            dropItem.baseInfo.setId(itemId)
            
            return dropItem
        else:
            return None

    def getDropItemTemplate(self, dropConfig):
        '''
                根据倒落配置得到物品模版
        @param dropConfig: 掉落配置
        '''
        itemTemplate = None
        r = random.randint(0, self._dropCoefficient)
        if r > 0 and r < dropConfig['primaryItemRate']:
            itemTemplateGenerator  = (template for template in dbaccess.all_ItemTemplate.values())
            try:
                itemTemplate = itemTemplateGenerator.next()
            except StopIteration:
                itemTemplate = 0
        else:
#            r = random.randint(0, 100000)
#            if r > 0 and r < dropConfig['secondaryItemRate']:
#                itemTemplates =[template for template in dbaccess.all_ItemTemplate.values() \
#                                if template['qualityLevel']>=dropConfig['secondaryItemQualityLevelLowerBound']\
#                                and template['qualityLevel']<=dropConfig['secondaryItemQualityLevelUpperBound']]
#                filterList = self.getItemTypeList(dropConfig['secondaryItemTypeFilter'])
#                itemTemplate = self.getItemWithFilter(itemTemplates, filterList)
            itemTemplate = 0
        return itemTemplate

    def getDropItemExtraAttribute(self, dropConfig, itemTemplate, dropcoefficient):
        '''
                    获取掉落物品的附加属性
        @param dropConfig: 掉落配置信息
        @param itemTemplate: 物品模版
        @param dropcoefficient: 掉落的附加属性几率修正
        '''
        dropItemExAttrId = []
        sExAttrId = []
        eExAttrId = []
        if not dropcoefficient:
            dropcoefficient = 100000
        if itemTemplate and dropConfig:
            templateId = itemTemplate['id']
            if templateId == dropConfig['primaryItemRate']:
                dropItemExAttrId = self.getExAttrIDByDropConfig(dropConfig['primaryItemAttributeID'], dropConfig['primaryItemAttributeRate'], \
                                                              dropConfig['primaryItemAttributeLowerBound'], dropConfig['primaryItemAttributeUpperBound'], \
                                                              True, dropcoefficient)
            else:
                dropItemExAttrId = self.getExAttrIDByDropConfig(dropConfig['secondaryItemAttributeID'], dropConfig['secondaryItemAttributeID'], \
                                                              dropConfig['secondaryItemAttributeLowerBound'], dropConfig['secondaryItemAttributeUpperBound'], \
                                                              False, dropcoefficient)
        tmp = dropItemExAttrId
        if (len(tmp) > 1):#多个附加属性
            sExAttrId = []
            eExAttrId = dropItemExAttrId
        elif (len(tmp) == 1):
            sExAttrId = [tmp[0]]
            eExAttrId = []
        else:
            sExAttrId = []
            eExAttrId = []
        if (itemTemplate["type"] > 999999):#道具没有附加属性,强制消除
            sExAttrId = []
            eExAttrId = []

        return  sExAttrId, eExAttrId

    def getExAttrIDByDropConfig(self, exAttrID, exAttrRate, lower, upper, isPrimaryDrop, dropCoefficient):
        '''
                    根据掉落配置随出一个extraAttribute的Id
        @param exAttrID: 配置中附加属性id
        @param exAttrRate: 配置中附加属性几率
        @param lower:配置中附加属性下限
        @param upper: 配置中附加属性上限
        @param isPrimaryDrop: 是否是指定物品掉落
        @param dropCoefficient: 玩家角色的掉落几率            
        '''
        if lower > upper:
            (lower, upper) = (upper, lower)
        ret_exAttributeId = []
        tmp_exAttributeId = [int(tmp_attr) for tmp_attr in exAttrID.split(';')]
        tmp_exAttributeRate = [int (tmp_attrRate) for tmp_attrRate in exAttrRate.split(';')]
        if isPrimaryDrop and [tmp_attr for tmp_attr in tmp_exAttributeId if int(tmp_attr)>=0]:
            ret_exAttributeId.append[tmp_exAttributeId[0]]
            return ret_exAttributeId
        
        if(lower == upper):
            lv = lower
        else:
            r = random.randint(lower, upper)
            cursor = connection.cursor()
            cursor.execute("select level from `exattribute_level` where value>=%d order by level" % r)
            ret = cursor.fetchall()
            cursor.close()
            lv = ret[0]['level']
        #从符合LV的附加属性项里随出一个项的ID
        cursor = connection.cursor()
        cursor.execute('select * from `extra_attributes` where level =%d' % lv)
        exAttrs = cursor.fetchall()
        l = len(exAttrs)
        if l > 0:#掉落项时,exattrrate参数做为掉落机率,先决定掉落类型
            for i in range(0, len(tmp_exAttributeRate)):
                r = random.randint(0, 100000)
                if r > 0 and r < tmp_exAttributeRate[i] * (dropCoefficient / 100000):
                    #随出本类型个数的MF
                    ret_exAttributeId = []
                    type = 0
                    c = 0
                    while c < (len(tmp_exAttributeRate) - i):
                        l = len(exAttrs)
                        r = random.randint(0, l - 1)
                        exAttr = exAttrs[r]
                        assert(exAttr)
                        exAttrs.remove(exAttr)
                        if (type & (1 << exAttr["type"])) == 0:      #没有同类型 的MF
                            ret_exAttributeId =ret_exAttributeId.append(exAttr["id"])
                            type |= (1 << exAttr["type"])
                            c += 1
                    break
                
        return ret_exAttributeId

    def getItemTypeList(self, type):
        '''从复合type转换为独立type列表'''
        typeList = []
        if(type >= 10000000):
            typeList.append(10000000)
            type -= 10000000

        if(type >= 7000000):
            typeList.append(4000000)
            typeList.append(2000000)
            typeList.append(1000000)
            type -= 7000000

        if(type >= 6000000):
            typeList.append(4000000)
            typeList.append(2000000)
            type -= 6000000

        if(type >= 5000000):
            typeList.append(4000000)
            typeList.append(1000000)
            type -= 5000000

        if(type >= 4000000):
            typeList.append(4000000)
            type -= 4000000

        if(type >= 3000000):
            typeList.append(2000000)
            typeList.append(1000000)
            type -= 3000000

        if(type >= 2000000):
            typeList.append(2000000)
            type -= 2000000

        if(type >= 1000000):
            typeList.append(1000000)
            type -= 1000000

        #消耗改造任务物品
        if(type >= 300000):
            typeList.append(100000)
            typeList.append(200000)
            type -= 300000

        if(type >= 200000):
            typeList.append(200000)
            type -= 200000

        if(type >= 100000):
            typeList.append(100000)
            type -= 100000

        #项链腰饰
        if(type >= 70000):
            typeList.append(40000)
            typeList.append(20000)
            typeList.append(10000)
            type -= 70000

        if(type >= 60000):
            typeList.append(40000)
            typeList.append(20000)
            type -= 60000

        if(type >= 50000):
            typeList.append(40000)
            typeList.append(10000)
            type -= 50000

        if(type >= 40000):
            typeList.append(40000)
            type -= 40000

        if(type >= 30000):
            typeList.append(20000)
            typeList.append(10000)
            type -= 30000

        if(type >= 20000):
            typeList.append(20000)
            type -= 20000

        if(type >= 10000):
            typeList.append(10000)
            type -= 10000

        #重皮布甲
        if(type >= 1120):
            typeList.append(640)
            typeList.append(320)
            typeList.append(160)
            type -= 1120

        if(type >= 960):
            typeList.append(320)
            typeList.append(640)
            type -= 960

        if(type >= 800):
            typeList.append(160)
            typeList.append(640)
            type -= 800

        if(type >= 640):
            typeList.append(640)
            type -= 640

        if(type >= 480):
            typeList.append(160)
            typeList.append(320)
            type -= 480

        if(type >= 320):
            typeList.append(320)
            type -= 320

        if(type >= 160):
            typeList.append(160)
            type -= 160

        #鞋子护腕披风
        if(type >= 150):
            typeList.append(10)
            typeList.append(20)
            typeList.append(40)
            typeList.append(80)
            type -= 150

        if(type >= 140):
            typeList.append(80)
            typeList.append(40)
            typeList.append(20)
            type -= 140

        if(type >= 130):
            typeList.append(80)
            typeList.append(40)
            typeList.append(10)
            type -= 130

        if(type >= 120):
            typeList.append(80)
            typeList.append(40)
            type -= 120

        if(type >= 110):
            typeList.append(80)
            typeList.append(20)
            typeList.append(10)
            type -= 110

        if(type >= 100):
            typeList.append(80)
            typeList.append(20)
            type -= 100

        if(type >= 90):
            typeList.append(80)
            typeList.append(10)
            type -= 90

        if(type >= 80):
            typeList.append(80)
            type -= 80

        if(type >= 70):
            typeList.append(40)
            typeList.append(20)
            typeList.append(10)
            type -= 70

        if(type >= 60):
            typeList.append(40)
            typeList.append(20)
            type -= 60

        if(type >= 50):
            typeList.append(40)
            typeList.append(10)
            type -= 50

        if(type >= 40):
            typeList.append(40)
            type -= 40

        if(type >= 30):
            typeList.append(20)
            typeList.append(10)
            type -= 30

        if(type >= 20):
            typeList.append(20)
            type -= 20

        if(type >= 10):
            typeList.append(10)
            type -= 10

        #头部上装腰带下装
        if(type >= 7):
            typeList.append(4)
            typeList.append(2)
            typeList.append(1)
            type -= 7

        if(type >= 6):
            typeList.append(4)
            typeList.append(2)
            type -= 6

        if(type >= 5):
            typeList.append(4)
            typeList.append(1)
            type -= 5

        if(type >= 4):
            typeList.append(4)
            type -= 4

        if(type >= 3):
            typeList.append(2)
            typeList.append(1)
            type -= 3

        if(type >= 2):
            typeList.append(2)
            type -= 2

        if(type >= 1):
            typeList.append(1)
            type -= 1

        return typeList

    def getItemWithFilter(self, items, filterList):
        l = len(items);
        ret = None
        if len(filterList) == 0:
            r = random.randint(0, l - 1);
            ret = items[r];
        else:
            ret_items = []
            for i in items:
                lhs = self.getItemTypeList(i["type"])
                if not self.isItemTypeHasSame(lhs, filterList):
                    ret_items.append(i);

            l = len(ret_items);
            if l > 0:
                r = random.randint(0, l - 1);
                ret = ret_items[r];
        return ret

    def isItemTypeHasSame(self, lhs, rhs):
        '''判断物品模版类型是否同名'''
        for i in lhs:
            if (i in rhs):
                return True;
        return False

    def getDropConfigOnNpc(self, npc):
        '''获取npc掉落物品'''
        levelgroup = npc['levelGroup'].split(';')
        encounteroddgroup = npc['encounterOddGroup'].split(';')
        dropitemidgroup = npc['dropItemIdGroup'].split(';')
        levelQueue = []
        totalSeed = 0
        i = 0
        while i < len(levelgroup):
            if (i < len(encounteroddgroup)):
                encounterodd = int(encounteroddgroup[i])
            else:
                encounterodd = 0
            if (i < len(dropitemidgroup)):
                dropitemid = int(dropitemidgroup[i])
            else:
                dropitemid = 0
            totalSeed = totalSeed + int(encounterodd)
            levelMap = {}
            levelMap['level'] = levelgroup[i]
            levelMap['encounterodd'] = encounterodd
            levelMap['dropItemId'] = dropitemid
            levelMap['seed'] = totalSeed
            levelQueue.append(levelMap)
            i = i + 1
        monster_dropitem_id = -1
        r = random.randint(0, totalSeed)
        for elm in levelQueue:
            if r < elm['seed']:
                monster_dropitem_id = elm['dropItemId']
                break;
        return monster_dropitem_id
    
    