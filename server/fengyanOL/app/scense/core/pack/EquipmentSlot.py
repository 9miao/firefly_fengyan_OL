#coding:utf8
'''
Created on 2011-3-29

@author: sean_lan
'''
from app.scense.component.pack.BasePackage import BasePackage
from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbItems
from app.scense.utils.DataLoader import loader
import copy
from app.scense import util
from app.scense.core.language.Language import Lg

BODYTYPE = ['body','trousers','header','bracer',
            'shoes','belt','necklace','waist','weapon','cloak']
    

class EquipmentSlot(BasePackage):
    '''角色装备栏'''
    #装备栏中装备位置编号（item的bodytype，装备在身体的部位）
    #0=衣服
    #1=裤子
    #2=头盔
    #3=手套
    #4=靴子
    #5=护肩
    #6=项链
    #7=戒指
    #8=主武器
    #9=副武器
    #10=双手
    
    def __init__(self,size = 10):
        '''
        @param size: int 包裹的大小
        @param EquipAttr: dict 装备属性
        '''
        BasePackage.__init__(self, size,packageType=0)
        self.EquipAttr = None
        
    def putEquipmentInEquipmentSlot(self,parts,equipment):
        '''根据数据库获取的信息设置物品
        @param part: str 部位名称
        @param equipment:  Item object 装备实例
        '''
        self.putItemByPosition(BODYTYPE.index(parts), equipment)
        
    def updateEquipment(self,characterId,partsId,equipment):
        '''更换装备
        @param characterId: int 角色的id
        @param partsId: int 角色的部位的id
        @param equipment: Item object 装备
        '''
        parts = BODYTYPE[partsId]
        if not equipment:
            itemId = -1
            self.dropItemByPosition(partsId)
        else:
            itemId = equipment.baseInfo.id
            self.putItemByPosition(partsId, equipment)
        result = dbaccess.updatePlayerEquipmen(characterId, parts, itemId)
        return result
    
    def getAllEquipttributes(self):
        '''得到玩家装备附加属性列表'''
        EXTATTRIBUTE = {}
        for item in [item['itemComponent'] for item in self._items]:
            info = item.getItemAttributes()
            EXTATTRIBUTE = util.gs.addDict(EXTATTRIBUTE, info)
        equipsetattr = self.getEquipmentSetAttr()
        EXTATTRIBUTE = util.gs.addDict(EXTATTRIBUTE, equipsetattr)
        return EXTATTRIBUTE
    
    def getWeaponType(self):
        '''获取武器类型'''
        item = self.getItemByPosition(9)
        if item:
            itemIfo = item.baseInfo.getItemTemplateInfo()
            return itemIfo.get('type',0)
        return 0
    
    def getZhuWeapon(self):
        '''获取主武器是否存在'''
        item = self.getItemByPosition(8)
        if item:
            return True#存在主武器
        return False#不存在主武器
    
    def getWeapon(self):
        '''获取武器信息'''
        item = self.getItemByPosition(9)
        itemInfo = {}
        if item:
            itemInfo = item.formatItemInfo()
        return itemInfo
    
    def getWeaponName(self):
        '''获取武器名称'''
        weaponInfo = self.getWeapon()
        return weaponInfo.get('name',Lg().g(504))
    
    def getItemDefenseInEquipSlot(self):
        '''获取装备基础防御'''
        defense = 0
        for item in [item['itemComponent'] for item in self._items]:
            itemInfo = item.baseInfo.getItemTemplateInfo()
            defense += max(0,itemInfo['defense'])
        return defense
    
    def getEquipmentleveBonus(self):
        '''得到装备等级加成'''
        levelBonus = 0
        for item in [item['itemComponent'] for item in self._items]:
            level = item.level._qualityLevel
            levelBonus += (level - 1) * 0.005
        return levelBonus
    
#===============获取装备附加一级属性============
            
    def getEquipmentStr(self):
        '''获取装备力量点'''
        eqstr = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseStr']!=-1:
                eqstr += itemInfo['baseStr']
            if itemInfo['extStr'] !=-1:
                eqstr += itemInfo['extStr']
        return eqstr      
          
    def getEquipmentVit(self):
        '''获取装备耐力点'''
        eqvit = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseVit']!=-1:
                eqvit += itemInfo['baseVit']
            if itemInfo['extVit'] !=-1:
                eqvit += itemInfo['extVit']
        return eqvit
                
    def getEquipmentDex(self):
        '''获取装备敏捷'''
        eqdex = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseDex']!=-1:
                eqdex += itemInfo['baseDex']
            if itemInfo['extDex'] !=-1:
                eqdex += itemInfo['extDex']
        return eqdex
                
    def getEquipmentWis(self):
        '''获取装备智力加成'''
        eqWis = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseWis']!=-1:
                eqWis += itemInfo['baseWis']
            if itemInfo['extWis'] !=-1:
                eqWis += itemInfo['extWis']
        return eqWis
    
#    def getEquipmentSpi(self):
#        '''获取装备精神加成'''
#        eqSpi = 0
#        for _item in self._items:
#            itemInfo =_item['itemComponent'].formatItemInfo_new()
#            if itemInfo['baseSpi']!=-1:
#                eqSpi += itemInfo['baseSpi']
#            if itemInfo['extSpi'] !=-1:
#                eqSpi += itemInfo['extSpi']
#        return eqSpi
                
#=======================获取装备附加二级属性=================
    def getEquipmentPhyAtt(self):
        '''获取装备物理攻击加成'''
        eqphyatt = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['basePhysicalAttack']!=-1:
                eqphyatt += itemInfo['basePhysicalAttack']
            if itemInfo['extPhysicalAttack'] !=-1:
                eqphyatt += itemInfo['extPhysicalAttack']
            if itemInfo['baseAttack'] !=-1:
                eqphyatt += itemInfo['baseAttack']
        return eqphyatt
    
    def getEquipmentPhyDef(self):
        '''获取装备物理防御'''
        eqphydef = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['basePhysicalDefense']!=-1:
                eqphydef += itemInfo['basePhysicalDefense']
            if itemInfo['extPhysicalDefense'] !=-1:
                eqphydef += itemInfo['extPhysicalDefense']
            if itemInfo['baseDefense'] !=-1:
                eqphydef += itemInfo['baseDefense']
        return eqphydef
    
    def getEquipmentMigAtt(self):
        '''获取装备魔法攻击'''
        eqmigatt = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseMagicAttack']!=-1:
                eqmigatt += itemInfo['baseMagicAttack']
            if itemInfo['extMagicAttack'] !=-1:
                eqmigatt += itemInfo['extMagicAttack']
            if itemInfo['baseAttack'] !=-1:
                eqmigatt += itemInfo['baseAttack']
        return eqmigatt
    
    def getEquipmentMigDef(self):
        '''获取装备魔法防御'''
        eqmigdef = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseMagicDefense']!=-1:
                eqmigdef += itemInfo['baseMagicDefense']
            if itemInfo['extMagicDefense'] !=-1:
                eqmigdef += itemInfo['extMagicDefense']
            if itemInfo['baseDefense'] !=-1:
                eqmigdef += itemInfo['baseDefense']
        return eqmigdef
    
    def getEquipmentMaxHp(self):
        '''获取装备最大血量加成'''
        eqmigdef = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseHpAdditional']!=-1:
                eqmigdef += itemInfo['baseHpAdditional']
            if itemInfo['extHpAdditional'] !=-1:
                eqmigdef += itemInfo['extHpAdditional']
        return eqmigdef
    
#    def getEquipmentMaxMp(self):
#        '''获取装备最大魔法加成'''
#        eqmigdef = 0
#        for _item in self._items:
#            itemInfo =_item['itemComponent'].formatItemInfo_new()
#            if itemInfo['baseMpAdditional']!=-1:
#                eqmigdef += itemInfo['baseMpAdditional']
#            if itemInfo['extMpAdditional'] !=-1:
#                eqmigdef += itemInfo['extMpAdditional']
#        return eqmigdef
    
    def getEquipmentHitRate(self):
        '''获取装备命中加成'''
        eqmigdef = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseHitAdditional']!=-1:
                eqmigdef += itemInfo['baseHitAdditional']
            if itemInfo['extHitAdditional'] !=-1:
                eqmigdef += itemInfo['extHitAdditional']
        return eqmigdef
    
    def getEquipmentDodge(self):
        '''获取装备闪避加成'''
        eqmigdef = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseDodgeAdditional']!=-1:
                eqmigdef += itemInfo['baseDodgeAdditional']
            if itemInfo['extDodgeAdditional'] !=-1:
                eqmigdef += itemInfo['extDodgeAdditional']
        return eqmigdef
    
    def getEquipmentCriRate(self):
        '''获取装备暴击加成'''
        eqmigdef = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseCritAdditional']!=-1:
                eqmigdef += itemInfo['baseCritAdditional']
            if itemInfo['extCritAdditional'] !=-1:
                eqmigdef += itemInfo['extCritAdditional']
        return eqmigdef
    
    def getEquipmentSpeed(self):
        '''获取装备攻速加成'''
        eqmigdef = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseSpeedAdditional']!=-1:
                eqmigdef += itemInfo['baseSpeedAdditional']
            if itemInfo['extSpeedAdditional'] !=-1:
                eqmigdef += itemInfo['extSpeedAdditional']
            if itemInfo['baseSpeed'] !=-1:
                eqmigdef += itemInfo['baseSpeed']
        return eqmigdef
    
    def getEquipmentBlock(self):
        '''获取装备格挡加成
        '''
        eqblock = 0
        for _item in self._items:
            itemInfo =_item['itemComponent'].formatItemInfo_new()
            if itemInfo['baseBlockAdditional']!=-1:
                eqblock += itemInfo['baseBlockAdditional']
            if itemInfo['extBlockAdditional'] !=-1:
                eqblock += itemInfo['extBlockAdditional']
        return eqblock
    
    def getEquipmentSetCont(self):
        '''获取装备中的装备的套装件数
        '''
        itemsetlist = [item['itemComponent'].baseInfo.itemtemplateInfo['suiteId'] \
                        for item in self._items \
                        if item['itemComponent'].baseInfo.itemtemplateInfo['suiteId']]
        nowsets = set(itemsetlist)
        setcontdict = {}
        for setid in nowsets:
            setcount = itemsetlist.count(setid)
            setcontdict[setid] = setcount
        return setcontdict
    
    def getEquipmentSetAttr(self):
        '''获取套装属性加成
        '''
        itemsetlist = [item['itemComponent'].baseInfo.itemtemplateInfo['suiteId'] \
                        for item in self._items \
                        if item['itemComponent'].baseInfo.itemtemplateInfo['suiteId']]
        nowsets = set(itemsetlist)
        info = {}
        for setid in nowsets:
            setinfo = dbItems.ALL_SETINFO[setid]
            setcount = itemsetlist.count(setid)
            allsetattr = eval(setinfo['effect'])
            for key,value in allsetattr.items():
                if key <= setcount:
                    effect = eval(value.get('effect'))
                    info = util.gs.addDict(info, effect)
        return info
    
    def getQualityEQCnt(self,quality):
        '''获取指定品质装备的数量'''
        itemlist = [item for item in self._items if item['itemComponent']\
                     and item['itemComponent'].baseInfo.getBaseQuality() == quality]
        return len(itemlist)
        
    def getGemLevel(self):
        '''获取角色身上装备的宝石的最高等级'''
        high = 0
        for iteminfo in self._items:
            item = iteminfo['itemComponent']
            nowlevel = item.mosaic.getItemGemLevel()
            if nowlevel>high:
                high = nowlevel
            if high>=14:
                break
        return high
        
        
    