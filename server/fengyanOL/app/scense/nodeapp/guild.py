#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import guild
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.guild import GetCorpsListInfo_pb2
from app.scense.protoFile.guild import CreateCorps1302_pb2
from app.scense.protoFile.guild import AcceptOrRefuseAppli_pb2
from app.scense.protoFile.guild import AppliOrUnsubscribe_pb2
from app.scense.protoFile.guild import TransferCorpsOrKickMember_pb2
from app.scense.protoFile.guild import ModifyCorpsAnnoun_pb2
from app.scense.protoFile.guild import CrusadeCorps_pb2
from app.scense.protoFile.guild import GetEmblemInfo1310_pb2
from app.scense.protoFile.guild import LevelUpEmblem_pb2
from app.scense.protoFile.guild import ModifyBugle_pb2
from app.scense.protoFile.guild import GetCorpsTechnologyListInfo1314_pb2
from app.scense.protoFile.guild import CorpsTechnologyDonate_pb2
from app.scense.protoFile.guild import LeaveCorps_pb2
from app.scense.protoFile.guild import TakeCorpsChief_pb2
from app.scense.protoFile.guild import ModifyDefaultDonate_pb2
from app.scense.protoFile.guild import GetCorpsMembListInfo_1303_pb2
from app.scense.protoFile.guild import GetCorpsAppliListInfo_1317_pb2
from app.scense.protoFile.guild import CorpsInviteOtherRequest_pb2
from app.scense.protoFile.guild import CorpsInviteReplyRequest_pb2
from app.scense.protoFile.guild import GetSingleUnionListRequest1322_pb2
from app.scense.protoFile.map import MapMessage_pb2
from app.scense.protoFile.guild import ModifyJoinLevel_1324_pb2
from app.scense.core.language.Language import Lg


@nodeHandle
def getGuildListInfo_1301(dynamicId,request_proto):
    '''获取行会列表'''
    arguments = GetCorpsListInfo_pb2.GetCorpsListInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GetCorpsListInfo_pb2.GetCorpsListInfoResponse()
    
    dynamicId = dynamicId
    characterId=arguments.id
    getType = arguments.getType
    curPage = arguments.curPage
    searchCriteria = arguments.searchCriteria
    data = guild.getGuildListInfo(dynamicId, characterId, getType, curPage, searchCriteria)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        result = data.get('data')
        response.data.curPage = result.get('curPage',1)
        response.data.maxPage = result.get('maxPage',1)
        for guildInfo in result['corpsInfo']:
            corpsInfo = response.data.corpsInfo.add()
            corpsInfo.corpsId = guildInfo['id']
            corpsInfo.corpsImg = guildInfo['emblemLevel']
            corpsInfo.corpsName = guildInfo['name']
            corpsInfo.corpsChief = guildInfo['nickname']
            corpsInfo.corpsLevel = guildInfo['level']
            corpsInfo.curNum = guildInfo['curMenberNum']
            corpsInfo.maxNum = guildInfo['memberCount']
            corpsInfo.onApplication = guildInfo['onApplication']
            corpsInfo.corpsTitle = guildInfo['bugle']
            corpsInfo.corpsAnnouncement = guildInfo['announcement']
            corpsInfo.leaderId = guildInfo['president']
            corpsInfo.runningFlag = bool(guildInfo['isOnline'])
            corpsInfo.levelrequired = guildInfo['levelrequired']
    return response.SerializeToString()
    
@nodeHandle
def creatGuild_1302(dynamicId,request_proto):
    '''创建行会'''
    arguments = CreateCorps1302_pb2.CreateCorpsRequest()
    arguments.ParseFromString(request_proto)
    response = CreateCorps1302_pb2.CreateCorpsResponse()
    
    dynamicId = dynamicId
    characterId=arguments.id
    corpsName = arguments.corpsName
    camp= arguments.type
    data = guild.creatGuild(dynamicId, characterId, corpsName,camp)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()
    
@nodeHandle
def AcceptOrRefuseApply_1304(dynamicId,request_proto):
    '''拒绝或同意申请'''
    arguments = AcceptOrRefuseAppli_pb2.AcceptOrRefuseAppliRequest()
    arguments.ParseFromString(request_proto)
    response = AcceptOrRefuseAppli_pb2.AcceptOrRefuseAppliResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id
    operType = arguments.operType
    appliId = arguments.appliId
    data = guild.AcceptOrRefuseApply(dynamicId, characterId, operType, appliId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def AppliOrUnsubscribe_1305(dynamicId,request_proto):
    '''申请加入国和取消
    '''
    arguments = AppliOrUnsubscribe_pb2.AppliOrUnsubscribeRequest()
    arguments.ParseFromString(request_proto)
    response = AppliOrUnsubscribe_pb2.AppliOrUnsubscribeResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id 
    operType = arguments.operType
    corpsId = arguments.corpsId
    data = guild.AppliOrUnsubscribe(dynamicId, characterId, operType, corpsId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def TransferCorpsOrKickMember_1306(dynamicId,request_proto):
    '''移交国长或开除成员'''
    arguments = TransferCorpsOrKickMember_pb2.TransferCorpsOrKickMemberRequest()
    arguments.ParseFromString(request_proto)
    response = TransferCorpsOrKickMember_pb2.TransferCorpsOrKickMemberResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id 
    operType = arguments.operType
    memberId = arguments.memberId
    data = guild.TransferCorpsOrKickMember(dynamicId, characterId, operType, memberId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def ModifyCorpsAnnoun_1307(dynamicId,request_proto):
    '''修改公告'''
    arguments = ModifyCorpsAnnoun_pb2.ModifyCorpsAnnounRequest()
    arguments.ParseFromString(request_proto)
    response = ModifyCorpsAnnoun_pb2.ModifyCorpsAnnounResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id 
    announContent = arguments.announContent
    data = guild.ModifyCorpsAnnoun(dynamicId, characterId, announContent)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def CrusadeCorps_1308(dynamicId,request_proto):
    '''行会战申请'''
    arguments = CrusadeCorps_pb2.CrusadeCorpsRequest()
    arguments.ParseFromString(request_proto)
    response = CrusadeCorps_pb2.CrusadeCorpsResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id 
    corpsId = arguments.corpsId
    data = guild.CrusadeCorps(dynamicId, characterId, corpsId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def GetEmblemInfo_1310(dynamicId,request_proto):
    '''获取行会管理信息'''
    arguments = GetEmblemInfo1310_pb2.GetEmblemInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GetEmblemInfo1310_pb2.GetEmblemInfoResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id
    data = guild.GetEmblemInfo(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        result = data.get('data')
        for item in result.items():
            if item[0]=='veteranList':
                for veteran in item[1]:
                    veteranList = response.data.veteranList.add()
                    veteranList.roleName = veteran
                continue
            if item[0]=='staffInfo':
                for staff in item[1]:
                    staffInfo = response.data.staffInfo.add()
                    staffInfo.roleName = staff
                continue
            if item[0]=='orderInfo':
                for order in item[1]:
                    orderInfo = response.data.orderInfo.add()
                    orderInfo.roleName = order
                continue
            setattr(response.data,item[0],item[1])
    return response.SerializeToString()

@nodeHandle
def LevelUpEmblem_1311(dynamicId,request_proto):
    '''升级军徽'''
    arguments = LevelUpEmblem_pb2.LevelUpEmblemRequest()
    arguments.ParseFromString(request_proto)
    response = LevelUpEmblem_pb2.LevelUpEmblemResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id
    data = guild.LevelUpEmblem(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def ModifyBugle_1312(dynamicId,request_proto):
    '''修改军号'''
    arguments = ModifyBugle_pb2.ModifyBugleRequest()
    arguments.ParseFromString(request_proto)
    response = ModifyBugle_pb2.ModifyBugleResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id
    bugleTxt = arguments.bugleTxt
    data = guild.ModifyBugle(dynamicId, characterId, bugleTxt)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def GetCorpsTechnologyListInfo_1314(dynamicId,request_proto):
    '''获取科技列表'''
    arguments = GetCorpsTechnologyListInfo1314_pb2.GetCorpsTechnologyListInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GetCorpsTechnologyListInfo1314_pb2.GetCorpsTechnologyListInfoResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id
    curPage = arguments.curPage
    data = guild.GetCorpsTechnologyListInfo(dynamicId, characterId, curPage)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        result = data.get('data')
        response.data.curPage = result['curPage']
        response.data.maxPage = result['maxPage']
        for technologyInfo in result['technologyInfo']:
            technology = response.data.technologyInfo.add()
            for item in technologyInfo.items():
                setattr(technology,item[0],item[1])
    return response.SerializeToString()
    
@nodeHandle
def CorpsTechnologyDonate_1315(dynamicId,request_proto):
    '''捐献'''
    arguments = CorpsTechnologyDonate_pb2.CorpsTechnologyDonateRequest()
    arguments.ParseFromString(request_proto)
    response = CorpsTechnologyDonate_pb2.CorpsTechnologyDonateResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id
    donateNum = arguments.donateNum
    technologyId = arguments.technologyId
    data = guild.CorpsTechnologyDonate(dynamicId, characterId, donateNum,technologyId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def LeaveCorps_1309(dynamicId,request_proto):
    '''离开行会'''
    arguments = LeaveCorps_pb2.LeaveCorpsRequest()
    arguments.ParseFromString(request_proto)
    response = LeaveCorps_pb2.LeaveCorpsResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id
    data = guild.LeaveGuild(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def TakeCorpsChief_1313(dynamicId,request_proto):
    '''接位国长'''
    arguments = TakeCorpsChief_pb2.TakeCorpsChiefRequest()
    arguments.ParseFromString(request_proto)
    response = TakeCorpsChief_pb2.TakeCorpsChiefResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id
    data = guild.TakeCorpsChief(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def ModifyDefaultDonate_1316(dynamicId,request_proto):
    '''修改科技捐献设置'''
    arguments = ModifyDefaultDonate_pb2.ModifyDefaultDonateRequest()
    arguments.ParseFromString(request_proto)
    response = ModifyDefaultDonate_pb2.ModifyDefaultDonateResponse()
    
    dynamicId = dynamicId
    characterId = arguments.id
    technologyId = arguments.technologyId
    data = guild.ModifyDefaultDonate(dynamicId, characterId, technologyId)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString() 

@nodeHandle
def GetCorpsMemberListInfo_1303(dynamicId,request_proto):
    '''获取成员列表信息'''
    arguments = GetCorpsMembListInfo_1303_pb2.GetCorpsMemberListInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GetCorpsMembListInfo_1303_pb2.GetCorpsMemberListInfoResponse()
    
    dynamicId = dynamicId
    characterId=arguments.id
    searchCriteria = arguments.searchCriteria
    curPage = arguments.curPage
    data = guild.GetCorpsMembListInfo(dynamicId, characterId, searchCriteria, curPage)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        result = data.get('data')
        response.data.curPage = result.get('curPage',1)
        response.data.maxPage = int(result['maxPage'])
        for member in result['MemberListBaseInfo']:
            memberInfo = response.data.memberListBaseInfo.add()
            for item in member.items():
                if item[0] =='memberProfession':
                    memberInfo.memberProfession = str(item[1])#{1:Lg().g(390),2:Lg().g(391),3:Lg().g(392),4:Lg().g(393)}.get()
                    continue
                setattr(memberInfo, item[0], item[1])
    return response.SerializeToString()

@nodeHandle
def GetCorpsAppliListInfo_1317(dynamicId,request_proto):
    '''获取申请列表'''
    arguments = GetCorpsAppliListInfo_1317_pb2.GetCorpsAppliListInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GetCorpsAppliListInfo_1317_pb2.GetCorpsAppliListInfoResponse()
    dynamicId = dynamicId
    characterId=arguments.id
    searchCriteria = arguments.searchCriteria
    curPage = arguments.curPage
    data = guild.GetCorpsAppliListInfo(dynamicId, characterId, searchCriteria, curPage)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    if data.get('data',None):
        result = data.get('data')
        response.data.curPage = result.get('curPage',1)
        response.data.maxPage = int(result['maxPage'])
        response.data.levelrequired = int(result['levelrequired'])
        for member in result['AppliListBaseInfo']:
            memberInfo = response.data.appliListBaseInfo.add()
            for item in member.items():
                if item[0] =='memberProfession':
                    memberInfo.memberProfession = {1:Lg().g(390),2:Lg().g(391),3:Lg().g(392),4:Lg().g(393)}.get(item[1])
                    continue
                setattr(memberInfo, item[0], item[1])
    return response.SerializeToString()

@nodeHandle
def UnionInviteOther_1318(dynamicId,request_proto):
    '''邀请加入行会'''
    arguments = CorpsInviteOtherRequest_pb2.UnionInviteOtherRequest()
    arguments.ParseFromString(request_proto)
    response = CorpsInviteOtherRequest_pb2.UnionInviteOtherResponse()
    
    dynamicId = dynamicId
    characterId=arguments.id
    otherid = arguments.otherid
    otername = arguments.otername 
    data = guild.CorpsInviteOther(dynamicId, characterId, otherid, otername)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()
 
@nodeHandle
def CorpsInviteReply_1320(dynamicId,request_proto):
    '''行会邀请的反馈'''
    arguments = CorpsInviteReplyRequest_pb2.UnionInviteReplyRequest()
    arguments.ParseFromString(request_proto)
    response = CorpsInviteReplyRequest_pb2.UnionInviteReplyResponse()
    
    dynamicId = dynamicId
    characterId=arguments.id
    union_id = arguments.union_id 
    is_ok = arguments.is_ok
    data = guild.CorpsInviteReply(dynamicId, characterId, union_id, is_ok)
    response.result = data.get('result',False)
    response.message = data.get('message',u'')
    return response.SerializeToString()

@nodeHandle
def GetSingleUnionInfo_1322(dynamicId,request_proto):
    '''获取单个国的信息'''
    arguments = GetSingleUnionListRequest1322_pb2.GetSingleUnionInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GetSingleUnionListRequest1322_pb2.GetSingleUnionInfoResponse()
    dynamicId = dynamicId
    characterId=arguments.id
    union_id = arguments.union_id 
    data = guild.GetSingleUnion(dynamicId, characterId, union_id)
    response.result = data.get('result',False)
    response.msg = data.get('message','')
    if response.result:
        guildInfo = data.get('data')
        response.corpsId = guildInfo['id']
        response.corpsImg = guildInfo['emblemLevel']
        response.corpsName = guildInfo['name']
        response.corpsChief = guildInfo['nickname']
        response.corpsLevel = guildInfo['level']
        response.curNum = guildInfo['curMenberNum']
        response.maxNum = guildInfo['memberCount']
        response.onApplication = False
        response.corpsTitle = guildInfo['bugle']
        response.corpsAnnouncement = guildInfo['announcement']
        response.leaderId = guildInfo['president']
    return response.SerializeToString()

@nodeHandle
def ChangeUnionColor_2503(dynamicId,request_proto):
    '''改变行会标识颜色'''
    argument = MapMessage_pb2.ChangeUnionColorRequest()
    argument.ParseFromString(request_proto)
    response = MapMessage_pb2.ChangeUnionColorResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    color = argument.color
    result = guild.ChangeUnionColor(dynamicId, characterId, color)
    response.result = result.get('result',False)
    response.message = result.get('message',u'')
    response.color = color
    return response.SerializeToString()
    
@nodeHandle
def ModifyJoinLevel_1324(dynamicId,request_proto):
    '''修改国加入等级限制'''
    argument = ModifyJoinLevel_1324_pb2.ModifyJoinLevelRequest()
    argument.ParseFromString(request_proto)
    response = ModifyJoinLevel_1324_pb2.ModifyJoinLevelResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    levelrequired  = argument.levelrequired 
    result = guild.ModifyJoinLevel(dynamicId, characterId, levelrequired)
    response.result = result.get('result',False)
    response.message = result.get('message',u'')
    return response.SerializeToString()
    
