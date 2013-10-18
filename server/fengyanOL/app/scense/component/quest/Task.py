#coding:utf8
'''
Created on 2011-12-7

@author: lan
'''
from twisted.python import log
from app.scense.utils.dbopera import dbtask
from app.scense.core.Item import Item

class Task(object):
    
    def __init__(self,taskId,status = 0,profession = -1,track = 0):
        '''初始化任务信息'''
        if taskId< 100000:
            self.format = dbtask.ALL_MAIN_TASK.get(taskId)
        self._id = taskId
        self._profession = profession#当前任务关联的职业
        self._status = status#任务的状态
        self._track = track#追踪状态 0未追踪 1追踪
        self._npcName = ''#关联到的NPC的名称
        self._roleName = ''#关联到的角色的名称
        
    def setNpcName(self,npcname):
        '''设置关联NPC的名称'''
        self._npcName = npcname
        
    def setRoleName(self,rolename):
        '''设置关联角色的名称'''
        self._roleName =  rolename
        
    def getStatus(self):
        '''获取任务状态'''
        return self._status
    
    def setStatus(self,status):
        '''设置任务状态'''
        self._status = status
        
    def getTrack(self):
        '''获取任务追踪状态'''
        return self._track
    
    def setTrack(self,track):
        '''设置任务追踪状态'''
        self._track = track
        
    def getProfession(self,profession):
        '''获取任务关联的职业'''
        return self._profession
    
    def setProfession(self,profession):
        '''设置任务关联的职业'''
        self._profession = profession
        
    def resolveGiveItem(self):
        '''解析接受任务时给予的物品'''
        giveItems = []
        taskInfo = self.format
        itemsDes = taskInfo.get('giveItem',u'')
        try:
            itemsDataInfo = eval(itemsDes)
        except Exception:
            log.err('Task %d `ItemPrize` field Configuration error !'%self._id)
            return []
        if itemsDataInfo:
            generaldata = itemsDataInfo.get(0,[])
            professiondata = itemsDataInfo.get(self._profession,[])
        else:
            generaldata = []
            professiondata = []
        for itemId,stack in generaldata:
            item = Item(itemTemplateId = itemId)
            item.pack.setStack(stack)
            giveItems.append(item)
        for itemId,stack in professiondata:
            item = Item(itemTemplateId = itemId)
            item.pack.setStack(stack)
            giveItems.append(item)
        return giveItems
        
    def resolveItemPrize(self):
        '''解析任务奖励'''
        itemsprize = []
        taskInfo = self.format
        itemsDes = taskInfo.get('ItemPrize',u'')
        try:
            itemsDataInfo = eval(itemsDes)
        except Exception:
            log.err('Task %d `ItemPrize` field Configuration error !'%self._id)
            return []
        if itemsDataInfo:
            generaldata = itemsDataInfo.get(0,[])
            professiondata = itemsDataInfo.get(self._profession,[])
        else:
            generaldata = []
            professiondata = []
            
        for itemId,stack in generaldata:
            item = Item(itemTemplateId = itemId)
            item.pack.setStack(stack)
            itemsprize.append(item)
        for itemId,stack in professiondata:
            item = Item(itemTemplateId = itemId)
            item.pack.setStack(stack)
            itemsprize.append(item)
        return itemsprize
        
    def SerializationTaskInfo(self,taskResponse):
        '''将自己的所有属性序列号付给Message对象
        @param bearer: Message Object 承载者
        '''
        taskInfo = self.format
        taskResponse.task_id = taskInfo.get('taskID')
        taskResponse.task_type = taskInfo.get('taskType')
        taskResponse.task_state = self._status
        taskResponse.task_is_track = self._track
        taskResponse.task_price_coins = taskInfo.get('CoinPrize')
        taskResponse.task_price_zuan = taskInfo.get('GoldPrize')
        taskResponse.task_exp = taskInfo.get('ExpPrize')
        taskResponse.task_name = taskInfo.get('taskName')
        taskResponse.task_lv = taskInfo.get('levelRequired')
        taskResponse.task_type_name = taskInfo.get('lableType')
        taskResponse.task_ui_des = taskInfo.get('taskDescription')
        taskResponse.task_runing_des = self._npcName+'\n'+taskInfo.get('NPCUnfinishTalk')
        taskResponse.task_taget = taskInfo.get('taskGoalDes')
        task_des = []
        if self._status==1:
            if taskInfo.get('NPCTalk1',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._npcName
                taskTalk.task_des = taskInfo.get('NPCTalk1',u'')
            if taskInfo.get('UserTalk1',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._roleName
                taskTalk.task_des = taskInfo.get('UserTalk1',u'')
                task_des.append(taskInfo.get('UserTalk1',u''))
            if taskInfo.get('NPCTalk2',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._npcName
                taskTalk.task_des = taskInfo.get('NPCTalk2',u'')
            if taskInfo.get('UserTalk2',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._roleName
                taskTalk.task_des = taskInfo.get('UserTalk2',u'')
            if taskInfo.get('NPCTalk3',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._npcName
                taskTalk.task_des = taskInfo.get('NPCTalk3',u'')
            if taskInfo.get('UserEnter',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._roleName
                taskTalk.task_des = taskInfo.get('UserEnter',u'')
        elif self._status==2:
            if taskInfo.get('NPCUnfinishTalk',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._npcName
                taskTalk.task_des = taskInfo.get('NPCUnfinishTalk',u'')
            if taskInfo.get('UserUnfinishEnter',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._roleName
                taskTalk.task_des = taskInfo.get('UserUnfinishEnter',u'')
        elif self._status==3:
            if taskInfo.get('NPCFinishTalk',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._npcName
                taskTalk.task_des = taskInfo.get('NPCFinishTalk',u'')
            if taskInfo.get('UserFinishEnter',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._roleName
                taskTalk.task_des = taskInfo.get('UserFinishEnter',u'')
        else:
            if taskInfo.get('demandDialogue',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._npcName
                taskTalk.task_des = taskInfo.get('demandDialogue',u'')
            if taskInfo.get('dialogueFinished',u''):
                taskTalk = taskResponse.task_des.add()
                taskTalk.roleType = self._roleName
                taskTalk.task_des = taskInfo.get('demandDialogue',u'')
                task_des.append(taskInfo.get('dialogueFinished',u''))
        itemBound = self.resolveItemPrize()
        for item in itemBound:
            itemPrice = taskResponse.task_price_item.add()
            item.SerializationItemInfo(itemPrice)
        return taskResponse
        
        
        
        