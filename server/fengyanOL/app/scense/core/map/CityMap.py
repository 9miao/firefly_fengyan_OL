#coding:utf8
'''
Created on 2012-12-21
城池地图
@author: lan
'''

from app.scense.core.map.Map import BaseMap
from app.scense.core.character.Monster import Monster


class CityMap(BaseMap):
    '''城镇地图
    '''
    
    def __init__(self, mid):
        '''初始化城池信息
        '''
        BaseMap.__init__(self, mid)
        self.banners = []#城镇的负旗帜
        self.main_banners = None#城池的主城
        self.initBanners()
        self.initMainBanners()
        
    def initMainBanners(self):
        '''初始化城镇的主帅旗帜
        '''
        sencename = self.getSceneGuildName()
        position = (1000,800)
        monster = Monster(id = 1,templateId = 15013)
        if sencename:
            monstername = monster.baseInfo.getName()
            monster.baseInfo.setName( u'【%s】%s'%(sencename,monstername))
        monster.baseInfo.setStaticPosition(position)
        monster.setMconfig(1)
        self.addMonster(monster)
        
    def initBanners(self):
        '''初始化副帅旗帜
        '''
        for i in range(2,6):
            self.produceBanners(i)
            
    def produceBanners(self,bannerId):
        '''生成副旗
        @param bannerId: 副旗的ID
        '''
        positions = {2:(500,800),3:(1500,800),4:(1000,500),5:(1000,1100)}
        position = positions[bannerId]
        sencename = self.getSceneGuildName()
        monster = Monster(id = bannerId,templateId = 15014)
        if sencename:
            monstername = monster.baseInfo.getName()
            monster.baseInfo.setName( u'【%s】%s'%(sencename,monstername))
        monster.baseInfo.setStaticPosition(position)
        monster.setMconfig(bannerId)
        try:
            self.addMonster(monster)
        except Exception:
            print 'ok'
        
    def produce(self):
        '''定时生成怪物
        '''
        _killed = []
        for mconfigid,delta in self._killed:
            if delta==0:
                if mconfigid==1:
                    self.initMainBanners()
                elif mconfigid in [2,3,4,5]:
                    self.produceBanners(mconfigid)
                else:
                    self._mProducers.send(mconfigid)
            else:
                delta -= 1
                _killed.append((mconfigid,delta))
        self._killed = _killed
        
