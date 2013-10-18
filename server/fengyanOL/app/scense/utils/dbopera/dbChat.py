#coding:utf8
'''
Created on 2011-9-24
聊天设置
@author: SIOP_09
'''
from app.scense.utils import dbaccess

tb_chat_astrict_name=None

def getBycharacter(characterid):
    '''更具角色id获取聊天设置信息'''
    sql="select * from tb_chat_astrict where characterid="+str(characterid)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    data={}
    if result:
        for i in range(len(tb_chat_astrict_name)):
            data[tb_chat_astrict_name[i]]=result[i]
    return data

#def getBycharacterid(characterid):
#    '''更具角色id获取聊天设置信息'''
#    sql="select * from tb_chat_astrict where characterid="+str(characterid)
#    cursor = dbaccess.dbpool.cursor()
#    cursor.execute(sql)
#    result = cursor.fetchone()
#    cursor.close()
#    if result:
#        for item in tb_chat_astrict_name:
#            if result[0]>0:
#            return True
#    return False


def getByTypeid(characterid,typeid):
    '''查看此种聊天类型是否有限制
    @param characterid: int 角色id
    @param typeid: int 1 系统信息 2提示信息  3全部 4队伍 5国 6私聊
    '''
    zd=""
    if typeid==1:
        zd='xt'
    elif typeid==2:
        zd='ts'
    elif typeid==3:
        zd='alls'
    elif typeid==4:
        zd='team'
    elif typeid==5:
        zd='jt'
    elif typeid==6:
        zd='sl'
        
    sql="select * from tb_chat_astrict where "+zd+"<1 "
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        if result[0]>0:
            return True
    return False
def updateTypeid(characterid,xt,ts,all,team,jt,sl):
    '''更改设置
    @param characterid: int 角色id
          剩下的依次是 系统 提示 全部 队伍 国 私聊 
    '''
    sql="update tb_chat_astrict set xt=%d,ts=%d,alls=%d,team=%d,jt=%d,sl=%d where characterid=%d"%(xt,ts,all,team,jt,sl,characterid)
    cursor = dbaccess.dbpool.cursor()
    count=cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def addset(characterid,xt,ts,all,team,jt,sl):
    '''添加
    @param characterid: int 角色id
        剩下的依次是 系统 提示 全部 队伍 国 私聊 
    '''
    sql="insert  into `tb_chat_astrict`(`characterid`,`team`,`ts`,`alls`,`jt`,`sl`,`xt`) values (%d,%d,%d,%d,%d,%d,%d);"%(characterid,xt,ts,all,team,jt,sl)
    cursor = dbaccess.dbpool.cursor()
    count=cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True

def getByCharacterid(characterid):
    '''查看是否存在此设置
    @param characterid: int 角色id
    '''
    sql="select count(*) from tb_chat_astrict where characterid="+str(characterid)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        if result[0]>0:
            return True
    return False

def CharByCharacter(characterid,xt,ts,all,team,jt,sl):
    '''添加
    @param characterid: int 角色id
        剩下的依次是 系统 提示 全部 队伍 国 私聊 
    '''
    xt1=0
    ts1=0
    all1=0
    team1=0
    jt1=0
    sl1=0
    if xt:
        xt1=1
    if ts:
        ts1=1
    if all:
        all1=1
    if team:
        team1=1
    if jt:
        jt1=1
    if sl:
        sl1=1
    if getByCharacterid(characterid): #如果存在此角色的限制
        return updateTypeid(characterid, xt1, ts1, all1, team1, jt1, sl1)
    else: #如果没有此角色的限制
        return addset(characterid, xt1, ts1, all1, team1, jt1, sl1)
    
    