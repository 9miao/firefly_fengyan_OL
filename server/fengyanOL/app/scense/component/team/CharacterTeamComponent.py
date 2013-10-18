#coding:utf8
'''
Created on 2010-3-11

@author: wudepeng
'''
from app.scense.component.Component import Component
from app.scense.core.team.TeamManager import TeamManager
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.language.Language import Lg

class CharacterTeamComponent(Component):
    '''
    CharacterTeamComponent
    '''
    _teamId = -1

    def __init__(self, owner):
        '''
        Constructor for character team component
        '''
        Component.__init__(self, owner)
    
    def setTeam(self,teamId):
        '''设置队伍'''
        self._teamId = teamId
        
    def getTeam(self):
        '''获取队伍'''
        team=TeamManager().getTeamByID(self._teamId)
        if team:
            return team
        return None
    
    def clearTeam(self):
        '''退出队伍'''
        self._teamId = -1
        
    def addTeamMember(self,characterId):
        '''添加队伍成员'''
        if characterId ==self._owner.baseInfo.id:
            return {'result':False,'message':Lg().g(491)}
        if self._teamId==-1:
            team =TeamManager().creatTeam(self._owner.baseInfo.id)
        else:
            team = TeamManager().getTeamByID(self._teamId)
        result = team.addMember(characterId)
        team.pushTeamMemberInfo()
        return result
    
    def amITeamLeader(self):
        '''判断自己是否是队长'''
        team = TeamManager().getTeamByID(self._teamId)
        if not team:
            return False
        if team.getLeader()==self._owner.baseInfo.id:
            return True
        return False
    
    def amITeamMember(self):
        '''判断是否在队伍中'''
        if self._teamId == -1:
            return False
        team = TeamManager().getTeamByID(self._teamId)
        if team :
            return True
        return False
    
    def amisteam(self):
        '''判断自己是否在队伍中'''
        team = TeamManager().getTeamByID(self._teamId)
        if team:
            return True
        return False
    
    def getMyTeamNumb(self):
        '''获取队伍人数'''
        team = TeamManager().getTeamByID(self._teamId)
        if not team:
            return -1
        else:
            team.getTeamMemberNumber()
    
    def getMyTeamLeader(self):
        '''获取队伍中的队长队长'''
        team = TeamManager().getTeamByID(self._teamId)
        if team:
            return team.getLeader()
        return self._owner
    
    def pushTeamMemberInfo(self):
        '''推送队伍成员信息'''
        if self._teamId == -1:
            pushObjectNetInterface.pushUpdatePlayerInfo(self._owner.getDynamicId())
            return
        team = TeamManager().getTeamByID(self._teamId)
        if team :
            team.pushTeamMemberInfo()
        else:
            self._owner.updatePlayerInfo()
            
    def IsMyTeamMember(self,memberId):
        '''判断是否是自己队伍的成员'''
        team = TeamManager().getTeamByID(self._teamId)
        if not team:
            return False
        teamMemberIdlist = team.getTeamMembers()
        if memberId in teamMemberIdlist:
            return True
        return False
            
    def getMyTeamMember(self):
        '''获取队伍成员信息'''
        team = TeamManager().getTeamByID(self._teamId)
        if team:
            return team._teamMembers
        return None
    
    def FireMember(self,memberId):
        '''踢出成员'''
        if not self.amITeamLeader():
            return {'result':False,'message':Lg().g(492)}
        team = TeamManager().getTeamByID(self._teamId)
        result = team.dropMenber(memberId)
        if not result['result']:
            return result
        teamerNumber = team.getTeamMemberNumber()
        if teamerNumber<2:
            TeamManager().dropTeamById(self._teamId)
            self.setTeam(-1)
        return  {'result':True,'message':Lg().g(112)}
    
    def exitTeam(self):
        '''退出队伍'''
        team = TeamManager().getTeamByID(self._teamId)
        if not team:
            return False
    
    
