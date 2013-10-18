#coding:utf8
'''
Created on 2012-5-3
日程表数据库操作
开服每日目标数据库操作
@author: Administrator
'''
from app.scense.utils import dbaccess,util
import datetime
from MySQLdb.cursors import DictCursor

SCHEDULE_CONFIG = {} #日程配置
SCHEDULE_BOUND = {}  #日程奖励

def getAllScheduleBound():
    '''获取所有日程奖励配置
    '''
    global SCHEDULE_BOUND
    sql = "SELECT * from tb_schedule_bound;"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for schedule_bound in result:
        SCHEDULE_BOUND[schedule_bound['bound_tag']] = schedule_bound
    

def getAllScheduleConfig():
    '''获取所有的日程进度
    '''
    global SCHEDULE_CONFIG
    sql = "SELECT * from tb_schedule_config;"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for schedule in result:
        SCHEDULE_CONFIG[schedule['schedule_tag']] = schedule

def insertTodaySchedule(characterId):
    '''加入角色今日进度
    @param characterId: int 角色的id
    '''
    sql = "insert into tb_schedule(characterId,scheduledate)\
     values(%d,current_date());"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getTodaySchedule(characterId):
    '''获取角色今日完成进度
    @param characterId: int 角色的id
    '''
    filedstr = "characterId,schedule_1,schedule_2,schedule_3,schedule_4,\
    schedule_5,schedule_6,schedule_7,schedule_8,schedule_9,schedule_10,schedule_11,schedule_12,\
    schedule_13,schedule_14,schedule_15,schedule_16,schedule_17,schedule_18,schedule_19,\
    schedule_20,scheduledate,activity,bound_1,bound_2,bound_3,bound_4"
    sql= "select %s from tb_schedule where datediff(scheduledate,current_date())=0\
     and characterId = %d;"%(filedstr,characterId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result
    insertTodaySchedule(characterId)
    return {'characterId':characterId,
            'schedule_1':0,'schedule_2':0,'schedule_3':0,'schedule_4':0,'schedule_5':0,
            'schedule_6':0,'schedule_7':0,'schedule_8':0,'schedule_9':0,'schedule_10':0,
            'schedule_11':0,'schedule_12':0,'schedule_13':0,'schedule_14':0,'schedule_15':0,
            'schedule_16':0,'schedule_17':0,'schedule_18':0,'schedule_19':0,'schedule_20':0,
            'scheduledate':datetime.date.today(),'activity':0,'bound_1':0,'bound_2':0,
            'bound_3':0,'bound_4':0}
    
def updateSchedule(characterId,props):
    '''更新角色日程进度
    @param characterId: int 角色的ID
    @param schedule_tag: int 进度标识
    @param props: dict 需要更新的值
    '''
    sql = "update `tb_schedule` set"
    sql = util.forEachUpdateProps(sql, props)
    sql += " where characterId = %d and datediff(scheduledate,current_date())=0;"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()




