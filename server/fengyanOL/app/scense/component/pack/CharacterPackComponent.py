#coding:utf8
'''
Created on 2011-3-27

@author: sean_lan
'''
from app.scense.component.Component import Component
from app.scense.core.pack import Package,EquipmentSlot
from app.scense.core.Item import Item
import copy,math,random
from app.scense.utils.dbopera import db_package, dbItems
from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbShop
from app.scense.netInterface.pushPrompted import pushPromptedMessage
from app.scense.netInterface.pushObjectNetInterface import pushCorpsApplication
from app.scense.core.language.Language import Lg


LOST_ONE = 1000#掉落一个几率
LOST_TOW = 10#掉落两个几率
LOST_THREE = 2#掉落三个几率
RATE_BASE = 100000#几率基础值
PET_EGG = 20700005
QHSIDLIST = [20030048,20030049,20030050]

def getlostnum():
    '''获取掉落装备的个数'''
    if (LOST_ONE+LOST_TOW+LOST_THREE)>RATE_BASE:
        raise Exception("keng die ne ?")
    rate = random.randint(0,RATE_BASE)
    if rate>(LOST_ONE+LOST_TOW+LOST_THREE):
        return 0
    elif rate>(LOST_ONE+LOST_TOW):
        return 3
    elif rate>(LOST_ONE):
        return 2
    else:
        return 1
    
def getLostPostion():
    '''获取掉落的位置'''
    count = getlostnum()
    lostposition = [random.choice(range(10)) for i in range(count)]
    return lostposition

def checkRate(rate):
    '''检测几率是否成功
    '''
    nowrate = random.randint(1,100)
    if nowrate<rate:
        return True
    return False


class CharacterPackageComponent(Component):
    '''角色的包裹组件
    '''
    
    def __init__(self, owner):
        '''初始化玩家包裹组件
        @param _package: Package object 包裹栏
        @param _tempPackage: TempPackage object 临时包裹栏
        @param _warehousePackage: WarehousePackage object 仓库栏
        @param _equipmentSlot: EquipmentSlot object 装备栏
        '''
        Component.__init__(self, owner)
        self._package = None
        self._tempPackage = None
        self._warehousePackage = None
        self._equipmentSlot = None
        
    def initPack(self,packageSize = 24):
        '''初始化包裹'''
        self.setPackage(size= packageSize)
        self.setEquipmentSlot()
    
    def getPackage(self):
        '''返回角色包裹信息'''
        return self._package
    
    def setPackage(self ,size = 12):
        '''读取数据库设置角色包裹
        @param size: int 包裹的大小
        '''
        self._package = Package.Package(size)
        itemsPackInfo = db_package.getPlayerItemsInPackage(self._owner.baseInfo.id)
        for itemPackInfo in itemsPackInfo:
            if itemPackInfo['itemId']==-1:
                continue
            item = Item(itemTemplateId=0,id =itemPackInfo['itemId'])
            self._package.putItemInPackage(itemPackInfo['position'], item,itemPackInfo['category'])
            
    def getEquipmentSlot(self):
        '''获取角色装备栏'''
        return self._equipmentSlot
    
    def isHaveStrengthen(self):
        '''判断是否有强化物品'''
        for bb in self._equipmentSlot.getItemList():
            item=bb.get('itemComponent',None)
            if item:
                if item.attribute.getStrengthen()>0:#如果物品被强化过
                    return True
        for cc in self._package._PropsPagePack.getItemList():
            item=cc.get('itemComponent',None)
            if item:
                if item.attribute.getStrengthen()>0:#如果物品被强化过
                    return True
        
        return False
    
    def isHaveXQ(self):
        '''判断是否有镶嵌过的物品'''
        for bb in self._equipmentSlot.getItemList():
            item=bb.get('itemComponent',None)
            if item:
                if item.mosaic.issolt():#如果物品镶嵌了宝石
                    return True
        for cc in self._package._PropsPagePack.getItemList():
            item=cc.get('itemComponent',None)
            if item:
                if item.mosaic.issolt():#如果物品镶嵌了宝石
                    return True
        
        return False
        
    def setEquipmentSlot(self,size = 10):
        '''设置角色装备栏
        @param size: int 装备栏默认为10个部位
        '''
        playerId = self._owner.baseInfo.id
        self._equipmentSlot = EquipmentSlot.EquipmentSlot()
        equipmentsInfo = db_package.getPlayerEquipInEquipmentSlot(self._owner.baseInfo.id)
        if not equipmentsInfo:
            db_package.initPlayerEquippack(playerId)
            equipmentsInfo = {}
        for equipmentInfo in equipmentsInfo.items():
            if equipmentInfo[1]==-1:
                continue
            item = Item(itemTemplateId=0,id=equipmentInfo[1])
            self._equipmentSlot.putEquipmentInEquipmentSlot(equipmentInfo[0], item)
        
    def putNewItemInPackage(self,item,position=-2,state = 1,turned = 0):
        '''放置一个新的物品到包裹栏中
        @param item: Item object 物品实例
        @param position: int 物品的位置
        @param packageType: int 包裹的类型
        @param state: int 是否及时的推送获取物品消息
        @param turned: int 是否是反牌子获取的
        '''
        packType = 1
        if item.baseInfo.getItemPageType()==4:
            packType = 2
        package = self._package.getPackageByType(packType)
        if position ==-2:
            position = package.findSparePositionForItem()
        if position==-1:
            return 1
        nowItem = package.getItemByPosition(position)
        if nowItem:#当所在的位置存在物品时
            return 1
        spacecnt = package.findSparePositionNum()
        if spacecnt<=5 :
            recCharacterId = self._owner.baseInfo.id
            tishiStr = Lg().g(377)
            contentStr = Lg().g(378)
            caozuoStr = Lg().g(379)
            pushCorpsApplication(recCharacterId, 7, tishiStr, contentStr, caozuoStr)
            _msg = Lg().g(380)
            pushPromptedMessage(_msg, [self._owner.getDynamicId()])
        msg = Lg().g(381)%(item.baseInfo.getRichName(),item.pack.getStack())
        maxstack = item.baseInfo.getItemTemplateInfo().get('maxstack',1)
        nowstack = item.pack.getStack()
        templateId = item.baseInfo.getItemTemplateId()
        if self._owner.pet.collectNotice(templateId,nowstack):
            if state:
                pushPromptedMessage(msg, [self._owner.getDynamicId()])
            else:
                self._owner.msgbox.putFightMsg(msg)
            return 2
        #先合并能合并的
        for _item in package.getItems():
            if _item['itemComponent'].baseInfo.getItemTemplateId()==templateId \
                                    and _item['itemComponent'].pack.getStack()<=maxstack:
                if _item['itemComponent'].pack.getStack()+nowstack<= maxstack:
                    _item['itemComponent'].pack.updateStack(_item['itemComponent'].pack.getStack()+nowstack)
                    nowstack = 0
                    break
        if nowstack:
            if item.baseInfo.getId()==0:
                item.InsertItemIntoDB(characterId = self._owner.baseInfo.id)
            package.putItemInstanceInPackDB(item, position, self._owner.baseInfo.getId())
        if state:
            pushPromptedMessage(msg, [self._owner.getDynamicId()])
        else:
            self._owner.msgbox.putFightMsg(msg)
        return 2
        
    def moveItem(self,packageType,fromPosition,toPosition,curpage):
        '''移动同一包裹中的物品
        @param packageType: int 包裹的类型     1:道具分页 2：任务物品分页
        @param fromPosition: int 物品的起始位置
        @param toPosition: int 物品的目的位置
        @param page: int 包裹的分页
        '''
        moveType = 1  #1:移动  2:合并    3:置换    4:拆分
        if fromPosition == toPosition: #无移动
            return {'result':False,'message':u''}
        
        if packageType==1:#道具包裹栏
            package = self._package.getPropsPagePack()
        elif packageType==2:#任务包裹栏
            package = self._package.getTaskPagePackItem()
        else:
            return {'result':False,'message':Lg().g(382)}
        fromPosition = package.getRealPostion(fromPosition, curpage)#获取真实的坐标
        toPosition = package.getRealPostion(toPosition, curpage)#获取真实的坐标
        fromItem = package.getItemByPosition(fromPosition)
        toItem = package.getItemByPosition(toPosition)
        if toPosition<0 or toPosition>=package.getSize():
            return {'result':False,'message':Lg().g(383)}
        if not fromItem:
            return {'result':False,'message':Lg().g(189)}
        if not toItem: #转移
            moveType = 1
            result = package.moveItemByPosition(fromPosition, toPosition)
            if result:
                data={'moveType':moveType,'packageType':packageType,
                      'fromstack':0,'tostack':fromItem.pack.getStack()}
                return {'result':True,'data':data}
            return {'result':False}
        else:
            maxstack = fromItem.baseInfo.getItemTemplateInfo().get('maxstack')
            fromstack = fromItem.pack.getStack()
            tostack = toItem.pack.getStack()
            if fromItem.baseInfo.getItemTemplateId()== \
            toItem.baseInfo.getItemTemplateId() and\
             maxstack>1 and fromstack !=maxstack and tostack!=maxstack:#合并以及部分合并
                moveType = 2
                if fromstack + tostack <= maxstack:
                    startstack = 0
                    endstack = fromstack + tostack
                    toItem.pack.updateStack(endstack)
                    package.deleteItemInPackage(fromPosition)
                    data={'moveType':moveType,'packageType':packageType}
                    return {'result':True,'data':data}
                else:
                    startstack = (fromstack + tostack) - maxstack
                    endstack = maxstack
                fromItem.pack.updateStack(startstack)
                toItem.pack.updateStack(endstack)
                data={'moveType':moveType,'packageType':packageType,\
                      'fromstack':startstack,'tostack':endstack}
                return {'result':True,'data':data}
                return {'result':False}
            else:#置换
                moveType = 3
                package.transpositionItems(fromPosition,toPosition)
                data={'moveType':moveType,'packageType':packageType,\
                      'fromstack':tostack,'tostack':fromstack}
                return {'result':True,'data':data}
            
    def itemConsignment(self,position,payNum,page,payType=1):
        '''物品寄卖
        @param position: int 物品在包裹中的位置
        '''
        package = self._package.getPropsPagePack()
        position = package.getRealPostion(position, page)
        item = package.getItemByPosition(position)
        if not item:
            return {'result':False,'message':Lg().g(189)}
        if item.attribute.getIsBound():
            return {'result':False,'message':Lg().g(384)}
        result = db_package.itemConsignment(self._owner.baseInfo.getId(),\
                                             item, payNum, payType)
        if not result:
            return {'result':False}
        result = db_package.updateItemInPackStack(3, item,0,tag=0)
        if not result:
            return {'result':False}
        package.removeItemByPosition(position)
        return {'result':True,'message':Lg().g(385)}

    def equipEquipment(self,fromPosition,toPosition,curpage,fromPackCategory):
        '''穿上装备
        @param fromPosition: int 物品在包裹中的位置
        @param toPosition: int 装备的位置 
        '''
        if self._owner.baseInfo.getStatus()==4:
            return {'result':False,'message':Lg().g(386)}
        if fromPackCategory==1:#道具包裹栏
            package = self._package.getPropsPagePack()
        elif fromPackCategory==2:#任务包裹栏
            package = self._package.getTaskPagePackItem()
        else:
            return {'result':False,'message':u'坑爹呢？'}
        fromPosition = package.getRealPostion(fromPosition, curpage)
        item = package.getItemByPosition(fromPosition)
        if not item:
            return {'result':False,'message':Lg().g(189)}
        itemPageType = item.baseInfo.getItemPageType()
        if itemPageType!=1:
            return self.useItem( fromPosition,fromPackCategory)
        if toPosition<0 or toPosition>10:
            return {'result':False,'message':Lg().g(383)}
        if item.baseInfo.getItemBodyType()==-1:
            return {'result':False,'message':Lg().g(387)}
        if item.baseInfo.getItemBodyType()!=toPosition:
            return {'result':False,'message':Lg().g(388)}
        professionRequired = item.baseInfo.getItemProfession()
        if professionRequired!=self._owner.profession.getProfession()\
         and professionRequired!=0:
            msg = Lg().g(389)%{1:Lg().g(390),2:Lg().g(391),\
                                3:Lg().g(392),4:Lg().g(393)}.get(professionRequired)
            return {'result':False,'message':msg}
        if item.baseInfo.getLevelRequired()> self._owner.level.getLevel():
            msg = Lg().g(394)%item.baseInfo.getLevelRequired()
            return {'result':False,'message':msg}
        equipPackage = self.getEquipmentSlot()
        if toPosition == 10:#作为双手武器的处理
            self.unloadedEquipment(9, -1, 1)
            toPosition = 8
        if toPosition ==9:
            mainHanditem = equipPackage.getItemByPosition(8)
            if mainHanditem and mainHanditem.baseInfo.getItemBodyType()==10:
                self.unloadedEquipment(8, -1, 1)
        toItem = equipPackage.getItemByPosition(toPosition)
        if not toItem:
            result1 = package.deleteItemInPackage(fromPosition,tag=0)
            if not result1:
                return {'result':False,'message':Lg().g(395)}
            result2 = equipPackage.updateEquipment(self._owner.baseInfo.id,\
                                                    toPosition, item)
            if result2:
                self._owner.teamcom.pushTeamMemberInfo()
                self._owner.quest.specialTaskHandle(101)#特殊任务处理
                cnt = equipPackage.getQualityEQCnt(3)
                self._owner.daily.noticeDaily(7,0,cnt)
                return {'result':True,'message':Lg().g(396)}
            else:
                return {'result':False,'message':Lg().g(395)}
        else:
            result1 = equipPackage.updateEquipment(self._owner.baseInfo.id,\
                                                    toPosition, item)
            result2 = package.deleteItemInPackage(fromPosition,tag=0)
            package.putItemInstanceInPackDB(toItem, fromPosition,\
                                             self._owner.baseInfo.id)
            if result1 and result2:
                self._owner.teamcom.pushTeamMemberInfo()
                self._owner.quest.specialTaskHandle(101)#特殊任务处理
                cnt = equipPackage.getQualityEQCnt(3)
                self._owner.daily.noticeDaily(7,0,cnt)
                return {'result':True,'message':Lg().g(396)}
            else:
                return {'result':False,'message':Lg().g(395)}
            
    def unloadedEquipment(self,fromPosition,toPosition,curpage):
        '''卸下装备
        @param fromPosition: int 物品在包裹中的位置
        @param toPosition: int 装备的位置 
        '''
        if self._owner.baseInfo.getStatus()==4:
            return {'result':False,'message':Lg().g(397)}
        equipPackage = self.getEquipmentSlot()
        package = self._package.getPropsPagePack()
        if toPosition==-1:
            toPosition = package.findSparePositionForItem()
        else:
            toPosition = package.getRealPostion(toPosition, curpage)
        if toPosition<0 or toPosition>=package.getSize():
            return {'result':False,'message':Lg().g(383)}
        
        item = equipPackage.getItemByPosition(fromPosition)
        toItem = package.getItemByPosition(toPosition)
        if toItem:
            return {'result':False,'message':Lg().g(397)}
        if not item:
            return {'result':False,'message':Lg().g(189)}
        package.putItemInPackDB(item, toPosition, self._owner.baseInfo.id)
        result2 = equipPackage.updateEquipment(self._owner.baseInfo.id, fromPosition, None)
        if result2:
            self._owner.teamcom.pushTeamMemberInfo()
            return {'result':True,'message':u''}
        else:
            return {'result':False,'message':u''}
        
    def dropItem(self,position,packageType,stack,dropType = 0,\
                 tag = 1,backupstate = 0,statu = 0):
        '''删除指定包裹中的物品
        @param position: int 物品在包裹中的位置
        @param packageType: int 包裹的类型
        @param stack: int 删除物品的数量
        @param tag: int 是否删除物品 1默认删除
        @param backupstate: int 是否备份物品信息
        @param statu: 1表示物品不足时照样删除
        @param dropType: int 丢弃类型，1为强制丢弃
        '''
        if packageType==1:#临时包裹栏
            package = self.getTempPackage()
        elif packageType==2:#仓库
            package = self.getWarehousePackage()
        elif packageType==3:#物品包裹
            package = self._package.getPropsPagePack()
        else:
            return {'result':False,'message':Lg().g(382)}
        item = package.getItemByPosition(position)
        if not item:
            return {'result':False,'message':Lg().g(189)}
        if not item.baseInfo.getItemDropType():
            return {'result':False,'message':Lg().g(398)}
        nowStack = item.pack.getStack()-stack
        if nowStack<0:
            return {'result':False,'message':Lg().g(374)}
        if nowStack == 0:
            package.deleteItemInPackage(position, tag=tag, backupstate=backupstate)
        else:
            item.pack.updateStack(item.pack.getStack()-stack)
        return {'result':True}
    
    def putNewItemsInPackage(self,itemTemplateId,count):
        '''添加物品到包裹栏'''
        item = Item(itemTemplateId =itemTemplateId)
        packType = 1
        if item.baseInfo.getitemPage()==4:
            packType = 2
        maxstack = item.baseInfo.getItemTemplateInfo().get('maxstack',1)
        package = self._package.getPackageByType(packType)
        itemcndlist = []
        while count - maxstack > 0:
            itemcndlist.append(maxstack)
            count -=maxstack
        itemcndlist.append(count)
        if package.findSparePositionNum()<len(itemcndlist):
            return False
        for count in itemcndlist:
            _item = copy.deepcopy(item)
            _item.pack.setStack( count)
            self.putNewItemInPackage(_item)
        return True
        
    def countItemTemplateId(self,TemplateId):
        '''判断是否存在物品'''
        itemInfo = dbaccess.all_ItemTemplate
        packType = 1
        if itemInfo.get('itemPage',1)==4:
            packType = 2
        package = self._package.getPackageByType(packType)
        count = package.countItemTemplateId(TemplateId)
        if not count:
            package = self._package.getTaskPagePackItem()
            count = package.countItemTemplateId(TemplateId)
        return count 
    
    def delItemByTemplateId(self,templateId,count):
        '''根据物品的模板id删除物品
        @param templateId: int 模板的id
        @param count: int 物品的数量
        '''
        itemInfo = dbaccess.all_ItemTemplate
        packType = 1
        if itemInfo.get('itemPage',1)==4:
            packType = 2
        package = self._package.getPackageByType(packType)
        positions = package.getItemTemplateIdPositions(templateId)
        if sum([item['stack'] for item in positions])< count:
            return -1#数量不足

        for item in positions:
            if count ==0:
                break
            if item['stack']>=count:
                self.dropItem(item['position'], 3, count)
                break
            else:
                self.dropItem(item['position'], 3, item['stack'])
                count -= item['stack']
        return 1#成功
    
    def delItemByItemId(self,itemId,count=1):
        '''根据物品的id删除物品
        @param itemId: int 物品的id
        @param count: int 物品的数量
        '''
        package = self._package.getPropsPagePack()
        position = package.getPositionByItemId(itemId)
        result = self.dropItem(position, 3, count)
        return result#成功
        
    def getNewItemInPackage(self,itemTemplateId):
        '''获取新的物品'''
        item = Item(itemTemplateId=itemTemplateId)
        item.InsertItemIntoDB(characterId=self._owner.baseInfo.id)
        self.putNewItemInPackage(item)
        
    def splitItemsInPack(self,packageType,fromposition,toposition,splitnum,curpage):
        '''拆分物品
        @param packageType: int 包裹的类型
        @param fromposition: int 物品的起始位置
        @param toposition: int 物品拆分到得包裹的位置 
        @param splitnum: int 拆分的数量 
        '''
        if splitnum==0:
            return {'result':False,'message':Lg().g(399)}
        if packageType==1:#道具包裹栏
            package = self._package.getPropsPagePack()
        elif packageType==2:#任务包裹栏
            package = self._package.getTaskPagePackItem()
        else:
            return {'result':False,'message':Lg().g(382)}
        fromposition = package.getRealPostion(fromposition, curpage)
        toposition = package.getRealPostion(toposition, curpage)
        if toposition<0 or toposition>=package.getSize():
            return {'result':False,'message':Lg().g(383)}
        if fromposition == toposition:
            return {'result':False,'message':u''}
        fromItem = package.getItemByPosition(fromposition)
        toItem = package.getItemByPosition(toposition)
        if not fromItem:
            return {'result':False,'message':Lg().g(189)}
        maxstack = fromItem.baseInfo.getItemTemplateInfo().get('maxstack',1)
        fromstack = fromItem.pack.getStack()
        if fromstack < splitnum:
            return {'result':False,'message':Lg().g(399)}
        startstack = fromstack
        endstack = 0
        if toItem:#转移到得地方有物品存在
            tostack = toItem.pack.getStack()
            if tostack + splitnum <= maxstack:
                endstack = tostack + splitnum
                startstack = fromstack-splitnum
            else:
                endstack = maxstack
                startstack = fromstack+tostack - maxstack
            if startstack<=0:
                package.deleteItemInPackage(fromposition)
            else:
                fromItem.pack.updateStack(fromstack-splitnum)
            toItem.pack.updateStack(endstack)
        else:#转移到得地方没有物品存在
            if splitnum>= fromstack:
                package.moveItemByPosition(fromposition, toposition)
                return {'result':True,'message':Lg().g(399)}
            else:
                fromItem.pack.updateStack(fromstack-splitnum)
            toItem = copy.deepcopy(fromItem)
            toItem.pack.setStack(splitnum)
            package.putItemInPackDB(toItem, toposition,self._owner.baseInfo.id)
        return {'result':True,'message':Lg().g(400)}
    
    def updateItemStack(self,packageType, position, stack):
        '''更新物品堆叠数'''
        package = self._package.getPackageByType(packageType)
        if not package:
            return {'result':False,'message':Lg().g(382)}
        package.updateItemStack(position,stack)
        
    def dropItemsInPack(self,position,packageType,curpage):
        '''丢弃物品
        @param packageType: int 包裹的类型
        @param position: int 物品在包裹中的位置
        '''
        package = self._package.getPackageByType(packageType)
        if not package:
            return {'result':False,'message':Lg().g(382)}
        position = package.getRealPostion(position, curpage)
        item = package.getItemByPosition(position)
        if not item:
            return {'result':False,'message':Lg().g(189)}
        package.deleteItemInPackage(position,backupstate=1)
        return {'result':True,'data':packageType}
        
    def packageArrange(self,packType):
        '''整理包裹'''
        package = self._package.getPackageByType(packType)
        package.Arrange()
        
    def sellItemInpack(self,fromPosition,frompackage,curpage,stack):
        '''出售包裹中的物品
        @param fromPosition: int 出售的物品的位置
        @param frompackage:  int 出售的物品的所在包裹分页
        @param curpage: int 当前页数
        '''
        package = self._package.getPackageByType(frompackage)
        fromPosition = package.getRealPostion(fromPosition, curpage)
        item = package.getItemByPosition(fromPosition)
        if not item:
            return {'result':False,'message':Lg().g(189)}
        if item.baseInfo.getItemSellType()==2:
            return {'result':False,'message':Lg().g(401)}
        if item.pack.getStack()<stack:
            return {'result':False,'message':Lg().g(374)}
        itemprice = item.baseInfo.getItemPrice()*stack
        if stack==item.pack.getStack():
            package.deleteItemInPackage(fromPosition,tag = 0)
            dbShop.addSellItem(item.baseInfo.getId(), self._owner.baseInfo.id)
        elif stack<item.pack.getStack():
            item.pack.updateStack(item.pack.getStack()-stack,tag=0)
            copyItem = copy.deepcopy(item)
            copyItem.pack.setStack(stack)
            copyItem.baseInfo.setId(0)
            copyItem.InsertItemIntoDB()
            dbShop.addSellItem(copyItem.baseInfo.getId(), self._owner.baseInfo.id)
        self._owner.finance.updateCoin(self._owner.finance.getCoin()+itemprice)
        self._owner.updatePlayerInfo()
        return {'result':True,'message':Lg().g(402)%itemprice}
    
    def checkPack(self,cunt):
        '''检测包裹
        '''
        if self._package._PropsPagePack.findSparePositionNum()<cunt:
            raise Exception(Lg().g(16))
    
    def useItem(self,position,fromPackCategory):
        '''使用物品
        @param packageType: int 包裹分页类型 1 全部 2
        @param position: int 物品所在包裹位置
        '''
        package = self._package.getPackageByType(fromPackCategory)
        item = package.getItemByPosition(position)
        if not item:
            return {'result':False,'message':Lg().g(189)}
        script = item.baseInfo.getUseScript()#物品使用的脚本
        if not script:
            pushPromptedMessage(Lg().g(403),[self._owner.getDynamicId()])
            return {'result':False,'message':Lg().g(403)}
        professionRequired = item.baseInfo.getItemProfession()
        if professionRequired!=self._owner.profession.getProfession() and professionRequired!=0:
            return {'result':False,'message':Lg().g(404)}
        if item.baseInfo.getLevelRequired()> self._owner.level.getLevel():
            return {'result':False,'message':Lg().g(405)}
        nowstack = item.pack.getStack()
        try:
            exec(script)#执行任务脚本
        except Exception,e:
            return {'result':False,'message':e.message}
        if nowstack-1>0:
            self.updateItemStack(fromPackCategory, position, nowstack-1)
        else:
            package.deleteItemInPackage(position)
        self._owner.updatePlayerInfo()
        usetype = 0
        if PET_EGG == item.baseInfo.getItemTemplateId():
            usetype =1
        return {'result':True,'message':Lg().g(406)%item.baseInfo.getName(),'usetype':usetype}
        
    def packageExpansion(self,packageType,curpage,position):
        '''包裹扩充'''
        package = self._package.getPackageByType(packageType)
        PurposeSize = (curpage-1)*self._package.LIMIT + position +1
        start = package.getSize()-24
        if start<0:
            return {'result':False,'message':u'坑爹呢！'}
        end = PurposeSize - package.getSize()
        if end<0:
            return {'result':False,'message':u'坑爹呢！'}
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
        dbaccess.updatePlayerInfo(self._owner.baseInfo.id, {'packageSize':PurposeSize})
        pushPromptedMessage(Lg().g(352)%cost,[self._owner.getDynamicId()])
        return {'result':True,'message':Lg().g(352)%cost}
        
    def _LostItem(self,position):
        '''爆掉物品'''
        equipPackage = self.getEquipmentSlot()
        item = equipPackage.getItemByPosition(position)
        if item:
            equipPackage.updateEquipment(self._owner.baseInfo.id, position, None)
        return item
    
    def LostItem(self):
        '''爆掉物品'''
        positionlist = getLostPostion()
        itemlist = []
        
#        for position in positionlist:
#            item = self._LostItem(position)
#            if item:
#                itemlist.append(item)
        return itemlist
        
    def openChest(self,itemsInfolist,default,requiredItem,requiredCount):
        '''开启宝箱
        @param itemsInfo: list [(物品ID，物品数量，随机区间)]随机掉落
        @param default: (物品ID，物品数量)默认掉落
        @param requiredItem: int 需要消耗的物品的模板ID
        @param requiredCount: int 需要消耗的物品的数量
        '''
        if requiredItem!=0:
            count = self._owner.pack.countItemTemplateId(requiredItem)
            itemInfo = dbaccess.all_ItemTemplate.get(requiredItem)
            if count<requiredCount:
                raise Exception(u'%s数量不足'%itemInfo.get('name'))
        itemsrates = [item[2] for item in itemsInfolist]
        iteminfo = None
        rate = random.randint(0,RATE_BASE)
        for index in range(len(itemsInfolist)):
            if rate<sum(itemsrates[:index+1]):
                iteminfo = itemsInfolist[index]
                break
        if not iteminfo:
            iteminfo = default
        result = self.putNewItemsInPackage(iteminfo[0], iteminfo[1])
        if not result:
            raise Exception(Lg().g(16))
        self.delItemByTemplateId(requiredItem, requiredCount)
    
    def GetStrengthenPackageInfo(self,curPage,limit = 24):
        '''获取强化包裹的信息'''
#        if self._owner.level.getLevel()<6:
#            return {'result':False,'message':Lg().g(301)}
        canstrItemList = []#可强化的物品的列表
#        qhsItemList = []#强化石列表
        maxPage = 1
        nowPage = curPage
        for _item in self._equipmentSlot._items:
            if _item and _item.get('itemComponent'):
                iteminfo = {}
                i_item = _item.get('itemComponent')
                iteminfo['item'] = i_item
                iteminfo['itemtag'] = 1
                canstrItemList.append(iteminfo)
        for _item in self._package._PropsPagePack._items:
            if _item and _item.get('itemComponent'):
                i_item = _item.get('itemComponent')
                if i_item.baseInfo.getItemBodyType()!=-1:
                    iteminfo = {}
                    iteminfo['item'] = i_item
                    iteminfo['itemtag'] = 2
                    canstrItemList.append(iteminfo)
#                elif i_item.baseInfo.getItemTemplateId() in QHSIDLIST:
#                    qhsItemList.append(i_item)
        if canstrItemList:
            maxPage = int(math.ceil(len(canstrItemList)*1.0/limit))
        return {'canstrItemList':canstrItemList[(curPage-1)*limit:curPage*limit],
                'maxPage':maxPage,
                'nowPage':nowPage}
        
    def getMosaicItemPackage(self,curPage,limit = 12):
        '''获取镶嵌装备包裹信息
        '''
        canMosaicItemList = []#可强化的物品的列表
        maxPage = 1
        nowPage = curPage
        for _item in self._equipmentSlot._items:
            if _item and _item.get('itemComponent'):
                iteminfo = {}
                i_item = _item.get('itemComponent')
                iteminfo['item'] = i_item
                iteminfo['itemtag'] = 1
                canMosaicItemList.append(iteminfo)
        for _item in self._package._PropsPagePack._items:
            if _item and _item.get('itemComponent'):
                i_item = _item.get('itemComponent')
                if i_item.baseInfo.getItemBodyType()!=-1:
                    iteminfo = {}
                    iteminfo['item'] = i_item
                    iteminfo['itemtag'] = 2
                    canMosaicItemList.append(iteminfo)
        if canMosaicItemList:
            maxPage = int(math.ceil(len(canMosaicItemList)*1.0/limit))
        data =  {'xqItemInfo':canMosaicItemList[(curPage-1)*limit:curPage*limit],
                'maxPage':maxPage,
                'nowPage':nowPage}
        return {'result':True,'data':data}
            
        
    def getMosaicGemPackage(self,curPage,limit = 8):
        '''获取镶嵌宝石包裹
        '''
        maxPage = 1
        nowPage = curPage
        gemItemList = []#镶嵌石列表    
        for _item in self._package._PropsPagePack._items:
            if _item and _item.get('itemComponent'):
                i_item = _item.get('itemComponent')
                gemtemplate = i_item.baseInfo.itemTemplateId
                if dbItems.ALL_GEMINFO.has_key(gemtemplate):
                    gemItemList.append(i_item)
        if gemItemList:
            maxPage = int(math.ceil(len(gemItemList)*1.0/limit))
        data =  {'itemsInfo':gemItemList[(curPage-1)*limit:curPage*limit],
                'maxPage':maxPage,
                'nowPage':nowPage}
        return {'result':True,'data':data}
        
    def ItemMosaic(self,packageType,itemId,gemId,position):
        '''镶嵌
        @param packageTyep: int 要镶嵌的物品所在的包裹
        @param itemId: int 要镶嵌的物品的ID
        @param gemId: int 宝石的ID
        @param position: int 镶嵌到的位置
        '''
        if packageType == 2:
            item = self._equipmentSlot.getItemInfoByItemid(itemId)
        else:
            item = self._package._PropsPagePack.getItemInfoByItemid(itemId)
        if self._owner.level.getLevel()<11:
            return {'result':False,'message':Lg().g(407)}
        if not item:
            return {'result':False,'message':Lg().g(189)}
        gem = self._package._PropsPagePack.getItemInfoByItemid(gemId)
        if not gem:
            return {'result':False,'message':Lg().g(408)}
        gemtemplate = gem.baseInfo.itemTemplateId
        geminfo = dbItems.ALL_GEMINFO.get(gemtemplate)
        if not geminfo:#如果选定的不是宝石
            return {'result':False,'message':Lg().g(409)}
        gemlevel = geminfo.get('level',0)
        viplevel = self._owner.baseInfo._viptype
        coinrequired =  int((gemlevel *2500 + 3000)*(1- 0.1 * viplevel))
        if self._owner.finance.getCoin()<coinrequired:
            return {'result':False,'message':Lg().g(88)}
        self._owner.finance.addCoin(-coinrequired)
        result = item.mosaic.Mosaic(gemtemplate,position)
        if result.get('result'):
            self._owner.schedule.noticeSchedule(3)#成功后的日程目标通知
            self._owner.quest.specialTaskHandle(121)#成功后的特殊任务通知
            self.delItemByItemId(gemId, 1)
            self._owner.pushInfoChanged()
            return {'result':True,'message':Lg().g(410)}
        return result
    
    def ItemRemoval(self,packageType,itemId,position):
        '''摘除宝石
        '''
        if packageType == 2:
            item = self._equipmentSlot.getItemInfoByItemid(itemId)
        else:
            item = self._package._PropsPagePack.getItemInfoByItemid(itemId)
        if not item:
            return {'result':False,'message':Lg().g(189)}
        gemtemplate = getattr(item.mosaic,'slot_%d'%position)
        if not gemtemplate:
            return {'result':False,'message':Lg().g(411)}
        if self._package._PropsPagePack.findSparePositionNum()<1:
                return {'result':False,'message':Lg().g(16)}
        geminfo = dbItems.ALL_GEMINFO.get(gemtemplate)
        gemlevel = geminfo.get('level',0)
        viplevel = self._owner.baseInfo._viptype
        coinrequired =  int((gemlevel *1000 + 3000)*(1- 0.1 * viplevel))
        if self._owner.finance.getCoin()<coinrequired:
            return {'result':False,'message':Lg().g(88)}
        self._owner.finance.addCoin(-coinrequired)
        compoundRate = min ( 100 - 5 * gemlevel + 10*viplevel , 100)
        if not checkRate(compoundRate):#检测合成几率，合成是否成功
            return {'result':True,'message':Lg().g(412)}
        itemTemplateId = item.mosaic.removal(position)
        if itemTemplateId:
            self.putNewItemsInPackage(itemTemplateId, 1)
            self._owner.pushInfoChanged()
            return {'result':True,'message':Lg().g(413)}
        return {'result':False,'message':Lg().g(412)}
    
    def getCompoundsInfo(self):
        '''获取所有合成的物品的信息
        '''
#        if self._owner.level.getLevel()<30:#功能等级开放限制
#            return {'result':False,'message':Lg().g(301)}
        equiplist = []#装备配方列表
        gemlist = []#宝石配方列表
        for compound in sorted(dbItems.ALL_COMPOUND.values(),key=lambda d:d['index']):
            info = {}
            info['itemId'] = compound['itemId']
            info['itemname'] = compound['name']
            info['level'] = compound['level']
            if compound['type'] == 1:
                equiplist.append(info)
            elif compound['type'] == 2:
                gemlist.append(info)
        return {'result':True,'data':{'equiplist':equiplist,'gemlist':gemlist}}
    
    def getOneItemCompoundInfo(self,itemId):
        '''获取某个物品的合成配方数据
        @param itemId: int 物品的ID
        '''
        compound = dbItems.ALL_COMPOUND.get(itemId)
        if not compound:
            return {'result':False,'message':u'配方信息部存在'}
        info = {}
        info['coinrequired'] = compound['coinrequired']
        info['itemA'] = compound['m1_item']
        info['itemAcnt'] = self._package._PropsPagePack.countItemTemplateId(info['itemA'])
        info['itemAGoal'] = compound['m1_cnt']
        info['itemB'] = compound['m2_item']
        info['itemBcnt'] = self._package._PropsPagePack.countItemTemplateId(info['itemB'])
        info['itemBGoal'] = compound['m2_cnt']
        info['itemBound'] = compound['itemId']
        return {'result':True,'data':info}
        
    def ItemCompound(self,itemId):
        '''合成物品
        @param param: 
        '''
        if self._owner.level.getLevel()<21:#功能等级开放限制
            return {'result':False,'message':Lg().g(414)}
        compound = dbItems.ALL_COMPOUND.get(itemId)
        if not compound:
            return {'result':False,'message':Lg().g(415)}
        coinrequired = compound['coinrequired']
        if coinrequired > self._owner.finance.getCoin():
            return {'result':False,'message':Lg().g(88)}
        itemArequired = compound['m1_cnt']
        nowitemAcnt = self._package._PropsPagePack.countItemTemplateId(compound['m1_item'])
        itemBrequired = compound['m2_cnt']
        nowitemBcnt = self._package._PropsPagePack.countItemTemplateId(compound['m2_item'])
        if itemArequired>nowitemAcnt or itemBrequired>nowitemBcnt:
            return {'result':False,'message':Lg().g(416)}
        self._owner.finance.addCoin(-coinrequired)
        itemname = compound.get('name','')
        if itemId in dbItems.ALL_GEMINFO.keys():
            gemlevel = compound.get('level',0)
            viplevel = self._owner.baseInfo._viptype
            compoundRate = min ( 100 - 5 * gemlevel + 10*viplevel , 100)
            if not checkRate(compoundRate):#检测合成几率，合成是否成功
                return {'result':True,'message':Lg().g(417)%itemname}
        self.delItemByTemplateId(compound['m1_item'], itemArequired)
        self.delItemByTemplateId(compound['m2_item'], itemBrequired)
        self.putNewItemsInPackage(itemId, 1)
        self._owner.schedule.noticeSchedule(4)#成功后的每日目标通知
        self._owner.quest.specialTaskHandle(125)#成功后的特殊任务通知
        return {'result':True,'message':Lg().g(418)%itemname}
    
    
    