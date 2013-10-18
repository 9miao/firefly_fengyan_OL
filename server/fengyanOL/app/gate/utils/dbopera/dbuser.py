#coding:utf8
'''
Created on 2012-3-1

@author: sean_lan
'''
from app.gate.utils import dbaccess,util
from MySQLdb.cursors import DictCursor
import datetime

NEWCHARACTERMAIL = u"    欢迎加入Crota2的世界！\n"+\
            u"    如果您对我们的产品有任何意见或者建议，\
            请及时和我们联系，来信回复Email：GM@Crota2.com"
            
TITLE = u"欢迎加入Crota2的世界！"


def getUserInfo(id):
    '''获取用户角色关系表所有信息
    @param id: int 用户的id
    '''
    sql = "select * from tb_user_character where id = %d"%(id)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def checkUserPassword(username,password):
    '''检测用户名户密码
    @param username: str 用户的用户名
    @param password: str 用户密码
    '''
    sql = "select id from `tb_register` where username = '%s' and password = '%s'" %( username, password)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    id = 0
    if result:
        id = result[0]
    return id

def getUserInfoByUsername(username,password):
    '''检测用户名户密码
    @param username: str 用户的用户名
    @param password: str 用户密码
    '''
    sql = "select * from `tb_register` where username = '%s'\
     and password = '%s'" %( username, password)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def creatUserCharacter(uid):
    '''为新用户建立空的用户角色关系记录
    @param id: int 用户id
    '''
    sql = "insert into `tb_user_character` (`id`) values(%d)" %uid
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False

def updateUserCharacter(userId ,fieldname ,characterId):
    '''更新用户角色关系表
    @param userId: 用户的id
    @param fieldname: str 用户角色关系表中的字段名，表示用户的第几个角色
    @param characterId: int 角色的id
    '''
    sql = "update `tb_user_character` set %s = %d where id = %d"%(fieldname ,characterId ,userId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False
    
def InsertUserCharacter(userId,characterId):
    '''加入角色用户关系'''
    sql = "update tb_register set characterId = %d where `id` = %d"%( characterId ,userId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False
    
def getCharacterIdByName(nickname):
    '''根据角色名获取角色的Id
    @param nickname: str 角色的昵称
    '''
    sql = "select id from `tb_character` where nickname = '%s' " %( nickname)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    id = 0
    if result:
        id = result[0]
    return id

def checkCharacterName(nickname):
    '''检测角色名是否可用
    @param nickname: str 角色的名称
    '''
    sql = "SELECT `id` from tb_character where nickname = '%s'"%nickname
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return False
    return True

def creatNewCharacter(nickname ,profession ,userId,sex=1):
    '''创建新的角色
    @param nickname: str 角色的昵称
    @param profession: int 角色的职业编号
    @param userId: int 用户的id
    @param fieldname: str 用户角色关系表中的字段名，表示用户的第几个角色
    '''
    nowdatetime = str(datetime.datetime.today())
#    pp = profession
#    if profession>3:
#        pp= profession-3
    sql = "insert into `tb_character`(nickName,profession,sex,createtime) \
    values('%s',%d,%d,'%s')"%(nickname ,profession,sex,nowdatetime)
    sql2 = "SELECT @@IDENTITY"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.execute(sql2)
    result = cursor.fetchone()
    cursor.close()
    if result and count:
        characterId = result[0]
        InsertUserCharacter(userId,characterId)
#        addMail(TITLE, -1, u'系统', characterId, NEWCHARACTERMAIL, 0)
        return characterId
    else:
        return 0
    
def deleteUserCharacter(userId,fieldname,characterId):
    '''删除用户的角色
    @param userId: int 用户的id
    @param fieldname: str 用户角色关系表中的字段名，表示用户的第几个角色
    @param characterId: int 角色的id 
    '''
    
    result = updateUserCharacter(userId ,fieldname ,0)
    deleteRole(characterId)
    return result

def deleteRole(characterId):
    '''删除角色所有相关信息'''
    sql1 = "delete from `tb_equipment` where characterId = %d"%characterId
    sql2 = "delete from `tb_practice` where characterId = %d" % characterId
    sql3 = "delete from `tb_character_shop` where characterId = %d" % characterId
    sql4 = "delete from `tb_character_skillsetting` where characterId = %d"% characterId
    sql5 = "delete from `tb_character_rest` where characterId = %d" % characterId
    sql6 = "delete from `tb_character_lobby` where characterId = %d" % characterId
    sql7 = "delete from `tb_character` where id = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    count1 = cursor.execute(sql1)
    count2 = cursor.execute(sql2)
    count3 = cursor.execute(sql3)
    count4 = cursor.execute(sql4)
    count5 = cursor.execute(sql5)
    count6 = cursor.execute(sql6)
    count7 = cursor.execute(sql7)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count1 > 0 and count2 >0  and count3 >0 and count4>0\
        and count5>0 and count6>0 and count7>0):
        return True
    else:
        return False

def updateLastCharacter(characterId,userId):
    '''更新上次登录的角色
    @param characterId: int 角色的ID
    @param userId: int 角色的ID
    '''
    sql = "update `tb_user_character` set `last_character` = %d where id = %d"%(characterId ,userId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
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
    
def getUserCharacterInfo(characterId):
    '''获取用户角色列表的所需信息
    @param id: int 用户的id
    '''
    sql = "select town from tb_character where id = %d"%(characterId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def insertUserInfo(Uid):
    '''插入用户信息'''
    sql = "insert into tb_register(username,`password`) values ('%s','crotaii')"%(Uid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def CheckUserInfo(Uid):
    '''检测用户信息'''
    sql = "SELECT * from tb_register where username = '%s'"%Uid
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def getUser(Uid):
    '''获取角色信息'''
    userInfo = CheckUserInfo(Uid)
    if userInfo:
        return userInfo
    else:
        insertUserInfo(Uid)
    return CheckUserInfo(Uid)


def updateAllPlayersEnergy(energy):
    '''更新所有角色的活力
    '''
    sql = "update tb_character set energy = 200;"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False






