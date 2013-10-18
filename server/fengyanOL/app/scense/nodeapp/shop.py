#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import shop
from app.scense.serverconfig.node import nodeHandle
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.protoFile.shop import buyItemInMyshop_pb2
from app.scense.protoFile.shop import GetNpcShopInfo206_pb2
from app.scense.protoFile.shop import NpcShopSellItem220_pb2
from app.scense.protoFile.shop import NpcShopBuyItem_pb2
from app.scense.protoFile.shop import getMallItemInfo208_pb2
from app.scense.protoFile.shop import getOneMallItemInfo_pb2
from app.scense.protoFile.shop import buyItemInMall214_pb2

@nodeHandle
def getMallItemInfo_208(dynamicId,request_proto):
    '''获取商城信息'''
    argument = getMallItemInfo208_pb2.getMallItemInfoRequest()
    argument.ParseFromString(request_proto)
    response = getMallItemInfo208_pb2.getMallItemInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id #角色id
    page = argument.page #查看页数
    tag=argument.categories #商城物品的分类1热卖2所有3强化4宠物
    
    data = shop.getMallItemInfo(dynamicId, characterId, page,tag)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        responseData = data.get('data')
        response.data.curpage = responseData.get('page',page)
        response.data.categories = tag
        response.data.goal = responseData.get('maxpage',1)
        items = responseData.get('items',[])
        if len(items)<1:
            response.data.items.extend([])
        else:
            for _item in items:
                oneitem = response.data.items.add()
                oneitem.templateId = _item.get('templateid',0)
                oneitem.type = _item.get('tag',0)
                oneitem.price = _item.get('gold',0)
                oneitem.count = _item.get('count',1)
                oneitem.itemID= _item.get('templateid',0)
                oneitem.templateId = _item.get('templateid',0)
                oneitem.priceNow= _item['cx']
        cxs = responseData.get('cx',[])
        if len(cxs)<1:
            response.data.zxItems.extend([])
        else:
            for item in cxs:
                it = response.data.zxItems.add()
                it.templateId = item.get('templateid',0)
                it.type = item.get('tag',0)
                it.price = item.get('gold',0)
                it.count = item.get('count',1)
                it.itemID= item.get('templateid',0)
                it.templateId = item.get('templateid',0)
                it.priceNow= item['cx']
    return response.SerializeToString()

@nodeHandle
def buyItemInMyshop_213(dynamicId,request_proto):
    '''购买商店中的物品'''
    argument = buyItemInMyshop_pb2.buyItemInMyshopRequest()
    argument.ParseFromString(request_proto)
    response = buyItemInMyshop_pb2.buyItemInMyshopResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    itemTemplateId = argument.itemTemplateId
    data = shop.buyItemInMyshop(dynamicId, characterId, itemTemplateId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def buyItemInMall_214(dynamicId,request_proto):
    '''购买商城中的物品'''
    argument = buyItemInMall214_pb2.buyItemInMallRequest()
    argument.ParseFromString(request_proto)
    response = buyItemInMall214_pb2.buyItemInMallResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    itemTemplateId = argument.itemTemplateId
    count=argument.count
    priceType=argument.priceType#
    buyType=argument.buyType
    presentName=argument.presentName
    data = shop.buyItemInMall(dynamicId, characterId, itemTemplateId,count,priceType,buyType,presentName)
    message = data.get('message',u'')
    response.result = data.get('result',False)
    response.message = message
    if message:
        pushOtherMessage(905, message, [dynamicId])
    data1=data.get('data',None)
    if data1:
        response.data.recharge=data1.get('recharge',False)
        response.data.priceType=data1.get('priceType',0)
        response.data.itemTemplateId=data1.get('itemTemplateId',-1)
        response.data.count=data1.get('count',-1)
        response.data.buyType=buyType
        response.data.presentName=presentName
    return response.SerializeToString()

@nodeHandle
def getMallItemTime_1605(dynamicId,request_proto):
    '''返回该特价商品的打折剩余时间'''

    argument=getOneMallItemInfo_pb2.getoneMallItemInfoRequest()
    argument.ParseFromString(request_proto)
    response=getOneMallItemInfo_pb2.getoneMallItemInfoResponse()
    
    itemid=argument.id
    data=shop.getMallByItemtemplateid(itemid)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    response.data.endtime=data.get('daga',-1)
    return response.SerializeToString()

@nodeHandle
def getNpcShopInfo_206(dynamicId,request_proto):
    '''获取公共商店信息'''
    argument=GetNpcShopInfo206_pb2.getNpcShopInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetNpcShopInfo206_pb2.getNpcShopInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    npcId = argument.npcId
    shopCategory = argument.shopCategory
    curPage = argument.curPage
    result = shop.getNpcShopInfo(dynamicId, characterId, npcId, shopCategory,curPage)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        data = result.get('data')
        response.data.shopCategory = data.get('shopCategory',0)
        response.data.curPage = data.get('curPage',0)
        response.data.maxPage = data.get('maxPage',1)
        for _item in data.get('items',[]):
            item = response.data.packageItemInfo.add()
            item.remainTime = _item.get('overTime',0)
            _item['item'].SerializationItemInfo(item.itemInfo)
            
    return response.SerializeToString()

@nodeHandle
def NpcShopSellItem_220(dynamicId,request_proto):
    '''出售物品'''
    argument=NpcShopSellItem220_pb2.npcShopSellItemRequest()
    argument.ParseFromString(request_proto)
    response = NpcShopSellItem220_pb2.npcShopSellItemResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    itemPos = argument.itemPos
    packageType = argument.packageType
    curpage = argument.curpage
    stack = argument.sellCount
    result = shop.NpcShopSellItem(dynamicId, characterId, itemPos, packageType, curpage,stack)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    response.data.packageType = packageType
    response.data.curpage = curpage
    return response.SerializeToString()

@nodeHandle
def NpcShopBuyItem_219(dynamicId,request_proto):
    '''购买，回购商品'''
    argument = NpcShopBuyItem_pb2.npcShopBuyItemRequest()
    argument.ParseFromString(request_proto)
    response = NpcShopBuyItem_pb2.npcShopBuyItemResponse()
    
    
    characterId = argument.id
    itemId = argument.itemId
    opeType = argument.opeType
    buyNum = argument.buyNum
    npcId = argument.npcId
    result = shop.NpcShopBuyItem(dynamicId, characterId, itemId, opeType,buyNum,npcId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    response.data.opeType = opeType
    return response.SerializeToString()
    
