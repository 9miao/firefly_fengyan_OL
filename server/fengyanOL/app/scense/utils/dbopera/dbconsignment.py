#coding:utf8
'''
Created on 2011-5-17

@author: sean_lan
'''
from app.scense.utils import dbaccess
import math

#--------------------------------------------------------------------------------------------------------------


def getAllcoin(change,ziduan,guize,page,counts,characterid=0):
    '''获取所有货币寄卖信息
    @param change:int 1金币兑换钻   2钻兑换金币 
    @param ziduan: int  1按时间排序,2按购买价格排序，3按物品价格排序
    @param guize: int 排序规则 1正序   2倒序
    @param page: int 当前页数
    @param counts: int 每页多少条信息
    @param characterid: int 当前用户角色id
    '''
    flist=['id','salemoney','saletype','buymoney','buytype','adtime','characterid']
    dt=[] #存放data
    conditions="" #条件
    orders="" #排序
    
    if change==1 or change==2:
        conditions+=" AND saletype="+str(change)

    if characterid>0:
        conditions+=" AND characterid="+str(characterid)+" "
    
    if ziduan==1:
        if guize==1:
            orders=" order by adtime "
        elif guize==2:
            orders=" order by adtime desc "
    elif ziduan ==2:
        if guize==1:
            orders=" order by buymoney "
        elif guize==2:
            orders=" order by buymoney desc "
    elif ziduan ==3:
        if guize==1:
            orders=" order by salemoney "
        if guize==2:
            orders=" order by salemoney desc "
    
    sql="SELECT id,salemoney,saletype,buymoney,buytype,DATE_ADD(operationTime, INTERVAL adtime HOUR) AS adtime,characterid from tb_gold_consignment where DATE_ADD(operationTime, INTERVAL adtime HOUR)>= CURRENT_TIMESTAMP  " +conditions+" "+orders+""
    sql+=" limit "+str((page-1)*counts)+","+str(counts)+""
    
    sql1="SELECT CEILING(COUNT(*)/"+str(counts)+") AS t FROM tb_gold_consignment where DATE_ADD(operationTime, INTERVAL adtime HOUR)>= CURRENT_TIMESTAMP  " +str(conditions) #一共多少页

    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    for item in result1:
        data={} #存放一条数据
        for i in range(len(flist)):
            data[flist[i]]=item[i]
        dt.append(data)
        
    cursor.execute(sql1)
    result2=cursor.fetchone() #共几页
    cursor.close()

    if not dt:
        return None,0
    
    return dt,result2[0]
    

def getItemByLikeItemName(itemname,up,down,quality,type,ziduan,guize,page,counts,characterid=0):
    '''寄卖搜索 (模糊查询)
    @param itemname: int 物品名称  模糊查询
    @param up: int 物品等级上限  最大90 最小1
    @param down: int 物品等级下限  最大90 最小1
    @param quality: int 物品品质 1灰 2白 3绿 4蓝 5紫 6橙 7红
    @param type: int 物品类型 -1金币兑换钻  -2钻兑换金币 0以上的是物品  #2001武器  2002装备 2003消耗品  2004材料
    @param ziduan: string 排序字段   name,levelRequire,addtime,price
    @param guize: int 排序规则  0不排序  1正序    2倒序
    @param page: int 当前页数
    @param counts: int 每页多少条信息
    @param characterid: int 当前用户角色id
    '''
    conditions="" #条件
    orders="" #排序
    zd="" #
    od=""#
    
    flist=["id","adtime","characterid","consignmentid","coinnum","cointype","count"] #查询出来的字段名称
    
    dt=[] #存放data
    if itemname:
        conditions+=" and c.name like'%"+itemname+"%' "
    if up<91 and up>0 and down>0 and down<91:
        if up<down:
            conditions+=" AND c.levelRequire>="+str(up)+" AND c.levelRequire<="+str(down)+" "
        else:
            conditions+=" AND c.levelRequire>="+str(down)+" AND c.levelRequire<="+str(up)+" "
    if quality>0 and quality<8:
        conditions+=" AND c.baseQuality="+str(quality)+" "
    
    if type>0 and type<2000:
        conditions+=" AND c.weaponType="+str(type)+" "
    elif type>2000:
        li="" #存储物品类型id
        if type==2001:
            li="1,2,3,4,5,6,7,8,9,10,11"
        elif type==2002:
            li="12,13,14,15,16,17,18,19"
        elif type==2003:
            li="20,21,22"
        elif type==2004:
            li="23,24"
        conditions+" and c.weaponType in("+li+")"
    if characterid>0: #如果查找自己的寄卖物品
        conditions+=" AND a.characterId="+str(characterid)+" "
    else: #如果查找所有角色寄卖的物品  添加条件=寄卖时间+寄卖小时>=当前时间
        conditions+=" AND DATE_ADD(a.operationTime, INTERVAL a.addtime HOUR)>= CURRENT_TIMESTAMP "
    ziduans=None
    if ziduan==1:
        ziduans='name'
    elif ziduan==2:
        ziduans='levelRequire'
    elif ziduan==3:
        ziduans='addtime'
    elif ziduan==4:
        ziduans='price'
    
    if ziduans:
        if ziduans=="price":
            if guize==2:
                orders+=" ORDER BY cointype,coinnum DESC "
            elif guize==1:
                orders+=" ORDER BY cointype,coinnum "
        elif ziduans=="addtime":
            if guize==2:
                od=" ORDER BY adtime DESC "
            elif guize==1:
                od=" ORDER BY adtime "
        else:
            if guize==2:
                orders+=" order by "+ziduans+" desc "
            elif guize==1:
                orders+=" order by "+ziduans+" "

    sql="SELECT c.id,DATE_ADD(a.operationTime, INTERVAL a.addtime HOUR) AS adtime,b.characterId,a.id,a.coinnum,a.cointype,a.stack FROM tb_item_consignment AS a,tb_item AS b,tb_item_template AS c "+"WHERE a.itemId=b.id AND a.characterId=b.characterId AND b.itemTemplateId=c.id  "+conditions+orders+od
    sql+=" limit "+str((page-1)*counts)+","+str(counts)+""

    #print sql
    
    sql1="SELECT CEILING(COUNT(*)/"+str(counts)+") AS t FROM tb_item_consignment AS a,tb_item AS b,tb_item_template AS c "+"WHERE a.itemId=b.id AND a.characterId=b.characterId AND b.itemTemplateId=c.id  "+str(conditions) #一共多少页
    
    
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result1=cursor.fetchall() #当前页的信息
    for item in result1:
        data={} #存放一条数据
        for i in range(len(flist)):
            data[flist[i]]=item[i]
        dt.append(data)
        
    cursor.execute(sql1)
    result2=cursor.fetchone() #共几页
    cursor.close()

    if not dt:
        return None,0
    
    return dt,result2[0]
    

def addItem(itemId,characterId,coinnum,cointype,addtime,stack):
    '''添加寄卖物品
    @param itemId: int 物品id (tb_item主键)
    @param characterId: int 寄卖人角色id
    @param coinnum: int 物品货币数量
    @param cointype: int 物品货币类型
    @param addtime: int 寄售多少小时
    @param stack: int 物品层叠数
    '''
    sql="INSERT  INTO `tb_item_consignment`(`itemId`,`characterId`,`coinnum`,`cointype`,`addtime`,`stack`) VALUES (%d,%d,%d,%d,%d,%d)"%(itemId,characterId,coinnum,cointype,addtime,stack)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count>=1:
        cursor.close()
        return True
    dbaccess.dbpool.rollback()#事物回滚
    cursor.close()
    return False

def addGold(salemoney,saletype,buymoney,buytype,adtime,characterid):
    '''添加寄卖金币
    @param salemoney:int 出售的货币 数量
    '''
    sql="INSERT  INTO `tb_gold_consignment`(`salemoney`,`saletype`,`buymoney`,`buytype`,`adtime`,`characterid`) VALUES (%d,%d,%d,%d,%d,%d)"%(salemoney,saletype,buymoney,buytype,adtime,characterid)
    #print sql
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count>=1:
        cursor.close()
        return True
    dbaccess.dbpool.rollback()#事物回滚
    cursor.close()
    return False

def buyGold(characterid,id,item):
    '''购买寄卖货币
    @param characterid: 购买人id
    @param id: 货币寄卖表主键id
    @param item: object 货币寄卖上架信息
    '''
    #1钻 2金币
    if not item:
        return{'result':False,'message':'该物品已下架','data':None}
    salemoney=item.get('salemoney',0)#寄卖的货币数量
    saletype=item.get('saletype',1)#寄卖的货币种类 1钻 2金币
    buymoney=item.get('buymoney',0)#换取的货币数量
    buytype=item.get('buytype',1)#换取的货币种类    1钻 2金币
    tocharacterid=item.get('characterid',0)#寄卖人的id
    
    jmtype="" #寄卖货币类型
    dhtype="" #兑换货币类型
    sql1="" #执行的第一个sql语句
    sql2="" #执行的第二个sql语句
    sql3="" #执行第三个sql语句
    if saletype==1:
        jmtype="gold"  #钻
    elif saletype==2:
        jmtype="coin"  #金币
        
    
    if buytype==1: #换取的货币类型  钻  ,寄卖的是金币
        dhtype="gold" #钻
        sql1="UPDATE tb_character SET "+jmtype+"="+jmtype+"-"+str(salemoney)+","+dhtype+"="+dhtype+"+"+str(buymoney)+" WHERE id="+str(tocharacterid)
        sql2="UPDATE tb_character SET "+jmtype+"="+jmtype+"+"+str(salemoney)+","+dhtype+"="+dhtype+"-"+str(buymoney)+" WHERE id="+str(characterid)
        sql3="DELETE FROM tb_gold_consignment WHERE id="+str(id)
        sql4="INSERT  INTO `tb_gold_consignment_record`(`goldNum`,`characterId`,`customerId`,`coinPrice`,`buytype`) VALUES ("+str(salemoney)+","+str(tocharacterid)+","+str(characterid)+","+str(buymoney)+",2)"
    elif buytype==2:#换取的货币类型  金币，寄卖的是钻
        dhtype="coin" #金币
        sql1="UPDATE tb_character SET "+jmtype+"="+jmtype+"-"+str(salemoney)+","+dhtype+"="+dhtype+"+"+str(int(math.ceil(buymoney/100.0*99)))+" WHERE id="+str(tocharacterid)
        sql2="UPDATE tb_character SET "+jmtype+"="+jmtype+"+"+str(salemoney)+","+dhtype+"="+dhtype+"-"+str(buymoney)+" WHERE id="+str(characterid)
        sql3="DELETE FROM tb_gold_consignment WHERE id="+str(id)
        sql4="INSERT  INTO `tb_gold_consignment_record`(`goldNum`,`characterId`,`customerId`,`coinPrice`,`buytype`) VALUES ("+str(buymoney)+","+str(tocharacterid)+","+str(characterid)+","+str(salemoney)+",1)"
    try:
        dbaccess.dbpool.autocommit(False)
        cursor = dbaccess.dbpool.cursor()
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        dbaccess.dbpool.commit()
        dbaccess.dbpool.autocommit(True)
        cursor.close()
        return True

    except Exception,err:
        dbaccess.dbpool.rollback()   #出现异常，事务回滚
        cursor.close()
        return False
    
def getOneGold(id):
    '''根据货币寄卖id获取货币寄卖上架信息
    @param id: 货币寄卖id
    '''
    flist=['id','salemoney','saletype','buymoney','buytype','adtime','characterid']
    sql="SELECT id,salemoney,saletype,buymoney,buytype,DATE_ADD(operationTime, INTERVAL adtime HOUR) AS adtime,characterid FROM tb_gold_consignment WHERE DATE_ADD(operationTime, INTERVAL adtime HOUR)>NOW() and id="+str(id)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data={}
    result=cursor.fetchone()
    if result:
        for i in range(len(flist)):
            data[flist[i]]=result[i]
        cursor.close()
        return data
    return None


def buyItem(characterid,item):
    '''购买寄卖物品
    @param characterid: int 购买者的角色id
    @param item: object 物品寄卖表的对象
    '''

    if not item:
        return{'result':False,'message':'该物品已下架','data':None}
    tocharacterid=item.get('characterid',0) #寄卖物品的角色id
    itemid=item.get('itemid',0) #tb_item中的主键id
    coinnum=item.get('coinnum',0) #购买物品需要的货币数量
    cointype=item.get('cointype',0) #购买物品需要的货币类型  1钻 2金币
    counts=item.get('count',0) #购买的数量
    
    "UPDATE tb_item SET characterId="+str(characterid)+" WHERE id="+str(itemid)
    
    #调用小蓝接口(包括一个失去  一个获得)
    #扣钱(一个+一个-)
    #如果小蓝接口成功——>删除寄卖记录 delItem(id)

def getOneItem(id):
    '''根据物品寄卖id获取寄卖物品信息
    @param id: int  物品寄卖id
    '''
    flist=["itemid","adtime","characterid","coinnum","cointype","count"] #查询出来的字段名称
    sql="SELECT b.id,DATE_ADD(a.operationTime, INTERVAL a.addtime HOUR) AS adtime,b.characterId,a.coinnum,a.cointype,a.stack FROM tb_item_consignment AS a,tb_item AS b WHERE a.itemId=b.id  AND a.id="+str(id)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data={}
    result=cursor.fetchone()
    if result:
        for i in range(len(flist)):
            data[flist[i]]=result[i]
        cursor.close()
        return data
    return None

def getItemByoneid(id):
    flist=["itemname","itemid","adtime","characterid","coinnum","cointype","count"] #查询出来的字段名称
    sql="SELECT c.name,b.id,DATE_ADD(a.operationTime, INTERVAL a.addtime HOUR) AS adtime,b.characterId,a.coinnum,a.cointype,a.stack FROM tb_item_consignment AS a,tb_item AS b,tb_item_template AS c WHERE a.itemId=b.id AND b.itemTemplateId=c.id AND a.id="+str(id)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    data={}
    result=cursor.fetchone()
    if result:
        for i in range(len(flist)):
            data[flist[i]]=result[i]
        cursor.close()
        return data
    return None


def getitemplatetidOneItem(id):
    '''根据物品寄卖id获取寄卖物品模板id
    @param id: int  物品寄卖id
    '''
    sql="SELECT c.id FROM tb_item_consignment AS a,tb_item AS b,tb_item_template AS c WHERE a.itemId=b.id AND b.itemTemplateId=c.id  AND a.id="+str(id)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    if result:
        return int(result[0])
    return 0

def isBuyItem(itemid):
    '''根据物品id判断此物品是否可以寄卖
    @param itemid: int 物品id
    '''
    flist=['isBound','durability','sellType','transType','baseDurability']
    # 是否可以绑定,装备当前耐久度 -1表示没有耐久限制,出售类型 1可出售 2不可出售,交易类型 1可交易 2不可交易,基础耐久,（可使用次数）
    sql="SELECT a.isBound,a.durability,b.sellType,b.transType,b.baseDurability FROM tb_item AS a,tb_item_template AS b WHERE a.itemTemplateId=b.id AND a.id="+str(itemid)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    data={}
    if not result:
        return None
    for i in range(len(flist)):
        data[flist[i]]=result[i]
    return data

def delItem(id):
    '''根据物品寄卖id删除记录
    @param id: int 寄卖物品主键id
    '''
    sql="DELETE FROM tb_item_consignment WHERE id="+str(id)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count>=1:
        cursor.close()
        return True
    dbaccess.dbpool.rollback()#事物回滚
    cursor.close()
    return False
    

def delGold(id):
    '''根据货币寄卖主键id删除寄卖记录
    @param id: int 货币寄卖主键id
    '''
    sql="DELETE FROM tb_gold_consignment WHERE id="+str(id)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count>=1:
        cursor.close()
        return True
    dbaccess.dbpool.rollback()#事物回滚
    cursor.close()
    return False
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
def getItemByCharacterName(characterName,sortType,limit,index):
    '''根据角色名称获取寄卖的信息
    @param characterName: str 角色的名称
    @param sortType: int 排序的方式(1、按总价高到低 2、按总价低到高    0、默认)
    @param limit: int 分页限制
    @param index: int 分页号
    '''
    if sortType ==1:
        sortStr = "ORDER BY a.coinPrice DESC"
    elif sortType==2:
        sortStr = "ORDER BY a.coinPrice ASC"
    else:
        sortStr = ""
    sql1 = "SELECT a.* FROM tb_item_consignment a,tb_character b\
     WHERE a.characterId =b.id AND b.nickname = '%s' %s limit %d,%d"%(characterName,sortStr,limit*(index-1),limit)
    sql2 = "SELECT count(a.id) FROM tb_item_consignment a,tb_character b\
     WHERE a.characterId =b.id AND b.nickname = '%s'"%(characterName)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql1)
    result1=cursor.fetchall()
    cursor.execute(sql2)
    result2=cursor.fetchone()
    cursor.close()
    return result1,result2

def getAllConsItem(sortType,limit,index):
    '''获取所有物品寄卖的信息
    @param sortType: int 排序的方式(1、按总价高到低 2、按总价低到高    0、默认)
    @param limit: int 分页限制
    @param index: int 分页号
    '''
    if sortType ==1:
        sortStr = "ORDER BY a.coinPrice DESC"
    elif sortType==2:
        sortStr = "ORDER BY a.coinPrice ASC"
    else:
        sortStr = ""
    sql1 = "SELECT * FROM tb_item_consignment a %s limit %d,%d"%(sortStr,limit*(index-1),limit)
    sql2 = "SELECT count(a.id) FROM tb_item_consignment a"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql1)
    result1=cursor.fetchall()
    cursor.execute(sql2)
    result2 = cursor.fetchone()
    cursor.close()
    return result1,result2
    
def goldConsignment(characterId,goldNum,coinPrice):
    '''金币寄卖
    @param characterId: 寄卖者的id
    @param goldNum: int 金币的数量
    @param coinPrice: int 金币的总价 
    '''
    sql = "INSERT INTO `tb_gold_consignment`(goldNum,coinPrice,characterId)\
     VALUES (%d,%d,%d)"%(goldNum,coinPrice,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    if count>=1:
        cursor.close()
        return True
    dbaccess.dbpool.rollback()#事物回滚
    cursor.close()
    return False

def getGoldConsignmentById(consignmentId):
    '''根据物品寄卖的id获取寄卖的信息
    @param consignmentId: int 物品寄卖的id
    '''
    sql = "SELECT * FROM `tb_gold_consignment` WHERE id = %d"%consignmentId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    return result

def getAllConsItemByCharacterId(characterId,index):
    '''根据角色的id获取角色寄售的所有物品信息
    @param characterId: int 角色的id
    @param index: int 页面号
    '''
    sql1 = "SELECT * FROM `tb_item_consignment` WHERE characterId = %d limit %d,10"%(characterId,(index-1)*10)
    sql2 = "SELECT count(a.id) FROM tb_item_consignment a where a.characterId = %d"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql1)
    result1=cursor.fetchall()
    cursor.execute(sql2)
    result2=cursor.fetchone()
    cursor.close()
    return result1,result2

def searchGoldByCharacterName(nickname,sortType,limit,index):
    '''更加角色名称获取金币寄卖信息
    @param nickname: 角色的名称
    @param sortType: int排序方式(1、按总价高到低 2、按总价低到高    0、默认)
    @param limit: int 分页限制
    @param index: int 分页号
    '''
    if sortType ==1:
        sortStr = "ORDER BY a.coinPrice DESC"
    elif sortType==2:
        sortStr = "ORDER BY a.coinPrice ASC"
    else:
        sortStr = ""
    sql1 = "SELECT a.* FROM tb_gold_consignment a,tb_character b\
     WHERE a.characterId = b.id AND b.nickname = '%s' %s limit %d,%d"%(nickname,sortStr,limit*(index-1),limit)
    sql2 = "SELECT count(a.id) FROM tb_gold_consignment a,tb_character b\
     WHERE a.characterId = b.id AND b.nickname = '%s'"%(nickname)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql1)
    result1=cursor.fetchall()
    cursor.execute(sql2)
    result2=cursor.fetchone()
    cursor.close()
    return result1,result2
    

def searchAllGold(sortType,limit=10,index = 1):
    '''获取所有金币寄卖的信息
    @param sortType: int排序方式(1、按总价高到低 2、按总价低到高    0、默认)
    @param limit: int 分页限制
    @param index: int 分页号
    '''
    if sortType ==1:
        sortStr = "ORDER BY a.coinPrice DESC"
    elif sortType==2:
        sortStr = "ORDER BY a.coinPrice ASC"
    else:
        sortStr = ""
    sql1 = "SELECT a.* FROM tb_gold_consignment a,tb_character b\
     WHERE a.characterId = b.id %s limit %d,%d"%(sortStr,limit*(index-1),limit)
    sql2 = "SELECT count(a.id)FROM tb_gold_consignment a,tb_character b\
    WHERE a.characterId = b.id"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    cursor.execute(sql2)
    result2 = cursor.fetchone()
    cursor.close()
    return result1,result2

def getAllConsGoldByCharacterId(characterId,index):
    '''根据角色的id获取寄卖的金币信息
    @param characterId: int 角色的id
    '''
    sql1 = "SELECT * FROM `tb_gold_consignment` WHERE characterId = %d limit %d,10"%(characterId,(index-1)*10)
    sql2 = "SELECT count(a.id) FROM tb_gold_consignment a where a.characterId = %d"%(characterId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql1)
    result1=cursor.fetchall()
    cursor.execute(sql2)
    result2=cursor.fetchone()
    cursor.close()
    return result1,result2

def creatGoldTradeRecord(goldNum,characterId,customerId,coinPrice):
    '''生成金币交易记录'''
    sql = "INSERT INTO `tb_gold_consignment_record`(goldNum,characterId,customerId,coinPrice)\
     VALUES(%d,%d,%d,%d)"%(goldNum,characterId,customerId,coinPrice)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getGolPriceTrends():
    '''得到近7天的金币走势图'''
    sql = "select recordData,sum(coinPrice)/sum(goldNum) from tb_gold_consignment_record where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(recordData) group by date(recordData) order by date(recordData);"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def revocationGoldConsById(goldConsId):
    '''取消金币寄卖
    @param goldConsId: int 金币寄卖的记录id
    '''
    sql = "DELETE FROM `tb_gold_consignment` WHERE id = %d"%goldConsId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def revocationItemConsById(itemConsId):
    '''取消物品寄卖
    @param itemConsId: int 物品寄卖的记录id
    '''
    sql = "DELETE FROM `tb_item_consignment` WHERE id = %d"%itemConsId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

