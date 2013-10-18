#coding:utf8
'''
Created on 2011-4-13

@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.netInterface.pushPrompted import pushPromptedMessage
from app.scense.core.language.Language import Lg

EQUIPPOSITION = [2,5,0,3,1,4,6,7,8,9]

def getItemsInPackage(dynamicId,characterId,packCategory,page):
    '''获取角色包裹信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param packCategory: int 1:普通物品  2:任务
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    packageItemInfo = player.pack._package.getCategoryPageItemInfo(packCategory,page)
    return {'result':True,'message':u'','data':packageItemInfo}

def getItemsInTempPackage(dynamicId,characterId):
    '''获取角色的临时包裹栏
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    package = player.pack.getTempPackage()
    packageItemInfo = package.getPackageItemInfo()
    data = {'packageItemInfo':packageItemInfo}
    return {'result':True,'message':u'','data':data}

def getItemsInEquipSlot(dynamicId,characterId):
    '''获取角色的装备栏信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    package = player.pack.getEquipmentSlot()
    equipmentList = package.getItemList()
    suitecount = package.getEquipmentSetCont()
    keys_copy = dict([(items['position'],items) for items in equipmentList])
    equipmentList_copy = []
    for position in EQUIPPOSITION:
        item = keys_copy.get(position,None)
        equipmentList_copy.append(item)
    data = {'packageItemInfo':equipmentList_copy,'suitecount':suitecount}
    return {'result':True,'message':u'','data':data}

def getWarehouseInfo(dynamicId,characterId):
    '''获取角色的仓库信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    package = player.pack.getWarehousePackage()
    packageItemInfo = package.getPackageItemInfo()
    data = {'packageItemInfo':packageItemInfo}
    return {'result':True,'message':u'','data':data}
    
def moveItem(dynamicId,characterId,packageType,fromPosition,toPosition,curpage):
    '''移动同一包裹中的物品
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param packageType: int 包裹的类型  1:临时包裹 2:仓库 3:普通物品包裹  4:任务物品包裹
    @param fromPosition: int 物品的起始位置
    @param toPosition: int 物品的目的位置
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.pack.moveItem(packageType,fromPosition,toPosition,curpage)
    return data

def moveItemToOtherPackage(dynamicId,characterId,fromPackageType,toPackageType,fromPosition,toPosition):
    '''移动不同包裹中的物品
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param fromPackageType: int 起始包裹的类型
    @param toPackageType: int 目标包裹的类型
    @param fromPosition: int 物品的起始位置
    @param toPosition: int 物品的目的位置
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.pack.moveItemToOtherPackage(fromPackageType,toPackageType,fromPosition,toPosition)
    return data

def equipEquipment(dynamicId,characterId,fromPosition,toPosition,curpage,fromPackCategory):
    '''穿上装备
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param fromPosition: int 物品在包裹中的位置
    @param toPosition: int 装备的位置
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.pack.equipEquipment(fromPosition,toPosition,curpage,fromPackCategory)
    if data.get('message'):
        pushOtherMessage(905,data.get('message',''),[dynamicId])
    return data
    
def unloadedEquipment(dynamicId,characterId,fromPosition,toPosition,curpage):
    '''卸下装备
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param fromPosition: int 装备的位置
    @param toPosition: int 放到包裹中的位置
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.pack.unloadedEquipment(fromPosition,toPosition,curpage)
    return data

def splitItemsInPack(dynamicId,characterId,packageType,fromposition,toposition,splitnum,curpage):
    '''物品拆分
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param packageType: int 包裹的类型
    @param fromposition: int 拆分的起始位置
    @param toposition: int 拆分到得位置
    @param splitnum: int 拆分的数量
    @param curpage: int 当前页
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.pack.splitItemsInPack(packageType,fromposition,toposition,splitnum,curpage)
    return data

def dropItemsInPack(dynamicId,characterId,position,packageType,curpage):
    '''丢弃物品
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param position: int 物品的位置
    @param packageType: int 包裹的类型
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.pack.dropItemsInPack(position,packageType,curpage)
    return data
    
def packageArrange(dynamicId,characterId,packageType):
    '''包裹整理'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    player.pack.packageArrange(packageType)
    pushPromptedMessage(Lg().g(158),[player.getDynamicId()])
    return {'result':True,'message':Lg().g(158)}

def packageExpansion(dynamicId, characterId,packageType,curpage,position):
    '''扩充包裹
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param packageType: int 包裹的类型
    @param curpage: int 包裹当前页
    @param position: int 包裹的坐标
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    return player.pack.packageExpansion(packageType,curpage,position)
    
    
