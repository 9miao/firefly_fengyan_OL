#coding:utf8
'''
Created on 2011-4-15

@author: sean_lan
'''
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.language.Language import Lg

class Team:
    '''队伍'''

    MAXMEMBERSNUMBER = 5#队伍最大的成员数量
    
    def __init__(self,id,leader):
        
        '''初始化队伍信息
        @param leader: int 队长的ID
        @param param: 
        '''
        self._id = id
        self._leader = leader#队长
        self._teamMembers = [leader]#队伍所有的成员
        self.matrix = None #队伍阵法信息
        player = PlayersManager().getPlayerByID(leader)
        player.teamcom.setTeam(self._id)

    def changeLeader(self,player):
        '''更换队长
        @param player: object 队长实例
        '''
        self._leader = player
        
    def getLeader(self):
        '''获取队伍队长'''
        return self._leader
        
    def setId(self,id):
        '''设置队伍id'''
        self._id = id
        
    def getID(self):
        '''获取队伍Id'''
        return self._id
    
    def getTeamMembers(self):
        '''获取队伍成员列表'''
        return self._teamMembers
        
    def getTeamMemberNumber(self):
        '''获取成员现在的数目'''
        return len(self._teamMembers)

    def IsMyTeamer(self,id):
        '''判断是否是自己的队员'''
        if id in self._teamMembers:
                return True
        return False
    
    def addMember(self,characterId):
        '''添加新的成员'''
        if len(self._teamMembers)> self.MAXMEMBERSNUMBER:
            return {'result':False,'message':Lg().g(575)}
        if self.IsMyTeamer(characterId):
            return {'result':False,'message':Lg().g(576)}
        self._teamMembers.append(characterId)
        role = PlayersManager().getPlayerByID(characterId)
        role.teamcom.setTeam(self._id)
#        self.position.append(characterId)
        if self.matrix:
            self.matrix.addMember(characterId)
        return {'result':True}
        
    def dropMenber(self,characterId):
        '''踢出成员'''
        self._teamMembers.remove(characterId)
        role = PlayersManager().getPlayerByID(characterId)
        role.teamcom.setTeam(self._id)
        self.pushTeamMemberInfo()
        if self.matrix:
            self.matrix.dropMember(characterId)
        return {'result':True}
        
    def pushTeamMemberInfo(self):
        '''推送队伍成员信息'''
        data = {}
        data['leaderId'] = self.getLeader()
        data['members'] = [PlayersManager().getPlayerByID(roleId) for \
                           roleId in self.getTeamMembers()]
        pushObjectNetInterface.pushTeamMemberInfo(data)
        
    def setMatrix(self,matrix):
        '''设置队伍正在使用的阵法'''
        self.matrix = matrix
    

