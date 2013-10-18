#coding:utf8
'''
Created on 2011-6-14

@author: lan
'''
from app.scense.utils import dbaccess,util
from MySQLdb.cursors import DictCursor
import datetime

all_TaskTemplate = {}
ALL_MAIN_TASK = {}#所有的主线任务
ALL_EXTEN_TASK = {}#所有的支线任务

#-------------------------主线任务------------------------
def getAllMainTask():
    '''获取所有的主线任务'''
    sql = "SELECT * FROM tb_task_main where taskID < 20000;"
    cursor = dbaccess.dbpool.cursor(cursorclass = DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data = {}
    for taskInfo in result:
        data[taskInfo['taskID']] = taskInfo
    return data

def getAllExtedTask():
    '''获取所有的支线任务'''
    sql = "SELECT * FROM tb_task_main where taskID > 20000"
    cursor = dbaccess.dbpool.cursor(cursorclass = DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data = {}
    for taskInfo in result:
        data[taskInfo['taskID']] = taskInfo
    return data

def InitMainTaskRecord(characterId):
    '''添加角色的主线任务记录
    @param characterId: int 角色的ID
    '''
    nowtime = datetime.datetime.now()
    sql = "INSERT INTO tb_task_main_record(characterId,applyTime) VALUES (%d,'%s')"\
    %(characterId,str(nowtime))
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False

def getMainTaskRecord(characterId):
    '''获取角色的主线任务记录
    @param characterId: int 角色的ID
    '''
    sql = "SELECT mainRecord,status FROM tb_task_main_record WHERE characterId = %d"\
    %characterId
    cursor = dbaccess.dbpool.cursor(cursorclass = DictCursor)
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result

def updateMainTaskRecord(characterId,props):
    '''更新角色的主线任务记录'''
    sql = "UPDATE tb_task_main_record SET "
    sql = util.forEachUpdatePropsForIncrement(sql, props)
    sql += " where characterId=%d " %(characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False

def InsertTaskProcess(characterId,taskID,trackStatu = 1):
    '''添加任务进度信息
    @param characterId: int 角色的id
    @param taskID:  int 任务的id
    '''
    sql = "INSERT INTO tb_task_process(taskId,characterId,trackStatu) VALUES(%d,%d,%d)"\
    %(taskID,characterId,trackStatu)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False
    
def UpdateTaskProcess(characterId,taskID,props):
    '''更新任务的进度'''
    sql = "UPDATE tb_task_process SET "
    sql = util.forEachUpdatePropsForIncrement(sql, props)
    sql += " where characterId=%d and taskId =%d" %(characterId,taskID)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False

def getTaskProcess(characterId,taskID):
    '''获取任务进度
    @param characterId: int 角色的id
    @param taskID: int 任务的ID
    '''
    sql = "SELECT * FROM tb_task_process WHERE taskId = %d AND characterId = %d"\
    %(taskID,characterId)
    cursor = dbaccess.dbpool.cursor(cursorclass = DictCursor)
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result

def DelTaskProcessInfo(characterId,taskID):
    '''删除任务进度信息
    @param characterId: int 角色的id
    @param taskID: int 任务的ID
    '''
    sql = "DELETE FROM tb_task_process WHERE taskId = %d AND characterId = %d"\
    %(taskID,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False

def getAllTaksProcessInfo(characterId):
    '''获取所有的在进行中的任务的列表
    @param characterId: int 角色的id
    '''
    sql = "SELECT * FROM tb_task_process WHERE  characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass = DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    return result

def getAllProcessInfo(characterId):
    '''获取所有的在进行中的任务的列表
    @param characterId: int 角色的id
    '''
    sql = "SELECT * FROM tb_task_process WHERE  characterId = %d "%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass = DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    return result

def getAllFinished(characterId):
    '''获取所有已经完成了的任务'''
    sql = "SELECT taskId FROM tb_task_process WHERE \
    characterId = %d and finished = 1"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    return [process[0] for process in result]

#---------------------------支线任务------------------

def getAllTaskInfo():
    '''获取所有的任务信息'''
    sql = "SELECT * FROM tb_task_info "
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data = {}
    for taskInfo in result:
        data[taskInfo['id']] = taskInfo
    return data

def getTaskInfoByID(taskID):
    '''根据任务ID获取任务信息'''
    sql = "SELECT * FROM tb_task_info WHERE id = %d "%taskID
    cursor = dbaccess.dbpool.cursor(cursorclass = DictCursor)
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result


#-----------------------*-----以下是老版本的任务-----*--------------------
def getTaskListInMap(senceId):
    '''获取场景中的任务列表
    @param senceId: int 任务的id
    '''
    sql = "SELECT * FROM `tb_task_info` WHERE vestmap = %d"%senceId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    return result

def getHasCommitQuestList(characterId):
    sql = "SELECT `taskId` FROM `tb_task_record` where characterId = %d and status=1"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    RecordList = [taskId[0] for taskId in result]
    return RecordList

def getQuestRecord( characterId):
    '''获取已经完成任务记录'''
    sql = "SELECT `taskId` FROM `tb_task_record` where characterId = %d "%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    RecordList = [taskId[0] for taskId in result]
    return RecordList

def getQuestOngoingCount(characterId):
    '''获取正在进行的任务数目'''
    sql = "SELECT count(id) FROM `tb_task_record` where characterId = %d and status != 1"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    return result[0]

def getQuestRecordInfoById(characterId,taskId):
    '''获取正在进行的人的信息'''
    sql = "SELECT * FROM `tb_task_record` where characterId = %d and\
     questtemplateId = %d and status != 1"%(characterId,taskId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    return result

def getQuestOngoingInfoList(characterId):
    '''获取正在进行的人的信息'''
    sql = "SELECT * FROM `tb_task_record` where characterId = %d and status != 1"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    return result

    
def updateQuestRecord(characterId,taskId,props):
    '''更新角色任务记录
    @param characterId: int 角色的id
    @param taskId: int 任务的id
    '''
    sql = 'update `tb_task_record` set '
    sql = util.forEachUpdateProps(sql, props)
    sql += " where taskId=%d and characterId = %d" %(taskId,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False

def getLastTaskRecordId():
    '''获取最后一条任务记录的id
    '''
    sql = "SELECT * FROM tb_task_record WHERE id = LAST_INSERT_ID()"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result[0]

def insertQuestRecord(characterId,taskInfo):
    '''插入任务记录
    @param characterId: int 角色的id
    @param taskId: int 任务的id
    '''
    sql = "INSERT INTO `tb_task_record`(taskId,characterId)\
     VALUES (%d,%d);"%(taskInfo['id'],characterId)
    sql2 = "SELECT @@IDENTITY"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.execute(sql2)
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return False
    recordId = result[0]
    stepList = eval("["+taskInfo['steps']+"]")
    goalList = []
    for step in stepList:
        goalList.append(selectQuestGoalIdById(step))
    for goal in goalList:
        insertQuestGoal(recordId,goal[0])
    return True

def getQuestByTemplateId(characterId,taskId):
    '''根据任务的模板id以及角色的id获取任务记录id'''
    sql = "SELECT `id` FROM tb_task_record WHERE \
    characterId = %d AND taskId = %d"%(characterId,taskId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    if not result:
        return 0
    return result[0]

def getQuestGoalprocessInfo(questtemplateId):
    '''更加任务的id获取任务目的进度信息'''
    sql = "SELECT * FROM tb_task_goal_progress WHERE questRecordId = %d"%questtemplateId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data = []
    fieldList = ['id','questRecordId','questGoalId',
                 'talkCount','killCount','useCount','collectCount','qualityLevel']
    for info in result:
        processInfo = {}
        for i in range(len(fieldList)):
            processInfo[fieldList[i]] = info[i]
        data.append(processInfo)
    return data

    
def getCollectionQuestItemCount(characterId,itemTemplateId):
    '''获取任务收集物品的数量
    @param characterId: int 角色的id
    @param itemTemplateId: int 物品的模板的id
    '''
    sql = "SELECT SUM(a.stack) FROM tb_package a,tb_item b WHERE\
     a.itemId = b.id AND a.characterId =%d \
    AND b.itemTemplateId = %d"%(characterId,itemTemplateId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    if result:
        return result[0]
    return 0
    
def selectQuestGoalIdById(goalId):
    '''根据任务的id获取任务的目的id
    @param taskId: int 任务的id
    '''
    sql = "SELECT * FROM tb_task_goal WHERE id = %d"%(goalId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result

def selectQuestGoalIdByTaskId(taskId):
    '''根据任务ID获取任务目的表'''
    sql = "SELECT steps FROM tb_task_info WHERE `id`=%d"%taskId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    stepList = eval("["+result[0]+"]")
    goalList = []
    for step in stepList:
        goalList.append(selectQuestGoalIdById(step))
    return goalList
    

def selectQuestFailCondition(taskId):
    '''获取指定任务的失败条件
    @param taskId: int 任务的id
    '''
    sql = "SELECT * FROM tb_task_fail WHERE taskId = %d"%taskId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result
    
    
def insertQuestGoal(taskRecordId,goalId):
    '''插入任务目标记录
    @param characterId: int 角色的id
    @param goalId: int 任务的目标id
    @param taskId: int 任务的id 
    '''
    sql = "INSERT INTO tb_task_goal_progress(questRecordId,\
    questGoalId) VALUES (%d,%d)"%(taskRecordId,goalId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False
    
def updateQuestGoal(questRecordId,questGoalId,props,limitprops= {}):
    '''更新角色任务进度
    @param characterId: int 角色的id
    @param taskId: int 任务的id
    '''
    sql = 'update `tb_task_goal_progress` set'
    sql = util.forEachUpdatePropsForIncrement(sql, props)
    sql += " where questRecordId=%d and questGoalId = %d" %(questRecordId,questGoalId)
    sql = util.produceSQLlimit(sql, limitprops)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False
    
def delQuestRecord(taskId,characterId):
    '''放弃任务时删除任务记录'''
    sql = "DELETE FROM tb_task_record WHERE questtemplateId\
     = %d AND characterId =%d"%(taskId,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    taskRecordId = getQuestByTemplateId(characterId,taskId)
    if taskRecordId:
        delQuestGoalRecord(taskRecordId)
    if count:
        return True
    return False

def delQuestGoalRecord(taskRecordId):
    '''删除任务进度记录
    @param taskRecordId: int 任务记录的id
    ''' 
    sql = "DELETE FROM tb_task_goal_progress WHERE questRecordId = %d"%taskRecordId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False

def getQuestFilishedInfo(taskId):
    '''获取任务完成后的信息'''
    sql = "SELECT * FROM tb_task_finish WHERE TaskID= %d"%taskId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result
    
def getTrackTaskCount(characterId):
    '''获取角色已经追踪的任务状态'''
    sql = "SELECT COUNT(id) FROM tb_task_record WHERE characterId = %d AND trackStatu = 1"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return 0
    
    
    