#coding:utf8
'''
Created on 2011-6-14
@author: SIOP_09
'''
from app.scense.applyInterface import instance_app, winning_app,tiaozhuan
from app.scense.serverconfig.node import nodeHandle
#from serverconfig.publicnode import publicnoderemote

from app.scense.protoFile.instance import escInstance_pb2
from app.scense.protoFile.instance import instanceActivate_pb2
from app.scense.protoFile.instance import GetCopySceneInfo1507_pb2
from app.scense.protoFile.instance import GetColonizationList2901_pb2
from app.scense.protoFile.instance import GetColonFuBenList2902_pb2
from app.scense.protoFile.instance import GetFuBenColon2903_pb2
from app.scense.core.language.Language import Lg

@nodeHandle
def enterInstance_1501(player,dynamicId,characterId,instanceId,famId):
    '''进入副本
    ''' 
    data=instance_app.enterInstance1(player,dynamicId, characterId, instanceId,famId) #进入副本
    if data.get('result'):
        pass
#        publicnoderemote.callRemote('updatePCharacterNodeId',characterId,getNodeId())
    return data

@nodeHandle
def iteranceInstances_1505(dynamicId,request_proto):
    '''重打副本'''
    argument=escInstance_pb2.escInstanceRequest()
    argument.ParseFromString(request_proto)
    response=escInstance_pb2.escInstanceResponse()
    characterId=argument.id #队长角色Id
    data=instance_app.iteranceInstance(characterId)
    response.result=data.get('result',False)
    response.message=data.get('message',u'')
    if data.get('data',None):
        response.data.placeId=data.get('data').get('placeId',-1)
    return response.SerializeToString()

@nodeHandle
def closeInstance_1502(dynamicId,request_proto):
    '''关闭副本'''
    argument= escInstance_pb2.escInstanceRequest()
    response = escInstance_pb2.escInstanceResponse()
    argument.ParseFromString(request_proto)
    characterId=argument.id #用户角色Id
    data=instance_app.closeInstance(dynamicId,characterId)
    response.result=data.get('result',False)
    response.message=data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def instanceActivate_1506(dynamicId,request_proto):
    '''通过传送阵获取所有副本信息'''
#    import datetime,time
#    from utils.dbopera import dbMap
    argument=instanceActivate_pb2.instanceActivateRequest()
    argument.ParseFromString(request_proto)
    response=instanceActivate_pb2.instanceActivateResponse()
    characterId=argument.id #用户角色Id
    csz=argument.csz #传送阵id
#    doorinfo = dbMap.ALL_DOOR_INFO.get(csz)#获取传送门的信息
#    if doorinfo.get('functionType')==1:#跳转场景
    tiaozhuan.tiaozhuan(dynamicId, characterId, csz)
    return
#        return
#    print 'ssssssssssssssssss'+str(datetime.datetime.fromtimestamp(time.time()))
    data=instance_app.getAllInstances(characterId,csz)#获取所有副本信息
#    print 'ssssssssssssssssss'+str(datetime.datetime.fromtimestamp(time.time()))
    response.result=data.get('result',False)
    response.message=data.get('message',u'')
    response.data.csz=csz
    dt=data.get('data',None)
    if dt:
        response.data.levelState=data.get('guild')
        for item in dt:
            itemInfo = response.data.info.add()
            itemInfo.id=item.get('id')#副本id
            itemInfo.state=item.get('state')#副本组状态
            itemInfo.score=item.get('score')#副本评分
            itemInfo.union_id=item.get('union_id') #殖民国id
            itemInfo.leader_id=item.get('leader_id') #殖民角色id
            itemInfo.union_name=item.get('union_name') #殖民国名称
            itemInfo.leader_name=item.get('leader_name') #殖民角色名称
            itemInfo.instanceList.extend(item.get("instanceList"))#副本难度列表
            itemInfo.stateList.extend(item.get("stateList"))#副本状态列表
            for dr in item.get('drop'):
                dropinfo=itemInfo.monsterinfos.add()
                moster=dr.get('moster')[0]
                dropinfo.lv=moster.formatInfo.get('level',0)
                dropinfo.name=moster.formatInfo.get('name',Lg().g(143))
                del moster
                for it in dr.get('dropitem'):
                    idinfo=dropinfo.items.add()
                    idinfo.nowQuality=it[0]
                    idinfo.name=it[1]
    else:
        response.data.levelState=0
        response.data.info.extend([])

                
    return response.SerializeToString()

#def roomGetByid_(dynamicId,request_proto):
#    '''在副本房间中或者组队房间中获取副本信息,包括怪物信息和物品信息
#    '''
#    from protoFile.instance.GetCopySceneInfo1805_pb2 import GetCopySceneInfoRequest
#    from protoFile.instance.GetCopySceneInfo1805_pb2 import GetCopySceneInfoResponse
#    argument=GetCopySceneInfoRequest()
#    argument.ParseFromString(request_proto)
#    response=GetCopySceneInfoResponse()
#    characterId=argument.id #用户角色Id
#    instanceId=argument.sceneId #副本id
#    data= instance_d.getInstance_dByid(instanceId)
#    if data:
#        response.result=data.get('result',False)
#        response.message=data.get('message',u'')
#        dt=data.get('data',None)
#        if dt:
#            response.data.name=dt.get('instancename',None)#副本名称
#            response.data.sceneResId=dt.get('instanceid',0)#副本id
#            for item in dt.get("dropitem"):
#                items = response.data.dropItemInfo.add()
#                item.SerializationItemInfo(items)
#            for item in dt.get("moster"):
#                ms=response.data.monsterInfo.add()
#                ms.id=item.baseInfo.id
#                ms.monsterLevel=item.formatInfo.get('level',0)
#                ms.monsterName=item.formatInfo.get('name',u'没取到怪物名字')
#                ms.monstertype=item.formatInfo.get('type',0)
#        return response.SerializeToString()

@nodeHandle
def GetCopySceneInfo_1507(dynamicId, request_proto):
    '''返回副本怪物数量，角色信息以及国信息'''
    argument=GetCopySceneInfo1507_pb2.GetCopySceneInfoRequest()
    argument.ParseFromString(request_proto)
    response=GetCopySceneInfo1507_pb2.GetCopySceneInfoResponse()
    
    pid=argument.id #角色id
    data=instance_app.GetCopySceneInfo(pid)
    if data:
        response.result=True
        response.message=u''
        response.monsterNum=data['count']
        response.corpsId=data['gid']
        response.corpsName=data['gname']
        response.rewardId=data['pid']
        response.rewardName=data['pname']
    else:
        response.result=False
        response.message=Lg().g(610)
    return response.SerializeToString()

@nodeHandle
def GetColonizationList_2901(dynamicId, request_proto):
    '''获取所有传送门信息,殖民特权中的所有传送门副本信息'''
    argument=GetColonizationList2901_pb2.GetColonizationListRequest()
    argument.ParseFromString(request_proto)
    response=GetColonizationList2901_pb2.GetColonizationListResponse()
    pid=argument.id
    page=argument.curPage#当前页数
    
    data=instance_app.getPortal(pid,page)
    response.rCurPage=page
    if not data[0] and len(data[0])<1:
        response.result=False
        response.maxPage=0
        response.coloList.extend([])
    else:
        response.result=True
        response.maxPage=data[1]
        for item in data[0]:
            it=response.coloList.add()
            it.coloId=item['id']#传送阵id
            it.coloName=item['name']#传送阵名称
            
    return response.SerializeToString()

@nodeHandle
def GetColonFuBenList_2902(dynamicId, request_proto):
    '''根据传送门获取所有副本信息'''
    
    argument=GetColonFuBenList2902_pb2.GetColonFuBenListRequest()
    argument.ParseFromString(request_proto)
    response=GetColonFuBenList2902_pb2.GetColonFuBenListResponse()
    
    pid=argument.id
    cszid=argument.coloId
    data=instance_app.getCsz(cszid,pid)#获取传送阵信息
    
    response.result=data.get('result',False)
    response.message=data.get('message',u'')
    sg=winning_app.getpublicstr()
    response.coloDes=sg
    dt=data.get('data',None)
    if dt:
        for item in dt:
            itemInfo = response.fuBenlist.add()
            itemInfo.fuBenId=item.get('id')##副本组中第一个副本的id
            itemInfo.fuBenName=item.get('name')#副本名称
            itemInfo.coloCorpsName=item.get('union_name') #殖民国名称
            itemInfo.lingzhu=item.get('leader_name') #殖民角色名称
            itemInfo.coloType=item.get("coloType")#占领类型  0没有占领   1己方占领  2其他国占领
            itemInfo._fu_camp=item.get('camp')#阵营
            
    return response.SerializeToString()

@nodeHandle
def GetFuBenColon_2903(dynamicId, request_proto):
    '''获取副本被攻击次数，及其输入信息'''
    argument=GetFuBenColon2903_pb2.GetFuBenColonRequest()
    argument.ParseFromString(request_proto)
    response=GetFuBenColon2903_pb2.GetFuBenColonResponse()
    
    pid=argument.id#角色id
    instanceid=argument.cId#副本组中最小的副本id
    
    list=winning_app.getStr(instanceid)
    response.result=True
    response.message=Lg().g(166)
    response.coloNum=list[1]
    response.coloDes=list[0]
    return response.SerializeToString()
    
    
    
    
    