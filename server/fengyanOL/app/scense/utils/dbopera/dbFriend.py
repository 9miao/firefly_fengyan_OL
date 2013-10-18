#coding:utf8
'''
Created on 2011-8-19
@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
from app.scense.core.language.Language import Lg

'''----------------------好友信息--------------------------'''
def getLastFriendInsertRecordId():
    '''获取最新一条加入的好友信息的id'''
    sql = "select friendId from `tb_friend` where friendId=LAST_INSERT_ID()"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    lastInsertItem = cursor.fetchone()
    cursor.close()
    if lastInsertItem:
        return lastInsertItem[0]
    return 0

def getPlayerFriend(characterId,friendType,ziduan,guize):
    '''根据好友类型获取角色的所有好友
    @param characterId: int 角色的id
    @param friendType: 好友类型(1,2,3)1:好友  2:黑名单  3:全部   4:仇敌
    @param ziduan: int  1按角色名称,0角色等级，2行会名称  3最近登录时间
    @param guize: int 排序规则 1正序   0倒序
    '''
    filedList = ['id','nickname','profession','level','name','LastonlineTime','clue','spirit']
    orders="" #排序
    dt=[] #存放data
    
    if ziduan==1:
        orders=" order by c.nickname "
    elif ziduan==0:
        orders=" order by c.level "
    elif ziduan==2:
        orders=" order by g.name "
    elif ziduan==3:
        orders=" order by c.LastonlineTime"
    if guize==0:
        orders+=" desc "
    
    sql = "SELECT c.id, c.nickname,c.profession,c.level,g.name,c.LastonlineTime,f.clue,c.spirit FROM tb_friend AS f ,tb_character AS c  LEFT JOIN tb_guild_character AS cg   ON c.id=cg.characterId LEFT JOIN tb_guild AS g ON cg.guildId=g.id WHERE f.playerId=c.id and f.characterId = "+str(characterId)+" and f.friendType = "+str(friendType)+" "+orders+""
    
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    for item in result1:
        data={} #存放一条数据
        for i in range(len(filedList)):
            if filedList[i]=='name':
                if not item[i]:
                    data[filedList[i]]=Lg().g(143)
                    continue
            data[filedList[i]]=item[i]
        dt.append(data)

    if not dt:
        return None
    
    return dt

def  getis(id,cid):
    '''查询是否是好友或者黑名单
    @param id:int 角色id
    @param cid: int 好友角色id
    @param type: int 好友关系   1好友  2黑名单  0没有关系
    '''
    sql="select friendType from tb_friend where characterid="+str(id)+" and playerid="+str(cid)+""
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return 0
    return result[0]

def pdcount(id,type):
    '''判断角色的好友类型中的好友数量
    @param id:int 角色id
    @param type: int 好友类型  1好友   2黑名单
    '''
    sql="select count(friendId) from tb_friend where characterid="+str(id)+" and friendType="+str(type)+""
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return 0
    return int(result[0])
    

def addFriend(characterId,playerId,friendType,isSheildedMail=0):
    '''添加一个好友
    @param characterId: int 角色的id
    @param playerId: int 好友的id
    @param friendType: int(1,2) 好友的类型 1:好友  2:仇敌
    @param isSheildedMail:int 是否屏蔽邮件 0.不屏蔽邮件 1.屏蔽
    '''
    sql = "insert into `tb_friend`(characterId,playerId,friendType,isSheildedMail)\
     values(%d,%d,%d,%d)"%(characterId,playerId,friendType,isSheildedMail)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def updataSheildedMail(characterId,friendId,isSheildedMail,friendType):
    '''更新好友邮件屏蔽状态
    @param characterId: int 角色的id
    @param playerId: int 好友的id
    @param isSheildedMail:int 是否屏蔽邮件 0.不屏蔽邮件 1.屏蔽
    '''
    sql = "update `tb_friend` set isSheildedMail = %d,friendType=%d where friendId = %d and characterId=%d"%(isSheildedMail,friendType,friendId,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def updataBlackList(characterId,friendId,friendType):
    '''更新好友状态
    @param characterId: int 角色的id
    @param playerId: int 好友的id
    @param isSheildedMail:int 是否屏蔽邮件 0.不屏蔽邮件 1.屏蔽
    '''
    sql = "update `tb_friend` set friendType = "+str(friendType)+" where characterId="+str(characterId)+" and playerId = "+str(friendId)+" "
    #print sql
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def deletePlayerFriend(characterId,friendId):
    '''删除角色好友
    @param friendId: int 好友编号
    '''
    sql = 'delete from `tb_friend` where characterId=%d friendId = %d'%(characterId,friendId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def selectFriend(name,ziduan,guize):
    '''查找好友（模糊查找）
    @param name: string 好友的角色的昵称(名字)
    @param ziduan: int  1按角色名称,0角色等级，2行会名称  3最近登录时间
    @param guize: int 排序规则 1正序   0倒序
    '''
    
    filedList = ['id','nickname','profession','level','name','LastonlineTime']
    orders="" #排序
    dt=[] #存放data
    
    if ziduan==1:
        orders=" order by c.nickname "
    elif ziduan==0:
        orders=" order by c.level "
    elif ziduan==2:
        orders=" order by g.name "
    elif ziduan==3:
        orders=" order by c.LastonlineTime"
    if guize==0:
        orders+=" desc "
    
    sql = "SELECT c.id, c.nickname,c.profession,c.level,g.name,c.LastonlineTime FROM tb_character AS c LEFT JOIN tb_guild_character AS cg ON c.id=cg.characterId LEFT JOIN tb_guild AS g ON cg.guildId=g.id WHERE c.nickname LIKE'%"+name+"%' "+orders+""
    
    
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    for item in result1:
        data={} #存放一条数据
        for i in range(len(filedList)):
            if filedList[i]=='name':
                if not item[i]:
                    data[filedList[i]]=Lg().g(143)
                    continue
            data[filedList[i]]=item[i]
        dt.append(data)
    cursor.close()

    if not dt:
        return None
    
    return dt

def setShowMesFlag(id,cid,tp):
    '''设置好友上线提示
    @param id: int 当前用户角色id
    @param cid: int 好友角色id
    @param tp: int 好友上线提示  0不提示  1提示
    '''
    ts="0"
    if tp:
        ts="1"
    else:
        ts="0"
    sql="UPDATE tb_friend SET clue="+ts+" WHERE characterid="+str(id)+" AND playerId="+str(cid)+" "
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def setType(id,cid,ty,isSheildedMail):
    '''设置黑名单或者好友
    @param ty: int 好友类型
    @param id: int 角色id
    @param cid: int 好友id
    isSheildedMail:int 是否屏蔽聊天和邮件 0不屏蔽  1屏蔽
    '''
    sql="UPDATE tb_friend SET friendType="+str(ty)+",isSheildedMail="+str(isSheildedMail)+" WHERE characterid="+str(id)+" AND playerId="+str(cid)+" "
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getAllFriendsId(id):
    '''获取角色所有好友的id列表
    @param id: int 当前角色id
    return None OR []
    '''
    sql="SELECT playerId FROM tb_friend WHERE characterid="+str(id)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    list=[]
    if not result:
        return None
    for item in result:
        list.append(item[0])
    return list

def getFirendListByFlg(pid,flg):
    '''获取角色的所有好友或者黑名单
    @param pid: int 角色id
    @param flg: int 1好友   2黑名单 
    '''
    sql="SELECT playerId FROM tb_friend WHERE characterId=%s AND friendType=%s"%(pid,flg)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    if not result:
        return []
    listdata=[]
    for item in result:
        listdata.append(item['playerId'])
    return listdata
    
def getBlackList(characterId,page):
    
    filedList=['id','nickname','profession','level','LastonlineTime']
    sql="select playerId from tb_friend where characterId=%d and isSheildedMail=1"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result= cursor.fetchall()
    cursor.close()
    list1=[]
    if not result:
        return None
    for item in result:
        list1.append(item[0])
    intos=""
    for item in list1:
        intos+=str(item)+','
    intos='('+intos[0:(len(intos)-1)]+')'
    sql1="select id,nickname,profession,level,LastonlineTime from tb_character where id in"+intos
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    typeGoodsInfo = {}
    data = []
    for friend in result1:
        itemInfo = {}
        for i in range(len(friend)):
            itemInfo[filedList[i]] = friend[i]
        itemInfo['zaixian']=False
        sql='SELECT guildId FROM tb_guild_character WHERE characterId=%d'%itemInfo['id']
        cursor = dbaccess.dbpool.cursor()
        cursor.execute(sql)
        guildid = cursor.fetchone()
        cursor.close()
        if guildid:
            sql='SELECT NAME FROM tb_guild WHERE id=%d'%guildid[0]
            cursor = dbaccess.dbpool.cursor()
            cursor.execute(sql)
            guildName = cursor.fetchone()
            cursor.close()
            if guildName:
                itemInfo['guildName']=guildName[0]
            else:
                itemInfo['guildName']=Lg().g(143)
        else:
            itemInfo['guildName']=Lg().g(143)
        data.append(itemInfo)
    
    
    for i in range(len(data)):
        page = (i/2)+1
        if i%2==0:
            typeGoodsInfo[page]=[]
        typeGoodsInfo[page].append(data[i])
    ds= typeGoodsInfo.get(page,[]),len(typeGoodsInfo)

    return ds