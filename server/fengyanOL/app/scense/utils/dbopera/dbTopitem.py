#coding:utf8
'''
Created on 2011-9-17
装备排行榜
@author: SIOP_09
'''

from app.scense.utils import dbaccess
from app.scense.core.language.Language import Lg

tb_topitem_Column_name=[] #存储数据库中的所有字段

def getTop(typeid):
    '''获取排行数据
    @param typeid: 物品类型   0武器  1装备 2饰品
    '''
    dt=[] #存放data
#    flist=['itemid','marks','profession','name','guildname']
#    sql="SELECT t.itemid,t.marks,c.profession,c.nickname,g.name FROM tb_topitem AS t LEFT JOIN tb_item AS i ON t.itemid=i.id LEFT JOIN tb_character AS c ON i.characterId=c.id JOIN tb_guild_character AS cg ON c.id=cg.characterId LEFT JOIN tb_guild AS g ON cg.guildId=g.id WHERE t.typeid="+str(typeid)+" order by t.marks,i.strengthen"
    flist=['cid','itemname','uname','profession','marks','itemid']
    sql="SELECT c.id, tit.name,c.nickname,c.profession,t.marks,t.itemid FROM tb_topitem AS t LEFT JOIN tb_item AS i ON t.itemid=i.id LEFT JOIN tb_character AS c ON i.characterId=c.id JOIN tb_item_template as tit on i.itemTemplateId=tit.id  WHERE t.typeid="+str(typeid)+" order by t.marks desc,i.strengthen desc"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    cursor.close()
    if not result1:
        return None
    for item in result1:
        data={} #存放一条数据
        for i in range(len(flist)):
            if flist[i]=='guildname':
                if not item[i]:
                    data[flist[i]]=Lg().g(143)
                    continue
            data[flist[i]]=item[i]
        dt.append(data)
    
    if len(dt)<1:
        return None
    return dt

    
def getTopBy(nickname,typeid):
    '''搜索个人排行 不一定在100名内
    @param typeid: 物品类型   0武器  1装备 2饰品
    '''
    flist=['rowno','itemname','uname','profession','marks','itemid']
#    sql="SET @rowno=0;SELECT sw.rowno,sw.* FROM(SELECT tit.name,c.nickname,c.profession,t.marks,t.itemid,(@rowno:=@rowno+1) as rowno FROM tb_topitmTemplateId=tit.id  WHERE t.typeid="+str(typeid)+" order by t.marks desc,i.strengthen desc)AS sw WHERE sw.nickname='"+nickname+"'"
#    sql="SELECT sw.rowno,sw.* FROM(SELECT c.name,c.nickname,c.profession,c.marks,c.itemid,(@rowno:=@rowno+1) AS rowno FROM toplistitem AS c ,(SELECT (@rowno:=0)) AS b WHERE c.typeid="+str(typeid)+" order by c.marks desc,c.strengthen desc) AS sw WHERE sw.nickname='"+nickname+"' ORDER BY sw.rowno"
#    #print sql
    cursor = dbaccess.dbpool.cursor()

    cursor.execute("CALL getTopListItem("+str(typeid)+","+nickname+")")
    result1=cursor.fetchall() #当前页的信息
    cursor.close()
    dt=[] #存放data
    for item in result1:
        data={} #存放一条数据
        for i in range(len(flist)):
            if flist[i]=='guildname':
                if not item[i]:
                    data[flist[i]]=Lg().g(143)
                    continue
            data[flist[i]]=item[i]
        dt.append(data)
    if len(dt)<1:
        return None
    return dt

def addTop(itemid,typeid,marks):
    '''添加一个物品
    @param itemid: int item表id
    @param typeid: int 物品类型 0武器 1装备 2饰品
    @param marks: int 分数 
    '''
    sql1="select count(*) from tb_topitem where itemid="+str(itemid)
    sql="insert  into `tb_topitem`(`itemid`,`typeid`,`marks`) values ("+str(itemid)+","+str(typeid)+","+str(marks)+")"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql1)
    result=cursor.fetchone()
    if not result or result[0]>=1:
        cursor.close()
        return False    
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
    
def updateTop(oitemid,itemid,marks):
    '''修改排行
    @param oitemid: int 旧的物品id
    @param itemid: int  物品id
    @param marks: int 获得分数
    '''
    sql="update tb_topitem set itemid="+str(itemid)+",marks="+str(marks)+" where itemid="+str(oitemid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False