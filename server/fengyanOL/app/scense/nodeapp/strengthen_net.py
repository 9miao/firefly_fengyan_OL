#coding:utf8
'''
Created on 2011-9-28
强化(铁匠铺)
@author: SIOP_09
'''

from app.scense.applyInterface import strengthen
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.strengthen import GetNextLevelItemInfo2117_pb2
from app.scense.protoFile.strengthen import StrengthenItem2102_pb2
from app.scense.protoFile.strengthen import GetStrengthenPackageInfo_pb2
from app.scense.protoFile.strengthen import StrengthenItem2118_pb2
from app.scense.protoFile.strengthen import StrengthenTime2120_pb2
from app.scense.protoFile.strengthen import CleanCD2121_pb2
from app.scense.core.language.Language import Lg

@nodeHandle
def BlacksmithStrengthenInfo_2117(dynamicId, request_proto):
    '''判断能否强化并返回各种信息'''
    argument = GetNextLevelItemInfo2117_pb2.GetNextLevelItemInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetNextLevelItemInfo2117_pb2.GetNextLevelItemInfoResponse()
    
    characterid = argument.id #角色id
    itemid = argument.itemId #物品id,物品1，存在物品赋值物品id,不存在赋值 -1(装备id)
    
    
    result = strengthen.isHaveQH(characterid, itemid)
    if not result.get('result', False):
        response.result = False
        response.message = result.get('message', Lg().g(614))
    else:
        data = result.get('data')
        response.result = True
        response.message = result.get('message', Lg().g(166))
        response.nextInfo.mubanid =data.get('itemTemplateId',-1)
        response.nextInfo.itemId =itemid
        try:
            response.nextInfo.strEff=data.get('syname',u'')#效果名称
        except:
            response.nextInfo.strEff=data.get('syname',u'').decode('utf8')#效果名称
        response.nextInfo.effValue=str(data.get('syvalue',-1))#效果值
        response.nextInfo.reqCoin=data.get('coin',999999999)#金币
        response.nextInfo.qhlevel=data.get('qlevel',-1)#下级强化等级

        return response.SerializeToString()

@nodeHandle
def StrengthenItem_2102(dynamicId, request_proto):
    '''强化装备'''
    argument = StrengthenItem2102_pb2.StrengthenItemRequest()
    argument.ParseFromString(request_proto)
    response = StrengthenItem2102_pb2.StrengthenItemResponse()
    characterid = argument.id #角色id
    itemid = argument.itemId #装备id
    
    result = strengthen.StrengthenItem(characterid, itemid)
    if not result.get('result', False):
        response.result = False
        response.message = result.get('message', Lg().g(620))
        return response.SerializeToString()
    response.result = True
    response.message = result.get('message', Lg().g(166))
    return response.SerializeToString()

@nodeHandle
def GetStrengthenPackageInfo_2109(dynamicId, request_proto):
    '''获取强化背包中的数据'''
    argument = GetStrengthenPackageInfo_pb2.GetStrengthenPackageInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetStrengthenPackageInfo_pb2.GetStrengthenPackageInfoResponse()
    
    characterId = argument.id
    curPage = argument.curPage
    result = strengthen.GetStrengthenPackageInfo(characterId,curPage)
    response.result = result.get('result', False)
    response.message = result.get('message', Lg().g(166))
    if result.get('data'):
        data = result.get('data')
        response.data.nowPage = data.get('nowPage')
        response.data.maxPage = data.get('maxPage')
        canstrItemList = data.get('canstrItemList')
        strItemList = response.data.strItemList
        for _item in canstrItemList:
            strItem = strItemList.add()
            strItem.itemtag = _item.get('itemtag')
            _item['item'].SerializationItemInfo(strItem.item)
    return response.SerializeToString()
    
    
@nodeHandle
def StrengthenItem_2118(dynamicId, request_proto):
    '''获取转移后的属性效果'''
    argument = StrengthenItem2118_pb2.StrengthenItemRequest()
    argument.ParseFromString(request_proto)
    response = StrengthenItem2118_pb2.StrengthenItemResponse()
    characterid = argument.id #角色id
    itemid1 = argument.itemId1 #装备id
    itemid2 = argument.itemId2 #装备id
    
    result = strengthen.getSxzy(characterid, itemid1,itemid2)

    response.result = True
    response.message = Lg().g(166)
    if result.get('qh',None)==None:
        response.result =False
        response.message = Lg().g(620)
    else:
        response.qh=result.get('qh',-1)
        response.coin=result.get('coin',-1)
    return response.SerializeToString()


@nodeHandle
def StrengthenItem_2119(dynamicId, request_proto):
    '''转移'''
    argument = StrengthenItem2118_pb2.StrengthenItemRequest()
    argument.ParseFromString(request_proto)
    response = StrengthenItem2118_pb2.StrengthenItemResponse()
    characterid = argument.id #角色id
    itemid1 = argument.itemId1 #装备id
    itemid2 = argument.itemId2 #装备id
    
    result = strengthen.runningSxzy(characterid, itemid1,itemid2)
    response.result = result.get('result', False)
    response.message = result.get('message', Lg().g(166))
    return response.SerializeToString()
    

@nodeHandle
def StrengthenItem_2120(dynamicId, request_proto):
    '''获取强化剩余秒数'''
    argument = StrengthenTime2120_pb2.StrengthenTimeRequest()
    argument.ParseFromString(request_proto)
    response = StrengthenTime2120_pb2.StrengthenTimeResponse()
    pid = argument.id #角色id
    
    result = strengthen.getSYtime(pid)
    response.result = True
    response.message =  Lg().g(166)
    response.reTime=result
    return response.SerializeToString()
    


@nodeHandle
def StrengthenItem_2121(dynamicId, request_proto):
    '''清除强化时间'''
    argument = CleanCD2121_pb2.CleanCDRequest()
    argument.ParseFromString(request_proto)
    response = CleanCD2121_pb2.CleanCDResponse()
    pid = argument.id #角色id
    
    result = strengthen.cleanCD(pid)
    if result:
        response.result = True
        response.message =  Lg().g(166)
    else:
        response.result = False
        response.message =  Lg().g(620)
    return response.SerializeToString()
    
    
    
