#coding:utf8
'''
Created on 2012-9-10
城镇征战管理
@author: Administrator
'''
from firefly.utils.singleton import Singleton
from app.scense.core.campaign.fortress import Fortress
from app.scense.utils.dbaccess import memdb
from app.scense.utils.dbopera import dbfortress


class FortressManager:
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化
        @param fortresss: dict{fortressID:fortress} 所有要塞的集合
        '''
        self.fortresss = {}
        self.initData()
        
    def initData(self):
        '''初始化要塞信息
        '''
        fortressInfos = dbfortress.getAllFortressInfo()
        for fortressInfo in fortressInfos:
            fortress = Fortress(fortressInfo['id'],'foretress%d'%fortressInfo['id'],memdb)
            fortress.initData(fortressInfo)
            self.fortresss[fortressInfo['id']] = fortress
            
    def getFortressById(self,fortressId):
        '''根据城镇要塞的ID获取城镇的实例
        '''
        fortress = self.fortresss.get(fortressId)
        return fortress
        
    def getAllFortressInfo(self):
        '''获取所有可征战城镇的ID
        '''
        infos = []
        for fortress in self.fortresss.values():
            fortressinfo = fortress.getForTressInfo()
            infos.append(fortressinfo)
        return infos
    
    def checkCanApply(self,guild):
        '''检测指定的国是否能够申请国战
        @param guild: int 国的ID
        '''
        for f in self.fortresss.values():
            if f.kimori == guild:
                return False
            if f.siege == guild:
                return False
        return True
    
    def getGuildFortressId(self,guild):
        '''获取国领地的城镇的ID
        @param guild: int 国的ID
        '''
        for f in self.fortresss.values():
            if f.kimori == guild:
                return f.id
        return 0
    
    def getFortressBySceneId(self,sceneId):
        '''根据城镇的ID获取城镇的占领信息
        '''
        for f in self.fortresss.values():
            if f.sceneId == sceneId:
                return f
        return None
    
    def guildFightFortressId(self,guild):
        '''获取国即将征战的城镇的ID
        @param guild: int 国的ID
        '''
        for f in self.fortresss.values():
            if f.kimori == guild:
                return f.id
            if f.siege == guild:
                return f.id
        return 0
    
    
    def updateAllFortress(self):
        '''更新所有国的信息
        '''
        for fortress in self.fortresss.values():
            fortress.updateDataInDB()
        
    def getBigMapInfo(self):
        '''获取打地图信息
        '''
        from app.scense.core.guild.GuildManager import GuildManager
        infolist = []
        for fortress in self.fortresss.values():
            guild = GuildManager().getGuildById(fortress.kimori)
            info = {}#{'id':1000,'color':randomcorlor(),'tax':10,'income':100,'scene_name':u'克洛村','union_name':'CCC'}
            info['cityid'] = fortress.sceneId
            info['color'] = 16777215 if not guild else guild.get('corlor')
            if not info['color']:
                info['color'] = 16777215
            info['reward'] = 10
            info['cityname'] = fortress.name
            info['gname'] = u'无' if not guild else guild.get('name')
            infolist.append(info)
        return infolist
        
        
