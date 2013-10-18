#coding:utf8
'''
Created on 2011-6-16

@author: lan
'''
from app.scense.applyInterface import quest
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.quest import getQuestListOnNpc_pb2
from app.scense.protoFile.quest import applyQuest_pb2
from app.scense.protoFile.quest import commitQuest_pb2
from app.scense.protoFile.quest import getQuestProcessList_pb2
from app.scense.protoFile.quest import getProcessQuestList_pb2
from app.scense.protoFile.quest import getCanReceivedquestList_pb2
from app.scense.protoFile.quest import getScenceNpcQuestStatus_pb2
from app.scense.protoFile.quest import updateQuestTraceStatu_pb2
from app.scense.protoFile.quest import getQuestInfoOnPanel_pb2
from app.scense.protoFile.quest import TaskNpcTaskInfoRequest1410_pb2
from app.scense.protoFile.quest import TaskNpcSubTaskRequest1411_pb2
from app.scense.protoFile.quest import TaskNpcAcceptTaskRequest1412_pb2
from app.scense.protoFile.quest import TaskExcuteTalkTaskRequest1419_pb2
from app.scense.protoFile.quest import TaskPlayerAcceptTaskListRequest1417_pb2
from app.scense.protoFile.quest import TaskPlayerDropTaskRequest1418_pb2
from app.scense.protoFile.quest import TaskPlayerTaskListRequest1416_pb2

@nodeHandle
def getQuestListOnNpc_1401(dynamicId, request_proto):
    '''获取NPC身上任务列表'''
    arguments = getQuestListOnNpc_pb2.getQuestListOnNpcRequest()
    arguments.ParseFromString(request_proto)
    response = getQuestListOnNpc_pb2.getQuestListOnNpcResponse()
    
    characterId = arguments.id
    npcId = arguments.npcId
    data = quest.getQuestListOnNpc(dynamicId, characterId, npcId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    
    if data.get('data',None):
        canReceivedquestList = data.get('data').get('canReceivedquestList')
        progressingquestList = data.get('data').get('progressingquestList')
        cancommitquestList = data.get('data').get('cancommitquestList')
        response.data.npcId = npcId
        for q in canReceivedquestList:
            questl = response.data.canReceivedquestList.add()
            questl.taskId = q['id']
            questl.taskname = q['name']
        for q in progressingquestList:
            questl = response.data.progressingquestList.add()
            questl.taskId = q['id']
            questl.taskname = q['name']
        for q in cancommitquestList:
            questl = response.data.cancommitquestList.add()
            questl.taskId = q['id']
            questl.taskname = q['name']
    return response.SerializeToString()

@nodeHandle
def applyQuest_1402(dynamicId, request_proto):
    '''接受任务'''
    arguments = applyQuest_pb2.applyQuestRequest()
    arguments.ParseFromString(request_proto)
    response = applyQuest_pb2.applyQuestResponse()
    
    characterId = arguments.id
    taskId = arguments.taskId
    data = quest.applyQuest(dynamicId, characterId, taskId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    response.data.taskId = taskId
    return response.SerializeToString()

@nodeHandle
def commitQuest_1403(dynamicId, request_proto):
    '''提交任务'''
    arguments = commitQuest_pb2.commitQuestRequest()
    arguments.ParseFromString(request_proto)
    response = commitQuest_pb2.commitQuestResponse()
    
    characterId = arguments.id
    taskId = arguments.taskId
    data = quest.commitQuest(dynamicId, characterId, taskId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    response.data.taskId = taskId
    return response.SerializeToString()

@nodeHandle
def getQuestProcessList_1405(dynamicId, request_proto):
    '''获取任务进度'''
    arguments = getQuestProcessList_pb2.getQuestProcessListRequest()
    arguments.ParseFromString(request_proto)
    response = getQuestProcessList_pb2.getQuestProcessListResponse()
    
    characterId = arguments.id
    data = quest.getQuestProcessList(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        questprocesslist = data.get('data')
        for _questprocess in questprocesslist:
            questprocess = response.data.questprocesslist.add()
            questprocess.taskId = _questprocess.get('taskId',0)
            processinfolist = _questprocess.get('processinfolist',[])
            for _pinfo in processinfolist:
                processinfo = questprocess.processinfolist.add()
                processinfo.questGoalId = _pinfo['questGoalId']
                processinfo.killMonsterCount = _pinfo['killMonsterCount']
                processinfo.collectItemCount = _pinfo['collectItemCount']
                processinfo.hasTalkedtoNPC = _pinfo['hasTalkedtoNPC']
                processinfo.resourcesCount = _pinfo['resourcesCount']
    
    return response.SerializeToString()

@nodeHandle
def getProcessQuestList_1406(dynamicId, request_proto):
    '''获取正在进行中的任务列表'''
    arguments = getProcessQuestList_pb2.getProcessQuestListRequest()
    arguments.ParseFromString(request_proto)
    response = getProcessQuestList_pb2.getProcessQuestListResponse()
    
    characterId = arguments.id
    data = quest.getProcessQuestList(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        processquestlist = data.get('data')
        for _questprocess in processquestlist:
            questprocess = response.data.progressingquestList.add()
            questprocess.taskId = _questprocess.get('id',0)
            questprocess.taskname = _questprocess.get('name','')
            questprocess.trackStatu = _questprocess.get('trackStatu',0)
    return response.SerializeToString()

@nodeHandle
def getCanReceivedquestList_1407(dynamicId, request_proto):
    '''获取可接任务的列表'''
    arguments = getCanReceivedquestList_pb2.getCanReceivedquestListRequest()
    arguments.ParseFromString(request_proto)
    response = getCanReceivedquestList_pb2.getCanReceivedquestListResponse()
    characterId = arguments.id
    data = quest.getCanReceivedquestList(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        questList = data.get('data')
        canReceivedquestList = response.data.canReceivedquestList
        for canReceivedquest in questList:
            Receivablequest = canReceivedquestList.add()
            Receivablequest.taskId = canReceivedquest.get('id')
            Receivablequest.taskname = canReceivedquest.get('name')
    return response.SerializeToString()

@nodeHandle
def getScenceNpcQuestStatus_1408(dynamicId, request_proto):
    '''获取场景中npc的任务状态'''
    arguments = getScenceNpcQuestStatus_pb2.getScenceNpcQuestStatusRequest()
    arguments.ParseFromString(request_proto)
    
    characterId = arguments.id
    quest.getScenceNpcQuestStatus(dynamicId, characterId)

@nodeHandle
def getQuestInfoOnPanel_1409(dynamicId, request_proto):
    '''获取任务的详细信息'''
    arguments = getQuestInfoOnPanel_pb2.getQuestInfoOnRequest()
    arguments.ParseFromString(request_proto)
    response = getQuestInfoOnPanel_pb2.getQuestInfoResponse()
    
    characterId = arguments.id
    taskID = arguments.taskID
    data = {}#quest.getQuestInfoOnPanel(dynamicId, characterId, taskID)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        data = data.get('data')
        questInfoOnPanel = data.get('questInfo',None)
        if questInfoOnPanel:
            questInfoOnPanel.SerializationQuestInfo(response.data.questInfo)
    return response.SerializeToString()
    
@nodeHandle
def updateQuestTraceStatu_1420(dynamicId, request_proto):
    '''更新任务追踪状态'''
    arguments = updateQuestTraceStatu_pb2.updateQuestTraceStatuRequest()
    arguments.ParseFromString(request_proto)
    response = updateQuestTraceStatu_pb2.updateQuestTraceStatuResponse()
    
    characterId = arguments.id
    taskID = arguments.taskID
    traceStatu = arguments.traceStatu
    data = quest.updateQuestTraceStatu(dynamicId, characterId, taskID, traceStatu)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

#--------------------新版任务---------------

@nodeHandle
def TaskNpcTaskInfo_1410(dynamicId, request_proto):
    '''获取NPC的任务'''
    arguments = TaskNpcTaskInfoRequest1410_pb2.TaskNpcTaskInfoRequest()
    arguments.ParseFromString(request_proto)
    response = TaskNpcTaskInfoRequest1410_pb2.TaskNpcTaskInfoResponse()
    
    characterId = arguments.id
    NpcID = arguments.npc_id
    data = quest.TaskNpcTaskInfo(dynamicId, characterId, NpcID)
    response.result = True
    response.npc_id = data.get('npc_id',0)
    response.npc_img = data.get('npc_img',0)
    response.npc_name = data.get('npc_name',u'ERROR_%d'%NpcID)
    response.npc_word = data.get('npc_word','')
    taskResponse = response.ncp_task_item
    taskInfo = data.get('ncp_task_item')
    for _task in taskInfo:
        taskRes = taskResponse.add()
        _task.SerializationTaskInfo(taskRes)
    return response.SerializeToString()

@nodeHandle
def TaskNpcSubTask_1411(dynamicId, request_proto):
    '''提交任务'''
    arguments = TaskNpcSubTaskRequest1411_pb2.TaskNpcSubTaskRequest()
    arguments.ParseFromString(request_proto)
    response = TaskNpcSubTaskRequest1411_pb2.TaskNpcSubTaskResponse()
    
    characterId = arguments.id
    task_id = arguments.task_id
    npc_id = arguments.npc_id
    data = quest.TaskNpcSubTask(dynamicId, characterId, task_id, npc_id)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    
    response.task_id = data.get('task_id',1001)
    return response.SerializeToString()
    
@nodeHandle
def TaskNpcAcceptTask_1412(dynamicId, request_proto):
    '''接受NPC任务'''
    arguments = TaskNpcAcceptTaskRequest1412_pb2.TaskNpcAcceptTaskRequest()
    arguments.ParseFromString(request_proto)
    response = TaskNpcAcceptTaskRequest1412_pb2.TaskNpcAcceptTaskResponse()
    
    characterId = arguments.id
    task_id = arguments.task_id
    NpcID = arguments.npc_id
    data = quest.TaskNpcAcceptTask(dynamicId, characterId, task_id, NpcID)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    response.task_id = data.get('task_id',task_id)
    return response.SerializeToString()

@nodeHandle
def TaskExcuteTalk_1419(dynamicId, request_proto):
    '''任务交谈'''
    arguments = TaskExcuteTalkTaskRequest1419_pb2.TaskExcuteTalkTaskRequest()
    arguments.ParseFromString(request_proto)
    response = TaskExcuteTalkTaskRequest1419_pb2.TaskExcuteTalkTaskResponse()
    characterId = arguments.id
    task_id = arguments.task_id
    npc_id = arguments.npc_id
    data = quest.TaskExcuteTalk(dynamicId, characterId, task_id, npc_id)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def TaskPlayerAcceptTaskList_1417(dynamicId, request_proto):
    '''角色的可接任务列表'''
    arguments = TaskPlayerAcceptTaskListRequest1417_pb2.TaskPlayerAcceptTaskListRequest()
    arguments.ParseFromString(request_proto)
    response = TaskPlayerAcceptTaskListRequest1417_pb2.TaskPlayerAcceptTaskListResponse()
    
    characterId = arguments.id
    data = quest.TaskPlayerAcceptTaskList(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('tasks',None):
        taskList = data.get('tasks')
        for taskInfo in taskList:
            taskResponse = response.tasks.add()
            taskInfo.SerializationTaskInfo(taskResponse)
    return response.SerializeToString()

@nodeHandle
def TaskPlayerDropTask_1418(dynamicId, request_proto):
    '''放弃任务'''
    arguments = TaskPlayerDropTaskRequest1418_pb2.TaskPlayerDropTaskRequest()
    arguments.ParseFromString(request_proto)
    response = TaskPlayerDropTaskRequest1418_pb2.TaskPlayerDropTaskResponse()
    
    characterId = arguments.id
    task_id = arguments.task_id
    data = quest.TaskPlayerDropTask(dynamicId, characterId, task_id)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()
    
@nodeHandle
def TaskPlayerTaskList_1416(dynamicId, request_proto):
    '''获取已接任务列表'''
    arguments = TaskPlayerTaskListRequest1416_pb2.TaskPlayerHaveTaskListRequest()
    arguments.ParseFromString(request_proto)
    response = TaskPlayerTaskListRequest1416_pb2.TaskPlayerHaveTaskListResponse()
    
    characterId = arguments.id
    data = quest.TaskPlayerTaskList(dynamicId, characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('tasks',None):
        taskList = data.get('tasks',[])
        for taskInfo in taskList:
            taskResponse = response.tasks.add()
            taskInfo.SerializationTaskInfo(taskResponse)
    return response.SerializeToString()



