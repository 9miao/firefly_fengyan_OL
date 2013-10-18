#coding:utf8
'''
Created on 2011-4-20

@author: sean_lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.language.Language import Lg

def invitedGroup(dynamicId,id,tid):
    '''邀请它人入队
    @param dynamicId: int 客户端的id
    @param id: int 邀请者的id
    @param tid: int 被邀请者的id
    '''
    player = PlayersManager().getPlayerByID(id)
    toplayer = PlayersManager().getPlayerByID(tid)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if not toplayer:
        return {'result':False,'message':Lg().g(91)}
    if player.teamcom.amITeamMember() and toplayer.teamcom.amITeamMember():
        return {'result':False,'message':Lg().g(251)}
    msg = Lg().g(252)%player.baseInfo.getNickName()
    sendPlayer = toplayer.teamcom.getMyTeamLeader()
    sendList = [sendPlayer.dynamicId]
    pushObjectNetInterface.pushInvitedGroup(id, msg, sendList)
    return {'result':True,'message':Lg().g(253)}

def applyInGroup(id,tid):
    '''申请入队
    @param id: 申请入队者id
    @param tid: 有队伍角色id
    '''
    player=PlayersManager().getPlayerByID(id)#申请入队角色
    players=PlayersManager().getPlayerByID(tid)#有队伍角色
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if not players:
        return {'result':False,'message':Lg().g(91)}
    if player.teamcom.amITeamMember():
        return {'result':False,'message':Lg().g(254)}
    if not player.teamcom.amITeamMember():
        return {'result':False,'message':Lg().g(255)}
    
    msg = u"%s 申请进入队伍"%player.baseInfo.getNickName()
    sendPlayer = players.teamcom.getMyTeamLeader()
    sendList = [sendPlayer.dynamicId]
    pushObjectNetInterface.pushInvitedGroup(id, msg, sendList)
    return {'result':True,'message':Lg().g(253)}
    

def argeeApplyGroup(id,tid):
    '''同意申请入队
    @param id: int 申请入队者id
    @param tid: int 有队的伍角色id
    '''
    player = PlayersManager().getPlayerByID(id)#申请入队者
    toplayer = PlayersManager().getPlayerByID(tid)#有队伍的角色id
    sendPlayer = toplayer.teamcom.getMyTeamLeader()#队长角色

    if not player:
        return {'result':False,'message':Lg().g(18)}
    if not toplayer:
        return {'result':False,'message':Lg().g(256)}
    if player.teamcom.amITeamMember():
        return {'result':False,'message':Lg().g(254)}
    if not player.teamcom.amITeamMember():
        return {'result':False,'message':Lg().g(255)}
    if sendPlayer.teamcom.amITeamMember():#如果队长有队伍
        data = sendPlayer.teamcom.addTeamMember(player)
    if data['result']:
        player.teamcom.pushTeamMemberInfo()
        pushObjectNetInterface.pushOtherMessage(905,Lg().g(257),[sendPlayer.dynamicId])
    return data
    
def agreeGroup(dynamicId,id,tid):
    '''同意组队邀请 (别人进来)
    @param dynamicId: int 客户端的id
    @param id: int 被邀请人id
    @param tid: int 邀请人id
    '''
    player = PlayersManager().getPlayerByID(id)#被邀请人
    toplayer = PlayersManager().getPlayerByID(tid)#邀请人
    sendPlayer=None #队长角色
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if not toplayer:
        return {'result':False,'message':Lg().g(256)}
    
    if player.teamcom.amITeamMember() and toplayer.teamcom.amITeamMember():#如果都有组队
        return {'result':False,'message':Lg().g(251)}
    elif not player.teamcom.amITeamMember() and not toplayer.teamcom.amITeamMember():#如果都没有队伍
        data = toplayer.teamcom.addTeamMember(player)#邀请者为队长
        sendPlayer=toplayer
    else:
        sendPlayer = toplayer.teamcom.getMyTeamLeader()#队长角色
        data = sendPlayer.teamcom.addTeamMember(player)
    if data['result']:
        player.teamcom.pushTeamMemberInfo()
        pushObjectNetInterface.pushOtherMessage(905,Lg().g(257),sendPlayer.dynamicId)
    return data


def zudui(id,tid):
    '''组队功能
        @param id: int 当前用户角色
        @param tid: int 角色2
    '''
    player1 = PlayersManager().getPlayerByID(id)#当前用户实例
    player2 = PlayersManager().getPlayerByID(tid)#角色2实例    
    player=None;#队长实例
    toplayer=None;#队员
    
    if not player1:#如果当前用户掉线
        return {'result':False,'message':Lg().g(18)}
    if not player2:#如果角色2掉线
        return {'result':False,'message':Lg().g(256)}
    if player1.teamcom.amITeamMember() and player2.teamcom.amITeamMember():#如果都有组队
        return {'result':False,'message':Lg().g(251)}
    
    if not player1.teamcom.amITeamMember() and not player2.teamcom.amITeamMember():#如果都没有队伍
        player=player1
        toplayer=player2
    elif player1.teamcom.amITeamMember():#如果当前用户有队伍
        player=player1.teamcom.getMyTeamLeader()#获取当前用户队伍中的队长
        toplayer=player2
    elif player2.teamcom.amITeamMember():#如果角色2有队伍
        player=player2.teamcom.getMyTeamLeader()#获取角色2队伍中的队长
        toplayer=player1
        
    data = player.teamcom.addTeamMember(toplayer)
    
def rejectGroup(dynamicId,id,tid):
    '''拒绝组队
    @param dynamicId: int 客户端的id
    @param id: int 角色id
    @param tid: int 申请者的id
    '''
    player = PlayersManager().getPlayerByID(id)
    toplayer = PlayersManager().getPlayerByID(tid)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if not toplayer:
        return {'result':False,'message':Lg().g(256)}
    sendList = []
    sendList.append(toplayer.dynamicId)
    msg = u'玩家 %s 拒绝了您的组队申请'%(player.baseInfo.getNickName())
    pushObjectNetInterface.pushOtherMessage(905,msg,sendList)
    return {'result':True}

def expelMember(id):
    '''踢出成员'''
    player = PlayersManager().getPlayerByID(id)#角色
    data=player.teamcom.FireMember(id)
    if data:
        return {'result':True,'message':Lg().g(259)%player.baseInfo.getNickName()}