#coding:utf8
'''
Created on 2012-8-8
组队副本战斗
@author: jt
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.core.teamfight.TeamFight import TeamFight
import cPickle
from app.scense.applyInterface import teamInstance_app
from app.scense.core.language.Language import Lg

@nodeHandle
def zudui_4300(dynamicId,request_proto):
    '''获取组队列表信息'''
    from app.scense.protoFile.zudui import ZuDuiListInfo4300_pb2
    argument=ZuDuiListInfo4300_pb2.ZuDuiListInfoRequest()
    argument.ParseFromString(request_proto)
    response=ZuDuiListInfo4300_pb2.ZuDuiListInfoResponse()
    
#    pid=argument.id
    page=argument.curPage#当前页数
    rs,zong=TeamFight().GetByPage(page)
    response.result=True
    response.message=u''
    response.zuDuiInfo.curPage=page#当前页数
    response.zuDuiInfo.maxPage=zong#总页数
    if len(rs)>0:#如果有值
        for item in rs:
            info=response.zuDuiInfo.duiWuInfo.add()
            info.dwId=item.get("dwId")
            info.dwType=item.get("dwType")
            info.curNum=item.get("curNum")
            info.leaderName=item.get("leaderName")
    else:
        response.zuDuiInfo.duiWuInfo.extend([])
    return response.SerializeToString()
            
@nodeHandle
def zudui_4301(player,dynamicId,pid,wz,typeid):
    '''创建副本队伍
    @param pid: int 角色id(队长)
    @param wz: int 位置
    @param typeid: int 副本类型    1(lv30荒城回廊)   2（lv60斗技庭院）    3(lv90混沌空间)
    '''
    from app.scense.protoFile.zudui import CreateZuDui4301_pb2
    response=CreateZuDui4301_pb2.CreateZuDuiResponse()
    player = cPickle.loads(player)
    dwid=TeamFight().CreateTeam(player, typeid, wz)
    if dwid==0:
        response.message=Lg().g(623)
        response.result=False
    else:
        response.message=u''
        response.result=True
    response.dwId=dwid
    return response.SerializeToString()

@nodeHandle
def zudui_4302(dynamicId,request_proto):
    '''获取队伍阵法信息（角色选择阵法界面）'''
    from app.scense.protoFile.zudui import GetDuiWuInfo4302_pb2
    argument=GetDuiWuInfo4302_pb2.GetDuiWuInfoRequest()
    argument.ParseFromString(request_proto)
    response=GetDuiWuInfo4302_pb2.GetDuiWuInfoResponse()
    
    pid=argument.id
    dwid=argument.dwId#队伍id
    
    result=TeamFight().getTeamInfoByPlayerId1(dwid)
    response.message=u''
    response.result=True
#    response.message=Lg().g(624)
#    response.result=False
    if len(result)>0:
        for item in result:
            info=response.posRoleInfo.add()
            info.roleId=item.get('roleId')
            info.pos=item.get('pos')
            info.level=item.get('level')
            info.roleName=item.get('roleName')
            info.roleType=item.get('roleType')
    else:
        response.message=Lg().g(624)
        response.result=False
        response.posRoleInfo.extend([])
    return response.SerializeToString()
        
@nodeHandle
def zudui_4303(player,dynamicId,pid,wz,dwid):
    '''角色加入到队伍中
    @param pid: int 角色id
    @param player: obj 角色实例
    @param wz: int 所选阵法位置
    @param dwid: int 队伍id
    '''
    from app.scense.protoFile.zudui import JoinDuiWu4303_pb2
    response=JoinDuiWu4303_pb2.JoinDuiWuResponse()
    player = cPickle.loads(player)
    result=TeamFight().TeamAddPlayer(player, dwid, wz)
    
    response.message=result.get('message')
    response.result=result.get('result')
    response.rdwId=result.get('tid')
    return response.SerializeToString()

@nodeHandle
def zudui_4304(dynamicId,request_proto):
    '''队伍详细信息'''
    from app.scense.protoFile.zudui import GetGroupInfo4304_pb2
    argument=GetGroupInfo4304_pb2.GetGroupInfoRequest()
    argument.ParseFromString(request_proto)
    response=GetGroupInfo4304_pb2.GetGroupInfoResponse()
    
    pid=argument.id
    dwid=argument.dwId#队伍id
    
    result=TeamFight().getTeamInfoByPlayerId(pid,dwid)
    response.message=u''
    response.result=True
    if len(result)>0:
        for item in result:
            info=response.dwMemberInfo.add()
            info.roleId=item.get('roleId')
            info.pos=item.get('pos')
            info.level=item.get('level')
            info.roleName=item.get('roleName')
            info.proType=item.get('roleType')
    else:
        info=response.dwMemberInfo.extend([])
    return response.SerializeToString()

@nodeHandle
def zudui_4305(dynamicId,request_proto):
    '''角色离开队伍'''
    from app.scense.protoFile.zudui import LeaveDuiWu4305_pb2
    argument=LeaveDuiWu4305_pb2.LeaveDuiWuRequest()
    argument.ParseFromString(request_proto)
    response=LeaveDuiWu4305_pb2.LeaveDuiWuResponse()
    
    pid=argument.id
#    dwid=argument.dwId
    TeamFight().TeamDelPlayer(pid)
    response.message=u''
    response.result=True
    return response.SerializeToString()

@nodeHandle
def zudui_4306(dynamicId,request_proto):
    '''踢出成员'''
    from app.scense.protoFile.zudui import TiRen4306_pb2
    argument=TiRen4306_pb2.TiRenRequest()
    argument.ParseFromString(request_proto)
    response=TiRen4306_pb2.TiRenResponse()
    
    pid=argument.id #队长角色id
    cid=argument.roleId #被踢出者角色id
    
    rs=TeamFight().TCTeamPlayer(pid, cid)
    response.message=rs.get('message')
    response.result=rs.get('result')
    return response.SerializeToString()

@nodeHandle
def getzudui_4307(dynamicId,pid):
    '''角色下线之后如果有队伍，则离开队伍'''
    TeamFight().TeamDelPlayer(pid)
    
@nodeHandle
def getzudui_4308(dynamicId,request_proto):
    '''多人副本战斗'''
    from app.scense.protoFile.zudui import GroupBattle4308_pb2
    argument=GroupBattle4308_pb2.FightRequest()
    argument.ParseFromString(request_proto)
    
    pid=argument.id#角色id
    
    teamInstance_app.TeamFighting(pid)
