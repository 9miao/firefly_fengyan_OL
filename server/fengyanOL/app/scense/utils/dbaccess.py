#coding:utf8
'''
Created on 2011-3-31

@author: sean_lan
'''
from twisted.python import log
from app.scense.utils import util
import datetime
import time
from MySQLdb.cursors import DictCursor
from app.scense.utils.dbpool import DBPool
from memhelper.memclient import MemClient

database = ''
servername = ''

dbpool = DBPool()
memclient = None
memdb = MemClient()
tb_guild_Column_name = []#tb_guild 表中所有的字段名
tb_mallitem_Column_name=[] #tb_mallitem_Column_name 表中所有字段和tb_item_template表的字段名
tb_mallitem_Column_name1=[]#tb_mallitem_Column_name 表中所有字段的字段名
tb_mall_log_Column_name=[] #tb_mall_log 表中所有字段的字段名
tb_instanceinfo_Columen_name=[]
tb_instance_activation_Columen_name=[]
tb_instance_close_Columen_name=[]
tb_instance_record_Columen_name=[]
tb_profession_Columen_name=[]
tb_marix_Columen_name=[]

all_marix_info = {} #所有阵法信息
all_ItemTemplate = {} #所有的物品模板信息
all_TaskTemplate = {} #所有的任务列表
tb_mall_restrict_Column_name=[] #tb_mall_restrict表中所有字段的名字
All_ShieldWord = []#屏蔽字符集
tb_Profession_Config = {}
tb_Experience_config = {}


'''------------------初始化常用信息------------------'''
def getAllMarix_Info():
    '''获取所有阵法信息'''
    sql = "SELECT * FROM tb_matrix"
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = {}
    for _item in result:
        data[_item['id']] = _item
    return data

def getAll_ShieldWord():
    sql = "SELECT sword FROM tb_shieldword;"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getExperience_Config():
    '''获取经验配置表信息'''
    sql = "select * from tb_experience"
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = {}
    for _item in result:
        data[_item['level']] = _item
    return data
    
def getProfession_Config():
    '''获取职业配置表信息'''
    sql = "select * from tb_profession"
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = {}
    for _item in result:
        data[_item['preId']] = _item
    return data
    
def getAll_ItemTemplate():
    sql="select * from `tb_item_template`"
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data = {}
    for _item in result:
        data[_item['id']] = _item
    return data

#-------------------------------------------------------------
def getMallInfoByCategories(type,page):
    '''根据分类获取商城物品'''
    import math
    allMallItem = getAllMallItem()
    typeGoodsInfo = {}
    goods = []
#    goods = [x for x in allMallItem.values() if type in exec("["+x['categorie']+"]") and x['isMallItem']==2]
    for _item in allMallItem.values(): #获取所有商品

        if _item['tag'].find(str(type))!=-1: #判断此商品是否属于此分类
            if _item['onoff']==1:
                if type==1:
                    cheapstart=_item['cheapstart'] #特价开始时间
                    cheapend=_item['cheapend'] #特价结束时间
                    discount=_item['discount'] #商品折扣率
                    up=_item['up']#上架时间
                    down=_item['down']#下架时间
                    if cheapstart and cheapend and discount!=-1:
                        nowtime=datetime.datetime.fromtimestamp(time.time()) #当前时间
                        if cheapstart<=nowtime and nowtime<=cheapend: #如果当前时间在折扣时间段内
                            if cheapstart>=up and cheapend<=down:
                                if _item['gold']!=-1:
                                    _item['gold']=int(math.ceil(_item['gold']*_item['discount']/100.0))
                                if _item['coupon']!=-1:
                                    _item['coupon']=int(math.ceil(_item['coupon']*_item['discount']/100.0))
                                goods.append(_item)
                                continue
                else: #如果type!=1
                    cheapstart=_item['cheapstart'] #特价开始时间
                    cheapend=_item['cheapend'] #特价结束时间
                    discount=_item['discount'] #商品折扣率
                    if cheapstart and cheapend and discount!=-1:
                        nowtime=datetime.datetime.fromtimestamp(time.time()) #当前时间
                        if cheapstart<nowtime and nowtime<cheapend: #如果当前时间在折扣时间段内
                            if _item['gold']!=-1:
                                _item['gold']=int(math.ceil(_item['gold']*_item['discount']/100.0))
                            if _item['coupon']!=-1:
                                _item['coupon']=int(math.ceil(_item['coupon']*_item['discount']/100.0))
                            goods.append(_item)
                            continue
                        else:
                            #print str(_item['name'])+"不在特价时间范围内"
                            continue
                    #判断当前时间是否在特价时间段中
                    #根据折扣率 重新设置商品的价格
                    goods.append(_item) #属于此分类的话添加此商品
                
    for i in range(len(goods)):
        page = (i/9)+1
        if i%9==0:
            typeGoodsInfo[page]=[]
        typeGoodsInfo[page].append(goods[i])
    return typeGoodsInfo.get(page,[]),len(typeGoodsInfo)

'''----------------更新所有用户的信息---------------'''

def updateAllPlayersEnergy(energy):
    '''系统给所有玩家增加相应的活力'''
    cursor = dbpool.cursor()
    sql1 = "update `tb_character` set energy=energy+%d" % energy
    cursor.execute(sql1)
    dbpool.commit()
    sql2 = "update `tb_character` set energy=200 where energy>200"
    cursor.execute(sql2)
    dbpool.commit()
    cursor.close()
        
'''---------------获取相应表中的所有字段---------------'''

def getTablecolumnName(tableName):
    '''获取相应表中的所有字段
    @param tableName: int 数据库表名
    '''
    sql = "SELECT  COLUMN_NAME FROM  `information_schema`.`COLUMNS` WHERE `TABLE_SCHEMA`='%s'  AND  `TABLE_NAME`='%s'"%(database,tableName)
    cursor=dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data = []
    for column_name in result:
        data.append(column_name[0])
    return data

def getLastInsertId(tableName):
    '''获取相应表中最后一条添加的数据
    @param tableName: int 数据库表名
    '''
    sql = "select id from %s where id=LAST_INSERT_ID()"%tableName
    cursor = dbpool.cursor()
    cursor.execute(sql)
    id = 0
    lastInsertItem = cursor.fetchone()
    cursor.close()
    if lastInsertItem:
        return lastInsertItem[0]
    return id

def getLastInsertCharacterInfo(tableName):
    '''获取相应表中最后一条添加的数据
    @param tableName: int 数据库表名
    '''
    sql = "select id from %s where id=LAST_INSERT_ID()"%tableName
    cursor = dbpool.cursor()
    cursor.execute(sql)
    id = 0
    lastInsertItem = cursor.fetchone()
    cursor.close()
    if lastInsertItem:
        return lastInsertItem[0]
    return id

'''------------用户注册相关数据库操作--------------'''
def hasRepeatUserName(username):
    '''检测是否有重复的用户名
    @param username: str 用户名
    '''
    sql = "select id from `tb_register` where username = '%s'" %( username)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    return False

def addRegist(username , password ,email):
    '''新用户注册
    @param username: str 用户名
    @param password: str 用户密码
    @param email: str 用户邮箱
    '''
    sql = "insert into `tb_register` values(null,'%s','%s','%s',-1)" %(username , password ,email)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False


'''---------------------用户信息相关-------------------------''' 

def getUserIdByUserNamePassword(username,password):
    '''根据用户名，密码获取用户的id
    @param username:str 用户名
    @param password: str 用户密码
    @return: id  用户的id
    '''
    sql = "select id from `tb_register` where username = '%s' and password = '%s'" %( username, password)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    id = 0
    if result:
        id = result[0]
    return id
    
def creatUserCharacter(id):
    '''为新用户建立空的用户角色关系记录
    @param id: int 用户id
    '''
    sql = "insert into `tb_user_character` (id) values(%d)" %id
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
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
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False

def creatNewCharacter(nickname ,profession ,userId ,fieldname):
    '''创建新的角色
    @param nickname: str 角色的昵称
    @param profession: int 角色的职业编号
    @param userId: int 用户的id
    @param fieldname: str 用户角色关系表中的字段名，表示用户的第几个角色
    '''
    sql = "insert into `tb_character`(nickName,profession,userId) values('%s',%d,%d)"%(nickname ,profession,userId )
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        characterId = getLastInsertCharacterInfo('tb_character')
        updateUserCharacter(userId,fieldname,characterId)
        initializeRole(characterId)
        return characterId
    else:
        return 0

def getUserInfo(id):
    '''获取用户角色关系表所有信息
    @param id: int 用户的id
    '''
    sql = "select * from tb_user_character where id = %d"%(id)
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def getUserCharacterInfo(id):
    '''获取用户角色列表的所需信息
    @param id: int 用户的id
    '''
    fieldNameList = ['id','nickname','profession','level','viptype','LastonlineTime']
    sqlstr = util.EachQueryProps(fieldNameList)
    sql = "select %s from tb_character where id = %d"%(sqlstr,id)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    data = {}
    if result:
        for i in range(len(fieldNameList)):
            if fieldNameList[i]=='LastonlineTime':
                data[fieldNameList[i]] = str(result[i])
                continue
            data[fieldNameList[i]] = result[i]
    return data

def checkUserPassword(userId,password):
    '''检测用户的密码'''
    sql = "SELECT id FROM tb_register WHERE id = %d AND `password`= '%s'"%(userId,password)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    return False

def deleteUserCharacter(userId,fieldname,characterId):
    '''删除用户的角色
    @param userId: int 用户的id
    @param fieldname: str 用户角色关系表中的字段名，表示用户的第几个角色
    @param characterId: int 角色的id 
    '''
    sql = "delete from `tb_character` where id = %d"%characterId
    result = updateUserCharacter(userId ,fieldname ,0)
    if result:
        cursor = dbpool.cursor()
        count = cursor.execute(sql)
        dbpool.commit()
        cursor.close()
        deleteRole(characterId)
        if count<1:
            log.err(_why="delete role(%d) some information unusual"%characterId)
    return result

'''----------------------------角色相关信息----------------------------------'''
def initializeRole(characterId):
    '''初始化新手表格
    @param characterId: int 角色的id
    '''
    sql1 = "INSERT INTO `tb_equipment` (`characterId`) VALUES(%d)"%characterId
    sql2 = "INSERT INTO `tb_practice`(characterId) values(%d)" % characterId
    sql3 = "INSERT INTO `tb_character_shop`(characterId,enterTime) values(%d,'%s')"%(characterId,str(datetime.datetime.now()))
    sql4 = "INSERT INTO `tb_character_skillsetting`(characterId) VALUES (%d)"% characterId
    sql5 = "INSERT INTO `tb_character_rest`(characterId) VALUES (%d)"%characterId
    sql6 = "INSERT INTO `tb_character_lobby`(characterId) VALUES (%d)"%characterId
    cursor = dbpool.cursor()
    count1 = cursor.execute(sql1)
    count2 = cursor.execute(sql2)
    count3 = cursor.execute(sql3)
    count4 = cursor.execute(sql4)
    count5 = cursor.execute(sql5)
    count6 = cursor.execute(sql6)
    dbpool.commit()
    cursor.close()
    if(count1 >= 1 and count2 >= 1 and count3 >= 1 and count4>=1 and count5>=1 and count6>=1):
        return True
    else:
        return False
    
def deleteRole(characterId):
    '''删除角色所有相关信息'''
    sql1 = "delete from `tb_equipment` where characterId = %d"%characterId
    sql2 = "delete from `tb_practice` where characterId = %d" % characterId
    sql3 = "delete from `tb_character_shop` where characterId = %d" % characterId
    sql4 = "delete from `tb_character_skillsetting` where characterId = %d"% characterId
    sql5 = "delete from `tb_character_rest` where characterId = %d" % characterId
    sql6 = "delete from `tb_character_lobby` where characterId = %d" % characterId
    cursor = dbpool.cursor()
    count1 = cursor.execute(sql1)
    count2 = cursor.execute(sql2)
    count3 = cursor.execute(sql3)
    count4 = cursor.execute(sql4)
    count5 = cursor.execute(sql5)
    count6 = cursor.execute(sql6)
    dbpool.commit()
    cursor.close()
    if(count1 >= 1 and count2 >= 1 and count3 >= 1 and count4>=1 and count5>=1 and count6>=1):
        return True
    else:
        return False

def getCharecterAllInfo(id):
    '''获取角色的所有信息
    @param id: int 角色的id
    '''
    sql = "select * from tb_character where id = %d"%(id)
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    return data

def getCharecterInfoByNickName(nickname):
    '''根据昵称获取角色的信息
    @param nickname: string 角色的昵称
    '''
    fieldNameList = ['id','nickname','profession','level','viptype']
    str = util.EachQueryProps(fieldNameList)
    sql = "select %s from tb_character where nickname = '%s'"%(str,nickname)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    data = {}
    if result:
        for i in range(len(fieldNameList)):
            data[fieldNameList[i]] = result[i]
        return data
    return None

def updateCharacter(id ,fieldname,valuse):
    '''更新角色的数据库信息
    @param id: int 角色的id
    @param fieldname: str 表的字段名
    @param valuse:str or int 更新的值
    '''
    sql = "update `tb_character` set `%s` = %d where id = %d"%(fieldname,valuse ,id)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        #log.err(_why='update character(%d) info %s filed!'%(id,fieldname))
        return False
    
def updateCharacterStr(id ,fieldname,valuse):
    '''更新角色的数据库信息
    @param id: int 角色的id
    @param fieldname: str 表的字段名
    @param valuse:str or int 更新的值
    '''
    sql = "update `tb_character` set %s = '%s' where id = %d"%(fieldname,valuse ,id)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        #log.err(_why='update character(%d) info %s filed!'%(id,fieldname))
        return False

def updatePlayerInfo(id, attrs):
    '''修改玩家信息'''
    sql = 'update `tb_character` set'
    sql = util.forEachUpdateProps(sql, attrs)
    sql += " where id=%d" % id
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    else:
        return False

def getCharacterIdByNickName(nickname):
    '''根据昵称获取角色的id
    @param nickname: string 角色的昵称
    '''
    sql = "select id from `tb_character` where nickname ='%s'"%nickname
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def updateCharacterLastOnlineTime(characterId):
    '''更新角色最后上线的时间'''
    sql = "UPDATE `tb_character` SET LastonlineTime = '%s' where id= %d"%(str(datetime.datetime.now()),characterId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    else:
        return False

'''---------------------玩家包裹相关（装备栏、包裹）----------------------'''

def getPlayerItemsInPackage(characterId):
    '''得到玩家包裹栏中物品
    @param characterId: int 角色的id
    '''
    sql = "select id,itemId,position,stack,category from `tb_package` where characterId=" + str(characterId)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = []
    for item in result:
        itemInfo = {}
        itemInfo['id'] = item[0]
        itemInfo['itemId'] = item[1]
        itemInfo['position'] = item[2]
        itemInfo['stack'] = item[3]
        itemInfo['category'] = item[4]
        data.append(itemInfo)
    return data
    

def getPlayerEquipInEquipmentSlot(characterId):
    '''得到玩家装备栏信息
    @param characterId: int 角色的id
    '''
    fields = "header,body,belt,trousers,shoes,bracer,cloak,necklace,waist,weapon"
    filedstr = util.EachQueryProps(fields)
    sql = "select %s from `tb_equipment` where characterId=%d"%(filedstr,characterId)
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result
    
def updatePlayerEquipmen(characterId,part,itemId):
    '''更新角色装备
    @param characterId:  int 角色的id
    @param part: str 角色部位名称，也是·tb_equipment·中的字段名
    '''
    sql = "update `tb_equipment` set %s = %d where characterId = %d"%(part,itemId,characterId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        log.err('updata character(%d) equipment %s filed!'%(characterId,part))
        return False
    
def putOneItemInTemPackage(characterId,itemId,position):
    '''放置一个物品到临时包裹中
    @param characterId: int 角色的id
    @param item: Item object 物品的实例
    @param position: int 物品的位置
    @param stack: int 叠加层数
    '''
    sql = "INSERT INTO `tb_temppackage`(characterId,itemId,position,stack)\
     values(%d,%d,%d,1); "%(characterId,itemId,position)
    sql2 = "SELECT @@IDENTITY"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    dbpool.commit()
    cursor.execute(sql2)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True,result[0]
    return False,-1

def putOneItemInPackage(characterId,itemId,position,stack = 1,category =1):
    '''放置一个物品到包裹栏中
    @param characterId: int 角色的id
    @param item: Item object 物品的实例
    @param position: int 物品的位置
    @param stack: int 叠加层数
    '''
    sql = "INSERT INTO `tb_package`(characterId,itemId,position,stack,category)\
     values(%d,%d,%d,%d,%d);"%(characterId,itemId,position,stack,category)
    sql2 = "SELECT @@IDENTITY"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    dbpool.commit()
    cursor.execute(sql2)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True,result[0]
    return False,-1
    
def putOneItemInWarehouse(characterId,itemId,position,stack):
    '''放置一个物品到仓库中
    @param characterId: int 角色的id
    @param item: Item object 物品的实例
    @param position: int 物品的位置
    @param stack: int 叠加层数
    '''
    sql = "INSERT INTO `tb_warehouse`(characterId,itemId,position,stack)\
     values(%d,%d,%d,%d);"%(characterId,itemId,position,stack)
    sql2 = "SELECT @@IDENTITY"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    dbpool.commit()
    cursor.execute(sql2)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True,result[0]
    return False,-1

def putItemInPack(characterId,packageType,item,position):
    '''放置一个物品到指定包裹中
    @param characterId: int 角色的id
    @param item: Item object 物品的实例
    @param position: int 物品的位置
    @param stack: int 叠加层数
    '''
    if packageType<=2:
        if packageType==1:
            packTableName ='tb_temppackage'
        elif packageType==2:
            packTableName = 'tb_warehouse'
        sql = "INSERT INTO `%s`(characterId,itemId,`position`,stack) VALUES \
    (%d,%d,%d,%d);"\
    %(packTableName,characterId,item.baseInfo.getId(),position,item.pack.getStack())
    elif packageType>2:
        packTableName = 'tb_package'
        sql = "INSERT INTO `%s`(characterId,itemId,`position`,category) VALUES \
            (%d,%d,%d,%d);"\
            %(packTableName,characterId,item.baseInfo.getId(),position,packageType-2)
    sql2 = "SELECT @@IDENTITY"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    dbpool.commit()
    cursor.execute(sql2)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True,result[0]
    return False,-1

def removeOneItemInTemPackage(characterId,itemId):
    '''移除临时包裹中的一个物品
    @param characterId: int 角色的id
    @param item: Item object 物品的实例
    '''
    sql = "DELETE FROM `tb_temppackage` where  characterId =%d and itemId = %d"%(characterId,itemId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
    
def moveItem(packageType,item,toPosition):
    '''更新物品的位置'''
    if packageType==1:
        packTableName ='tb_temppackage'
    elif packageType==2:
        packTableName = 'tb_warehouse'
    elif packageType>=3:
        packTableName = 'tb_package'
        
    sql = "UPDATE `%s` SET `position` = %d WHERE itemId = %d"%(packTableName,toPosition,item.baseInfo.id)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def deleteItemInPack(packageType,item,tag = 1,backupstate = 0):
    '''删除包裹中的物品'''
    cursor = dbpool.cursor()
    if packageType<=2:
        packTableName = 'tb_package'
    sql = "DELETE FROM `%s` WHERE itemId = %d"%(packTableName,item.baseInfo.getId())
    count = cursor.execute(sql)
    if backupstate:
        sql3 = "INSERT INTO tb_itemdorp_backup SELECT *,CURRENT_TIMESTAMP() AS dropTime FROM tb_item WHERE id = %d"%(item.baseInfo.getId())
        cursor.execute(sql3)
    if tag:
        sql2 = "DELETE FROM `tb_item` WHERE id = %d"%(item.baseInfo.getId())
        cursor.execute(sql2)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def itemInDBBackup(itemId):
    '''物品信息备份'''
    

def updateItemInPackStack(packageType,item,stack,tag = 1):
    '''更新包裹中物品的层叠数'''
    cursor = dbpool.cursor()
    count2 = 1
    if packageType==1:
        packTableName ='tb_temppackage'
    elif packageType==2:
        packTableName = 'tb_warehouse'
    elif packageType>=3:
        packTableName = 'tb_package'
    if not stack:
        sql = "DELETE FROM `%s` WHERE itemId = %d"%(packTableName,item.baseInfo.getId())
        if tag:
            sql2 = "DELETE FROM `tb_item` WHERE id = %d"%(item.baseInfo.getId())
            count2 = cursor.execute(sql2)
            dbpool.commit()
    else:
        sql = "UPDATE `%s` SET `stack` = %d WHERE id = %d"%(packTableName,stack,item.pack.getIdInPack())
    
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1 and count2>=1:
        return True
    return False

def removeItemInPackage(packageType,item):
    ''''''
    sql = "DELETE FROM `tb_package` WHERE id = %d"%(item.pack.getIdInPack())
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getLastPackRecordId(packageType):
    if packageType==1:
        packTableName ='tb_temppackage'
    elif packageType==2:
        packTableName = 'tb_warehouse'
    elif packageType==3 or packageType==4:
        packTableName = 'tb_package'
    sql = "select id from `%s` where id=LAST_INSERT_ID()"%packTableName
    cursor = dbpool.cursor()
    cursor.execute(sql)
    lastInsertItem = cursor.fetchone()
    cursor.close()
    return lastInsertItem[0]

'''-----------------------------物品信息-----------------------------'''
#def getItemInfo(itemId):
#    '''获取物品信息
#    @param itemId: int 物品在数据库中的id
#    '''
#    sql = "select * from `tb_item` where id =%d"%itemId
#    cursor = dbpool.cursor()
#    cursor.execute(sql)
#    result = cursor.fetchone()
#    cursor.close()
#    data = {}
#    for i in range(len(tb_item_Column_name)):
#        if tb_item_Column_name[i] == 'selfExtraAttributeId' or tb_item_Column_name[i] == 'dropExtraAttributeId':
#            AttributeList = []
#            exec("AttributeList = ["+result[i]+"]")
#            data[tb_item_Column_name[i]] = AttributeList
#            continue
#        try:
#            data[tb_item_Column_name[i]] = result[i]
#        except Exception as e:
#            pass
#            #print tb_item_Column_name, result,itemId
#    return data


def updateItemInfo(itemId,fieldname,valuse):
    '''更新物品信息
    @param itemId: int 物品的id
    @param fieldname: str 物品的属性字段名
    @param valuse: int or str 需要更新的字段的对应值
    '''
    if type(valuse)==str:
        sql = "update `tb_item` set %s = %s where id = %s"%(fieldname,valuse,itemId)
    elif type(valuse)==int or type(valuse)==long:
        sql = "update `tb_item` set %s = %s where id = %d"%(fieldname,valuse,itemId)
    else:
        log.msg("this function uncallable : update ("+str(fieldname)+','+str(valuse)+")")
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def produceOneItem(characterId,itemTemplateId,selfExtraAttributeId,dropExtraAttributeId,
                   isBound,quality,durability,identification,starLevel,stack):
    '''生成一个物品
    @param itemTemplateId: int 物品的模板id
    @param selfExtraAttributeId: str 物品的自身属性
    @param dropExtraAttributeId: str 物品的掉落属性
    @param isBound: int (0,1) 物品的绑定属性
    @param itemLevel: int 物品的等级
    @param durability: int 物品的耐久
    @param aliveTime: int 物品的剩余时间 
    '''
    selfExtraAttributeIdStr = util.formatListToString(selfExtraAttributeId)
    dropExtraAttributeIdStr = util.formatListToString(dropExtraAttributeId)
    sql = "insert into `tb_item`(characterId,itemTemplateId,selfExtraAttributeId,dropExtraAttributeId,\
    isBound,quality,durability,identification,starLevel,stack) values(%d,%d,'%s','%s',%d,%d,%d,%d,%d,%d)"%(characterId,itemTemplateId,
    selfExtraAttributeIdStr,dropExtraAttributeIdStr,isBound,quality,durability,identification,starLevel,stack)
#    #print sql
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def getLastItemRecordId():
    '''获取最后一条插入的物品Id'''
    sql = "select id from `tb_item` where id=LAST_INSERT_ID()"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    lastInsertItem = cursor.fetchone()
    cursor.close()
    return lastInsertItem[0]

def deleteItem(itemId):
    '''删除数据库中的一个物品
    @param itemId: int 物品的id
    '''
    sql = "delete from `tb_item` where id =%d"%itemId
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

'''----------------------好友信息--------------------------'''
def getLastFriendInsertRecordId():
    '''获取最新一条加入的好友信息的id'''
    sql = "select friendId from `tb_friend` where friendId=LAST_INSERT_ID()"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    lastInsertItem = cursor.fetchone()
    cursor.close()
    if lastInsertItem:
        return lastInsertItem[0]
    return 0

def getOneData(tabl_name,select_ziduan,tj,tj_value):
    '''获取tabl_name表中满足字段为tj的值为tj_value的数据的select_ziduan字段'''
    sql="select "+select_ziduan+" from "+tabl_name+" where "+tj+"="+str(tj_value)+" "
    cursor = dbpool.cursor()
    cursor.execute(sql)
    lastInsertItem = cursor.fetchone()
    cursor.close()
    if lastInsertItem:
        return lastInsertItem[0]
    return 0

def getPlayerFriend(characterId,friendType):
    '''获取角色的所有好友
    @param characterId: int 角色的id
    @param friendType: 好友类型(1,2,3)1:好友  2:黑名单  3:全部   4:仇敌
    '''
    filedList = ['friendId','characterId','playerId','friendType','isSheildedMail']
    str = util.EachQueryProps(filedList)
    sql = "select %s from `tb_friend` where characterId = %d"%(str,characterId)
    str = ""
    if friendType==1:
        sql += " and friendType = %d"%friendType
    elif friendType==2:
        sql += " and friendType = %d"%friendType
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    data = []
    for friend in result:
        itemInfo = {}
        for i in range(len(friend)):
            itemInfo[filedList[i]] = friend[i]
        data.append(itemInfo)
    return data

def addFriend(characterId,playerId,friendType,isSheildedMail=0):
    '''添加一个好友
    @param characterId: int 角色的id
    @param playerId: int 好友的id
    @param friendType: int(1,2) 好友的类型 1:好友  2:仇敌
    @param isSheildedMail:int 是否屏蔽邮件 0.不屏蔽邮件 1.屏蔽
    '''
    sql = "insert into `tb_friend`(characterId,playerId,friendType,isSheildedMail)\
     values(%d,%d,%d,%d);"%(characterId,playerId,friendType,isSheildedMail)
    sql2 = "SELECT @@IDENTITY"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    dbpool.commit()
    cursor.execute(sql2)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return 0

def updataSheildedMail(characterId,friendId,isSheildedMail,friendType):
    '''更新好友邮件屏蔽状态
    @param characterId: int 角色的id
    @param playerId: int 好友的id
    @param isSheildedMail:int 是否屏蔽邮件 0.不屏蔽邮件 1.屏蔽
    '''
    sql = "update `tb_friend` set isSheildedMail = %d,friendType=%d where friendId = %d and characterId=%d"%(isSheildedMail,friendType,friendId,characterId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
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
    sql = "update `tb_friend` set friendType = %d where characterId=%d friendId = %d"%(friendType,characterId,friendId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def deletePlayerFriend(characterId,friendId):
    '''删除角色好友
    @param friendId: int 好友编号
    '''
    sql = 'delete from `tb_friend` where characterId=%d and playerId = %d'%(characterId,friendId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False




    
    
'''--------------------------邮件相关---------------------------'''
def getPlayerMailList(characterId):
    '''获取角色邮件列表
    @param characterId: int 角色的id
    '''
    filedList = ['id','title','senderId','type','content','isReaded','sendTime','systemType','reference']
    str = ''
    str = util.forEachQueryProps(str, filedList)
    sql = "select %s from `tb_mail` where receiverId = %d"%(str,characterId)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    data = []
    for mail in result:
        mailInfo = {}
        for i in range(len(mail)):
            mailInfo[filedList[i]] = mail[i]
        data.append(mailInfo)
    return data
    
def deletePlayerMail(id):
    '''删除邮件
    @param id: int 邮件的id
    '''
    sql1 = "DELETE FROM `tb_mail` WHERE id = %d"%id
    sql2 = "DELETE FROM `tb_mail_package` WHERE id = %d"%id
    cursor = dbpool.cursor()
    count1 = cursor.execute(sql1)
    cursor.execute(sql2)
    dbpool.commit()
    cursor.close()
    if count1>=1:
        return True
    return False

def insertMail(senderId,receiverId,content,title='',type=1,systemType=1,reference=''):
    '''添加邮件'''
    cursor = dbpool.cursor()
    sql = "INSERT INTO `tb_mail`(title,senderId,receiverId,`type`,content,systemType,reference)\
     VALUES ('%s',%d,%d,%d,'%s',%d,'%s')"%(title,senderId,receiverId,type,content,systemType,reference)
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    else:
        return False

'''----------------------角色商店相关-----------------------'''
def getRefreshShopTime(characterId):
    '''获取角色上次刷新商品的时间'''
    sql = "select enterTime from `tb_character_shop` where characterId =%d"%characterId
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    if not result:
        return datetime.datetime.now()
    else:
        return result[0]

def updateRefreshShopTime(characterId):
    '''更新刷新商店的时间进入商店的'''
    sql = "update `tb_character_shop` set enterTime = '%s' where characterId = %d"%(str(datetime.datetime.now()),characterId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
    
'''--------------------------修炼相关--------------------------'''
def updatePlayerPracticeRecord(characterId, props):
    '''修改玩家修炼记录'''
    sql = "update `tb_practice` set"
    sql = util.forEachUpdateProps(sql, props)
    sql += " where characterId = %d" % characterId
    cursor = dbpool.cursor()
    cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    
def getPlayerPracticeRecord(characterId):
    '''获取玩家修炼记录'''
    sql = "select * from `tb_practice` where characterId = %d" % characterId
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

'''---------------------宿屋信息---------------------'''
def getRestNum(characterId):
    '''获取休息次数'''
    sql = "select * from `tb_character_rest` where characterId = %d"%characterId
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def updatePlayerRestRecord(characterId,record):
    '''修改玩家宿屋操作记录'''
    sql = "update `tb_character_rest` set"
    sql = util.forEachUpdateProps(sql, record)
    sql += " where characterId = %d" % characterId
    cursor = dbpool.cursor()
    cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    
def getPlayerRestRecord(characterId):
    '''获取玩家当天的宿屋各种操作的次数'''
    sql = "select * from `tb_character_rest` where characterId = %d" % characterId
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

'''--------------------技能相关-------------------'''
def getLearnedSkills(characterId):
    '''获取角色已学习的技能
    @param characterId: int 角色的id
    '''
    sql = "select *from `tb_skill` where characterId = %d"%characterId
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def updateSkillLevel(id,level):
    '''更新技能等级
    @param id: int 技能的id
    @param level: int 技能的等级
    '''
    sql ="update `tb_skill` set skillLevel = %d where id = %d"%(level,id)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def LearnSkill(characterId,skillId):
    '''学习技能
    @param characterId: int 角色的id
    @param skillId: int 技能的模板id
    '''
    sql = "INSERT INTO `tb_skill`(characterId,skillId) VALUES (%d,%d)"%(characterId,skillId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def equipSkill(characterId,skillId,skillPosition):
    '''装备技能
    @param characterId: int 角色的id
    @param skillId: int 技能的模板id
    @param skillPosition: str 技能栏的位置 'firstSkillId','secondSkillId','thirdSkillId'
    '''
    sql = "update `tb_character_skillsetting` set %s = %d where characterId = %d"%(skillPosition,skillId,characterId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
    
def getSkillSetting(characterId):
    '''获取角色技能设置
    @param characterId: int 角色的id
    '''
    filedList = ['firstSkillId','secondSkillId','thirdSkillId']
    str = ''
    str = util.forEachQueryProps(str, filedList)
    sql = "select %s from `tb_character_skillsetting` where characterId = %d"%(str,characterId)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    settingInfo = {}
    for mail in result:
        for i in range(len(mail)):
            settingInfo[filedList[i]] = mail[i]
    return settingInfo

#'''---------------------行会----------------------'''
def getCharacterGuild(characterId):
    '''获取角色的行会'''
    sql = "SELECT * FROM `tb_guild_character` WHERE characterId = %d"%(characterId)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def getCharacterGuildInfo(guildId,characterId):
    '''获取角色在指定行会中的信息'''
    sql = "SELECT * FROM `tb_guild_character` WHERE guildId = %d AND characterId = %d"%(guildId,characterId)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result
    

def getGuildInfoByFieldName(guildId,fieldName):
    '''获取行会的指定信息'''
    sql = "SELECT %s FROM `tb_guild` WHERE id = %d"%(fieldName,guildId)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def countGuildMenberNum(guildId):
    '''获取行会当前成员数量
    @param guildId: int 行会的id
    '''
    sql = "SELECT count(id) FROM `tb_guild_character` WHERE guildId = %d"%guildId
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result[0]

def getGuildMembersById(guildId,index):
    '''获取行会成员信息
    @param guildId: 行会的id
    '''
    sql = "SELECT * FROM `tb_guild_character` WHERE guildId = %d limit %d,10"%(guildId,(index-1)*10)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGuildMembersIdByGuildId(guildId):
    '''获取行会成员的id列表'''
    sql = "SELECT characterId FROM `tb_guild_character` WHERE guildId = %d"%(guildId)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = [chid[0] for chid in result]
    return data

def isGuildMenber(guildId,characterId):
    '''判断是否是行会成员'''
    sql = "SELECT id FROM `tb_character_guild` WHERE guildId =%d AND characterId =%d"%(guildId,characterId)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    return False

def updateGuildInfo(guildId,fieldName,value):
    '''更新行会信息
    @param guildId: int 行会的id
    @param fieldName : str 行会的字段名
    @param value: int 更新后的值
    '''
    sql = "UPDATE `tb_guild` SET %s = %d WHERE id = %d"%(fieldName,value,guildId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def quitGuild(characterId):
    '''退出行会'''
    sql = "DELETE FROM `tb_character_guild` WHERE characterId =%d"%characterId
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def updateCharacterInfoInGuild(characterId,fieldname,val):
    '''更新自己在行会中的信息'''
    sql = "UPDATE `tb_character_guild` SET %s = %d WHERE\
     characterId =%d"%(fieldname,val,characterId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def applyChallenge(guildId,eachGuilId):
    '''发起挑战
    @param guildId: int 行会的id
    @param eachGuilId: int 对方行会的id
    '''
    sql = "INSERT INTO `tb_guild_battle`(askCommunity,answerCommunity) VALUES(%d,%d)"%(guildId,eachGuilId)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

#'''---------------------交易行------------------------'''

def itemConsignment(characterId,item,payNum,payType):
    '''物品寄卖
    @param itemId: int 物品在物品表中的id
    @param payNum: int 物品设定的价格
    @param payType: int 物品价格方式  1:游戏币    2:金币
    '''
    if payType==1:
        priceName = 'coinPrice'
    else:
        priceName = 'goldPrice'
    sql = "insert into `tb_item_consignment`(itemId,characterId,%s,stack) values(%d,%d,%d,%d\
    )"%(priceName,item.baseInfo.getId(),characterId,payNum,item.pack.getStack())
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def goldConsignment(characterId,goldNum,coinPrice):
    '''金币寄卖'''
    sql = "INSERT INTO `tb_gold_consignment`(characterId,goldNum,coinPrice) values (%d,%d,%d)"%(characterId,goldNum,coinPrice)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False


def dbbuyItem(characterId,itemInConsignmentId,coinPrice):
    '物品购买'
    cursor = dbpool.cursor()
    sql_consign= "delete from `tb_item_consignment` where id=%s" % itemInConsignmentId # 物品交易表
    cursor.execute(sql_consign)
    dbpool.commit()
    cursor.close()
    return True
    
def dbItemSignCoins(itemInConsignmentId):
    '获取交易物品的价格,游戏币，金币，物品表id '
    cursor = dbpool.cursor()
    sql = 'select coinPrice,goldPrice,itemId,characterId from `tb_item_consignment` where id = %s' % itemInConsignmentId;
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close() 
    return result

def dbCharacterCoins(characterId):
    '获取玩家的游戏币,金币 '
    cursor = dbpool.cursor()
    sql = 'select coin,gold from `character` where id = %s' % characterId;
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close() 
    return result
    
def dbPackage(characterId,itemId):
    "获取玩家的包裹信息"
    cursor = dbpool.cursor()
    sql = 'select id,characterId,itemId from `tb_package` where characterId=%s and itemId=%s ' % (characterId,itemId);
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close() 
    return result

def dbCommissionItems(characterId,itemId,coinPrice,*args):
    '物品寄卖'
    cursor = dbpool.cursor()
    try:
        dbpool.autocommit(False)
        #sql_pack= "delete from `packhage` where id=%s" % packId #调用接口
        sql_commiss = "insert into `tb_item_consignment`(itemId,characterId,coinPrice) \
                values(%s,%s,%s)" % (itemId,characterId,coinPrice)
        sql_LastId = "select last_insert_id() "
        cursor.execute(sql_commiss)
        #cursor.excute(sql_pack)
        cursor.execute(sql_LastId)
        result = cursor.fetchone()
        dbpool.commit()
        dbpool.autocommit(True)
        cursor.close()
        return True,result
    except Exception,err:
        dbpool.rollback()   #出现异常，事务回滚
        cursor.close()
        return False
    
def dbCommissionGold(goldNum,coinPrice,characterId):
    '金币寄卖'
    cursor = dbpool.cursor()
    try:
        dbpool.autocommit(False)
        sql_commiss = "insert into `tb_gold_consignment`(goldNum,coinPrice,characterId) values \
                    (%s,%s,%s)" % (goldNum,coinPrice,characterId)
        sql_LastId = "select last_insert_id() "
        cursor.execute(sql_commiss)
        cursor.execute(sql_LastId)
        result = cursor.fetchone()
        dbpool.commit()
        dbpool.autocommit(True)
        cursor.close()
        return True,result
    except Exception ,err:
        dbpool.rollback()   #出现异常，事务回滚
        cursor.close()
        return False
    
def dbgoldInfor(goldInConsignmentId):
    "获取信息金币交易表 单条详细信息"
    cursor = dbpool.cursor()
    sql = "select id,goldNum,coinPrice,characterId from `tb_gold_consignment` where id=%s" % goldInConsignmentId
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close() 
    return result

def dbbuyGold(characterId,goldInConsignmentId,goldInfor,*args):
    '金币购买'
    cursor = dbpool.cursor()
    try:
        dbpool.autocommit(False)
        sql_commiss = "delete from `tb_gold_consignment` where id=%s" % goldInConsignmentId
        sql_gold_record = "insert into `tb_gold_consignment_record`(goldNum,characterId,customerId,coinPrice,recordData) \
                values(%s,%s,%s,%s,now()) " % (goldInfor[1],goldInfor[3],characterId,goldInfor[2])
        cursor.execute(sql_commiss)
        cursor.execute(sql_gold_record)
        dbpool.commit()
        dbpool.autocommit(True)
        cursor.close()
        return True
    except Exception,err:
        dbpool.rollback()   #出现异常，事务回滚
        cursor.close()
        return False

def getSearchToSortByTypeOne(keyName):
    '''根据角色id,得到数据,并且已金币降序.'''
    sql = "select id,itemId,characterId,coinPrice,goldPrice,operationTime from `tb_item_consignment` where characterId = %d order by coinPrice desc" % (keyName)
    ##print sql
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
    
def getSearchToSortByTypeTwo(keyName):
    '''根据角色id,得到数据,并且已金币升序.'''
    sql = "select id,itemId,characterId,coinPrice,goldPrice,operationTime from `tb_item_consignment` where characterId = %d order by coinPrice" % (keyName)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
def getSearchToSortByTypeThree(keyName):
    '''根据角色id,得到数据,并且已时间降序.'''
    sql = "select id,itemId,characterId,coinPrice,goldPrice,operationTime from `tb_item_consignment` where characterId = %d order by operationTime desc" % (keyName)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
def getSearchToSortByTypeFour(keyName):
    '''根据角色id,得到数据,并且已时间升序.'''
    sql = "select id,itemId,characterId,coinPrice,goldPrice,operationTime from `tb_item_consignment` where characterId = %d order by operationTime" % (keyName)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    

def getSearchByTypeTwoToSortByTypeOne(keyName):
    '''根据角色id,得到数据,并且已金币降序.'''
    sql = "select id,itemId,characterId,coinPrice,goldPrice,operationTime from `tb_item_consignment` where itemId= %d order by coinPrice desc" % (keyName)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
def getSearchByTypeTwoToSortByTypeTwo(keyName):
    '''根据角色id,得到数据,并且已金币降序.'''
    sql = "select id,itemId,characterId,coinPrice,goldPrice,operationTime from `tb_item_consignment` where itemId= %d order by coinPrice" % (keyName)
    ##print sql
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
def getSearchByTypeTwoToSortByTypeThree(keyName):
    '''根据角色id,得到数据,并且已金币降序.'''
    sql = "select id,itemId,characterId,coinPrice,goldPrice,operationTime from `tb_item_consignment` where itemId= %d order by operationTime desc" % (keyName)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
def getSearchByTypeTwoToSortByTypeFour(keyName):
    '''根据角色id,得到数据,并且已金币降序.'''
    sql = "select id,itemId,characterId,coinPrice,goldPrice,operationTime from `tb_item_consignment` where itemId= %d order by operationTime" % (keyName)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGlodByDescOrder():
    '''以金币多少,降序排序'''
    sql = "select id,goldNum,coinPrice,characterId,operationTime from `tb_gold_consignment` order by coinPrice desc;"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGlodByOrder():
    '''已金币多少,升序排序'''
    sql = "select id,goldNum,coinPrice,characterId,operationTime from `tb_gold_consignment` order by coinPrice;"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGlodByDescOrderToDate():
    '''以时间,进行金币降序排序'''
    sql = "select id,goldNum,coinPrice,characterId,operationTime from `tb_gold_consignment` order by operationTime desc;"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGlodByOrderToDate():
    '''以时间,进行金币升序排序'''
    sql = "select id,goldNum,coinPrice,characterId,operationTime from `tb_gold_consignment` order by operationTime;"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGlodByDescOrderAtId(nickName):
    '''以金币多少,降序排序,条件为角色id'''
    sql = "select id,goldNum,coinPrice,characterId,operationTime from `tb_gold_consignment` where characterId = %d order by coinPrice desc" % (nickName)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGlodByOrderAtId(nickName):
    '''已金币多少,升序排序,条件为角色id'''
    sql = "select id,goldNum,coinPrice,characterId,operationTime from `tb_gold_consignment` where characterId = %d order by coinPrice" % (nickName)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGlodByDescOrderToDateAtId(nickName):
    '''以时间,进行金币降序排序,条件为角色id'''
    sql = "select id,goldNum,coinPrice,characterId,operationTime from `tb_gold_consignment` where characterId = %d order by operationTime desc" % (nickName)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getGlodByOrderToDateAtId(nickName):
    '''以时间,进行金币升序排序,条件为角色id'''
    sql = "select id,goldNum,coinPrice,characterId,operationTime from `tb_gold_consignment` where characterId = %d order by operationTime" % (nickName)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getTrends():
    '''得到近7天的金币走势图'''
    sql = "select recordData,avg(coinPrice) from `tb_gold_consignment_record` where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(recordData) group by recordData;"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
#'''-----------------------大厅操作------------------------'''
def updatePlayerLobbyRecord(characterId, props):
    '''修改玩家大厅记录'''
    sql = "update `tb_character_lobby` set"
    sql = util.forEachUpdateProps(sql, props)
    sql += " where characterId = %d" % characterId
    cursor = dbpool.cursor()
    cursor.execute(sql)
    dbpool.commit()
    cursor.close()

def getPlayerLobbyRecord(characterId):
    '''获取玩家大厅记录'''
    sql = "select * from `tb_character_lobby` where characterId = %d" % characterId
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def dbTest():
    sql = "insert into `tb_item`(characterId,selfExtraAttributeId,dropExtraAttributeId) values(%d,'%s','%s')"%(1000001,'','')
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def pingMysql():
    cursor = dbpool.cursor()
    cursor.execute("select id from `tb_ping` where id = 1")
    cursor.close()
    
def execSqlStr(sql):
    cursor = dbpool.cursor()
    cursor.execute(sql)
    dbpool.commit()
    cursor.close()

#'''-----------------------商城操作------------------------'''
def getAllMallItem():
    '''获取商城中所有物品信息'''
    sql="SELECT item.*,mall.item_templateid,mall.tag as itemType,mall.promotion,mall.gold,mall.coupon,mall.restrict,mall.cheapstart,mall.cheapend,mall.discount,mall.up,mall.down,mall.onoff FROM tb_mall_item AS mall,tb_item_template AS item  WHERE  DATEDIFF(SYSDATE(),down ) <=0 AND DATEDIFF(SYSDATE(),up ) >=0 AND onoff=1 AND item.id=mall.item_templateid"

    cursor=dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data = {}
    for good in result:
        goodInfo = {}
        index = good[0]#获取物品模板Id
        for i in range(len(tb_mallitem_Column_name)):

            goodInfo[tb_mallitem_Column_name[i]] = good[i]
        data[index] = goodInfo
    return data
def getMallItemById(itemid):
    '''根据物品Id获取商城物品信息
    @param itemid: int 物品模板Id
    '''
    sql="select * from tb_mall_item where item_templateid=%d"%itemid
    cursor=dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data={}
    if not result:
        return None
    for i in range(len(tb_mallitem_Column_name1)):
        data[tb_mallitem_Column_name1[i]]=result[0][i]
            
    return data

def getMallRestrict(characterid,itemid):
    '''查询商城——角色物品限制信息
    @param characterid: int 角色Id
    @param itemid: int 物品模板Id
    '''
    sql="select * from tb_mall_restrict where characterid=%d and itemid=%d"%(characterid,itemid)
    cursor=dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    data={}
    if not result:
        return None
    for i in range(len(tb_mall_restrict_Column_name)):
        data[tb_mall_restrict_Column_name[i]]=result[0][i]
    return data

def insertMallRestrict(characterid,itemid,count,firsttime=time.strftime("%Y-%m-%d %X",time.localtime())):
    '''添加商城——角色物品限制信息
    @param characterid: int 角色id
    @param itemid: int 物品模板id
    @param count: int 物品数量
    @param firsttime: datetime 第一次购买时间  默认值为当前时间
    '''
    
    sql="insert  into `tb_mall_restrict`(`id`,`characterid`,`itemid`,`counts`,`firsttime`) values (Null,%d,%d,%d,'%s')"%(characterid,itemid,count,str(firsttime))
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
def deleteMallRestrict(characterid,itemid):
    '''删除商城——角色物品限制信息
    @param characterid: int 角色id
    @param itemid: int 物品模板id
    '''
    sql="delete from `tb_mall_restrict` where characterid=%d and itemid=%d"%(characterid,itemid)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def updateMallRestrict(characterId,itemid,count):
    '''距第一次购买没超过x小时 修改商城角色物品限制
    @param characterid: int 角色id
    @param itemid: int 物品模板id
    '''
    sql="update tb_mall_restrict SET counts=counts+%d WHERE characterid=%d AND itemid=%d"%(count,characterId,itemid)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
def clearMallRestrict(characterId,itemid,count,firsttime=time.strftime("%Y-%m-%d %X",time.localtime())):
    '''距第一次购买超过x小时 修改商城角色物品限制
    @param characterid: int 角色id
    @param itemid: int 物品模板id
    @param count: int 物品数量
    @param firsttime: datetime 第一次购买该物品的时间
    '''
    sql="update tb_mall_restrict SET counts=%d ,firsttime='%s' WHERE characterid=%d AND itemid=%d"%(count,str(firsttime),characterId,itemid)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
#-------------------------商城购买记录--------------------------------------
def addMallLog(characterid,itemid,count=1,gold=-1,coupon=-1,stime=time.strftime("%Y-%m-%d %X",time.localtime())):
    '''添加商城——角色物品限制信息
    @param characterid: int 角色id
    @param itemid: int 物品模板id
    @param count: int 物品数量
    @param gold: int 钻价格
    @param coupon: int 魔晶价格
    @param stime: datetime 购买时间
    '''
    
    sql="insert  into `tb_mall_log`(`id`,`characterid`,`item_templateid`,`counts`,`shopingtime`,`gold`,`coupon`) values (null,%d,%d,%d,'%s',%d,%d);"%(characterid,itemid,count,str(stime),gold,coupon)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False


def getInstanceInfo(name,id):
    '''根据Id获取副本信息
    @param id: 副本id
    '''
    #print str(id)
    sql="select * from tb_instanceinfo where %s=%d"%(name,id)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    data = {}
    if result:
        for i in range(len(tb_instanceinfo_Columen_name)):
            data[tb_instanceinfo_Columen_name[i]] = result[i]
    return data


def getAllInstanceByAreaSceneid(id):
    '''根据区域场景id获取副本列表'''
    sql="select * from tb_instanceinfo where areasceneid=%d"%id
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = []
    if result:
        for item in result:
            data.append(item[0])
    return data

def getAllInstance():
    '''获取所有副本的id'''
    sql="select id from tb_instanceinfo"
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = []
    if result:
        for item in result:
            data.append(item[0])
    return data

def getSceneIdsByAreas(areaid):
    '''获取相同区域的场景Id列表
    @param areaid: 区域id
    '''
    sql="select id from tb_scene where areaid=%d"%(areaid)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = []
    if result:
        for item in result:
            data.append(item[0])
    return data

def getInstanceActivationInfo(name,id):
    '''获取副本激活条件信息
    @param id: 副本激活条件id
    '''
    sql="select * from tb_instance_activation where %s=%d"%(name,id)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    data = {}
    if result:
        for i in range(len(tb_instance_activation_Columen_name)):
            data[tb_instance_activation_Columen_name[i]] = result[i]
    return data

def getInstanceCloseInfo(name,id):
    '''获取副本关闭条件信息
    @param id: 副本关闭条件id
    '''
    sql="select * from tb_instance_close where %s=%d"%(name,id)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    data = {}
    if result:
        for i in range(len(tb_instance_close_Columen_name)):
            data[tb_instance_close_Columen_name[i]] = result[i]
    return data

def insertInstanceRecord(characterid,instanceid):
    '''添加副本激活通关记录
    @param characterid: int 角色id
    @param instanceid: int副本id
    @param stateid: int 副本激活通关状态 1激活 2通关
    '''
    sql="insert  into `tb_instance_record`(`id`,`characterid`,`instanceid`) values (null,%d,%d)"%(characterid,instanceid)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
def getInstanceRecordInfo(characterid,instanceid):
    '''获取副本激活通关记录
    @param characterid: int 角色id
    @param instanceid: int副本id
    @param stateid: int 副本激活通关状态 1激活 2通关
    '''
    sql="select * from tb_instance_record where characterid=%d and instanceid=%d"%(characterid,instanceid)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    data = {}
    if result:
        for i in range(len(tb_instance_record_Columen_name)):
            data[tb_instance_record_Columen_name[i]] = result[i]
    return data

def getInstanceRecordByCharacterid(characterid):
    '''通过角色获取副本激活通关记录
    @param characterid: int 角色id
    '''
    sql="select * from tb_instance_record where characterid=%d "%characterid
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = []
    if not result:
        return None
    if result:
        list={}
        for item in result:
            for i in range(len(tb_instance_record_Columen_name)):
                list[tb_instance_record_Columen_name[i]] = item[i]
            data.append(list)
    return data

def getisInstanceRecord(characterid,instanceid):
    '''判断角色是否通关副本组，返回通关分数 或者没有通关None
    @param characterid: int 角色id
    @param instanceid: int副本组id
    '''
    sql="select score from tb_instance_record where characterid=%d and instanceid=%d"%(characterid,instanceid)
    cursor = dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return None


def dbbuyConsItem(characterId,tocharacterId,consID,newitemId,the_coin,to_coin , position,buytype):
    '''购买寄卖物品
    @param characterId: int 购买者的id
    @param tocharacterId: int 寄卖者的ID
    @param itemId: int 物品的ID
    @param itemCount: int 物品的数量
    @param buytype: int 购买的类型 1 金币 2钻
    '''
    cursor = dbpool.cursor()
    try:
        dbpool.autocommit(False)
#        sql_item_change = "UPDATE tb_item SET characterId = %d WHERE id = %d"%(characterId,newitemId)
        sql_item_inpack = "INSERT INTO tb_package(characterId,itemId,`position`)\
             VALUES (%d,%d,%d)"%(characterId,newitemId,position)
        if buytype == 1:
            sql_character_coin = "UPDATE tb_character SET coin = %d WHERE id = %d"%(the_coin,characterId)
            sql_tocharacter_coin = "UPDATE tb_character SET coin = coin+%d WHERE id = %d"%(to_coin,tocharacterId)
        else:
            sql_character_coin = "UPDATE tb_character SET gold = %d WHERE id = %d"%(the_coin,characterId)
            sql_tocharacter_coin = "UPDATE tb_character SET gold = gold+%d WHERE id = %d"%(to_coin,tocharacterId)
        sql_cons_item_clean = "delete from `tb_item_consignment` where id=%s" % consID
        
        count1 = cursor.execute(sql_item_inpack)
        count2 = cursor.execute(sql_character_coin)
        count3 = cursor.execute(sql_tocharacter_coin)
        count4 = cursor.execute(sql_cons_item_clean)
        if not (count1 and count4):#(count1 and count2 and count3 and count4):
            raise 
        dbpool.commit()
        dbpool.autocommit(True)
        cursor.close()
        return True
    
    except Exception,err:
        #print err
        dbpool.rollback()   #出现异常，事务回滚
        cursor.close()
        return False



