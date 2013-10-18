#coding:utf8
'''
Created on 2011-8-8

@author: lan
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
from app.scense.utils import util

LEVEL_MAIL = {}#所有等级的邮件提示

def getAllLevelMail():
    '''获取所有的等级邮件提示
    '''
    global  LEVEL_MAIL
    sql="SELECT * FROM tb_levelmail"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    scenesInfo = {}
    for scene in result:
        scenesInfo[scene['level']] = scene
    LEVEL_MAIL = scenesInfo
    return scenesInfo


def getPlayerMailCnd(characterId,type):
    '''获取角色邮件列表长度
    @param characterId: int 角色的ID
    @param type: int 邮件的分页类型
    '''
    cnd = 0
    if type ==0:
        cnd = getPlayerAllMailCnd(characterId)
    elif type ==1:
        cnd = getPlayerSysMailCnd(characterId)
    elif type ==2:
        cnd = getPlayerFriMailCnd(characterId)
    elif type ==3:
        cnd = getPlayerSavMailCnd(characterId)
    return cnd
    
def getPlayerAllMailCnd(characterId):
    '''获取玩家所有邮件的数量'''
    sql = "SELECT COUNT(`id`) FROM tb_mail WHERE receiverId = %d and isSaved = 0"%characterId
    #print sql
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result[0]

def getPlayerFriMailCnd(characterId):
    '''获取角色玩家邮件的数量'''
    sql = "SELECT COUNT(id) FROM tb_mail WHERE receiverId = %d AND `type`=1  and isSaved = 0"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result[0]

def getPlayerSysMailCnd(characterId):
    '''获取角色系统邮件数量'''
    sql = "SELECT COUNT(id) FROM tb_mail WHERE receiverId = %d AND `type`=0  and isSaved = 0"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result[0]

def getPlayerSavMailCnd(characterId):
    '''获取保存邮件的数量'''
    sql = "SELECT COUNT(id) FROM tb_mail WHERE receiverId = %d AND `isSaved`=1"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result[0]

def getPlayerMailList(characterId,mailType,page,limit = 7):
    '''获取角色邮件列表'''
    data = []
    if mailType ==0:
        data = getPlayerAllMailList(characterId, page, limit)
    elif mailType ==1:
        data = getPlayerSysMailList(characterId, page, limit)
    elif mailType ==2:
        data = getPlayerFriMailList(characterId, page, limit)
    elif mailType ==3:
        data = getPlayerSavMailList(characterId, page, limit)
    return data
    

def getPlayerAllMailList(characterId,page,limit):
    '''获取角色邮件列表
    @param characterId: int 角色的id
    '''
    filedList = ['id','title','type','isReaded','sendTime','content']
    sqlstr = ''
    sqlstr = util.forEachQueryProps(sqlstr, filedList)
    sql = "select %s from `tb_mail` where receiverId = %d  and isSaved = 0\
     order by isReaded ,sendTime desc LIMIT %d,%d"%(sqlstr,characterId,(page-1)*limit,limit)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = []
    for mail in result:
        mailInfo = {}
        for i in range(len(mail)):
            mailInfo[filedList[i]] = mail[i]
        data.append(mailInfo)
    return data

def getPlayerSysMailList(characterId,page,limit):
    '''获取角色邮件列表
    @param characterId: int 角色的id
    '''
    filedList = ['id','title','type','isReaded','sendTime','content']
    sqlstr = ''
    sqlstr = util.forEachQueryProps(sqlstr, filedList)
    sql = "select %s from `tb_mail` where receiverId = %d and `type`=0  and isSaved = 0\
     order by isReaded,sendTime desc LIMIT %d,%d "%(sqlstr,characterId,(page-1)*limit,limit)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = []
    for mail in result:
        mailInfo = {}
        for i in range(len(mail)):
            mailInfo[filedList[i]] = mail[i]
        data.append(mailInfo)
    return data

def getPlayerFriMailList(characterId,page,limit):
    '''获取角色邮件列表
    @param characterId: int 角色的id
    '''
    filedList = ['id','title','type','isReaded','sendTime','content']
    sqlstr = ''
    sqlstr = util.forEachQueryProps(sqlstr, filedList)
    sql = "select %s from `tb_mail` where receiverId = %d and `type`=1  and isSaved = 0\
     order by isReaded LIMIT %d,%d "%(sqlstr,characterId,(page-1)*limit,limit)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = []
    for mail in result:
        mailInfo = {}
        for i in range(len(mail)):
            mailInfo[filedList[i]] = mail[i]
        data.append(mailInfo)
    return data

def getPlayerSavMailList(characterId,page,limit):
    '''获取角色邮件列表
    @param characterId: int 角色的id
    '''
    filedList = ['id','title','type','isReaded','sendTime','content']
    sqlstr = ''
    sqlstr = util.forEachQueryProps(sqlstr, filedList)
    sql = "select %s from `tb_mail` where receiverId = %d and `isSaved`=1\
     order by isReaded LIMIT %d,%d "%(sqlstr,characterId,(page-1)*limit,limit)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = []
    for mail in result:
        mailInfo = {}
        for i in range(len(mail)):
            mailInfo[filedList[i]] = mail[i]
        data.append(mailInfo)
    return data

def checkMail(mailId,characterId):
    '''检测邮件是否属于characterId
    @param characterId: int 角色的ID
    @param mailId: int 邮件的ID
    '''
    sql = "SELECT `id` FROM tb_mail WHERE id = %d AND receiverId=%d"%(mailId,characterId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    return False

def getMailInfo(mailId):
    '''获取邮件详细信息'''
    sql = "select * from `tb_mail` where id = %d"%(mailId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result
    
def updateMailInfo(mailId,prop):
    '''更新邮件信息'''
    sql = 'update `tb_mail` set'
    sql = util.forEachUpdateProps(sql, prop)
    sql += " where id=%d" % mailId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False
    
def addMail(title,senderId,sender,receiverId,content,mailtype):
    '''添加邮件'''
    sql = "INSERT INTO tb_mail(title,senderId,sender,receiverId,\
    `type`,content,sendTime) VALUES ('%s',%d,'%s',%d,%d,'%s',\
    CURRENT_TIMESTAMP())"%(title,senderId,sender,receiverId,mailtype,content)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False
    
def deleteMail(mailId):
    '''删除邮件'''
    sql = "DELETE FROM tb_mail WHERE id = %d"%mailId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False
    
