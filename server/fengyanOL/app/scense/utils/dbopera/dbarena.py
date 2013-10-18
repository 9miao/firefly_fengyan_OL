#coding:utf8
'''
Created on 2012-7-1
竞技场信息
@author: Administrator
'''
from app.scense.utils import dbaccess,util
from MySQLdb.cursors import DictCursor
import datetime

def getCharacterArenaInfo(characterId):
    '''获取角色竞技场信息
    @param characterId: int 角色的ID
    '''
    sql = "SELECT * FROM tb_arena where characterId =%d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if not result:
        insertCharacterArenaInfo(characterId)
        result = {'characterId':characterId,'score':0,'liansheng':0,
                  'lastresult':0,'lasttime':datetime.datetime(2012,6,20,12),
                  'ranking':0,'surplustimes':15,'buytimes':0,'receive':0,
                  'recorddate':datetime.date.today()}
    return result  

def insertCharacterArenaInfo(characterId):
    '''插入角色竞技场信息
    '''
    datestr = datetime.date.today()
    sql = "insert into tb_arena(characterId,recorddate,ranking)\
     values(%d,'%s',%d)"%(characterId,datestr,characterId-1000000)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    
def updateCharacterArenaInfo(characterId,props):
    '''更新角色的竞技场信息
    '''
    sqlstr = "update `tb_arena` set"
    sqlstr = util.forEachUpdateProps(sqlstr, props)
    sqlstr += " where characterId = %d" % characterId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sqlstr)
    dbaccess.dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False
    
def getCharacterArenaRank(characterId):
    '''获取角色的排名
    '''
    sql = "SELECT ranking from tb_arena where characterId = %d;"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    else:
        return 0
    
def getCharacterRivalList(ranklist):
    '''获取角色的对手列表
    '''
    orsql = util.forEachSelectORByList('b.ranking', ranklist)
    if orsql:
        sql = "SELECT b.characterId,b.ranking,\
        a.nickname,a.level,a.profession from tb_character as a,\
        tb_arena as b where a.id=b.characterId and (%s) order by `ranking`;"%(orsql)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
def getCharacterBattleLog(characterId):
    '''获取角色战斗日志
    '''
    sql = "SELECT * from tb_arena_log where tiaozhan = %d \
    or yingzhan = %d order by recordtime desc limit 0,5;"%(characterId,characterId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
def insertBattleLog(characterId,tocharacterId,fname,tname,success,rankingChange):
    '''插入战斗日志
    '''
    sql = "insert into tb_arena_log(tiaozhan,yingzhan,\
    tiaozhanname,yingzhanname,success,rankingChange)\
     values(%d,%d,'%s','%s',%d,%d)"%(characterId,\
                                     tocharacterId,fname,tname,success,rankingChange)
    
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    
    
    
    
    
    
    