#coding:utf8
'''
Created on 2012-5-3
每日目标的
@author: Administrator
'''
from app.scense.utils import dbaccess,util
from MySQLdb.cursors import DictCursor
import datetime

ALL_DAILY = {}
DAILY_INDEX = {}

def getDailyForToday(dailytype,createtime):
    '''获取符合今日的目标
    '''
    thisdate = datetime.date.today()
    daysdelta = (createtime.date()-thisdate).days+1
    dailylist = []
    for daily in ALL_DAILY.values():
        if daysdelta <= daily['dateindex'] and daily['dailytype']==dailytype:
            dailylist.append(daily)
    return dailylist

def getDailyForDateindex(dateindex):
    '''根据日期序号获取目标列表'''
    dailylist = [daily for daily in ALL_DAILY.values() if daily['dateindex']==dateindex]
    return dailylist

def getAllDaily():
    '''获取所有的每日目标
    '''
    global ALL_DAILY,DAILY_INDEX
    sql = "SELECT * from tb_dailygoal;"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for daily in result:
        ALL_DAILY[daily['id']] = daily
        dateindex = daily['dateindex']
        if not DAILY_INDEX.has_key(dateindex):
            DAILY_INDEX[dateindex] = []
        DAILY_INDEX[dateindex].append(daily)
        

def insertCharacterDaily(characterId,dailyId):
    '''插入角色目标记录
    @param characterId: int 角色的ID
    @param dailyId: int 每日目标的ID
    '''
    sql = "insert into tb_character_daily(characterId,dailyId) values (%d,%d);"%(characterId,dailyId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getCharacterAllDaily(characterId):
    '''获取角色所有的每日目标记录
    @param characterId: int 角色的id
    '''
    sql = "SELECT * from tb_character_daily where characterId = %d;"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def updateCharacterDaily(characterId,dailyId,props):
    '''更新角色目标记录
    @param characterId: int 角色的id
    @param dailyId: int 每日目标的ID
    @param current: int 当前进度
    '''
    sql = "update `tb_character_daily` set"
    sql = util.forEachUpdateProps(sql, props)
    sql += " where characterId = %d and dailyId = %d;"%(characterId,dailyId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    
    
    
    





