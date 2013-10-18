#coding:utf8
'''
Created on 2011-8-16
商店相关数据
@author: lan
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor

def getPlayerRepurchaseInfo(characterId):
    '''获取物品回购物品信息'''
    sql = "SELECT *,TIMEDIFF(CURRENT_TIMESTAMP(),sellTime) AS overTime FROM tb_repurchase\
     WHERE TIMEDIFF(CURRENT_TIMESTAMP(),sellTime) < TIME('03:00:00') and characterId = %d ORDER BY id DESC LIMIT 0,15"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def getSellItemOut(characterId):
    '''查找不超过可回购范围的记录'''
    sql = "SELECT id FROM tb_repurchase\
     WHERE TIMEDIFF(CURRENT_TIMESTAMP(),sellTime) < TIME('03:00:00') and characterId = %d ORDER BY id DESC LIMIT 15,10"%characterId
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def delSellItemOut(characterId):
    '''删除超过范围的数据'''
    data = getSellItemOut(characterId)
    if not data:
        return True
    ss = ""
    if len(data)==1:
        ss = "(%d)"%int(data[0][0])
    else:
        data = tuple( int(i[0]) for i in data)
        ss = str(data)
    sql = "DELETE FROM tb_repurchase WHERE id IN " +ss
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False
    
def addSellItem(itemId,characterId):
    '''添加卖出的物品到回购表'''
    sql = "INSERT INTO tb_repurchase(itemId,characterId,sellTime)\
     VALUES (%d,%d,CURRENT_TIMESTAMP())"%(itemId,characterId)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        delSellItemOut(characterId)
        return True
    return False

def checkSellItem(itemId,characterId):
    '''检测物品是否可以回购'''
    sql = "SELECT count(id) FROM tb_repurchase WHERE \
    TIMEDIFF(CURRENT_TIMESTAMP(),sellTime) < TIME('03:00:00') \
    and itemId = %d and characterId = %d"%(itemId,characterId)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if not result or not result[0]:
        return False
    return True

def delSellItem(itemId):
    '''清除回购物品信息'''
    sql = "DELETE FROM tb_repurchase WHERE itemId = %d"%itemId
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if(count >= 1):
        return True
    return False

def getShopInfo(npcId):
    '''获取Npc的商店信息'''
    sql = "SELECT * FROM tb_npc_shop WHERE npcId = %d"%npcId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
def getItemPrice(itemId,npcId):
    '''获取商品的信息
    @param itemId: int 物品的id
    '''
    sql = "SELECT * FROM tb_npc_shop WHERE npcId = %d"%npcId
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result
    
    
    
    

