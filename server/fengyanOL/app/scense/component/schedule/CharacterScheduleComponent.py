#coding:utf8
'''
Created on 2012-5-3
角色每日日程表
开服目的表
@author: Administrator
'''
from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbSchedule

import datetime
from app.scense.core.language.Language import Lg

#日程字典
SCHEDULE_DICT = {}

class CharacterScheduleComponent(Component):
    
    def __init__(self,owner):
        '''初始化
        @param schedule: dict 今日进度
        '''
        Component.__init__(self, owner)
        self.schedule = {}
        self.initSchedule()
        
    def initSchedule(self):
        '''初始化今日进度'''
        characterId = self._owner.baseInfo.id
        self.schedule = dbSchedule.getTodaySchedule(characterId)
        
    def noticeSchedule(self,scheduleType,goal = 1):
        '''进度通知
        @param scheduleType: int 进度类型
        '''
        schedule = dbSchedule.SCHEDULE_CONFIG.get(scheduleType)
        if not schedule:
            return 
        if self.schedule.get('schedule_%d'%scheduleType)>=schedule.get('schedule_goal',1):
            return
        scheduletag = 'schedule_%d'%scheduleType
        self.schedule[scheduletag] +=goal
        if self.schedule[scheduletag]>schedule.get('schedule_goal',1):
            self.schedule[scheduletag] = schedule.get('schedule_goal',1)
        props = {}
        props[scheduletag] = self.schedule[scheduletag]
        if self.schedule[scheduletag]>=schedule.get('schedule_goal',1):
            activityadd = schedule.get('schedule_activity',0)
            self.schedule['activity'] += activityadd
            props['activity'] = self.schedule['activity']
        dbSchedule.updateSchedule(self._owner.baseInfo.id, props)
        
    def receiveBound(self,step):
        '''领取奖励
        @param step: int 步骤
        '''
        if self.schedule['bound_%d'%step]:
            return {'result':False,'message':Lg().g(287)}
        boundinfo = dbSchedule.SCHEDULE_BOUND.get(step)
        if not boundinfo:
            return {'result':False,'message':Lg().g(464)}
        activityrequired = boundinfo.get('vitality_required',100)
        if activityrequired>self.schedule.get('activity'):
            return {'result':False,'message':Lg().g(456)}
        itembound = boundinfo.get('item_bound')
        if self._owner.pack._package._PropsPagePack.findSparePositionNum()<1:
            return {'result':False,'message':Lg().g(16)}
        self._owner.pack.putNewItemsInPackage(itembound,1)
        self.schedule['bound_%d'%step] = 1
        dbSchedule.updateSchedule(self._owner.baseInfo.id, {'bound_%d'%step:1})
        return {'result':True,'message':Lg().g(288)}
    
    def getScheduleInfo(self):
        '''获取日程进度信息'''
        lastdate = self.schedule.get('scheduledate')
        if datetime.date.today()!=lastdate:
            self.initSchedule()
        activity = self.schedule.get('activity')
        finishedlist = []
        unfinishedlist = []
        scheduleBound = []
        for schedule in dbSchedule.SCHEDULE_CONFIG.values():
            info = {}
            info['desc'] = schedule.get('schedule_des',Lg().g(272))
            info['total'] = schedule.get('schedule_goal',1)
            info['now'] = self.schedule.get('schedule_%d'%schedule.get('schedule_tag'),0)
            info['required'] = schedule.get('schedule_activity',0)
            if self.schedule.get('schedule_%d'%schedule.get('schedule_tag'),0)>=info['total']:
                finishedlist.append(info)
            else:
                unfinishedlist.append(info)
        for index in [1,2,3,4]:
            bound = {}
            bound['step'] = index
            bound['received'] = self.schedule['bound_%d'%index]
            scheduleBound.append(bound)
        return {'result':True,'data':{'activity':activity,'finishedlist':finishedlist,
                                      'unfinishedlist':unfinishedlist,'scheduleBound':scheduleBound}}
        
        
        
