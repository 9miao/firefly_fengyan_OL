#coding:utf8
'''
Created on 2011-7-14
对物品表（tb_item）的操作
@author: lan
'''
from app.chatServer.utils import dbaccess
from twisted.python import log
from MySQLdb.cursors import DictCursor

ALL_SETINFO = {}#所有的套装信息
ALL_GEMINFO = {}#所有宝石的信息
ALL_COMPOUND = {}#所有合成配方的数据

def getAllsetInfo():
    '''获取所有的套装信息
    '''
    global ALL_SETINFO
    sql = "SELECT * from tb_equipmentset;"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for setinfo in result:
        ALL_SETINFO[setinfo['id']] = setinfo
        
def getAllGemInfo():
    '''获取所有的宝石信息
    '''
    global ALL_GEMINFO
    sql = "SELECT * from tb_item_gem;"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for geminfo in result:
        ALL_GEMINFO[geminfo['gemId']] = geminfo
        
def getAllCompoundInfo():
    '''获取所有的合成配置信息
    '''
    global ALL_COMPOUND
    sql = "SELECT * from tb_item_compound;"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    for compound in result:
        ALL_COMPOUND[compound['itemId']] = compound

def getItemInfo(itemId):
    '''获取物品信息
    @param itemId: int 物品在数据库中的id
    '''
    sql = "select * from `tb_item` where id =%d"%itemId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    return data

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
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def produceOneItem(characterId,itemTemplateId,isBound,durability,identification,stack):
    '''生成一个物品
    @param itemTemplateId: int 物品的模板id
    @param selfExtraAttributeId: str 物品的自身属性
    @param dropExtraAttributeId: str 物品的掉落属性
    @param isBound: int (0,1) 物品的绑定属性
    @param itemLevel: int 物品的等级
    @param durability: int 物品的耐久
    @param aliveTime: int 物品的剩余时间 
    '''
    sql = "INSERT INTO `tb_item`(characterId,itemTemplateId,isBound,accesstime,durability,\
    identification,stack) VALUES(%d,%d,%d,CURRENT_TIMESTAMP(),%d,%d,%d);"\
    %(characterId,itemTemplateId,isBound,durability,identification,stack)
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

def getLastItemRecordId():
    '''获取最后一条插入的物品Id'''
    sql = "select id from `tb_item` where id=LAST_INSERT_ID()"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    lastInsertItem = cursor.fetchone()
    cursor.close()
    return lastInsertItem[0]

def deleteItem(itemId):
    '''删除数据库中的一个物品
    @param itemId: int 物品的id
    '''
    sql = "delete from `tb_item` where id =%d"%itemId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

