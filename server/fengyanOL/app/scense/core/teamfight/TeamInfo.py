#coding:utf8
'''
Created on 2012-8-7
组队挑战副本类
@author: jt
'''

class TeamInfo():
    '''组队挑战副本类'''


    def __init__(self,tid,player,type,wz):
        '''初始化
        @param tid: int 队伍id
        @param player: obj 角色实例
        @param type: int 副本类型
        @param wz: int 队长阵法位置
         '''
        self.teamid=tid#队伍id
        self.pname=player.baseInfo.getNickName()#队长名称
        self.pid=player.baseInfo.getId()#队长id
        self.type=type#副本类型id
        self.count=1#当前人数
        self.players={self.pid:player}#成员列表key:角色id，value:角色实例
        self.zf={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}#阵法信息 key阵法信息，value:>0表示角色在此位置
        self.zf[wz]=self.pid
        
    def addTeamPlayer(self,player,wz):
        '''添加队伍成员
        @param player: obj 角色实例
        @param wz: int 角色所在位置
        '''
        pid=player.baseInfo.getId()#角色id
        self.players[pid]=player#加添队伍成员实例
        self.zf[wz]=pid#设置此角色所在的阵法位置
        self.count+=1#设置队伍人数
    
    def delTeamPlayer(self,pid):
        '''角色退出队伍
        @param pid: int 退出的角色id
        '''
        del self.players[pid]#重新设置成员列表
        for key,value in self.zf.items():
            if value==pid:
                self.zf[key]=0#重新设置阵法位置
        self.count-=1#重新设置队伍人数
                
    def getZfInfo(self):
        '''获取阵法信息'''
        info={}
        for k,v in self.zf.items():
            if v>0:
                info[v]=k
        return info
    
        