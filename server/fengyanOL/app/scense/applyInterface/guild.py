#coding:utf8
'''
Created on 2011-5-25

@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.guild.GuildManager import GuildManager
from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbGuild
from app.scense.netInterface.pushObjectNetInterface import pushInviteOtherJoinGuild,pushOtherMessage
from app.scense.netInterface.pushPrompted import pushPromptedMessage
from app.scense.core.language.Language import Lg

AllCharacterGuildInfo={} #存储角色与行会对应关系
LEVELREQUIRED = 12

def getGuildListInfo(dynamicId,characterId,getType,curPage,searchCriteria):
    '''获取国列表
    @param dynamicId: int 客户端动态id
    @param characterId: int 角色的id
    @param getType: int 获取类型  0获取所有1搜索
    @param curPage: int 当前页数
    @param searchCriteria: str 搜索条件
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    info = GuildManager().getGuildListInfo(characterId, getType, curPage, searchCriteria)
    return {'result':True,'data':info}

def creatGuild(dynamicId,characterId,corpsName,camp):
    '''创建国
    @param dynamicId: int 客户端动态id
    @param characterId: int 角色的id
    @param corpsName: int 国的名称
    @param camp: int 国阵营 1光明 2黑暗
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if player.level.getLevel()<LEVELREQUIRED:
        return {'result':False,'message':Lg().g(77)}
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    for word in dbaccess.All_ShieldWord:
        cnt = corpsName.find(word[0])
        if cnt!=-1:
            return {'result':False,'message':Lg().g(78)}
    data = player.guild.creatGuild(corpsName,camp)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return data
    
def GetCorpsMemberOrAppliListInfo(dynamicId,characterId,getType,searchCriteria,curPage):
    '''获取成员列表或申请列表
    @param dynamicId: int 客户端的动态id
    @param characterId: int 客户端的动态id
    @param getType: int //0获取国成员列表1按条件查找国成员2获取申请列表3按条件查找申请成员
    @param searchCriteria: str//搜索条件
    @param curPage: int 当前页面号
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    result = player.guild.GetCorpsMemberOrAppliListInfo(getType,searchCriteria,curPage)
    return result

def AcceptOrRefuseApply(dynamicId,characterId,operType,appliId ):
    '''拒绝或同意申请
    @param dynamicId: int 客户端的动态id
    @param characterId: int 客户端的动态id
    @param operType: int 操作类型 0 接受 1 拒绝
    @param appliId: int 申请ID
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    if operType==0:
        data = guild.acceptGuildApply(characterId,appliId)
        reason = {0:Lg().g(80),-1:Lg().g(81),-2:Lg().g(82),\
                  -3:Lg().g(83),-4:Lg().g(84)}
        if data ==1:
            
            result = {'result':True,'message':Lg().g(85)}
        else:
            result = {'result':False,'message':reason[data]}
    else:
        data = guild.refuseGuildApply(characterId,appliId)
        reason = {0:Lg().g(80),-1:Lg().g(81),-4:Lg().g(84)}
        if data ==1:
            result = {'result':True,'message':Lg().g(85)}
        else:
            result = {'result':False,'message':reason[data]}
    return result

def AppliOrUnsubscribe(dynamicId,characterId,operType,corpsId):
    '''申请加入或取消申请
    @param dynamicId: int 客户端的动态id
    @param characterId: int 客户端的动态id
    @param operType: int 操作类型 0 申请进入 1 取消申请
    @param corpsId: int 国的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if operType==0:
        if player.level.getLevel()<LEVELREQUIRED:
            return {'result':False,'message':Lg().g(86)}
        result = player.guild.AppliJionGuild(corpsId)
    else:
        result = player.guild.UnsubscribeJionGuild(corpsId)
    return result

def TransferCorpsOrKickMember(dynamicId,characterId,operType,memberId):
    '''移交团长或踢出成员
    @param dynamicId: int 客户端的动态id
    @param characterId: int 客户端的id
    @param operType: int 操作类型
    @param memberId: int 被操作者的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    if operType==0:#移交国长
        data = guild.TransferCorps(characterId,memberId)
    else:
        data = guild.fireMember(characterId,memberId)
    return data
    
def ModifyCorpsAnnoun(dynamicId,characterId,announContent):
    '''发布行会公告
    @param dynamicId: int 客户的动态id
    @param characterId: int 操作者的id
    @param announContent: str 公告的内容
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    for word in dbaccess.All_ShieldWord:
        cnt = announContent.find(word[0])
        if cnt!=-1:
            return {'result':False,'message':Lg().g(78)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    data = guild.modifyCorpsAnnoun(characterId,announContent)
    return data

def CrusadeCorps(dynamicId,characterId,corpsId):
    '''国讨伐申请
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param corpsId: int 国的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    toGuild = GuildManager().getGuildById(corpsId)
    if not toGuild:
        return {'result':False,'message':Lg().g(87)}
    data = guild.CrusadeCorps(characterId,guildId)
    return data

def GetEmblemInfo(dynamicId,characterId):
    '''获取行会的管理信息
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    data = guild.GetEmblemInfo()
    return {'result':True,'data':data}

def LevelUpEmblem(dynamicId,characterId):
    '''升级军徽
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    emblemlevel = guild.guildinfo.get('emblemLevel',0)
    goldRequired = {1:100,2:200,3:500,4:1000,5:2000,6:5000,7:10000,8:20000,9:50000,10:10000}
    goldcons = goldRequired.get(emblemlevel,100)
    if goldcons > player.finance.getGold():
        msg = Lg().g(190)
        pushOtherMessage(905, msg, [dynamicId])
        return {'result':False,'message':msg}
    data = guild.LevelUpEmblem(characterId)
    if data.get('result',False):
        player.finance.consGold(goldcons,6)#升级军徽消耗钻
        player.guild.addContribution(int(goldcons*1.5))
        player.updatePlayerInfo()
    else:
        pushOtherMessage(905, data.get('message',''), [dynamicId])
    return data

def ModifyBugle(dynamicId,characterId,bugleTxt):
    '''修改军号
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param bugleTxt: str 军号
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    data = guild.ModifyBugle(characterId,bugleTxt)
    return data

def GetCorpsTechnologyListInfo(dynamicId,characterId,curPage):
    '''获取行会科技列表信息
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param curPage: int 当前页数
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    data = guild.getTechnologyList(characterId,curPage)
    return {'result':True,'data':data}

def CorpsTechnologyDonate(dynamicId,characterId,donateNum,technologyId):
    '''科技捐献
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param donateNum: int 捐献的数量
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if player.finance.getCoin()<donateNum:
        return {'result':False,'message':Lg().g(88)}
    result = player.guild.Donate(technologyId)
    return result

def LeaveGuild(dynamicId,characterId):
    '''离开行会
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.guild.leaveGuild()
    if data.get('result',False):
        pushPromptedMessage(Lg().g(89), [dynamicId])
    return data

def TakeCorpsChief(dynamicId,characterId):
    '''接位国长
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    data = guild.takeCorpsChief(characterId)
    return data

def ModifyDefaultDonate(dynamicId,characterId,technologyId):
    '''修改科技捐献设置
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param technologyId: int 科技的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    data = guild.ModifyDefaultDonate(characterId,technologyId)
    return data
    
def GetCorpsMembListInfo(dynamicId,characterId,searchCriteria,curPage):
    '''获取国的成员列表
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    if curPage<1:
        return {'result':False,'message':Lg().g(90)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    data = guild.searchGuildMemberInfo(searchCriteria,curPage)
    return {'result':True,'data':data}
    
def GetCorpsAppliListInfo(dynamicId,characterId,searchCriteria,curPage):
    '''获取行会申请列表
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    if curPage<1:
        return {'result':False,'message':Lg().g(90)}
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    data = guild.searchApplyJoinGuildInfo(searchCriteria,curPage)
    return {'result':True,'data':data}
    
def CorpsInviteOther(dynamicId,characterId,otherid,otername):
    '''邀请加入行会
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param otherid: int 对方的Id
    @param otername: 对方的名称
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    toplayer = PlayersManager().getPlayerByID(otherid)
    if not toplayer:
        return {'result':False,'message':Lg().g(91)}
    if toplayer.level.getLevel()<LEVELREQUIRED:
        return {'result':False,'message':Lg().g(86)}
    guild = GuildManager().getGuildById(guildId)
    if guild.guildinfo.get('curMenberNum',50)>=guild.guildinfo.get('memberCount',50):
        return {'result':False,'message':Lg().g(83)}
    sendList = [toplayer.getDynamicId()]
    pushInviteOtherJoinGuild(characterId, guildId, player.baseInfo.getName(),\
                              guild.getGuildName(), sendList)
    msg = Lg().g(92)
    pushOtherMessage(905, msg, [dynamicId])
    return {'result':True}
        
def CorpsInviteReply(dynamicId,characterId,union_id,is_ok):
    '''邀请加入行会的反馈信息
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param union_id: int 行会的id(邀请者的ID)
    @param is_ok: int 是否同意 0否 1是
    '''
    player = PlayersManager().getPlayerByID(characterId)
    fplayer = PlayersManager().getPlayerByID(union_id)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    nowguildId = player.guild.getID()
    toguildId = dbGuild.getCharacterGuildId(union_id)
    if fplayer and not is_ok:
        msg = "%s拒绝了你的邀请"%player.baseInfo.getName()
        pushOtherMessage(905, msg, [fplayer.getDynamicId()])
        return {'result':True}
    if nowguildId:
        return {'result':False,'message':Lg().g(94)}
    guild = GuildManager().getGuildById(toguildId)
    if not guild:
        return {'result':False,'message':Lg().g(95)}
    surplushours = player.guild.getCanJoinTime()
    if surplushours:
        return {'result':False,'message':Lg().g(647)%surplushours}
    result = guild.JointGuild(characterId)
    if result.get('result',False):
        
        msg = u'成功加入%s'%guild.getGuildName()
        pushOtherMessage(905, msg, [dynamicId])
    else:
        nmsg = result.get('message','')
        pushOtherMessage(905, nmsg, [dynamicId])
    return result
    
def GetSingleUnion(dynamicId,characterId,union_id):
    '''获取单个国的信息'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guild = GuildManager().getGuildById(union_id)
    if not guild:
        return {'result':False,'message':Lg().g(95)}
    guildInfo = guild.getGuildInfo(characterId)
    if not guildInfo:
        return {'result':False,'message':Lg().g(95)}
    return {'result':True,'data':guildInfo}
    
def ChangeUnionColor(dynamicId,characterId,color):
    '''修改本国势力颜色'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    return guild.changeColor(characterId,color)

def ModifyJoinLevel(dynamicId,characterId,levelrequired):
    '''修改申请加入等级限制
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param levelrequired: int 等级限制
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    data = guild.ModifyJoinLevel(characterId,levelrequired)
    reason = {0:Lg().g(80),-1:Lg().g(81)}
    if data ==1:
        result = {'result':True,'message':Lg().g(85)}
    else:
        result = {'result':False,'message':reason[data]}
    return result


