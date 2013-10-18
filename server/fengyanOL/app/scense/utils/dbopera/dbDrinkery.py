#coding:utf8
'''
Created on 2011-9-8
酒店
@author: SIOP_09
'''
from app.scense.utils import dbaccess

tb_drinkery_Column_name=[] #存储数据库中酒店表中的所有字段

def getByTypeAndCharacterid(characterid,drinktype):
    '''根据角色id和角色使用的物品类型查看使用过几次
    @param characterid: int 当前角色id
    @param drinktype: int 酒店中物品类型 1魔法泡沫就   2 普通果汁酒   3神器果汁酒
    '''
    tiaojian=" DATE(dtime)=CURDATE() "#获取当天数据  DATE(dtime)只取到天数,精确到天       CURDATE()获取当前日期 精确到天
    sql="select count from tb_drinkery where "+str(tiaojian)+" and characterid="+str(characterid)+" and drinktype="+str(drinktype)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return 0
    return int(result[0])  #返回使用过几次


def getHotelinfo(characterid):
    '''根据角色id获取酒店商品使用信息
    @param characterid: int 角色id
    '''
    tiaojian=" DATE(dtime)=CURDATE() "#获取当天数据  DATE(dtime)只取到天数,精确到天       CURDATE()获取当前日期 精确到天
    sql="select * from tb_drinkery where "+str(tiaojian)+" and characterid="+str(characterid)+" order by drinktype"
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    if not result:
        return None
    list=[]
    if result:
        for item in result:
            data={}
            for i in range(len(tb_drinkery_Column_name)):
                data[tb_drinkery_Column_name[i]] = item[i]
            list.append(data)
    return list

def updateByCharacteridAndtype(characterid,typeid,count):
    '''根据角色名称和酒店物品类型修改角色使用物品次数
    @param characterid: int 当前角色id
    @param typeid: int 酒店物品类型
    '''
    sql="update tb_drinkery set count=count+"+str(count)+" where drinktype="+str(typeid)+" and characterid="+str(characterid)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def delByCharacter(characterid,typeid):
    '''根据角色id和类型删除物品
    @param characterid: int 当前角色id
    @param typeid: int 酒店物品类型
    '''
    sql="delete from tb_drinkery where characterid="+str(characterid)+" and drinktype="+str(typeid)+"  "
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def add(characterid,typeid,count):
    '''添加酒店记录
    @param characterid: 角色id
    @param typeid: int 酒店物品类型
    @param count: int 使用数量
    '''
    sql="insert  into `tb_drinkery`(`characterid`,`drinktype`,`count`) values ("+str(characterid)+","+str(typeid)+","+str(count)+")"
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False