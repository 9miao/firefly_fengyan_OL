#coding:utf8
'''
Created on 2011-9-13
行会（国）数据库处理
@author: lan
'''
from app.scense.utils import dbaccess
from app.scense.utils import util
from MySQLdb.cursors import DictCursor
import datetime
from app.scense.core.language.Language import Lg

lEVEL_TECHNOLOGY = {} #国等级对科技的等级的限制
All_TECHNOLOGY = {}#所有的国科技


def getAllGuildInfo():
    '''获取所有的国信息
    '''
    sql = "SELECT a.*, b.nickname as presidentname FROM tb_guild a ,\
    tb_character b WHERE  b.id = a.president"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getAllSysGuildInfo():
    '''获取系统国信息
    '''
    sql = "SELECT * FROM tb_guild  WHERE  guildtype=1"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for guild in result:
        guild['presidentname'] = getCharacterNameByID(guild['president'])
    return result

def getTechnologyLimit():
    '''获取科技等级限制条件'''
    global lEVEL_TECHNOLOGY
    sql = "SELECT * FROM tb_guildlevel_technology "
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for levellimit in result:
        lEVEL_TECHNOLOGY[levellimit['guildLevel']] = levellimit
    

def getTop100ByName(name,typeid):
    '''根据国名字获取排行
    @param name:int 国名称
    @param typeid: 1国等级 2国实力 
    '''
    sw=""
    od=""
    if typeid==1:
        sw="(g.level*g.memberCount+10)as er "
        od=" g.level desc,g.emblemLevel desc,g.id desc "
    elif typeid==2:
        sw="(g.level*g.memberCount)AS tt"
        od=" g.level*g.memberCount DESC,g.id desc"
        
    flist=['topnum','id','name','nickname','level','other']
    cursor = dbaccess.dbpool.cursor()
    cursor.nextset()
    cursor.execute("CALL getTopGuild('"+sw+"','"+od+"','"+str(name)+"')")
    result1=cursor.fetchall() #当前页的信息
    cursor.close()
    if not result1:
        return None
    dt=[]
    for item in result1:
        data={} #存放一条数据
        for i in range(len(flist)):
            if flist[i]=='nickname':
                if not item[i]:
                    data[flist[i]]=Lg().g(143)
                    continue
            data[flist[i]]=item[i]
        dt.append(data)
    
    if len(dt)<1:
        return None
    return dt

def getTop100(typeid):
    '''获取国等级前10名排行
    @param typeid: 1国等级 2国实力
    '''
    sw=""
    od=""
    if typeid==1:
        sw="(g.level*g.memberCount+10)as er "
        od=" order by g.level desc,g.id "
    elif typeid==2:
        sw="g.level*g.memberCount"
        od=" order by g.level*g.memberCount desc,g.id"
        
    flist=['cid','id','name','nickname','level','other']
    
    sql="SELECT c.id, g.id,g.name,c.nickname,g.level,"+sw+" FROM tb_guild AS g LEFT JOIN tb_character as c on c.id=g.president   "+od+" "
    sql+=" limit 0,10"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    cursor.close()
    if not result1:
        return None
    dt=[]
    for item in result1:
        data={} #存放一条数据
        for i in range(len(flist)):
            if flist[i]=='nickname':
                if not item[i]:
                    data[flist[i]]=Lg().g(143)
                    continue
            data[flist[i]]=item[i]
        dt.append(data)
    
    if len(dt)<1:
        return None
    return dt



def getTopAll(typeid):
    '''获取国排名
    @param typeid: 1国等级 2国实力
    '''
    od=""
    if typeid==1:
        od=" order by g.level desc,g.id "
    elif typeid==2:
        od=" order by g.level*g.memberCount desc,g.id"
    
    sql="SELECT c.id FROM tb_guild AS g LEFT JOIN tb_character as c on c.id=g.president   "+od+" "
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    cursor.close()
    return result1
    
def getCharacterGuild(characterId):
    '''获取角色行会信息'''
    sql = "SELECT *FROM tb_guild_character WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def creatGuild(guildName,president,camp):
    '''创建一个行会'''
    nowDate = str(datetime.date.today())
    sql = "INSERT INTO tb_guild(`name`,bugle,camp,president,creator,createDate) \
    VALUES('%s','%s',%d,%d,%d,'%s')"%(guildName,guildName[0],camp,\
                                      president,president,nowDate)
    sql2 = "SELECT @@IDENTITY"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.execute(sql2)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return 0
    
def getAllGuildID():
    '''获取所有行会的id'''
    sql = "SELECT id FROM tb_guild"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def insertCharacterGuildInfo(characterId,guildId,post=0):
    '''插入角色行会关系
    @param characterId: int 角色的id
    @param guildId: int 行会的id
    @param post: 行会职务 默认 0 普通成员
    '''
    nowDate = str(datetime.date.today())
    sql = "INSERT INTO tb_guild_character(characterId,guildId,post,joinTime)\
     VALUES (%d,%d,%d,'%s')"%(characterId,guildId,post,nowDate)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def updateCharacterGuildInfo(characterId,prot):
    '''更新角色的行会关系表'''
    sql = 'update `tb_guild_character` set'
    sql = util.forEachUpdateProps(sql, prot)
    sql += " where characterId = %d" % characterId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def modifyDefaultDonate(characterId,technologyId):
    '''修改角色行会科技捐献设置
    @param characterId: int 角色的id
    @param technologyId: int 科技的id
    '''
    sql = "UPDATE tb_guild_character SET defaultDonate = %d WHERE \
    characterId = %d"%(technologyId,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def deleteCharacterGuildRelation(characterId):
    '''删除角色行会关系'''
    sql = "DELETE FROM tb_guild_character WHERE characterId = %d"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getGuildInfoById(guildId):
    '''获取行会信息
    @param guildId: int 行会的id
    '''
    sql = "SELECT a.*, b.nickname as presidentname FROM tb_guild a ,tb_character b WHERE\
     b.id = a.president AND a.id = %d"%(guildId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    curMenberNum = countGuildMenberNum(guildId)
    if result:
        result['curMenberNum'] = curMenberNum
    return result

def getGuildInfo(guildId):
    '''获取国基础信息
    @param guildId: int 行会的id
    '''
    sql = "SELECT * FROM tb_guild  WHERE `id` = %d"%(guildId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def countGuildMenberNum(guildId):
    '''获取行会当前成员数量
    @param guildId: int 行会的id
    '''
    sql = "SELECT count(id) FROM `tb_guild_character` WHERE guildId = %d"%guildId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result[0]

def countSearchMemberNum(guildId,searchCriteria):
    '''获取搜索到的成员的数量'''
    sql = "SELECT count(a.id) FROM tb_guild_character a,tb_character b WHERE\
     guildId = %d AND a.characterId=b.id AND b.nickname\
      LIKE '%%%s%%'"%(guildId,searchCriteria)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result[0]

def countSearchApplyerNum(guildId,searchCriteria):
    '''获取行会成员列表'''
    sql = "SELECT count(a.id) FROM tb_guild_app a,tb_character b WHERE\
     a.guildID = %d AND a.applicant=b.id AND b.nickname LIKE '%s'"%\
     (guildId,searchCriteria)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result[0]
    
def updateGuildInfo(guildId, attrs):
    '''修改玩家信息'''
    sql = 'update `tb_guild` set'
    sql = util.forEachUpdateProps(sql, attrs)
    sql += " where id=%d" % guildId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    else:
        return False

def getGuildMemberInfo(guildId,index,limit):
    '''获取行会成员列表
    '''
    sql = "SELECT a.*,b.nickname,b.outtime,b.isOnline,b.level,b.profession FROM tb_guild_character a,tb_character b WHERE\
     guildId = %d AND a.characterId=b.id LIMIT %d,%d"%(guildId,(index-1)*limit,limit)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGuildMemberIdList(guildId):
    ''' 获取行会成员id列表
    @param guildId: int 行会的id
    '''
    sql = "SELECT characterId FROM tb_guild_character WHERE guildId = %d"%guildId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return [character[0] for character in result]
    
def searchGuildMemberInfo(guildId,searchCriteria,curPage,limit):
    '''搜索行会成员名称'''
    sql = "SELECT a.*,b.nickname,b.outtime,b.isOnline,b.level,b.profession FROM tb_guild_character a,tb_character b WHERE\
     guildId = %d AND a.characterId=b.id AND b.nickname\
      LIKE '%%%s%%' limit %d,%d"%(guildId,searchCriteria,(curPage-1)*limit,limit)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
def applyJoinGuild(characterId,guildId):
    '''申请加入行会'''
    nowDate = str(datetime.date.today())
    sql = "INSERT INTO tb_guild_app(guildId,applicant,appTime)\
     VALUES (%d,%d,'%s')"%(guildId,characterId,nowDate)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def checkHasApply(guildId,characterId):
    '''检查角色是否有指定行会的申请记录
    @param guildId: int 行会的id
    @param characterID: int 角色的id
    '''
    sql = "SELECT COUNT(id) FROM tb_guild_app WHERE guildID = %d AND applicant = %d"%(guildId,characterId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result and result[0]:
        return True
    return False

def checkCharacterHasGuild(characterId):
    '''检查角色是否加入行会
    @param characterId: int 角色的id
    '''
    sql = "SELECT COUNT(id) FROM tb_guild_character WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result and result[0]:
        return True
    return False

def checkCharacterInGuild(characterId,guildId):
    '''检测角色是否在指定的行会中
    @param characterId: int 角色的id
    @param guildId: int 行会的id
    '''
    sql = "SELECT COUNT(id) FROM tb_guild_character WHERE characterId=%d AND guildId=%d"%(characterId,guildId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result and result[0]:
        return True
    return False

def getApplyJoinGuildList(guildId,index,limit):
    '''获取申请加入行会的列表'''
    sql = "SELECT a.*, b.nickname,b.level,b.profession FROM tb_guild_app a,tb_character b WHERE\
     a.guildID = %d AND a.applicant=b.id LIMIT %d,%d"%(guildId,(index-1)*limit,limit)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def searchApplyJoinGuildInfo(guildId,searchCriteria,curPage,limit=10):
    '''搜索行会申请信息
    @param guildId: int 行会的id
    @param searchCriteria: str 搜索条件
    '''
    sql = "SELECT a.*, b.nickname,b.level,b.profession FROM tb_guild_app a,tb_character b WHERE\
     a.guildID = %d AND a.applicant=b.id AND b.nickname LIKE '%%%s%%' limit %d,%d"%\
     (guildId,searchCriteria,(curPage-1)*limit,limit)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def countGuildApplyNum(guildId):
    '''获取行会申请条目数量
    @param guildId: int 行会的id
    '''
    sql = "SELECT count(id) FROM `tb_guild_app` WHERE guildID = %d"%guildId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result[0]

def deleteApplyJoinGuildRecord(recoredID):
    '''删除申请记录
    @param recoredID: int 记录的id
    '''
    sql = "DELETE FROM tb_guild_app WHERE id = %d"%recoredID
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def delGuildApplyJoinRecord(guildId,characterId):
    '''删除申请记录
    @param recoredID: int 记录的id
    '''
    sql = "DELETE FROM tb_guild_app WHERE guildID = %d and applicant=%d"%(guildId,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def delCharacterAllApply(characterId):
    '''删除角色所有的申请记录
    @param characterId: int 角色的id
    '''
    sql = "DELETE FROM tb_guild_app WHERE  applicant=%d"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def checkHasGuildByName(guildname):
    '''检测行会名是否重复'''
    sql = "SELECT id FROM tb_guild WHERE `name` ='%s'"%guildname
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    return False

def searchGuildByName(characterId,searchCriteria,curPage,limit):
    '''根据行会名称获取行会信息
    @param characterId: int 角色的id
    @param searchCriteria: str 搜索的关键字
    '''
    sql = "SELECT a.*, b.nickname,b.isOnline FROM tb_guild a ,\
    tb_character b WHERE b.id = a.president AND \
    (a.name LIKE '%%%s%%' OR b.nickname LIKE '%%%s%%')\
     limit %d,%d;"%(searchCriteria,searchCriteria,(curPage-1)*limit,limit)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    guildInfo = []
    for guild in result:
        info = guild
        curMenberNum = countGuildMenberNum(info['id'])
        info['onApplication'] = checkHasApply(info['id'],characterId)
        info['curMenberNum'] = curMenberNum
        guildInfo.append(info)
    return guildInfo

def getGuildInfoByID(characterId,guildId):
    '''根据行会名称获取行会信息
    @param characterId: int 角色的id
    @param guildId: str 行会的ID
    '''
    sql = "SELECT a.*, b.nickname FROM tb_guild a ,\
    tb_character b WHERE b.id = a.president AND a.id = %d"%(guildId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        curMenberNum = countGuildMenberNum(result['id'])
        result['onApplication'] = checkHasApply(result['id'],characterId)
        result['curMenberNum'] = curMenberNum
    return result
    
def getGuildInfoList(characterId,curPage,limit):
    '''获取行会列表
    @param characterId: int 角色的id
    @param curPage: int 当前页数
    @param limit: int 每页显示条目 
    '''
    if curPage==0:
        curPage=1
    sql = "SELECT a.*, b.nickname,b.isOnline FROM tb_guild a ,tb_character b WHERE\
     b.id = a.president ORDER BY b.isOnline DESC,`level` DESC LIMIT %d,%d"%((curPage-1)*limit,limit)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    guildInfo = []
    for guild in result:
        info = guild
        curMenberNum = countGuildMenberNum(info['id'])
        info['onApplication'] = checkHasApply(info['id'],characterId)
        info['curMenberNum'] = curMenberNum
        guildInfo.append(info)
#    guildInfo.sort(key=lambda d: d['curMenberNum'],reverse=True)
    return guildInfo
     
def TransferCorps(guildId,operator,memberId):
    '''移交国长
    @param operator: int 角色的操作者的id
    @param memberId: int 被操作的id
    '''
    dbpool = dbaccess.dbpool
    cursor = dbpool.cursor()
    sql1= "UPDATE tb_guild SET president =%d WHERE id = %d"%(memberId,guildId)
    count1 = cursor.execute(sql1)
    dbpool.commit()
    cursor.close()
    if count1:
        return True
    return False

     
def insertBattleApply(guildId,toGuildID):
    '''添加一条战斗申请记录
    @param guildId: int 申请行会的id
    @param toGuildID: int 目标行会的id
    '''
    nowDate = str(datetime.date.today())
    sql = "INSERT INTO tb_guild_battle(askCommunity,answerCommunity,askTime,confirmdTime)\
     VALUES(%d,%d,'%s','%s')"%(guildId,toGuildID,nowDate,nowDate)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def checkCanApplyBattle(guildId):
    '''检测行会是否能申请国战'''
    sql = "SELECT COUNT(id) FROM tb_guild_battle WHERE\
     (askCommunity=%d OR answerCommunity=%d) AND result !=0"%(guildId,guildId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result and result[0]:
        return False
    return True

def getCharacterNameByID(characterId):
    '''根据id获取角色的名称
    @param characterId: int 角色的id
    '''
    sql = "SELECT nickname FROM tb_character WHERE id = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return ''

def getAllTechnology():
    '''获取所有的科技'''
    global All_TECHNOLOGY
    sql = "SELECT * FROM tb_technology"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for technology in result:
        All_TECHNOLOGY[technology['technology']] = technology
        
def guilGuildTechnologylist(guildId):
    '''获取国科技列表'''
    sql = "SELECT technology,curSchedule,technologyLevel,\
    updatedTime FROM tb_guild_technology WHERE\
     guildId = %d"%(guildId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    technologylist = {}
    result = cursor.fetchall()
    cursor.close()
    for tech in result:
        technologylist[tech['technology']] = tech
    return technologylist

def getGuildTechnologyLevel(guildId,TechnologyId):
    '''获取行会的科技等级
    @param guildId: int 行会的id
    @param TechnologyId: int 科技的id
    '''
    sql = "SELECT * FROM tb_guild_technology WHERE\
     guildId = %d AND technology = %d"%(guildId,TechnologyId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result
    return {}

def insertGuildTechnology(guildId,TechnologyId):
    '''添加行会科技'''
    sql = "INSERT INTO tb_guild_technology(guildId,technology)\
     VALUES(%d,%d)"%(guildId,TechnologyId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def TakeCorpsChief(guildId,characterId,president):
    '''接位
    @param guildId: int 行会的id
    @param characterId: int 接位者的id
    @param president: int 原会长的id
    '''
    dbpool = dbaccess.dbpool
    cursor = dbpool.cursor()
    sql1 = "UPDATE tb_guild a, tb_character b SET a.president = %d \
    WHERE a.id = %d AND b.id = a.president AND \
    DATE_SUB(CURDATE(), INTERVAL 7 DAY) >= DATE(b.LastonlineTime)"%(characterId,guildId)
    sql2 = "UPDATE tb_guild_character SET post = 0 WHERE characterId = %d"%president
    sql3 = "UPDATE tb_guild_character SET post = 4 WHERE characterId = %d"%characterId
    count1 = cursor.execute(sql1)
    count2 = cursor.execute(sql2)
    count3 = cursor.execute(sql3)
    if not (count1 and count2 and count3):
        return False 
    dbpool.commit()
    cursor.close()
    return True


def findNewPresident(guild,president):
    '''寻找新的会长'''
    sql = "SELECT characterId FROM tb_guild_character WHERE\
     guildId = %d AND characterId!=%d ORDER BY contribution"%(guild,president)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return 0
    
def TechnologyDonate(guildId,TechnologyId,level,curSchedule):
    '''科技捐献
    @param guildId: int 行会的id
    @param TechnologyId: int 科技的id
    @param funds: int 捐献的资金数量
    '''
    sql = "UPDATE tb_guild_technology SET curSchedule = %d ,technologyLevel =%d \
    WHERE guildId = %d AND technology = %d"%(curSchedule,level,guildId,TechnologyId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getAllGuildCharacterId(guildId):
    '''获取国中所有成员的id号'''
    sql = "SELECT characterId FROM tb_guild_character WHERE \
    guildId = %d "%guildId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGuildCharacterTop19(guildId):
    '''获取国前19位成员的信息
    @param guildId: int 国的id
    '''
    sql = "SELECT characterId FROM tb_guild_character WHERE \
    guildId = %d AND contribution>0 AND post!=4 ORDER BY contribution DESC LIMIT 0,18"%guildId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def updateGuildPost(guildId):
    '''更新国中的职位'''
    characterList = getGuildCharacterTop19(guildId)
    characterList = [int(character['characterId']) for character in characterList ]
    posts = {}
    posts[3] = characterList[:2]
    posts[2] = characterList[2:8]
    posts[1] = characterList[8:18]
    info = {'veterans':str(posts[3])[1:-1],'staffOfficers':str(posts[2])[1:-1],'senators':str(posts[1])[1:-1]}
    return info
#    updateGuildInfo(guildId,{'veterans':str(posts[3])[1:-1]})
#    updateGuildInfo(guildId,{'staffOfficers':str(posts[2])[1:-1]})
#    updateGuildInfo(guildId,{'senators':str(posts[1])[1:-1]})
    
def getCharacterGuildId(characterId):
    '''获取角色的国'''
    sql = "SELECT guildId FROM tb_guild_character WHERE characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return 0

def getGuildCharacterIdList(guildId):
    sql = "SELECT characterId FROM tb_guild_character WHERE guildId = %d"%guildId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getAllCharacterGuildInfo():
    '''获取所有角色的行会名称与行会id'''
    sql="SELECT gc.characterId AS pid,gc.guildId AS gid,g.name AS gname FROM tb_guild_character AS gc LEFT JOIN  tb_guild AS g ON gc.guildId=g.id"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    list={}
    if result and len(result)>0 :
        for item in result:
            list[item['pid']]=item
    return list

def InsertCharacterWishRecord(characterId):
    '''插入角色的需要记录
    '''
    sql = "insert into tb_wish_record(characterId,recordDate)\
     values(%d,'%s')"%(characterId,str(datetime.date.today()))
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
    
def getCharacterWishRecord(characterId):
    '''获取角色的许愿记录
    '''
    sql = "SELECT * from tb_wish_record where characterId = %d"%characterId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    if not result:#如果没有角色的许愿记录则插入一条
        InsertCharacterWishRecord(characterId)
    return result

def updateCharacterWishRecord(characterId,props):
    '''更新角色的许愿记录
    '''
    sql = 'update `tb_wish_record` set'
    sql = util.forEachUpdateProps(sql, props)
    sql += " where characterId = %d" % characterId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

