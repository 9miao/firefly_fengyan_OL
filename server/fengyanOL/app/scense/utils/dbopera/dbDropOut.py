#coding:utf8
'''
Created on 2011-8-19

@author: SIOP_09
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
from twisted.python import log

tb_dropout_Column_name=[] #存储数据库中的所有字段名称


def getAll():
    '''获取所有掉落信息'''
    sql="select * from tb_dropout"
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    if not result:
        return None
    data={}
    for item in result:
        try:
            item['itemid']=eval("["+item['itemid']+"]")
            item['coupon']=eval("["+item['coupon']+"]")
            data[item['id']]=item
        except:
            log.err("-------------------%d"%item['id'])
    return data

#def  getByid(id):
#    '''根据掉落id获得掉落物品
#    @param id: int 掉落表主键id
#    '''
#    sql="select * from tb_dropout where id=%d"%id
#    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
#    cursor.execute(sql)
#    result = cursor.fetchone()
#    cursor.close()
#    if not result:
#        return None
#    data={}
#    if result:
#        for i in range(len(tb_dropout_Column_name)):
#            if tb_dropout_Column_name[i]=='itemid':
#                data['itemid']=eval("["+result[1]+"]")
#                continue
#            if tb_dropout_Column_name[i]=='coupon':
#                data['coupon']=eval("["+result[4]+"]")
#                continue
#            data[tb_dropout_Column_name[i]] = result[i]
#    return data
#
#def getDropoutInfoByID(dropId):
#    '''根据掉落id获得掉落物品
#    @param id: int 掉落表主键id
#    '''
#    sql="select * from tb_dropout where id=%d"%dropId
#    cursor = dbaccess.dbpool.cursor(DictCursor)
#    cursor.execute(sql)
#    result = cursor.fetchone()
#    cursor.close()
#    itemsInfo = eval("["+result['itemid']+"]")
#    for item in itemsInfo:
#        rate = random.randint(1,1000000)
#        if rate < item[2]:
#            result['itemInfo'] = item
#            break
#    return result
#    
    
    
