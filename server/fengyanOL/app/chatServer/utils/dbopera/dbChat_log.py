#coding:utf8
'''
Created on 2011-11-29
私聊聊天记录
@author: SIOP_09
'''
from app.chatServer.utils import dbaccess
from MySQLdb.cursors import DictCursor
dbaccess=dbaccess

def getChatByid(fid,tid):
    '''获取两人私聊信息
    @param fid: int 其中一人id
    @param tid: int 另一个角色id
    '''
    
    gdid=0
    if fid>tid: #保证fid比tid小
        gdid=fid
        fid=tid
        tid=gdid
        
    sql="SELECT * FROM tb_friend_chat_log WHERE fromid="+str(fid)+" AND toid="+str(tid)+" AND (DATE_ADD(times, INTERVAL 24 HOUR)>= CURRENT_TIMESTAMP) ORDER BY times"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if not data:
        return None
    return data

def getCount(fid,tid):
    '''获取聊天条数
    @param fid: int 其中一人角色id
    @param tid: int 另一个角色id 
    '''
    sql="SELECT count(*) FROM tb_friend_chat_log WHERE ((fromid="+str(fid)+" AND toid="+str(tid)+" )OR (fromid="+str(tid)+" AND toid="+str(fid)+")) AND (DATE_ADD(times, INTERVAL 24 HOUR)>= CURRENT_TIMESTAMP) ORDER BY times"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if not data:
        return None
    return data[0]

def delChat(fid,tid):
    '''删除过时信息
    @param fid: int 角色id
    @param tid: int 角色id
    '''
    sql="DELETE FROM tb_friend_chat_log WHERE ((fromid="+fid+" AND toid="+tid+") OR (fromid="+tid+" AND toid="+fid+")) AND (DATE_ADD(times, INTERVAL 24 HOUR)< CURRENT_TIMESTAMP) ORDER BY times"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False

def delAllChat():
    '''删除所有过时信息'''
    sql="DELETE FROM tb_friend_chat_log WHERE DATE_ADD(times, INTERVAL 24 HOUR)< CURRENT_TIMESTAMP"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False