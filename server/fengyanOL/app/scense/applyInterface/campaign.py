#coding:utf8
'''
Created on 2012-9-11

@author: Administrator
'''
from app.scense.core.campaign.FortressManager import FortressManager
from app.scense.core.guild.GuildManager import GuildManager
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.language.Language import Lg

def GetGroupLingDiInfo4400(dynamicId,characterId):
    '''获取国领地信息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    guildInfo = guild.guildinfo
    info = {}
    ldID = FortressManager().getGuildFortressId(guildId)
    fortress = FortressManager().getFortressById(ldID)
    if fortress:
        if not fortress.isOccupied:
            fortress = None
    info['ldType'] = ldID if fortress else 0
    info['groupName'] = guildInfo['name']
    info['groupLevel'] = guildInfo['level']
    info['groupLeader'] = guildInfo['presidentname']
    info['obtainJL'] = True if fortress else False
    info['icon'] = guildInfo['emblemLevel']
    info['battleInfo'] = [] if not fortress else fortress.fightlog
    info['battleTime'] = 0 if not fortress else fortress.getNextFightTime()
    return {'result':True,'data':info}

def ObtainJiangLi4401(dynamicId,characterId):
    '''领取奖励殖民'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    ldID = FortressManager().getGuildFortressId(guildId)
    if not ldID:#没有领地
        return {'result':False,'message':Lg().g(657)}
    result = player.guild.ObtainFortressReward()
    msgID = result.get('msgID',0)
    message = u''
    if msgID:
        message = Lg().g(msgID)
    return {'result':result.get('result',False),'message':message}

def GetCityListInfo4402(dynamicId,characterId):
    '''获取城镇征战信息列表'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    info = FortressManager().getAllFortressInfo()
    return {'result':True,'data':info}

def GroupPK4403(dynamicId,characterId,pkId):
    '''国战申请
    '''
    HAOJIAO = 20700072
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    if not FortressManager().checkCanApply(guildId):
        return {'result':False,'message':Lg().g(648)}
    
    fortress = FortressManager().getFortressById(pkId)
    if not fortress:
        return {'result':False}
    itemcount = player.pack.countItemTemplateId(HAOJIAO)#检测战斗号角数量
    if itemcount<1:
        return {'result':False,'message':Lg().g(656)}
    data = fortress.SignUp(guildId)
    result = data.get('result',False)
    if result:
        player.pack.delItemByTemplateId(HAOJIAO,1)#扣除战斗号角
    msgID = data.get('msgID',0)
    message = u''
    if msgID:
        message = Lg().g(msgID)
    return {'result':result,'message':message}
    
def GetXuYuanInfo4404(dynamicId,characterId):
    '''获取许愿相关信息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    guild = GuildManager().getGuildById(guildId)
    info = guild.GetXuYuanInfo()
    info['xyValue'] = player.petShop.xy
    return {'result':True,'data':info}
    
def UseXingYun4405(dynamicId,characterId,usetype):
    '''许愿获取幸运
    @param characterId: int 角色的ID
    @param usetype: int 类型  0四叶草1郁金香2蝴蝶兰3紫罗兰4曼陀罗
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.guild.UseXingYun(usetype)
    result = data.get('result',False)
    msgID = data.get('msgID',0)
    message = u''
    if msgID:
        message = Lg().g(msgID)
    return {'result':result,'message':message}
    
def GetBattleInfo4406(dynamicId,characterId):
    '''获取战斗信息'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    ldID = FortressManager().guildFightFortressId(guildId)
    fortress = FortressManager().getFortressById(ldID)
    if not fortress:
        return {'result':False,'message':Lg().g(654)}
    guildBattleInfo = {}
    guildBattleInfo['roundCount'] = fortress.getRound()
    guildBattleInfo['remainTime'] = fortress.getBattleRemainTime()
    guildBattleInfo['jishaCount'] = player.guild.successTimes
    guildBattleInfo['obtainCoin'] = player.guild.coinBound
    guildBattleInfo['failCount'] = player.guild.failTimes
    guildBattleInfo['obtainSw'] = player.guild.prestigeBound
    guildBattleInfo['battleInfoList'] = fortress.battleInfoList
    
    guild1Id = fortress.get('kimori')
    guild2Id = fortress.get('siege')
    guild1Info = {}
    guild2Info = {}
    if guild1Id:
        guild1 = GuildManager().getGuildById(guild1Id)
        guild1Info = {}
        guild1Info['groupName'] = guild1.get('name')
        guild1Info['groupCount'] = fortress.kimoriScore
        guild1Info['icon'] = guild1.get('emblemLevel')
        guild1Info['groupMember'] = fortress.kimoriMembers
        
    if guild2Id:
        guild2 = GuildManager().getGuildById(guild2Id)
        guild2Info = {}
        guild2Info['groupName'] = guild2.get('name')
        guild2Info['groupCount'] = fortress.siegeScore
        guild2Info['icon'] = guild2.get('emblemLevel')
        guild2Info['groupMember'] = fortress.siegeMembers
        
    guildBattleInfo['group1Info'] = guild1Info
    guildBattleInfo['group2Info'] = guild2Info
    return {'result':True,'data':guildBattleInfo}
    
def Participate4407(dynamicId,characterId):
    '''国战参战
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    ldID = FortressManager().guildFightFortressId(guildId)
    fortress = FortressManager().getFortressById(ldID)
    if not fortress:
        return {'result':False,'message':Lg().g(654)}
    chName = player.baseInfo.getName()
    chLevel = player.level.getLevel()
    fortress.Participate(guildId,characterId,chName,chLevel)
    return {'result':True}

def AutoJoinBattle4408(dynamicId,characterId,autoJoinFlag):
    '''自动参战或取消自动参战
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    ldID = FortressManager().guildFightFortressId(guildId)
    fortress = FortressManager().getFortressById(ldID)
    if not fortress:
        return {'result':False,'message':Lg().g(654)}
    if autoJoinFlag:
        chName = player.baseInfo.getName()
        chLevel = player.level.getLevel()
        fortress.Participate(guildId,characterId,chName,chLevel)
        result = fortress.autoJoin(characterId)
    else:
        result = fortress.cancelAutoJoin(characterId)
    return {'result':result}
    
def CancelParticipate4409(dynamicId,characterId):
    '''取消国战参战
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        return {'result':False,'message':Lg().g(79)}
    ldID = FortressManager().guildFightFortressId(guildId)
    fortress = FortressManager().getFortressById(ldID)
    if not fortress:
        return {'result':False,'message':Lg().g(654)}
    chName = player.baseInfo.getName()
    chLevel = player.level.getLevel()
    fortress.cancelParticipate(guildId,characterId,chName,chLevel)
    return {'result':True}

