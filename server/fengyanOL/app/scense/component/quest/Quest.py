#coding:utf8
'''
Created on 2011-12-7

@author: lan
'''
from twisted.python import log
from app.scense.utils.dbopera import dbtask
from app.scense.core.Item import Item

class Quest(object):
    '''任务类'''
    
    def __init__(self,taskId,characterId = 0,status = 2):
        '''初始化任务信息
        @param taskId: int 
        @param characterId: int 接受任务的角色的id
        @param process: dict 任务的进度
        @param trackStatu: int 任务的追踪状态
        @param status: int  0非法 1可接  2进行中 3完成
        '''
        self._id = taskId
        self.characterId = characterId
        self.process = {'killCount':0,'collectCount':0,'talkCount':0,
                        'goldCount':0,'checkpointCount':0}
        if taskId<20000:
            self.format = dbtask.ALL_MAIN_TASK.get(self._id)
        else:
            self.format = dbtask.ALL_EXTEN_TASK.get(self._id)
        self._status = status
        self._profession = 0
        self._roleName = ''
        self._npcName = ''
        self._track = 1
        self._finishedState = self.format['finishedState']
        
    def initQuestData(self,data):
        '''初始化任务的进度'''
        killCount = data.get('killCount',0)
        collectCount = data.get('collectCount',0)
        talkCount = data.get('talkCount',0)
        goldCount = data.get('goldCount',0)
        checkpointCount = data.get('checkpointCount',0)
        self.trackStatu = data.get('trackStatu',0)
        self.process = {'killCount':killCount,'collectCount':collectCount,
                        'talkCount':talkCount,'goldCount':goldCount,
                            'checkpointCount':checkpointCount}
        
    def getStatus(self):
        '''获取任务状态'''
        return self._status
            
    def setCharacterId(self,characterId):
        '''设置角色的'''
        self.characterId = characterId
        
    def getCharacterId(self):
        '''获取角色的ID'''
        return self.characterId
    
    def setProfession(self,profession):
        '''设置profession'''
        self._profession = profession
    
    def setNpcName(self,npcname):
        '''设置关联NPC的名称'''
        self._npcName = npcname
        
    def setRoleName(self,rolename):
        '''设置关联角色的名称'''
        self._roleName =  rolename
        
    def getTrack(self):
        '''获取任务追踪状态'''
        return self._track
    
    def setTrack(self,track):
        '''设置任务追踪状态'''
        self._track = track
        
    def updateTrack(self,track):
        '''更新任务追踪状态
        @param track: 0 不追踪 1追踪
        '''
        self._track = track
        props = {'trackStatu':track}
        return dbtask.UpdateTaskProcess(self.characterId, self._id, props)
        
    def updateProcess(self,props):
        '''更新任务进度'''
        for key ,value in props.items():
            self.process[key] = value
        dbtask.UpdateTaskProcess(self.characterId, self._id, props)
        
    def resolveGiveItem(self):
        '''解析接受任务时给予的物品
        @param profession: int 给予的职业
        '''
        giveItems = []
        taskInfo = self.format
        itemsDes = taskInfo.get('giveItem',u'')
        if not itemsDes:
            return giveItems
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
        '''解析任务奖励
        @param profession: int 给予的职业
        '''
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
    
    def hasFinished(self):
        '''查看任务是否可以提交
        @param taskId: int 任务的ID
        '''
        taskInfo = self.format
        taskprocess = self.process
        if taskInfo.get('taskType',1)==1:
            return True
        elif taskInfo.get('taskType',1)==2:
            if taskprocess['killCount']>=taskInfo['monsterCount']:
                return True
            return False
        elif taskInfo.get('taskType',1)==3:
            if taskprocess['checkpointCount']>0:
                return True
            return False
        elif taskInfo.get('taskType',1)==4:
            if taskprocess['goldCount']>=taskInfo['demandGold']:
                return True
            return False
        elif taskInfo.get('taskType',1)==5:
            package = self._owner.pack._package.getPackageByType(2)
            if package.countItemTemplateId(taskInfo['demandItem'])>=taskInfo['itemCount']:
                return True
            return False
        else:
            if taskprocess['talkCount']>0:
                return True
            return False
        return False
        
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
            itemPrice.itemId = item.baseInfo.itemTemplateId
            itemPrice.stack = item.pack.getStack()
#            item.SerializationItemInfo(itemPrice)
        return taskResponse
        
    def InsertProcess(self):
        '''写入任务进度'''
        if self.characterId:
            return dbtask.InsertTaskProcess( self.characterId, self._id)
        return False
            
    def delProcess(self):
        '''删除任务进度'''
        dbtask.DelTaskProcessInfo(self.characterId, self._id)
        
        
        