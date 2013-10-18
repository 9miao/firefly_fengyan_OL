#coding:utf8
'''
Created on 2011-9-17
角色表
@author: SIOP_09
'''
from app.scense.utils import dbaccess,util
import datetime
from MySQLdb.cursors import DictCursor
#from app.scense.serverconfig.dbnode import dbnoderemote

from twisted.python import log
from app.scense.core.language.Language import Lg

#dbnoderemote = dbnoderemote

def getTop100(typeid):
    '''获取角色排行前10数据
    @param typeid: int 0玩家等级排行  1游戏币排行  2声望排行   3综合战斗力排行
    '''
    filedList = ['cid','name','profession','guildname','orther']
    dt=[] #存放data
    od="" #排序条件
    xs="c.id,c.nickname,c.profession,g.name" #需要显示的字段
    
    if typeid==0: #玩家等级排行
        od=" order by c.level desc,c.exp desc,c.id desc "
        xs+=",c.level "
    elif typeid==1: #游戏币排行
        od=" order by c.coin desc "
        xs+=",c.coin "
#    elif typeid==2: #声望排行
#        od=" order by "
#        xs+=""
#    elif type==3: #综合战力排行
#        od=" order by "
#        xs+=""

    sql="select "+xs+" from tb_character as c LEFT JOIN tb_guild_character AS cg   ON c.id=cg.characterId  LEFT JOIN tb_guild AS g ON cg.guildId=g.id"+od
    sql+=" limit 0,10"
    #print sql
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    cursor.close()
    for item in result1:
        
        data={} #存放一条数据
        for i in range(len(filedList)):
            if filedList[i]=='guildname':
                if not item[i]:
                    data[filedList[i]]=Lg().g(143)
                    continue
            data[filedList[i]]=item[i]
            
        dt.append(data)
        
    if not dt or len(dt)<1:
        return None
    return dt


def getTopAll(typeid):
    '''获取角色排名
    @param typeid: int 0玩家等级排行  1游戏币排行  2声望排行   3综合战斗力排行
    '''
    
    if typeid==0: #玩家等级排行
        od=" order by c.level desc,c.exp desc,c.id desc "
    elif typeid==1: #游戏币排行
        od=" order by c.coin desc "
#    elif typeid==2: #声望排行
#        od=" order by "
#        xs+=""
#    elif type==3: #综合战力排行
#        od=" order by "
#        xs+=""

    sql="select c.id from tb_character as c LEFT JOIN tb_guild_character AS cg   ON c.id=cg.characterId  LEFT JOIN tb_guild AS g ON cg.guildId=g.id"+od

    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    cursor.close()
    return result1
    
def getOneTopByNname(nickname,typeid):
    '''
    @param typeid: int 哪种类型排行    0玩家等级排行  1游戏币排行  2声望排行 
    '''
    filedList = ['topnum','name','profession','guildname','orther']
    datas={} #存放一条数据
    od="" #排序条件
    xs="" #需要显示的字段
    
    if typeid==0: #玩家等级排行
        od=" order by c.level desc,c.exp desc,c.id desc "
        xs+="c.level "
    elif typeid==1: #游戏币排行
        od=" order by c.coin desc "
        xs+="c.coin "
    cursor = dbaccess.dbpool.cursor()
    cursor.nextset()
    cursor.execute('CALL getTopListCharacter(%s,%s,%s)',(xs,od,nickname))
    result1=cursor.fetchone() #当前页的信息
    cursor.close()
    if result1:
        for i in range(len(filedList)):
            if filedList[i]=='guildname':
                if not result1[i]:
                    datas[filedList[i]]=Lg().g(143)
                    continue
            datas[filedList[i]]=result1[i]
    return datas

def isNickName(nickname):
    '''判断此角色名称是否存在
    @param nickname: string 角色名称
    '''
    sql = "select count(*) from `tb_character` where nickname='"+nickname+"'"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    lastInsertItem = cursor.fetchone()
    cursor.close()
    if lastInsertItem:
        if lastInsertItem[0]>0:
            return True
    return False

def getFriendByLikeNames(characterid,nickname):
    '''根据好友名称模糊查找好友
    @param nickname: int 角色名称
    '''
    
    filedList = ['id','nickname']
    dt=[] #存放data
    
    sql="SELECT c.id,c.nickname FROM tb_character AS\
     c LEFT JOIN  tb_friend AS f ON c.id=f.playerId \
      WHERE f.friendType=1 AND c.nickname LIKE'%"+nickname+"%'\
       AND f.characterId="+str(characterid)
    
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    cursor.close()
    for item in result1:
        data={} #存放一条数据
        for i in range(len(filedList)):
            data[filedList[i]]=item[i]
        dt.append(data)
        
    if not dt or len(dt)<1:
        return None
    return dt
    
def isPresident(characterid):
    '''判断角色是否是行会长'''
    sql = "SELECT post FROM tb_guild_character WHERE characterId = %d"%characterid
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchone() #当前页的信息
    cursor.close()
    if result1 and result1[0]==4:
        return True
    return False
    
def getCharacterLastOnlien(characterId):
    '''获取角色的最后在线时间'''
    sql = "SELECT outtime FROM tb_character WHERE id = %d"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchone() #当前页的信息
    cursor.close()
    if result1:
        return result1[0]
    return datetime.datetime.now()

def getCharacterBattleAll():
    '''获取所有角色的战斗力'''
    sql="SELECT id,hp+mp+baseStr+id+profession FROM tb_character"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    cursor.close()
    data=[]
    if result1:
        for item in result1:
            data.append(item)
    if len(data)>0:
        return data
    return None

def getCinfo():
    sql="SELECT nickname,level FROM tb_character where id=1000061"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchone() #当前页的信息
    cursor.close()
    return result1

def updateCharacter(id ,fieldname,valuse):
    '''更新角色的数据库信息
    @param id: int 角色的id
    @param fieldname: str 表的字段名
    @param valuse:str or int 更新的值
    '''
    sql = "update `tb_character` set `%s` = %d where id = %d"%(fieldname,valuse ,id)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        #log.err(_why='update character(%d) info %s filed!'%(id,fieldname))
        return False

def getGuildinfoByPlayerid(characterid):
    '''根据角色id获取行会信息'''
    sql = "SELECT g.* FROM tb_guild_character AS gc,tb_guild AS g \
    WHERE characterId ="+str(characterid)+" AND gc.guildId=g.id"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    if not data:
        return None
    return data

def getAllpid():
    '''获取所有角色id'''
    sql="SELECT  id AS id FROM tb_character "
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    if not data:
        return None
    return data

def updatePlayerDB(player):
    '''更新角色的数据库信息'''
    characterId = player.baseInfo.id
    position = player.baseInfo.getPosition()
    props = {'level':player.level.getLevel(),'coin':player.finance.getCoin(),
             'town':player.baseInfo.getTown(),'energy':player.attribute.getEnergy(),
             'exp':player.level.getExp(),'hp':player.attribute.getHp(),
             'contribution':player.guild.contribution,'outtime':str(datetime.datetime.now()),
             'LastonlineTime':str(player.lastOnline),
             'isOnline':0,'novicestep':player.award.awardstep,
             'leavetime':str(player.guild.getLeaveTime()),
             'prestige':player.finance.getPrestige(),
             'morale':player.finance.getMorale(),
             'NobilityLevel':player.nobility.getLevel(),
             'position_x':position[0],
             'position_y':position[1]}
    sqlstr = "update `tb_character` set"
    sqlstr = util.forEachUpdateProps(sqlstr, props)
    sqlstr += " where id = %d" % characterId
#    dbnoderemote.execSql_defered(sqlstr, println)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sqlstr)
    dbaccess.dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
#        log.err(sqlstr)
        return False
    
def updatePlayerInfoByprops(characterId,props):
    '''更新角色数据库信息'''
    sqlstr = "update `tb_character` set"
    sqlstr = util.forEachUpdateProps(sqlstr, props)
    sqlstr += " where id = %d" % characterId
#    dbnoderemote.execSql_defered(sqlstr, println)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sqlstr)
    dbaccess.dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
#        log.err(sqlstr)
        return False
    
def updatePlayerOnline(playerId,online):
    '''更新角色在线的状态
    @param playerId: int 角色的id
    @param online: int 角色的在线状态
    '''
    sql = "update tb_character set isOnline = %d where `id` = %d"%(online,playerId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()

def getRepurchaseGold(characterId):
    '''获取角色的充值金额
    '''
    sql = "SELECT sum(gold) from tb_repurchase_gold  where characterId = %d;"%(characterId)
    sql2 = "DELETE From tb_repurchase_gold where characterId = %d"%(characterId)
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    dbaccess.dbpool.commit()
    gold = 0
    if data:
        gold =data[0]
        cursor.execute(sql2)
        dbaccess.dbpool.commit()
    cursor.close()
    return gold

    

    

    