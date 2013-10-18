#coding:utf8
'''
Created on 2011-11-14

@author: lan
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

def getPlayerItemsInPackage(characterId):
    '''得到玩家包裹栏中物品
    @param characterId: int 角色的id
    '''
    sql = "select * from `tb_package` where characterId=" + str(characterId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getItemsInstancePackage(characterId):
    '''得到玩家包裹栏中物品
    @param characterId: int 角色的id
    '''
    sql = "select * from `tb_instance_package` where characterId=" + str(characterId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getPlayerEquipInEquipmentSlot(characterId):
    '''得到玩家装备栏信息
    @param characterId: int 角色的id
    '''
    filedstr = "header,body,belt,trousers,shoes,bracer,cloak,necklace,waist,weapon"
    sql = "select %s from `tb_equipment` where characterId=%d"%(filedstr,characterId)
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def putOneItemInPackage(characterId,packageType,itemId,position,stack = 1,category =1):
    '''放置一个物品到包裹栏中
    @param characterId: int 角色的id
    @param item: Item object 物品的实例
    @param position: int 物品的位置
    @param stack: int 叠加层数
    '''
    if packageType<=2:
        sql = "INSERT INTO `tb_package`(characterId,itemId,position,stack,category)\
        values(%d,%d,%d,%d,%d)"%(characterId,itemId,position,stack,category)
    if packageType ==5:
        sql = "INSERT INTO `tb_instance_package`(characterId,itemId,position,stack)\
        values(%d,%d,%d,%d)"%(characterId,itemId,position,stack)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def deleteItemInPack(packageType,item,tag = 1,backupstate = 0):
    '''删除包裹中的物品'''
    cursor = dbaccess.dbpool.cursor()
    if packageType<=2:
        packTableName = 'tb_package'
    elif packageType==5:
        packTableName = 'tb_instance_package'
    sql = "DELETE FROM `%s` WHERE itemId = %d"%(packTableName,item.baseInfo.getId())
    count = cursor.execute(sql)
#    if backupstate:
#        sql3 = "INSERT INTO tb_itemdorp_backup SELECT *,\
#        CURRENT_TIMESTAMP() AS dropTime FROM tb_item WHERE id = %d"%(\
#                                                item.baseInfo.getId())
#        cursor.execute(sql3)
    if tag:
        sql2 = "DELETE FROM `tb_item` WHERE id = %d"%(item.baseInfo.getId())
        cursor.execute(sql2)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def updateItemInPackStack(packageType,item,stack,tag = 1):
    '''更新包裹中物品的层叠数'''
    cursor = dbaccess.dbpool.cursor()
    count2 = 1
    if packageType<=2:
        packTableName = 'tb_package'
    if not stack:
        sql = "DELETE FROM `%s` WHERE itemId = %d"%(packTableName,\
                                                    item.baseInfo.getId())
        if tag:
            sql2 = "DELETE FROM `tb_item` WHERE id = %d"%(item.baseInfo.getId())
            count2 = cursor.execute(sql2)
            dbaccess.dbpool.commit()
    else:
        sql = "UPDATE `%s` SET `stack` = %d WHERE id = %d"%(packTableName,\
                                stack,item.pack.getIdInPack())
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1 and count2>=1:
        return True
    return False

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
    sql = "insert into `tb_item_consignment`(itemId,characterId,%s,stack)\
     values(%d,%d,%d,%d\
    )"%(priceName,item.baseInfo.getId(),characterId,payNum,item.pack.getStack())
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def moveItem(packageType,item,toPosition):
    '''更新物品的位置'''
    if packageType<=2:
        packTableName = 'tb_package'
    elif packageType==5:
        packTableName = 'tb_instance_package'
    sql = "UPDATE `%s` SET `position` = %d WHERE itemId = %d"%(\
                                packTableName,toPosition,item.baseInfo.id)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def initPlayerEquippack(playerId):
    '''初始化角色的装备栏表记录'''
    sql = "insert into tb_equipment(characterId) values (%d)"%(playerId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False


