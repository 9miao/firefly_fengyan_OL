#coding:utf8
'''
Created on 2012-5-7

@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.applyInterface import schedule
from app.scense.protoFile.schedule import GetCalendarTaskInfo_pb2
from app.scense.protoFile.schedule import ReceivedCalendarBound_pb2
from app.scense.protoFile.schedule import GetTargetInfo3203_pb2
from app.scense.protoFile.schedule import ObtainTargetReward3204_pb2

@nodeHandle
def GetCalendarTaskListInfo_3100(dynamicId, request_proto):
    '''获取日程信息'''
    argument = GetCalendarTaskInfo_pb2.GetCalendarTaskListInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetCalendarTaskInfo_pb2.GetCalendarTaskInfoResponse()
    characterId = argument.id
    data = schedule.GetCalendarTaskListInfo(characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        scheduleinfo = data.get('data')
        response.data.totalLivenessNum = scheduleinfo.get('activity',0)
        unfinishedlist = scheduleinfo.get('unfinishedlist')
        finishedlist = scheduleinfo.get('finishedlist')
        scheduleBound = scheduleinfo.get('scheduleBound')
        unfinishedresponse = response.data.unfinished
        finishedresponse = response.data.finished
        scheduleBoundresponse = response.data.scheduleBound
        for _schedule in unfinishedlist:
            unfinished = unfinishedresponse.add()
            unfinished.desc = _schedule.get('desc',u'').decode('utf8')
            unfinished.now = _schedule.get('now',0)
            unfinished.total = _schedule.get('total',0)
            unfinished.activity = _schedule.get('required',0)
        for _schedule in finishedlist:
            finished = finishedresponse.add()
            finished.desc = _schedule.get('desc',u'').decode('utf8')
            finished.now = _schedule.get('now',0)
            finished.total = _schedule.get('total',0)
            finished.activity = _schedule.get('required',0)
        for _bound in scheduleBound:
            bound = scheduleBoundresponse.add()
            bound.step = _bound.get('step',0)
            bound.received = _bound.get('received',0)
    return response.SerializeToString()

@nodeHandle
def ReceivedCalendarBound_3101(dynamicId, request_proto):
    '''领取日程奖励
    '''
    argument = ReceivedCalendarBound_pb2.ReceivedCalendarBoundRequest()
    argument.ParseFromString(request_proto)
    response = ReceivedCalendarBound_pb2.ReceivedCalendarBoundResponse()
    characterId = argument.id
    step = argument.step
    data = schedule.ReceivedCalendarBound(characterId, step)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()

@nodeHandle
def GetTargetInfo_3203(dynamicId,request_proto):
    '''获取所有的每日目标
    '''
    argument = GetTargetInfo3203_pb2.GetTargetInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetTargetInfo3203_pb2.GetTargetInfoResponse()
    characterId = argument.id
    data = schedule.GetTargetInfo(characterId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        alltargetlist = data.get('data')
        dayTaskInfo = response.dayTaskInfo
        for dayInfo in alltargetlist:
            daytarget = dayTaskInfo.add()
            daytarget.isSucFlag = dayInfo.get('isSucFlag',False)
            daytarget.isOpenFlag = dayInfo.get('isOpenFlag',False)
            dayListTaskInfo = daytarget.dayListTaskInfo
            for target in dayInfo.get('dayListTaskInfo',[]):
                targetinfo = dayListTaskInfo.add()
                targetinfo.taskId = target.get('taskId',0)
                targetinfo.isCompleteFlag = target.get('isCompleteFlag',False)
                targetinfo.icon = target.get('icon','0')
                targetinfo.taskDes = target.get('taskDes',u'').decode('utf8')
                targetinfo.isObtainFlag = target.get('isObtainFlag',False)
                rewardInfo = targetinfo.rewardInfo
                for _reward in target.get('rewardInfo',[]):
                    reward = rewardInfo.add()
                    reward.itemId = _reward.get('itemId',0)
                    reward.icon = _reward.get('icon',0)
                    reward.stack = _reward.get('stack',0)
                    reward.type = _reward.get('type',0)
                    reward.rewardType = _reward.get('rewardType',0)
    return response.SerializeToString()
                
@nodeHandle
def ObtainTargetReward_3204(dynamicId,request_proto):
    '''领取每日目标奖励'''
    argument = ObtainTargetReward3204_pb2.ObtainTargetRewardRequest()
    argument.ParseFromString(request_proto)
    response = ObtainTargetReward3204_pb2.ObtainTargetRewardResponse()
    characterId = argument.id
    taskId = argument.taskId
    data = schedule.ObtainTargetReward(characterId, taskId)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()
    
    