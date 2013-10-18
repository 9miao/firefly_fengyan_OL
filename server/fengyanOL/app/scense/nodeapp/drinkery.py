#coding:utf8
'''
Created on 2011-9-13

@author: SIOP_09
'''
from app.scense.applyInterface import drinkery
from app.scense.core.PlayersManager import PlayersManager
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.drinkery import GetHotelInfo_pb2
from app.scense.protoFile.drinkery import UseItem_pb2

@nodeHandle
def getHotelinfo_1901(dynamicId, request_proto):
    argument=GetHotelInfo_pb2.GetHotelInfoRequest()
    argument.ParseFromString(request_proto)
    response=GetHotelInfo_pb2.GetHotelInfoResponse()
    
    id=argument.id#角色
    result=drinkery.getHotelinfo(id)
    player=PlayersManager().getPlayerByID(id)#当前角色实例
    level=player.level._level #角色当前等级
    Hp=player.attribute.getMaxHp()-player.attribute._hp #最大血量-当前血量
    Mp=player.attribute.getMaxMp()-player.attribute._mp #最大魔法-当前魔法
    list2=3
    list3=1
    if not result.get('result',False):
        response.result=True
        response.message=result.get('message',u'')
        h1 = response.hotelInfo.add()
        import math
        h1.canUseTimes=0
        h1.coinNum=int(math.ceil((Hp+Mp)/5.0))
        
        h2= response.hotelInfo.add()
        h2.canUseTimes=3
        h2.coinNum=10
        
        h3=response.hotelInfo.add()
        h3.canUseTimes=1
        h3.coinNum=35
        
        return response.SerializeToString()
        
    if result.get('result',False):
        response.result=result.get('result',False)
        response.message=result.get('message',u'')
        data=result.get('data')
        for item in data:
            if item.get('drinktype')==2: #普通果汁酒
                list2=3-item.get('count')#剩余次数
            if item.get('drinktype')==3: #神器果汁酒
                list3=0#剩余次数
        h1 = response.hotelInfo.add()
        import math
        h1.canUseTimes=0
        h1.coinNum=int(math.ceil((Hp+Mp)/5.0))
        
        h2= response.hotelInfo.add()
        h2.canUseTimes=list2
        h2.coinNum=10
        
        h3=response.hotelInfo.add()
        h3.canUseTimes=list3
        h3.coinNum=35
        
        return response.SerializeToString()
            
@nodeHandle
def HotelUseItem_1902(dynamicId, request_proto):
    argument=UseItem_pb2.UseItemRequest()
    argument.ParseFromString(request_proto)
    response=UseItem_pb2.UseItemResponse()
    
    id=argument.id#角色id
    typeid=argument.type #0魔法泡沫酒 1普通果汁酒 2神奇果汁酒
    result=drinkery.HotelUseItem(id, typeid)
    
    response.result=result.get('result')
    response.message=result.get('message',u'')
    response.failType=1
        
    return response.SerializeToString()