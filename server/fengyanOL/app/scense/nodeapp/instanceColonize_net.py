#coding:utf8
'''
Created on 2011-12-22
副本殖民相关
@author: SIOP_09
'''
from app.scense.applyInterface import  InstanceColonizeGuerdon, instance_app
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.PlayersManager import PlayersManager
from app.scense.serverconfig.node import nodeHandle
from twisted.python import log
from app.scense.protoFile.instance import ColonizationBattle712_pb2
from app.scense.protoFile.instance import EscColonizationBattle713_pb2
from app.scense.protoFile.defence import GetColonizationSceneInfo2405_pb2
from app.scense.protoFile.defence import ActivationElixir2406_pb2
from app.scense.protoFile.defence import ObtainItem2408_pb2
from app.scense.protoFile.defence import OpenCangku2409_pb2
from app.scense.protoFile.packageInfo import getItemsInPackage_pb2
from app.scense.applyInterface.playerInfo import CanDoServer
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

@nodeHandle
def instanceColonizeBattle_712(dynamicId, request_proto):
    '''副本殖民战斗'''

    argument = ColonizationBattle712_pb2.FightRequest()
    argument.ParseFromString(request_proto)
    response = ColonizationBattle712_pb2.FightResponse()
    
    dynamicId = dynamicId
    cid = argument.id #角色id 挑战方ids
    instanceid = argument.copyId #副本id（难度最小的那个）
    player=PlayersManager().getPlayerByID(cid)
    res = CanDoServer(cid)
    if not res['result']:
        pushOtherMessage(905, res.get('message',u''), [dynamicId])
        return res
    if player:
        player.quest.specialTaskHandle(106,state=0) #特殊任务处理
    else:
        log.err(u"instanceColonize_net-76row-not playerid-%s-error"%cid)
    
    iname=InstanceColonizeGuerdon.getInstancenameByinstanceid(instanceid)
    if not InstanceColonizeGuerdon.goClonizeGue(cid): #如果没有战书
        response.result = False
        response.message=Lg().g(611)
        return response.SerializeToString()
        
    list1,zon,pid= InstanceColonizeGuerdon.getBattlePlayer(instanceid,cid) #返回  list,zon
    if not list1:
        response.result = False
        response.message=zon;
        response.data.setData.itemsBonus.extend([])
        response.data.setData.sceneName=u""
        response.data.battleResult = 0
        response.data.centerX = 0
        response.data.centerY = 0
        return response.SerializeToString()
        
    data1=InstanceColonizeGuerdon.getFightData(cid, list1, zon,instanceid)
    response.result = True
    response.data.battleResult = data1.battleResult
    response.data.centerX = data1.center
    response.data.centerY = 325
    rResArr = response.data.rResArr
    startData = response.data.startData
    setpdata = response.data.stepData
    data1.SerializationResource(rResArr)
    data1.SerializationInitBattleData(startData)
    data1.SerializationStepData(setpdata)
    pids=InstanceColonizeGuerdon.getPidByinstanceid(instanceid)
    
    cb=False #入侵成功或者失败 ，默认失败
    if data1.battleResult==1:
        cb=True
    else:
        cb=False
    
    
    if pids>0:
        if pids==cid:
            response.result = False
            response.message=Lg().g(612)
            response.data.setData.itemsBonus.extend([])
            response.data.setData.sceneName=iname
            return response.SerializeToString()
        else:
            pushObjectNetInterface.pushEnterPlace_new(pid,[dynamicId]) #推送进入场景
    else:
        pushObjectNetInterface.pushEnterPlace_new(pid,[dynamicId]) #推送进入场景
   
    itemList=instance_app.dropItem(cid, instanceid, cb,iname)##########添加成功失败记录，获取掉落物品，返回物品列表和副本名称
    if (not itemList) or (len(itemList))<1:
        response.data.setData.itemsBonus.extend([])
    else:
        it=response.data.setData.itemsBonus.add()
        for item in itemList:
            item.SerializationItemInfo(it)
    response.data.setData.sceneName=iname
    ct=InstanceColonizeGuerdon.getWinningCount(cid)
    response.data.setData.sucNum=ct#连胜次数
    plv=player.level.getLevel()
    response.data.setData.goldNum=plv*1000 #连胜奖金
    
    return response.SerializeToString()


@nodeHandle
def ColonizeBattleAfter_713(dynamicId, request_proto):
    '''副本殖民战斗之后回到原场景'''
    argument = EscColonizationBattle713_pb2.EscColonizationBattleRequest()
    argument.ParseFromString(request_proto)
    response = EscColonizationBattle713_pb2.EscColonizationBattleResponse()
    
    dynamicId = dynamicId
    cid = argument.id #角色id
    battleResult=argument.battleResult #副本战斗结果
    instanceid=argument.sceneId #副本id
    InstanceColonizeGuerdon.backScnee(cid,instanceid,battleResult)
    response.result = True
    response.message = u''
    pushObjectNetInterface.pushApplyMessage(713, response.SerializeToString(), [dynamicId])

@nodeHandle
def GetColonizationSceneInfo_2405(dynamicId, request_proto):
    '''殖民管理获取当前页副本及其相关信息'''
    argument=GetColonizationSceneInfo2405_pb2.GetColonizationSceneInfoRequest()
    argument.ParseFromString(request_proto)
    response=GetColonizationSceneInfo2405_pb2.GetColonizationSceneInfoResponse()
    pid=argument.id
    page=argument.curPage #当前页数
    data,zong=InstanceColonizeGuerdon.getInstanceinfoBypid(pid, page)
    if len(data)<1:
        response.data.curPage=page
        response.data.maxPage=zong
        response.message=Lg().g(613)
        response.result=False
        return response.SerializeToString()
    response.message=u''
    response.result=True
    response.data.curPage=page
    response.data.maxPage=zong
    for val in data:
        info=response.data.copyInfo.add()
        info.c_id=val.get('id',0)
        info.c_name=val.get('name',u'')
        info.li_liang=val.get('liliang',0)
        info.add_li_liang=val.get('jialiliang',0)
        info.min_jie=val.get('minjie',0)
        info.add_min_jie=val.get('jiaminjie',0)
        info.zhi_li=val.get('zhili',0)
        info.add_zhi_li=val.get('jiazhili',0)
        info.nai_li=val.get('naili',0)
        info.add_nai_li=val.get('jianaili',0)
        info.ji_shen=val.get('jingshen',0)
        info.add_ji_shen=val.get('jiajingshen',0)
        info.wu_gong=val.get('wugong',0)
        info.wu_fang=val.get('wu_fang',0)
        info.mo_gong=val.get('mogong',0)
        info.mo_fang=val.get('mofang',0)
        info.gong_su=val.get('gongsu',0)
        info.ming_zhong=val.get('mingzhong',0)
        info.bao_ji=val.get('baoji',0)
        info.shan_bi=val.get('shanbi',0)
        d=val.get('state',None)
        info.liliang_info.status=d[1]['status']
        info.liliang_info.remainTime=d[1]['remainTime']
        info.minjie_info.status=d[2]['status']
        info.minjie_info.remainTime=d[2]['remainTime']
        info.zhili_info.status=d[3]['status']
        info.zhili_info.remainTime=d[3]['remainTime']
        info.naili_info.status=d[4]['status']
        info.naili_info.remainTime=d[4]['remainTime']
        info.jingshen_info.status=d[5]['status']
        info.jingshen_info.remainTime=d[5]['remainTime']
    return response.SerializeToString()

@nodeHandle 
def ActivationElixir_2406(dynamicId, request_proto):
    '''副本殖民购买状态'''
    argument=ActivationElixir2406_pb2.ActivationElixirRequest()
    argument.ParseFromString(request_proto)
    response=ActivationElixir2406_pb2.ActibationElixirResponse()
    
    pid=argument.id #角色id
    tagid = dynamicId #角色动态id
    groupid=argument.c_id #副本组id
    itemid=argument.elixirType #药剂类型 1力量、2敏捷 、3智力、4精神、5耐力、6所有
    #itemid 
#    if itemid==6:
#        InstanceColonizeGuerdon.addAllProperty(groupid, itemid, tagid, pid)
#    else:
#        InstanceColonizeGuerdon.addProperty(groupid, itemid, tagid, pid)
    response.result=False
    response.message=u'此功能暂未开放'
    return response.SerializeToString()

@nodeHandle
def ObtainItem_2408(dynamicId, request_proto):
    '''放到自己背包中'''
    argument=ObtainItem2408_pb2.ObtainItemRequest()
    argument.ParseFromString(request_proto)
    response=ObtainItem2408_pb2.ObtainItemResponse()
    
    id=argument.id #角色id
    type=argument.type #0获取所有 1获取单个
    pos=argument.pos # 单个在背包的位置
    player=PlayersManager().getPlayerByID(id) #角色实例
    if type==0:
        data=player.instance.putAllItemsInPack()
        if not data:
            response.result=False
            response.message=Lg().g(16)
            pushObjectNetInterface.pushOtherMessage(905, Lg().g(16), [player.getDynamicId()])
            return response.SerializeToString()
    else:
        data=player.instance.getOneItemInPackByPosition(pos)
        if not data:
            response.result=False
            response.message=Lg().g(16)
            return response.SerializeToString()
    response.result=True
    response.message=u''
    return response.SerializeToString()

@nodeHandle
def OpenCangku_2409(dynamicId, request_proto):
    '''扩张背包'''
    argument=OpenCangku2409_pb2.OpenCangkuRequest()
    argument.ParseFromString(request_proto)
    response=OpenCangku2409_pb2.OpenCangkuResponse()
    id=argument.id #角色id
    pos=argument.pos #隋开格子的位置
    player=PlayersManager().getPlayerByID(id)
    player.instance.packageExpansion(pos)
    response.result=True
    response.message=u''
    return response.SerializeToString()

@nodeHandle
def GetInstancePackage_2407(dynamicId, request_proto):
    '''获取殖民背包信息'''
    argument = getItemsInPackage_pb2.getItemsInPackageRequest()
    argument.ParseFromString(request_proto)
    response = getItemsInPackage_pb2.getItemsInPackageResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    packCategory = argument.packCategory
    curpage = argument.curpage
    data = instance_app.getItemsInFamPackage(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        info = data.get('data')
        response.data.packCategory = packCategory
        response.data.packageSize = info['size']
        response.data.curpage = curpage
        response.data.maxpage = 1
        response.data.totalsize = 30
        for _item in info['items']:
            packageItemInfo = response.data.packageItemInfo.add()
            packageItemInfo.position = _item['position']
            _item['itemComponent'].SerializationItemInfo(packageItemInfo.itemInfo)
    
    return response.SerializeToString()

            