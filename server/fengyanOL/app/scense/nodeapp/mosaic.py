#coding:utf8
'''
Created on 2012-5-18
装备镶嵌相关
@author: Administrator
'''
from app.scense.applyInterface import mosaic
from app.scense.serverconfig.node import nodeHandle

@nodeHandle
def GetXiangQianPackInfo_2110(dynamicId,request_proto):
    '''获取镶嵌装备包裹
    '''
    from app.scense.protoFile.item import GetXiangQianPackInfo2110_pb2
    argument = GetXiangQianPackInfo2110_pb2.GetXiangQianPackInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetXiangQianPackInfo2110_pb2.GetXiangQianPackInfoResponse()
    characterId = argument.id
    curpage = argument.page
    
    result = mosaic.GetXiangQianPackInfo2110(dynamicId, characterId, curpage)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        data = result.get('data')
        response.xqPackInfo.curPage = data.get('nowPage')
        response.xqPackInfo.maxPage = data.get('maxPage')
        xqItemInfoList = data.get('xqItemInfo')
        for _item in xqItemInfoList:
            xqItem = response.xqPackInfo.xqItemInfo.add()
            xqItem.inBody = _item.get('itemtag')
            _item['item'].SerializationItemInfo(xqItem.itemsInfo)
    msg = response.SerializeToString()
    return msg
    
@nodeHandle
def GetXiangQianStoreInfo_2111(dynamicId,request_proto):
    '''获取镶嵌装备包裹
    '''
    from app.scense.protoFile.item import GetXiangQianStoreInfo2111_pb2
    argument = GetXiangQianStoreInfo2111_pb2.GetXiangQianStoreInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetXiangQianStoreInfo2111_pb2.GetXiangQianStoreInfoResponse()
    characterId = argument.id
    curpage = argument.page
    
    result = mosaic.GetXiangQianStoreInfo2111(dynamicId, characterId, curpage)
    response.result = result.get('result')
    response.message = result.get('message','')
    if result.get('data',None):
        data = result.get('data')
        response.xqStoreInfo.curPage = data.get('nowPage')
        response.xqStoreInfo.maxPage = data.get('maxPage')
        xqStoreInfoList = data.get('itemsInfo')
        for _item in xqStoreInfoList:
            xqStore = response.xqStoreInfo.itemsInfo.add()
            _item.SerializationItemInfo(xqStore)
    return response.SerializeToString()

@nodeHandle
def XiangQian_2112(dynamicId,request_proto):
    '''镶嵌
    '''
    from app.scense.protoFile.item import XiangQian2112_pb2
    argument = XiangQian2112_pb2.XiangQianRequest()
    argument.ParseFromString(request_proto)
    response = XiangQian2112_pb2.XiangQianResponse()
    characterId = argument.id
    equipId = argument.equipId
    sId = argument.sId
    packageType = argument.type
    position = argument.position
    
    data = mosaic.XiangQian2112(dynamicId, characterId, equipId, sId, packageType, position)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def UnloadXiangQian_2113(dynamicId,request_proto):
    '''宝石摘除
    '''
    from app.scense.protoFile.item import UnloadXiangQian2113_pb2
    argument = UnloadXiangQian2113_pb2.UnLoadXiangQianRequest()
    argument.ParseFromString(request_proto)
    response = UnloadXiangQian2113_pb2.UnLoadXiangQianResponse()
    characterId = argument.id
    equipId = argument.equipId
    packageType = argument.type
    position = argument.position
    
    data = mosaic.UnloadXiangQian2113(dynamicId, characterId, equipId, packageType, position)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()


