#coding:utf8
'''
Created on 2011-12-7
角色排行表
@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
from app.scense.core.language.Language import Lg

def getTopList():
    '''获取角色战力排行前10名''' 
    filedList = ['cid','name','profession','guildname','orther']
    dt=[] #存放data
    od="" #排序条件
    xs="c.id,c.nickname,c.profession,g.name,ct.battle " #需要显示的字段
    sql="SELECT "+xs+"  FROM tb_character_top AS ct LEFT JOIN tb_character AS c ON ct.characterid=c.id   LEFT JOIN tb_guild_character AS cg   ON ct.characterid=cg.characterId LEFT JOIN tb_guild AS g ON cg.guildId=g.id ORDER BY ct.battle DESC,ct.characterid desc  LIMIT 0,10"
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall()
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


def getTopListAll():
    '''获取所有角色战力排名''' 
   
    sql="SELECT c.id  FROM tb_character_top AS ct LEFT JOIN tb_character AS c ON ct.characterid=c.id   LEFT JOIN tb_guild_character AS cg   ON ct.characterid=cg.characterId LEFT JOIN tb_guild AS g ON cg.guildId=g.id ORDER BY ct.battle DESC,ct.characterid desc"
    cursor=dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall()
    cursor.close()
    return result1

def getMysely(nickname):
    '''获取自己战斗力的排名
    @param nickname: str 角色名称
    '''
    datas={} #存放一条数据
    filedList = ['topnum','name','profession','guildname','orther']
    cursor = dbaccess.dbpool.cursor()
    cursor.nextset()
    cursor.execute('CALL getCharacterTop(%s)',(nickname))
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

def delTop():
    '''删除所有排行'''
    sql="DELETE FROM tb_character_top"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False

def addTopList(characterList):
    '''添加角色战力排行
    @param characterList: [[],[],[]]  [[角色id,战斗力],[角色id,战斗力]]
    '''
    it=""
    for item in characterList:
        it+="("+str(item[0])+","+str(item[1])+"),"
        
    if len(it)<3:
        return
    it=it[:-1]+";"
    sql="insert  into `tb_character_top`(`characterid`,`battle`) values "+it
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count:
        return True
    return False