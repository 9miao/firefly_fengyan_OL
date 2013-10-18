#coding:utf8
'''
Created on 2011-6-16

@author: lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

def getQuestListOnNpc(dynamicId,characterId,npcId):
    '''获取npc身上任务列表
    @param dynamicId: int 客户端动态Id
    @param characterId: int 角色的id
    @param npcId: int npc的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    player.quest.pushPlayerScenceNpcQuestStatus()
    return {'result':True}

def applyQuest(dynamicId,characterId,taskId):
    '''接受任务
    @param dynamicId: int 任务的id
    @param characterId: int 角色的id
    @param taskId: int 任务的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if  not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.quest.applyQuest(taskId)
    return data

def commitQuest(dynamicId,characterId,taskId):
    '''提交任务
    @param dynamicId: int 任务的id
    @param characterId: int 角色的id
    @param taskId: int 任务的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.quest.commitQuest(taskId)
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905,msg,[dynamicId])
    return data
    
def getQuestProcessList(dynamicId,characterId):
    '''获取任务进度列表'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result  = player.quest.getQuestProcessList()
    data = {'result':True,'message':u'','data':result}
    return data

def getProcessQuestList(dynamicId,characterId):
    '''获取正在进行的任务列表'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = []#player.quest.getProcessQuestList()
    data = {'result':True,'message':u'','data':result}
    return data

def getCanReceivedquestList(dynamicId,characterId):
    '''获取可接任务列表'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    result = player.quest.getCanReceivedquestList()
    data = {'result':True,'message':u'','data':result}
    return data

def getScenceNpcQuestStatus(dynamicId,characterId):
    '''获取场景中NPC的任务状态'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    player.quest.pushPlayerScenceNpcQuestStatus()

def updateQuestTraceStatu(dynamicId,characterId,taskID,traceStatu):
    '''更新任务追踪状态'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.quest.updateQuestTraceStatu(taskID,traceStatu)
    if data.get('result',False) and traceStatu==1:
        msg = u'该任务已添加至追踪列表'
        pushOtherMessage(905,msg,[dynamicId])
    return data

#----------------新版任务--------------------

def TaskNpcTaskInfo(dynamicId,characterId,NpcID):
    '''获取NPC的主线任务
    @param dynamicId: int 客户端动态id
    @param characterId: int 角色的id
    @param NpcID: int npc的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False}
    data = player.quest.formatNpcQuestInfo(NpcID)
    return data

def TaskNpcAcceptTask(dynamicId,characterId,task_id,npc_id):
    '''接受任务
    @param dynamicId: int 客户端的动态id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False}
    data = player.quest.applyQuest(task_id,npc_id)
    return data

def TaskExcuteTalk(dynamicId,characterId,task_id,npc_id):
    '''任务交谈'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False}
    data = player.quest.talkWithNpc(npc_id,task_id)
    return {'result':data,'message':u''}

def TaskNpcSubTask(dynamicId,characterId,task_id,npc_id):
    '''提交任务'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False}
    data = player.quest.commitQuest(task_id,npc_id)
    data['task_id'] = task_id
    msg = data.get('message','')
    if msg:
        pushOtherMessage(905,msg,[dynamicId])
    return data

def TaskPlayerTaskList(dynamicId,characterId):
    '''获取角色已接任务列表'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.quest.getTaskProcessInfo()
    return {'result':True,'tasks':data}
    
def TaskPlayerAcceptTaskList(dynamicId,characterId):
    '''获取可接任务列表
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.quest.getCanReceivedQuestList()
    return {'result':True,'tasks':data}
    
def TaskPlayerDropTask(dynamicId,characterId,task_id):
    '''放弃任务'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':Lg().g(18)}
    data = player.quest.abandonQuest(task_id)
    return data
    
    

    