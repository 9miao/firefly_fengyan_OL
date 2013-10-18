#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import packageInfo
from app.scense.serverconfig.node import nodeHandle

from app.scense.protoFile.packageInfo import getItemsInPackage_pb2
from app.scense.protoFile.packageInfo import getItemsInEquipSlot_pb2
from app.scense.protoFile.packageInfo import equipEquipment_pb2
from app.scense.protoFile.packageInfo import unloadedEquipment_pb2
from app.scense.protoFile.packageInfo import moveItem212_pb2
from app.scense.protoFile.packageInfo import splitItemsInPack_pb2
from app.scense.protoFile.packageInfo import dropItemsInPack_pb2
from app.scense.protoFile.packageInfo import packageArrange_pb2
from app.scense.protoFile.packageInfo import PackageExpansion_223_pb2

@nodeHandle
def getItemsInPackage_204(dynamicId, request_proto):
    '''获取包裹栏物品信息'''
    argument = getItemsInPackage_pb2.getItemsInPackageRequest()
    argument.ParseFromString(request_proto)
    response = getItemsInPackage_pb2.getItemsInPackageResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    packCategory = argument.packCategory
    curpage = argument.curpage
    data = packageInfo.getItemsInPackage(dynamicId, characterId, packCategory,curpage)
    
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        info = data.get('data')
        response.data.packCategory = info['packCategory']
        response.data.packageSize = info['packageSize']
        response.data.curpage = info['curpage']
        response.data.maxpage = info['maxpage']
        response.data.totalsize = info['totalsize']
        for _item in info['itemList']:
            packageItemInfo = response.data.packageItemInfo.add()
            packageItemInfo.position = _item['position']
            _item['itemComponent'].SerializationItemInfo(packageItemInfo.itemInfo)
    
    return response.SerializeToString()


def getItemsInTempPackage(dynamicId, request_proto):
    '''获取临时包裹栏信息'''


def getWarehouseInfo(dynamicId, request_proto):
    '''获取仓库信息'''
    

@nodeHandle  
def getItemsInEquipSlot_203(dynamicId, request_proto):
    '''获取装备栏信息'''
    argument = getItemsInEquipSlot_pb2.getItemsInEquipSlotRequest()
    argument.ParseFromString(request_proto)
    response = getItemsInEquipSlot_pb2.getItemsInEquipSlotResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    
    data = packageInfo.getItemsInEquipSlot(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        info = data.get('data')
        suitecount = info.get('suitecount',{})
        for _item in info['packageItemInfo']:
            packageItemInfo = response.data.packageItemInfo.add()
            if not _item:
                continue
            packageItemInfo.position = _item['position']
            suiteid = _item['itemComponent'].baseInfo.getItemTemplateInfo()['suiteId']
            cnt = suitecount.get(suiteid,0)
            _item['itemComponent'].SerializationItemInfo(packageItemInfo.itemInfo,
                                                         suitecnt = cnt)
    
    return response.SerializeToString()

@nodeHandle
def equipEquipment_210(dynamicId, request_proto):
    '''装备装备'''
    argument = equipEquipment_pb2.equipEquipmentRequest()
    argument.ParseFromString(request_proto)
    response = equipEquipment_pb2.equipEquipmentResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    fromPosition = argument.fromPosition
    toPosition = argument.toPosition
    curpage = argument.curpage
    fromPackCategory = argument.fromPackCategory
    
    data = packageInfo.equipEquipment(dynamicId, characterId, fromPosition,\
                                      toPosition,curpage,fromPackCategory)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        pass
    return response.SerializeToString()

@nodeHandle
def unloadedEquipment_211(dynamicId, request_proto):
    '''卸下装备'''
    argument = unloadedEquipment_pb2.unloadedEquipmentRequest()
    argument.ParseFromString(request_proto)
    response = unloadedEquipment_pb2.unloadedEquipmentResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    fromPosition = argument.fromPosition
    toPosition = argument.toPosition
    curpage = argument.curpage
    data = packageInfo.unloadedEquipment(dynamicId, characterId, fromPosition, toPosition,curpage)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        pass
    return response.SerializeToString()

@nodeHandle
def moveItem_212(dynamicId, request_proto):
    '''在同一包裹栏中移动物品'''
    argument = moveItem212_pb2.moveItemRequest()
    argument.ParseFromString(request_proto)
    response = moveItem212_pb2.moveItemResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    packageType = argument.packageType
    fromPosition = argument.fromPosition
    toPosition = argument.toPosition
    curpage = argument.curpage
    data = packageInfo.moveItem(dynamicId,characterId,packageType,fromPosition,toPosition,curpage)
    
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        response.data.packageType = data.get('data')['packageType']
    return response.SerializeToString()


def moveItemToOtherPackage(dynamicId, request_proto):
    '''在不同包裹中移动物品'''

@nodeHandle
def splitItemsInPack_215(dynamicId, request_proto):
    '''拆分物品'''
    argument = splitItemsInPack_pb2.splitItemsInPackRequest()
    argument.ParseFromString(request_proto)
    response = splitItemsInPack_pb2.splitItemsInPackResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    packageType = argument.packageType 
    fromposition = argument.fromposition 
    toposition = argument.toposition 
    splitnum = argument.splitnum 
    data = packageInfo.splitItemsInPack(dynamicId, characterId, packageType, fromposition, toposition, splitnum)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    response.data = packageType
    return response.SerializeToString()

@nodeHandle
def dropItemsInPack_216(dynamicId, request_proto):
    '''丢弃物品'''
    argument = dropItemsInPack_pb2.dropItemsInPackRequest()
    argument.ParseFromString(request_proto)
    response = dropItemsInPack_pb2.dropItemsInPackResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    position = argument.position 
    packageType = argument.packageType
    curPage = argument.curPage
    data = packageInfo.dropItemsInPack(dynamicId, characterId, position, packageType,curPage)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    response.data = packageType
    return response.SerializeToString()

@nodeHandle
def packageArrange_217(dynamicId, request_proto):
    '''整理包裹'''
    argument = packageArrange_pb2.packageArrangeRequest()
    argument.ParseFromString(request_proto)
    response = packageArrange_pb2.packageArrangeResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    packageType = argument.packageType
    data = packageInfo.packageArrange(dynamicId, characterId,packageType)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def PackageExpansion_223(dynamicId,request_proto):
    '''扩充包裹'''
    argument = PackageExpansion_223_pb2.PackageExpansionRequest()
    argument.ParseFromString(request_proto)
    response = PackageExpansion_223_pb2.PackageExpansionResponse()
    
    
    characterId = argument.characterId
    packageType = argument.packageType
    curpage = argument.curpage
    position = argument.position
    data = packageInfo.packageExpansion(dynamicId, characterId,packageType,curpage,position)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    response.data.packageType = packageType
    response.data.curpage = curpage
    return response.SerializeToString()




