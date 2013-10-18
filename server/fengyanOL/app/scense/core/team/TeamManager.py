#coding:utf8
'''
Created on 2011-4-15

@author: sean_lan
'''
from app.scense.core.singleton import Singleton
from app.scense.core.team.Team import Team

class TeamManager:
    '''组队管理器'''
    
    __metaclass__ = Singleton
    _teamTag = 1001

    def __init__(self):
        self.teams = {}

    def getTeamByID(self, id):
        '''根据id获取队伍实例'''
        return self.teams.get(id,None)
        
    def dropTeamById(self,teamId):
        '''删除队伍管理器中的队伍
        @param teamId: int 队伍的ID
        '''
        try:
            del self.teams[teamId]
        except Exception:
            pass
    
    def dropTeamByTeam(self,team):
        '''删除队伍管理器中的队伍'''
        teamId = team.getID()
        self.dropTeamById(teamId)

    def creatTeam(self, Leader):
        '''添加一个新成立的
        @param Leader: int 队长的ID
        '''
        team = Team(self._teamTag,Leader)
        if self.teams.has_key(team._id):
            raise Exception("系统记录冲突")
        self.teams[team._id] = team
        self._teamTag += 1
        return team
        

