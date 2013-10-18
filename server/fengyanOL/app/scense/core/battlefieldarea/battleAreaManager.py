#coding:utf8
'''
Created on 2011-9-26
行会战区域管理器
@author: lan
'''
from app.scense.core.singleton import Singleton
from app.scense.core.battlefieldarea.BattlefieldArea import BattlefieldArea
from app.scense.utils.dbopera import dbGuildBattle

class BattleAreaManager(object):
    '''行会战区域管理器'''
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化战场
        @param __tag: 动态标记
        @param __areas: 行会战区域
        '''
        self.__tag = 8001
        self.__areas = {}
        
    def creatAreas(self,attackCamp,defenseCamp):
        '''创建一个行会战区域
        @param attackCamp: int 攻击方阵营（国id）
        @param defenseCamp: int 防守方阵营（id）
        '''
        area = BattlefieldArea(self.__tag,attackCamp,defenseCamp)
        self.addArea(area)
        return area.id
    
    def addArea(self,area):
        '''添加一个区域到区域管理中,动态标识加1
        @param area:  BattlefieldArea object
        '''
        self.__areas[area.id] = area
        self.__tag +=1
        
    def dropAreaById(self,areaId):
        '''删除区域根据区域的id
        @param areaId: int 区域的id
        '''
        try:
            del self.__areas[areaId]
        except Exception:
            pass
        
    def getBattleAreaById(self,areaId):
        '''根据战场id获取战场区域实例
        @param areaId: int 区域的id
        '''
        return self.__areas.get(areaId,None)
        
    def prepareGuildBattle(self):
        '''准备好所有的行会战副本'''
        battles = dbGuildBattle.getGuildBattleChecklist()
        for battle in battles:
            self.creatAreas(battle['askCommunity'], battle['answerCommunity'])
            result = dbGuildBattle.creatGuildBattlefield(battle['id'], self.__tag)
            if not result:
                self.dropAreaById(self.__tag)
                
    def getGuildBattleAreaByGuildId(self,guildId):
        '''根据行会的id获取行会战区域的实例
        @param guildId: int 行会的id
        '''
        for battle in self.__areas.items():
            if battle[1].attackCamp == guildId or battle[1].defenseCamp == guildId:
                return battle[1]
        return None
        
    
    def pushAreasInfo(self):
        '''推送所有区域的信息'''
        for area in self.__areas.values():
            area.pushAreaInfo()
            
            
            
    