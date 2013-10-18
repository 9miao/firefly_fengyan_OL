#coding:utf8
'''
Created on 2012-4-7
角色主界面右上角图标列表
@author: Administrator
'''

from app.scense.component.Component import Component
import time
#import datetime

from app.scense.netInterface.pushObjectNetInterface import pushApplyMessage
from app.scense.protoFile.defence import GameTopTitle2400_pb2
#from applyInterface import configure
#from core.campaign import fortress

def pushGameTopTitle2400(sendList,typelist):
    '''推送奖励图标
    @param typeid: int 奖励类型 1为殖民  2殖民管理 3流光溢彩的殖民管理 
    4新手奖励 5每日奖励6点石成金7VIP 8竞技场 9组队副本
    '''
    response=GameTopTitle2400_pb2.GameTopTitleResponse()
    response.message = u'你妹'
    anouInfos = response.anouInfo
    for icon in typelist:
        icontype = icon.getItype()
        if icontype in [2,3]:
            continue
        anouInfo = anouInfos.add()
        anouInfo.anouType = icontype
        anouInfo.surplusTimes = icon.getSurplustime()
    data = response.SerializeToString()
    pushApplyMessage(2400 , data, sendList)
    


class Icon:
    '''图标类
    '''
    def __init__(self,itype,totaltime):
        ''''''
        self.itype = itype #1为殖民奖金  2殖民管理  3流光溢彩的殖民管理 4新手奖励 5每日奖励6点石成金 9组队副本
        self.totaltime = totaltime 
        self.starttime = time.time()
        
    def getItype(self):
        '''获取图标类型'''
        return self.itype
        
    def getSurplustime(self):
        '''计算剩余时间'''
        if self.totaltime==0:
            return 0
        pasttime = time.time()-self.starttime
        surplus = int(self.totaltime - pasttime)
        return surplus if surplus >0 else 0 
    
    def formatIcon(self):
        '''格式化图标信息'''
        iconformat = {}
        iconformat['anouType'] = self.itype
        iconformat['surplusTimes'] = self.getSurplustime()
        return iconformat
    

class CharacterIconComponent(Component):
    '''角色图标列表'''
    
    NEW_AWARD = 4 #新手在线奖励
    DAY_AWARD = 5 #每日奖励
    TURN_GOLD = 6 #点石成金
    VIP_AWARD = 7 #vip礼包
    ARENA_AWARD = 8#竞技场奖励
    
    def __init__(self,owner):
        '''初始化
        @param iconlist: Icon object list 角色的图标列表
        '''
        Component.__init__(self, owner)
        self.iconlist = {}
        
    def getIconByType(self,icontype):
        '''根据图标类型获取图标'''
        return self.iconlist.get(icontype)
        
    def addIcon(self,icontype,totaltime,state = 1):
        '''添加一个图标'''
        icon = Icon(icontype,totaltime)
        self.iconlist[icontype] = icon
        if state:
            self.pushGameTopIcon()
        
    def removeIcon(self,icontype,state = 1):
        '''移除一个图标'''
        try:
            del self.iconlist[icontype]
        except Exception:
            pass
        if state:
            self.pushGameTopIcon()
        
    def pushGameTopIcon(self):
        '''推送图标列表信息'''
        iconlist = self.iconlist.values()
        pushGameTopTitle2400([self._owner.getDynamicId()],iconlist)
        
    def groupIconManager(self,state):
        '''组队的图标管理
        '''
        groupIconType = 9
        
        if state and self._owner.level.getLevel()>=17:
            if not self.iconlist.has_key(groupIconType):
                self.addIcon(groupIconType, 0)
        else:
            if self.iconlist.has_key(groupIconType):
                self.removeIcon(groupIconType)
        
    def guildFightManager(self,state):
        '''国战图标管理
        '''
        guildfightIconType = 10
        if state:
            if not self.iconlist.has_key(guildfightIconType):
                self.addIcon(guildfightIconType, 0)
        else:
            if self.iconlist.has_key(guildfightIconType):
                self.removeIcon(guildfightIconType)
        
    
        
    
    
    
