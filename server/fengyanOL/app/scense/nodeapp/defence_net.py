#coding:utf8
'''
Created on 2012-2-15
保卫防御
@author: jt
'''
from app.scense.applyInterface import defencelog_app
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.defence import GetRewardBattleInfo2404_pb2
from app.scense.protoFile.defence import ObtainReward2402_pb2
from app.scense.protoFile.defence import ObtainAllReward2403_pb2
from app.scense.protoFile.defence import GetRewardList2401_pb2
from app.scense.core.language.Language import Lg

@nodeHandle
def GetRewardBattleInfo_2404(dynamicId, request_proto):
    '''返回入侵列表'''
    argument = GetRewardBattleInfo2404_pb2.GetRewardBattleInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetRewardBattleInfo2404_pb2.GetRewardBattleInfoResponse()
    
    pid = argument.id #角色id
    r_id=argument.r_id #奖励id
    page=argument.page #当前页数
    
    dataList,zong=defencelog_app.getInvadeList(pid, page, 5)
    if len(dataList)<=0:
        pass
    else:
        response.result=True
        response.message=Lg().g(603)
        response.battleListInfo.r_id=r_id
        response.battleListInfo.curPage=page
        response.battleListInfo.maxPage=int(zong)
        for item in dataList: #遍历入侵列表
            fe =response.battleListInfo.battleInfo.add()
            fe.battleName=item['name'] #城镇或副本名称
            fe.battleResult=item['battleResult'] #战斗是否成功
            if item['cgid']>0: #成功者id
                ffe=fe.sucRoleInfo.add()
                ffe.roleId=item['cgid']#成功者id
                ffe.roleName=item['cgname'] #角色名称
            else:
                fe.sucRoleInfo.extend([])
            
            if len(item['sb'])>0:
                for key,value in item['sb'].items():
                    ff=fe.failRoleInfo.add() #失败者信息
                    ff.roleId=key #失败者id
                    ff.roleName=value #失败者名称
            else:
                fe.failRoleInfo.extend([])
    return response.SerializeToString()
@nodeHandle
def ObtainReward_2402(dynamicId, request_proto):
    '''领取单个保卫奖励'''
    argument=ObtainReward2402_pb2.ObtainRewardRequest()
    argument.ParseFromString(request_proto)
    response=ObtainReward2402_pb2.ObtainRewardResponse()
    id=argument.id #角色id
    r_id=argument.r_id #保卫奖励表主键id
    dynamicId = dynamicId
    result,message=defencelog_app.ObtainReward(id,r_id) #返回执行结果和返回信息
    defencelog_app.isReward(id,dynamicId)#刷新图标
       
    response.result=result
    response.message=message
    return response.SerializeToString()
@nodeHandle
def ObtainAllReward_2403(dynamicId, request_proto):
    '''领取所有保卫奖励'''
    argument=ObtainAllReward2403_pb2.ObtainAllRewardRequest()
    argument.ParseFromString(request_proto)
    response=ObtainAllReward2403_pb2.ObtainAllRewardResponse()
    id=argument.id #角色id
    dynamicId = dynamicId
    result,message=defencelog_app.ObtainAllReward(id) #返回执行结果和返回信息
    defencelog_app.isReward(id,dynamicId)#刷新图标
    response.result=result
    response.message=message
    return response.SerializeToString()

@nodeHandle
def GetRewardList_2401(dynamicId, request_proto):
    '''返回殖民奖金列表'''
    argument=GetRewardList2401_pb2.GetRewardListRequest()
    argument.ParseFromString(request_proto)
    response=GetRewardList2401_pb2.GetRewardListResponse()
    id=argument.id #角色id
    page=argument.page #当前页数
    dynamicId = dynamicId
    rList,zong=defencelog_app.getRewardList(id, page,5) #返回奖励列表和总页数
    if not rList: #如果没有记录
        response.result=True
        response.message=u''
        response.rewardListInfo.curPage=1
        response.rewardListInfo.maxPage=1
        response.rewardListInfo.rewardInfo.extend([])
        return response.SerializeToString()
    response.result=True
    response.message=u''
    response.rewardListInfo.curPage=page
    response.rewardListInfo.maxPage=int(zong)
    for item in rList:
        r=response.rewardListInfo.rewardInfo.add()
        r.r_id=item['r_id']
        r.r_type=item['r_type']
        r.t_name=item['t_name']
        r.t_e1=str(item['t_e1'])
        r.t_e2=str(item['t_e2'])
        r.t_e3=str(item['t_e3'])
        r.t_e4=item['t_e4']
    return response.SerializeToString()
    