#coding:utf8
'''
Created on 2011-3-28

@author: sean_lan
'''

from app.chatServer.component.baseInfo.ItemBaseInfoComponent import ItemBaseInfoComponent
from app.chatServer.component.attribute.ItemAttributeComponent import ItemAttributeComponent
from app.chatServer.component.item.ItemMosaicComponent import ItemMosaicComponent
from app.chatServer.component.pack.ItemPackComponent import ItemPackComponet
from app.chatServer.utils.dbopera import dbItems
from app.chatServer.app import configure
from app.chatServer.core.language.Language import Lg
#import math

class Item(object):
    '''物品类'''
    
    def __init__(self,itemTemplateId = 0,id = 0,name =''):
        '''初始化物品类
        @param id: int 物品在数据库中的id
        @param itemTemplateId: int 物品的模板id
        @param selfExtraAttributeId: []int list 物品自身附加属性
        @param dropExtraAttributeId: []int list 物品掉落时的附加属性 
        '''
        self.baseInfo = ItemBaseInfoComponent(self,id,name,itemTemplateId)
        self.attribute = ItemAttributeComponent(self)
        self.mosaic = ItemMosaicComponent(self)
        self.pack = ItemPackComponet(self)
        if id!=-1 and id!=0:
            self.initItemInstance()
        
    def initItemInstance(self):
        '''初始化实际物品信息
        '''
        itemInstance = dbItems.getItemInfo(self.baseInfo.id)
        if not itemInstance:
            pass
        self.baseInfo.setItemTemplateId(itemInstance['itemTemplateId'])
        self.attribute.setDurability(itemInstance['durability'])
        self.attribute.setIsBound(itemInstance['isBound'])
        self.attribute.setIdentification(itemInstance['identification'])
        self.attribute.strengthen=itemInstance['strengthen'] #物品强化等级
        self.attribute.workout=itemInstance['workout'] #物品祭炼成长值
        self.pack.setStack(itemInstance['stack'])
        self.mosaic.setSlot(itemInstance['slot_1'], itemInstance['slot_2'],
                             itemInstance['slot_3'], itemInstance['slot_4'])
        self.updateFJ()
        
    def updateFJ(self):
        '''更新物品附加信息（适用于强化物品）'''
        qh=self.attribute.getStrengthen()

        pz=self.baseInfo.getItemTemplateInfo().get("baseQuality",0)#获取品质
#        qh=StrengthenManager().getGainInfo(self.attribute.strengthen,pz) #获取强化信息
        itemProfession=self.baseInfo.getItemProfession()#职业类型限制 1战士 2 法师 3 游侠 4 牧师
#        if not qh:
#            return False
#        if self.attribute.strengthen>=0:
#            pass
#            #print " "
        iteminfo=self.baseInfo.getItemTemplateInfo() #物品模板id信息
        typeid=iteminfo.get('bodyType',0)
        array=configure.getAttributeByZyAndWqTypeid(itemProfession, typeid,qh)
        if array[0]==Lg().g(36):
            self.attribute.extMagicAttack=array[1]#附加魔法攻击
        elif array[0]==Lg().g(34):
            self.attribute.extPhysicalAttack= array[1]#附加物理攻击
        elif array[0]==Lg().g(35):
            self.attribute.extPhysicalDefense=array[1] #附加物理防御
        elif array[0]==Lg().g(37):
            self.attribute.extMagicDefense= array[1]#附加魔法防御
        elif array[0]==Lg().g(55):
            self.attribute.extSpeedAdditional=array[1]#附加攻速
        elif array[0]==Lg().g(32):
            self.attribute.extHpAdditional=array[1]#附加最大血量
        
    def getWQtype(self):
        '''获取装备类型 #0=衣服#1=裤子 #2=头盔#3=手套#4=靴子#5=护肩#6=项链#7=戒指#8=主武器#9=副武器#10=双手'''
        iteminfo=self.baseInfo.getItemTemplateInfo() #物品模板id信息
        typeid=iteminfo.get('bodyType',0)
        return typeid
    
    def formatItemInfo_new(self,suitecnt = 0):
        '''格式化物品信息'''
        data = self.baseInfo.getItemTemplateInfo() #字典类型
        if self.baseInfo.getItemFinalyPrice()>0:
            data['buyingRateCoin'] = self.baseInfo.getItemFinalyPrice()
        data['stack'] = self.pack.getStack()
        data['templateId'] = self.baseInfo.getItemTemplateId()
        if self.baseInfo.getId()!=0:
            data['id']= self.baseInfo.getId()
        else:
            data['id'] = self.baseInfo.getItemTemplateId()
        data['prefixNmae'] = ''#u'开天辟地'
        data['suffixName'] = ''#u'魂'
        data['isBound'] = self.attribute.getIsBound()
        data['nowQuality'] = data['baseQuality']
        data['extAttack'] = 0
        data['extStr'] = -1
        data['extVit'] = -1
        data['extDex'] = -1
        data['extWis'] = -1
        data['extPhysicalAttack'] = self.attribute.extPhysicalAttack
        data['extMagicAttack'] = self.attribute.extMagicAttack
        data['extPhysicalDefense'] = self.attribute.extPhysicalDefense
        data['extMagicDefense'] = self.attribute.extMagicDefense
        data['extHpAdditional'] = self.attribute.extHpAdditional
        data['extHitAdditional'] = -1
        data['extCritAdditional'] = -1
        data['extBlockAdditional'] = -1
        data['extDodgeAdditional'] = -1
        data['extSpeedAdditional'] = self.attribute.extSpeedAdditional
        data['equipEffect'] = u''
        data['devilEffect'] = u''
        data['suiteEffect'] = u''
        data['SuiteItems'] = []#[{'suitItemName':data['name'],'hasSiutitem':1},{'suitItemName':data['name'],'hasSiutitem':1}]
        data['nowDurability'] = 0
        data['extDefense'] = 0
        data['starLevel'] = self.attribute.strengthen #强化等级
        data['itemPage']=self.baseInfo.getitemPage()
        data['xqInfo'] = self.mosaic.getMosaicInfo()
        data['suiteInfo'] = {}
        if data.get('suiteId',0):
            setinfo = dbItems.ALL_SETINFO[data.get('suiteId',0)]
            allsetattr = eval(setinfo['effect'])
            data['suiteInfo']['suitename'] = setinfo['setname']
            data['suiteInfo']['nowcnt'] = suitecnt
            data['suiteInfo']['maxcnt'] = 6
            data['suiteInfo']['suiteeffct'] = []
            for key,value in allsetattr.items():
                info = {}
                info['effectstr'] = value.get('desc')
                info['enable'] = False
                if key <= suitecnt:
                    info['enable'] = True
                data['suiteInfo']['suiteeffct'].append(info)
        return data
    
    def formatItemInfo(self):
        '''格式化物品信息'''
        data = self.baseInfo.getItemTemplateInfo()
        data['id']= self.baseInfo.getId()
        data['templateId'] = self.baseInfo.getItemTemplateId()
        data['stack'] = self.pack.getStack()
        return data
    
    def getItemAttributes(self):
        '''获取装备的附加属性
        '''
        info = {}
        data = self.baseInfo.getItemTemplateInfo()
        mosaicattr = self.mosaic.getSlotAttr()
        mosaicStr = mosaicattr.get('Str',0)
        mosaicDex = mosaicattr.get('Dex',0)
        mosaicVit = mosaicattr.get('Vit',0)
        mosaicWis = mosaicattr.get('Wis',0)
        mosaicMaxHp = mosaicattr.get('MaxHp',0)
        mosaicPhyAtt = mosaicattr.get('PhyAtt',0)
        mosaicPhyDef = mosaicattr.get('PhyDef',0)
        mosaicMigAtt = mosaicattr.get('MigAtt',0)
        mosaicMigDef = mosaicattr.get('MigDef',0)
        mosaicHitRate = mosaicattr.get('HitRate',0)
        mosaicDodge = mosaicattr.get('Dodge',0)
        mosaicCriRate = mosaicattr.get('CriRate',0)
        mosaicSpeed = mosaicattr.get('Speed',0)
        mosaicBlock = mosaicattr.get('Block',0)
        info['Str'] = data.get('baseStr')+ mosaicStr if data.get('baseStr')>0 else mosaicStr
        info['Dex'] = data.get('baseDex')+ mosaicDex if data.get('baseDex')>0 else mosaicDex
        info['Vit'] = data.get('baseVit')+ mosaicVit if data.get('baseVit')>0 else mosaicVit
        info['Wis'] = data.get('baseWis')+ mosaicWis if data.get('baseWis')>0 else mosaicWis
        info['MaxHp'] = data.get('baseHpAdditional')+ mosaicMaxHp if data.get('baseHpAdditional')>0 else mosaicMaxHp
        info['PhyAtt'] = data.get('basePhysicalAttack')+ mosaicPhyAtt if data.get('basePhysicalAttack')>0 else mosaicPhyAtt
        info['PhyAtt'] += self.attribute.extPhysicalAttack 
        info['PhyDef'] = data.get('basePhysicalDefense')+ mosaicPhyDef if data.get('basePhysicalDefense')>0 else mosaicPhyDef
        info['PhyDef'] += self.attribute.extPhysicalDefense
        info['MigAtt'] = data.get('baseMagicAttack')+ mosaicMigAtt if data.get('baseMagicAttack')>0 else mosaicMigAtt
        info['MigAtt'] += self.attribute.extMagicAttack
        info['MigDef'] = data.get('baseMagicDefense')+ mosaicMigDef if data.get('baseMagicDefense')>0 else mosaicMigDef
        info['MigDef'] += self.attribute.extMagicDefense
        info['HitRate'] = data.get('baseHitAdditional')+ mosaicHitRate if data.get('baseHitAdditional')>0 else mosaicHitRate
        info['Dodge'] = data.get('baseDodgeAdditional')+ mosaicDodge if data.get('baseDodgeAdditional')>0 else mosaicDodge
        info['CriRate'] = data.get('baseCritAdditional')+ mosaicCriRate if data.get('baseCritAdditional')>0 else mosaicCriRate
        info['Speed'] = data.get('baseSpeedAdditional')+ mosaicSpeed if data.get('baseSpeedAdditional')>0 else mosaicSpeed
        info['Speed'] += self.attribute.extSpeedAdditional
        info['Block'] = data.get('baseBlockAdditional')+ mosaicBlock if data.get('baseBlockAdditional')>0 else mosaicBlock
        info['StrPercen'] = mosaicattr.get('StrPercen',0)
        info['DexPercen'] = mosaicattr.get('DexPercen',0)
        info['VitPercen'] = mosaicattr.get('VitPercen',0)
        info['WisPercen'] = mosaicattr.get('WisPercen',0)
        info['PhyAttPercen'] = mosaicattr.get('PhyAttPercen',0)
        info['PhyDefPercen'] = mosaicattr.get('PhyDefPercen',0)
        info['MigAttPercen'] = mosaicattr.get('MigAttPercen',0)
        info['MigAttPercen'] = mosaicattr.get('MigAttPercen',0)
        info['MaxHpPercen'] = mosaicattr.get('MaxHpPercen',0)
        return info
        
    def InsertItemIntoDB(self,characterId = 0):
        '''将物品信息写入数据库'''
        itemTemplateId = self.baseInfo.itemTemplateId
        isBound = 0
        if self.baseInfo.getItemTemplateInfo()['bindType']== 1:#物品的绑定类型是拾取后绑定
            isBound = 1
        durability = self.baseInfo.getItemTemplateInfo()['baseDurability']
        identification = self.attribute.getIdentification()
        stack = self.pack.getStack()
        result = dbItems.produceOneItem(characterId,itemTemplateId,isBound,
                                        durability,identification,stack)
        itemId = result
        self.baseInfo.setId(itemId)
        return itemId
    
    def destroyItemInDB(self):
        '''删除数据库中的自身的信息'''
        if self.baseInfo.id!=0:
            return dbItems.deleteItem(self.baseInfo.id)
        return False
    
    def SerializationItemInfo(self,bearer,suitecnt = 0):
        '''将自己的所有属性序列号付给Message对象
        @param bearer: Message Object 承载者
        @param stack: int 物品数量
        '''
        data = self.formatItemInfo_new(suitecnt = suitecnt)
        filednames = ['id', 'prefixNmae','suffixName','isBound', 'extAttack',
                           'extStr', 'extVit','extDex', 'extWis',
                            'extPhysicalAttack','extMagicAttack',
                            'extPhysicalDefense','extMagicDefense', 
                            'extHpAdditional','extHitAdditional', 
                            'extCritAdditional','extBlockAdditional',
                            'extDodgeAdditional','extSpeedAdditional',
                            'buyingRateCoin','extDefense',
                            'stack','starLevel','templateId','xqInfo','suiteInfo']
        for fd in filednames:
            if fd=='xqInfo':
                xqInforesponse = bearer.xqInfo
                xqInfo = data[fd]
                for key,value in xqInfo.items():
                    try:
                        setattr(xqInforesponse,key,value)
                    except:
                        setattr(xqInforesponse,key,value.decode('utf8'))
            elif fd=='suiteInfo':
                suiteInfo = data.get('suiteInfo')
                suiteInforesponse = bearer.suiteInfo
                if not suiteInfo:
                    continue
                suiteInforesponse.nowcnt = suitecnt
                suiteInforesponse.maxcnt = suiteInfo.get('maxcnt',6)
                try:
                    suiteInforesponse.suitename = suiteInfo.get('suitename','')
                except:
                    suiteInforesponse.suitename = suiteInfo.get('suitename','').decode('utf8')
                suiteeffctlist = suiteInforesponse.suiteeffct
                for suiteeffct in suiteInfo.get('suiteeffct',[]):
                    suiteeffctresponse = suiteeffctlist.add()
                    suiteeffctresponse.enable = suiteeffct.get('enable',False)
                    try:
                        suiteeffctresponse.effectstr = suiteeffct.get('effectstr','')
                    except:
                        suiteeffctresponse.effectstr = suiteeffct.get('effectstr','').decode('utf8')
            else:
                setattr(bearer,fd,data[fd])
        return bearer

        