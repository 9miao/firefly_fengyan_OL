#coding:utf8
'''
Created on 2012-6-7

@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.applyInterface import fate
from app.scense.protoFile.fate import GetXingYunList3600_pb2
from app.scense.protoFile.fate import ZhanXing3601_pb2
from app.scense.protoFile.fate import YiJianObtainAndDrop3602_pb2
from app.scense.protoFile.fate import YiJianZhanXing3603_pb2
from app.scense.protoFile.fate import GetRoleAndPetList3604_pb2
from app.scense.protoFile.fate import GetPackXingYunListInfo3605_pb2
from app.scense.protoFile.fate import YiJianHeCheng3606_pb2
from app.scense.protoFile.fate import OpeXingXun3607_pb2
from app.scense.protoFile.fate import JiFeng_pb2
from app.scense.protoFile.fate import QueRenExchange3610_pb2

@nodeHandle
def GetXingYunList_3600(dynamicId, request_proto):
    '''获取星运信息
    '''
    argument = GetXingYunList3600_pb2.GetXingYunListRequest()
    argument.ParseFromString(request_proto)
    response = GetXingYunList3600_pb2.GetXingYunListResponse()
    
    characterId = argument.id
    data = fate.GetXingYunList(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        info = data.get('data')
        response.showIndex = info.get('showIndex')
        response.maxCount = info.get('maxCount')
        fatelist = info.get('xyList')
        fatelistresponse = response.xyList
        for _fateInfo in fatelist:
            fateinfo = fatelistresponse.add()
            _fateInfo.SerializationFateInfo(fateinfo)
    return response.SerializeToString()

@nodeHandle
def ZhanXing_3601(dynamicId, request_proto):
    '''开始占星
    '''
    argument = ZhanXing3601_pb2.ZhanXingRequest()
    argument.ParseFromString(request_proto)
    response = ZhanXing3601_pb2.ZhanXingResponse()
    
    characterId = argument.id
    fatelevel = argument.sIndex
    data = fate.ZhanXing(dynamicId, characterId, fatelevel)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        info = data.get('data')
        response.showIndex = info.get('showIndex')
        response.maxCount = info.get('maxCount')
        fateins = info.get('fateIns')
        fateins.SerializationFateInfo(response.xyInfo)
    return response.SerializeToString()

@nodeHandle
def YiJianObtainAndDrop_3602(dynamicId, request_proto):
    '''一键拾取或卖出
    '''
    argument = YiJianObtainAndDrop3602_pb2.YiJianObtainAndDropRequest()
    argument.ParseFromString(request_proto)
    response = YiJianObtainAndDrop3602_pb2.YiJianObtainAndDropResponse()
    
    characterId = argument.id
    opearType = argument.type
    fate.YiJianObtainAndDrop(dynamicId, characterId, opearType)
    response.result = True#data.get('result',False)
    return response.SerializeToString()
    
@nodeHandle
def YiJianZhanXing_3603(dynamicId, request_proto):
    '''一键占星
    '''
    argument = YiJianZhanXing3603_pb2.YiJianZhanXingRequest()
    argument.ParseFromString(request_proto)
    response = YiJianZhanXing3603_pb2.YiJianZhanXingResponse()
    
    characterId = argument.id
    data = fate.YiJianZhanXing(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        info = data.get('data')
        yjXYinfoList = response.yjXYinfoList
        for _zhanxing in info:
            zhanxing = yjXYinfoList.add()
            zhanxing.showIndex = _zhanxing.get('showIndex')
            zhanxing.maxCount = _zhanxing.get('maxCount')
            fateins = _zhanxing.get('fateIns')
            fateins.SerializationFateInfo(zhanxing.xyInfo)
    return response.SerializeToString()

@nodeHandle
def GetRoleAndPetList_3604(dynamicId, request_proto):
    '''获取角色和宠物的星运装备栏信息
    '''
    argument = GetRoleAndPetList3604_pb2.GetRoleAndPetListRequest()
    argument.ParseFromString(request_proto)
    response = GetRoleAndPetList3604_pb2.GetRoleAndPetListResponse()
    
    characterId = argument.id
    data = fate.GetRoleAndPetList(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        roleAndPetInfo = data.get('data')
        roleAndPetInfoResponse = response.roleAndPetInfo
        for _rolefate in roleAndPetInfo:
            rolefate = roleAndPetInfoResponse.add()
            rolefate.rpId = _rolefate.get('rpId')
            rolefate.rpName = _rolefate.get('rpName')
            rolefate.rpLevel = _rolefate.get('rpLevel')
            rolefate.icon = _rolefate.get('icon')
            rolefate.rpType = _rolefate.get('rpType')
            xyBody1 = _rolefate.get('xyBody1')
            if xyBody1:
                xyBody1.SerializationFateInfo(rolefate.xyBody1)
            xyBody2 = _rolefate.get('xyBody2')
            if xyBody2:
                xyBody2.SerializationFateInfo(rolefate.xyBody2)
            xyBody3 = _rolefate.get('xyBody3')
            if xyBody3:
                xyBody3.SerializationFateInfo(rolefate.xyBody3)
            xyBody4 = _rolefate.get('xyBody4')
            if xyBody4:
                xyBody4.SerializationFateInfo(rolefate.xyBody4)
            xyBody5 = _rolefate.get('xyBody5')
            if xyBody5:
                xyBody5.SerializationFateInfo(rolefate.xyBody5)
            xyBody6 = _rolefate.get('xyBody6')
            if xyBody6:
                xyBody6.SerializationFateInfo(rolefate.xyBody6)
            
    return response.SerializeToString()

@nodeHandle
def GetPackXingYunListInfo_3605(dynamicId, request_proto):
    '''获取星运包裹信息
    '''
    argument = GetPackXingYunListInfo3605_pb2.GetPackXingYunListInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetPackXingYunListInfo3605_pb2.GetPackXingYunListInfoResponse()
    
    characterId = argument.id
    data = fate.GetPackXingYunListInfo(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        packinfo = data.get('data')
        xyPackList = response.xyPackList
        for _packfate in packinfo:
            packfate = xyPackList.add()
            packfate.postion = _packfate.get('position')
            fateins = _packfate.get('fate')
            fateins.SerializationFateInfo(packfate.xyInfo)
    return response.SerializeToString()
    
@nodeHandle
def YiJianHeCheng_3606(dynamicId, request_proto):
    '''一键合成'''
    argument = YiJianHeCheng3606_pb2.YiJianHeChengRequest()
    argument.ParseFromString(request_proto)
    response = YiJianHeCheng3606_pb2.YiJianHeChengResponse()
    
    characterId = argument.id
    data = fate.YiJianHeCheng(dynamicId, characterId)
    response.result = data.get('result',False)
    return response.SerializeToString()
    
@nodeHandle
def OpeXingXun_3607(dynamicId, request_proto):
    '''星运移动'''
    argument = OpeXingXun3607_pb2.OpeXingXunRequest()
    argument.ParseFromString(request_proto)
    response = OpeXingXun3607_pb2.OpeXingXunResponse()
    
    characterId = argument.id
    opear = argument.opeId
    opeType = argument.opeType
    frompos = argument.fromPos
    topos = argument.toPos
    data = fate.MoveXingYun(dynamicId, characterId, opear, opeType, frompos, topos)
    response.result = data.get('result',False)
    response.oType = opeType
    return response.SerializeToString()

@nodeHandle
def JiFeng_3609(dynamicId, request_proto):
    '''获取积分商城信息
    '''
    argument = JiFeng_pb2.GetJiFengListInfoRequest()
    argument.ParseFromString(request_proto)
    response = JiFeng_pb2.GetJiFengListInfoResponse()
    
    characterId = argument.id
    nowpage = argument.nowpage
    data = fate.GetJiFengShopInfo(dynamicId, characterId, nowpage)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        shopInfo = data.get('data')
        response.data.jiFengTotal = shopInfo.get('score')
        response.data.curpage = shopInfo.get('nowpage')
        response.data.totalpage = shopInfo.get('maxpage')
        fatelist = shopInfo.get('fatelist')
        exchInfo = response.data.exchInfo
        for _fate in fatelist:
            fateinfo = exchInfo.add()
            _fate.SerializationFateInfo(fateinfo.xingYun)
            fateinfo.jifengValue = _fate.templateinfo['score']
    return response.SerializeToString()
            
@nodeHandle
def QueRenExchange_3610(dynamicId, request_proto):
    '''积分兑换星运
    '''
    argument = QueRenExchange3610_pb2.QueRenExchangeRequest()
    argument.ParseFromString(request_proto)
    response = QueRenExchange3610_pb2.QueRenExchangeResponse()
    
    characterId = argument.id
    fateId = argument.wId
    data = fate.QueRenExchange(dynamicId, characterId, fateId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()
    
    
    
